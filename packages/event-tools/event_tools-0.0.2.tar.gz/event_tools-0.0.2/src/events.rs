//! Detect events from raw nanopore signal data
//! It's a modified Rust version for events.c in f5c (https://github.com/hasindu2008/f5c/blob/master/src/events.c)
use sorting_rs;
use pyo3::prelude::*;
use anyhow::{Result, anyhow, ensure};

use crate::stat::median;

/**
  The following code taken from scrappie at https://github.com/nanoporetech/scrappie (c) 2016 Oxford Nanopore Technologies Ltd.
  scrappie is licensed under the Mozilla Public License 2.0
  https://github.com/nanoporetech/scrappie/blob/master/LICENSE.md
*/

#[derive(Debug, Clone, Copy)]
pub struct DetectorParam {
    window_length1: usize,
    window_length2: usize,
    threshold1: f32,
    threshold2: f32,
    peak_height: f32,
}

// Always const rather than static when no need for memory location is required
pub const EVENT_DETECTION_DEFAULTS: DetectorParam = DetectorParam {
    window_length1: 3,
    window_length2: 6,
    threshold1: 1.4,
    threshold2: 9.0,
    peak_height: 0.2
};

pub const EVENT_DETECTION_RNA: DetectorParam = DetectorParam {
    window_length1: 7,
    window_length2: 14,
    threshold1: 2.5,
    threshold2: 9.0,
    peak_height: 1.0
};

// From scrappie
#[derive(Debug)]
pub struct RawTable {
    pub n: usize,
    pub start: usize,
    pub end: usize,
    pub raw: Vec<f32>,
}

impl Default for RawTable {
    fn default () -> RawTable {
        RawTable { n: 0, start: 0, end: 0, raw: vec![] }
    }
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct EventT {
    #[pyo3(get)]
    pub start: usize,
    #[pyo3(get)]
    pub length: f32,
    #[pyo3(get)]
    pub mean: f32,
    #[pyo3(get)]
    pub stdv: f32,
    #[pyo3(get)]
    pub pos: isize,
    #[pyo3(get)]
    pub state: isize,
}

impl Default for EventT {
    fn default () -> EventT {
        EventT { start: 0, length: 0.0f32, mean: 0.0f32, stdv: 0.0f32, pos: 0, state: 0 }
    }
}

#[pyclass]
#[derive(Debug)]
pub struct EventTable {
    #[pyo3(get)]
    pub n: usize,
    #[pyo3(get)]
    pub start: usize,
    #[pyo3(get)]
    pub end: usize,
    #[pyo3(get)]
    pub event: Vec<EventT>,
}

impl Default for EventTable {
    fn default () -> EventTable {
        EventTable { n: 0, start: 0, end: 0, event: vec![] }
    }
}

/** Quantiles from n array
 *
 *	Using a relatively inefficent qsort resulting in O(n log n)
 *	performance but better performance is possible for small np.
 *	The array p is modified inplace, containing which quantiles to
 *	calculation on input and the quantiles on output; on error, p
 *	is filled with the value NAN.
 *
 *	@param x  An array to calculate quantiles from
 *	@param nx Length of array x
 *	@param p  An array containing quantiles to calculate [in/out]
 *	@param np Length of array p
 *
 *	@return void
 **/
fn quantilef(
    x: &[f32],
    nx: usize,
    p: &mut [f32],
    np: usize,
) -> Result<()> {
    if p.len() == 0 {
        return Ok(())
    }
    for i in 0 .. np {
        ensure!(p[i] >= 0f32 && p[i] <= 1f32, "Only 0 <= p <= 1 is valid");
    }
    if x.len() == 0 {
        for i in 0 .. np{
            p[i] = f32::NAN;
        }
        return Ok(())
    }

    // Sort array using K-sort
    let mut space = x.to_owned();
    sorting_rs::ksort(&mut space);

    // Extract quantiles
    for i in 0 .. np {
        let idx: usize = (p[i] * (nx - 1) as f32) as usize;
        let remf: f32 = p[i] * (nx - 1) as f32 - idx as f32;
        if idx < nx - 1 {
            p[i] = (1.0 - remf) * space[idx] + remf * space[idx + 1];
        } else {
            // Should only occur when p is exactly 1.0
            p[i] = space[idx];
        }
    }

    Ok(())
}

/** Median Absolute Deviation of an array
 *
 *	@param x   An array to calculate the MAD of
 *	@param n   Length of array
 *	@param med Median of the array.	 If NAN then median is calculated.
 *
 *	@return MAD of array on success, NAN otherwise.
 **/
fn madf(
    x: &[f32],
    n: usize,
) -> Result<f32>{
    let mad_scaling_factor = 1.4826;
    if x.len() == 0{
        return Ok(f32::NAN);
    }
    if n == 1 {
        return Ok(0.0f32);
    }

    let mut absdiff: Vec<f32> = Vec::with_capacity(n);
    if n == 0 {
        return Ok(f32::NAN);
    }

    let _med = median(&x, n)?;

    for i in 0 .. n {
        absdiff.push((x[i] - _med).abs());
    }

    let mad = median(&absdiff, n)?;

    Ok(mad*mad_scaling_factor)
}


/** Simple segmentation of a raw read by thresholding the MAD
 *
 *	The MAD of the raw signal is calculated for non-overlapping chunks and then
 *	thresholded to find regions at the beginning and end of the signal that have
 *	unusually low variation (generally a stall or open pore).  The threshhold is
 *	derived from the distribution of the calaculated MADs.
 *
 *	The threshold is chosen to be high since a single chunk above it will trigger
 *	the end of the trimming: the threshhold is chosen so it is unlikely to be
 *	exceeded in the leader but commonly exceeded in the main read.
 *
 *	@param rt         Structure containing raw signal
 *	@param chunk_size Size of non-overlapping chunks
 *	@param perc	  The quantile to be calculated to use for threshholding
 *
 *	@return A range structure containing new start and end for read
 **/
fn trim_raw_by_mad(
    rt: &mut RawTable,
    chunk_size: usize,
    perc: f32,
) -> Result<&mut RawTable> {
    ensure!(chunk_size > 1, "Only chunk_size > 1 is valid");
    ensure!(perc >= 0.0 && perc <= 1.0, "Only 0 <= perc <= 1 is valid");

    let nsample: usize = rt.end - rt.start;
    let nchunk: usize = nsample / chunk_size;
    // Truncation of end to be consistent with Sloika
    rt.end = nchunk * chunk_size;

    let mut madarr: Vec<f32> = Vec::with_capacity(nchunk);
    for i in 0 .. nchunk {
        let chunk = &rt.raw[rt.start + i * chunk_size .. rt.start + (i + 1) * chunk_size];
        madarr.push(madf(chunk, chunk_size)?);
    }

    let mut p = vec![perc];
    let _tmp_ret = quantilef(&madarr, nchunk, &mut p, 1)?;

    let thresh: f32 = p[0];
    for i in 0 .. nchunk {
        if madarr[i] > thresh {
            break;
        }
        rt.start += chunk_size;
    }

    for i in (1 ..= nchunk).rev() {
        if madarr[i-1] > thresh {
            break;
        }
        rt.end -= chunk_size;
    }
    ensure!(rt.end > rt.start, "Only rt.end > rt.start is valid");

    Ok(rt)
}

fn trim_and_segment_raw(
    rt: &mut RawTable,
    trim_start: usize,
    trim_end: usize,
    varseg_cunk: usize,
    varseg_thresh: f32,
) -> Result<&mut RawTable> {
    trim_raw_by_mad(rt, varseg_cunk, varseg_thresh)?;

    rt.start += trim_start;
    rt.end -= trim_end;

    if rt.start >= rt.end {
        return Err(anyhow!("Null trimmed position"))
    }

    Ok(rt)
}

////////////////////////////////////////////////////////////////////////

#[derive(Debug, Clone)]
struct Detector {
    def_peak_pos: isize,
    def_peak_val: f32,
    signal: Vec<f32>,
    signal_length: usize,
    threshold: f32,
    window_length: usize,
    masked_to: usize,
    peak_pos: isize,
    peak_value: f32,
    valid_peak: bool,
}

impl Detector {
    fn update_peak_value(&mut self, val: f32) {
        self.peak_value = val;
    }

    fn update_peak_pos(&mut self, val: isize) {
        self.peak_pos = val;
    }

    fn update_masked_to(&mut self, val: usize) {
        self.masked_to = val;
    }

    fn update_valid_peak(&mut self, val: bool) {
        self.valid_peak = val;
    }
}


/**
 *   Compute cumulative sum and sum of squares for a vector of data
 *
 *   Element i  sum (sumsq) is the sum (sum of squares) up to but
 *   excluding element i of the inputy data.
 *
 *   @param data      double[d_length]   Data to be summed over (in)
 *   @param sum       double[d_length + 1]   Vector to store sum (out)
 *   @param sumsq     double[d_length + 1]   Vector to store sum of squares (out)
 *   @param d_length                     Length of data vector
 **/
fn compute_sum_sumsq(
    data: &[f32],
    sum: &mut [f64],
    sumsq: &mut [f64],
    d_length: usize,
) -> Result<()> {
    ensure!(d_length > 0, "Only d_length > 0 is valid");

    sum[0] = 0.0f64;
    sumsq[0] = 0.0f64;
    for i in 0 .. d_length {
        sum[i + 1] = sum[i] + data[i] as f64;
        sumsq[i + 1] = sumsq[i] + (data[i]*data[i]) as f64;
    }
    Ok(())
}

/**
 *   Compute windowed t-statistic from summary information
 *
 *   @param sum       double[d_length]  Cumulative sums of data (in)
 *   @param sumsq     double[d_length]  Cumulative sum of squares of data (in)
 *   @param d_length                    Length of data vector
 *   @param w_length                    Window length to calculate t-statistic over
 *
 *   @returns float array containing tstats.  Returns NULL on error
 **/
fn compute_tstat(
    sum: &[f64],
    sumsq: &[f64],
    d_length: usize,
    w_length: usize,
) -> Result<Vec<f32>> {
    ensure!(d_length > 0, "Only d_length > 0 is valid");
    ensure!(w_length > 0, "Only d_length > 0 is valid");

    let mut tstat: Vec<f32> = vec![0.0f32; d_length];

    let eta = f64::MIN;
    let w_lengthf: f64 = w_length as f64;

    // Quick return:
    //   t-test not defined for number of points less than 2
    //   need at least as many points as twice the window length
    if d_length < 2 * w_length || w_length < 2 {
        return Ok(tstat)
    }
    // fudge boundaries
    // Not necessary after initialization, but kept for code integrity
    // for i in 0 .. w_length {
    //     tstat[i] = 0.0f32;
    //     tstat[d_length - i - 1] = 0.0f32;
    // }

    // get to work on the rest
    for i in w_length ..= d_length - w_length {
        let mut sum1 = sum[i];
        let mut sumsq1 = sumsq[i];
        if i > w_length {
            sum1 -= sum[i - w_length];
            sumsq1 -= sumsq[i - w_length];
        }
        let sum2 = sum[i + w_length] - sum[i];
        let sumsq2 = sumsq[i + w_length] - sumsq[i];
        let mean1 = sum1 / w_lengthf;
        let mean2 = sum2 / w_lengthf;
        let mut combined_var = sumsq1 / w_lengthf - mean1 * mean1 +
                                    sumsq2 / w_lengthf - mean2 * mean2;

        // Prevent problem due to very small variances
        combined_var = f64::max(combined_var, eta);

        //t-stat
        //  Formula is a simplified version of Student's t-statistic for the
        //  special case where there are two samples of equal size with
        //  differing variance
        let delta_mean: f64 = mean2 - mean1;
        let _t = delta_mean.abs() / (combined_var / w_lengthf).sqrt();
        if _t > 0.0f64 {
            tstat[i] = _t as f32;
        }
    }

    Ok(tstat)

}

/**
 *
 *   @returns array of length nsample whose elements contain peak positions
 *   Remaining elements are padded by zeros.
 **/
fn short_long_peak_detector(
    short_detector: &mut Detector,
    long_detector: &mut Detector,
    peak_height: f32,
) -> Result<Vec<usize>> {
    ensure!(short_detector.signal_length == long_detector.signal_length,
            "The signal_length of short_detector and long_detector should be equal");

    let signal_len = short_detector.signal_length;
    let mut peaks= vec![0usize; signal_len];
    let mut peak_count: usize = 0;

    for i in 0 .. signal_len {
        // Split operations of short & long detectors sequentially
        // Carry on if we've been masked out
        if short_detector.masked_to >= i {
            // continue
        } else {
            let current_value: f32 = short_detector.signal[i];

            if short_detector.peak_pos == short_detector.def_peak_pos {
                // CASE 1: We've not yet recorded a maximum
                if current_value < short_detector.peak_value {
                    // Either record a deeper minimum ...
                    short_detector.update_peak_value(current_value);
                } else if current_value - short_detector.peak_value > peak_height {
                    // ... or we've seen a qualifying maximum
                    short_detector.update_peak_value(current_value);
                    short_detector.update_peak_pos(i as isize);
                    // otherwise, wait to rise high enough to be considered a
                    // peak
                }
            } else {
                // CASE 2: In an existing peak, waiting to see if it is good
                if current_value > short_detector.peak_value {
                     // Update the peak
                     short_detector.update_peak_value(current_value);
                     short_detector.update_peak_pos(i as isize);
                }
                // Dominate other tstat signals if we're going to fire at some
                // point, only for short_detector
                if short_detector.peak_value > short_detector.threshold {
                    long_detector.update_masked_to(
                        short_detector.peak_pos as usize + short_detector.window_length);
                    long_detector.update_peak_pos(long_detector.def_peak_pos);
                    long_detector.update_peak_value(long_detector.def_peak_val);
                    long_detector.update_valid_peak(false);
                }

                // Have we convinced ourselves we've seen a peak
                if short_detector.peak_value - current_value > peak_height &&
                    short_detector.peak_value > short_detector.threshold {
                    short_detector.update_valid_peak(true);
                }

                // Finally, check the distance if this is a good peak
                if short_detector.valid_peak &&
                    i - short_detector.peak_pos as usize > short_detector.window_length / 2 {
                    // Emit the boundary and reset
                    peaks[peak_count] = short_detector.peak_pos as usize;
                    peak_count += 1;
                    short_detector.update_peak_pos(short_detector.def_peak_pos);
                    short_detector.update_peak_value(current_value);
                    short_detector.update_valid_peak(false);
                }
            }
        }

        // Next, scan use long_detector
        // Carry on if we've been masked out
        if long_detector.masked_to >= i {
            // continue
        } else {
            let current_value = long_detector.signal[i];

            if long_detector.peak_pos == long_detector.def_peak_pos {
                // CASE 1: We've not yet recorded a maximum
                if current_value < long_detector.peak_value {
                    // Either record a deeper minimum ...
                    long_detector.update_peak_value(current_value);
                } else if current_value - long_detector.peak_value > peak_height {
                    // ... or we've seen a qualifying maximum
                    long_detector.update_peak_value(current_value);
                    long_detector.update_peak_pos(i as isize);
                    // otherwise, wait to rise high enough to be considered a peak
                }
            } else {
                // CASE 2: In an existing peak, waiting to see if it is good
                if current_value > long_detector.peak_value {
                     // Update the peak
                     long_detector.update_peak_value(current_value);
                     long_detector.update_peak_pos(i as isize);
                }

                // Have we convinced ourselves we've seen a peak
                if long_detector.peak_value - current_value > peak_height &&
                    long_detector.peak_value > long_detector.threshold {
                    long_detector.update_valid_peak(true);
                }

                // Finally, check the distance if this is a good peak
                if long_detector.valid_peak &&
                    i - long_detector.peak_pos as usize > long_detector.window_length / 2 {
                    // Emit the boundary and reset
                    peaks[peak_count] = long_detector.peak_pos as usize;
                    peak_count += 1;
                    long_detector.update_peak_pos(long_detector.def_peak_pos);
                    long_detector.update_peak_value(current_value);
                    long_detector.update_valid_peak(false);
                }
            }
        }
    }

    Ok(peaks)
}

/**  Create an event given boundaries
 *
 *   Note: Bounds are CADLAG (i.e. lower bound is contained in the interval but
 *   the upper bound is not).
 *
 *  @param start Index of lower bound
 *  @param end Index of upper bound
 *  @param sums
 *  @param sumsqs
 *  @param nsample  Total number of samples in read
 *
 *  @returns An initialised event.  A 'null' event is returned on error.
 **/
fn create_event(
    start: usize,
    end: usize,
    sums: &[f64],
    sumsqs: &[f64],
    nsample: usize,
) -> Result<EventT> {
    ensure!(start < nsample, "Start out of bound");
    ensure!(end <= nsample, "End out of bound");

    // println!("{:?}", (start, end, sums[start], sums[end]));
    let mut event: EventT = EventT::default();
    // event.pos = -1;
    // event.state = -1;

    ensure!(end < sums.len(), "Out of bound for sums"); // Replace NULL in the original code

    event.start = start;
    event.length = (end - start) as f32;
    event.mean = (sums[end] - sums[start]) as f32 / event.length;
    let deltasqr: f32 = (sumsqs[end] - sumsqs[start]) as f32;
    let var = deltasqr / event.length - event.mean * event.mean;
    event.stdv = f32::max(var, 0.0f32).sqrt();

    Ok(event)
}

fn create_events(
    peaks: Vec<usize>,
    sums: Vec<f64>,
    sumsqs: Vec<f64>,
    nsample: usize,
) -> Result<EventTable>{
    let mut et: EventTable = EventTable::default();

    // Count number of events found
    let mut n: usize = 1;
    for i in 0 .. peaks.len() {
        if peaks[i] > 0 && peaks[i] < nsample {
            n += 1;
        }
    }

    ensure!(n > 1, "No peaks detected");
    et.event = Vec::with_capacity(n);

    et.n = n;
    et.end = et.n;

    // First event -- starts at zero
    match create_event(0usize, peaks[0], &sums, &sumsqs, nsample) {
        Ok(x) => et.event.push(x),
        Err(_) => et.event.push(EventT::default()),
    }
    // Other events -- peak[i-1] -> peak[i]
    for ev in 1 .. n-1 {
        match create_event(peaks[ev-1], peaks[ev], &sums, &sumsqs, nsample) {
            Ok(x) => et.event.push(x),
            Err(_) => et.event.push(EventT::default()),
        }
    }

    // Last event -- ends at nsample
    match create_event(peaks[n-2], nsample, &sums, &sumsqs, nsample) {
        Ok(x) => et.event.push(x),
        Err(_) => et.event.push(EventT::default()),
    }

    Ok(et)
}

pub fn detect_events(
    rt: RawTable,
    edparam: DetectorParam,
) -> Result<EventTable> {
    let mut sums = vec![0.0f64; rt.n + 1];
    let mut sumsqs = vec![0.0f64; rt.n + 1];

    let _ret = compute_sum_sumsq(&rt.raw, &mut sums, &mut sumsqs, rt.n)?;

    let tstat1 = compute_tstat(&sums, &sumsqs, rt.n, edparam.window_length1)?;
    let tstat2 = compute_tstat(&sums, &sumsqs, rt.n, edparam.window_length2)?;

    let mut short_detector: Detector = Detector {
        def_peak_pos: -1,
        def_peak_val: f32::MAX,
        signal: tstat1,
        signal_length: rt.n,
        threshold: edparam.threshold1,
        window_length: edparam.window_length1,
        masked_to: 0,
        peak_pos: -1,
        peak_value: f32::MAX,
        valid_peak: false,
    };

    let mut long_detector: Detector = Detector {
        def_peak_pos: -1,
        def_peak_val: f32::MAX,
        signal: tstat2,
        signal_length: rt.n,
        threshold: edparam.threshold2,
        window_length: edparam.window_length2,
        masked_to: 0,
        peak_pos: -1,
        peak_value: f32::MAX,
        valid_peak: false,
    };

    let peaks = short_long_peak_detector(&mut short_detector, &mut long_detector,
                                                     edparam.peak_height)?;

    let mut et = match create_events(peaks, sums, sumsqs, rt.n) {
        Ok(x) => x,
        Err(_) => EventTable::default(),
    };

    et.start = rt.start;
    et.end = rt.end;

    Ok(et)
}

// interface to scrappie functions
pub fn getevents(
    nsample: usize,
    rawptr: &[f32],
    rna: bool,
) -> Result<EventTable> {
    let mut et = EventTable::default();
    let mut rt: RawTable = RawTable { n: nsample, start: 0, end: nsample, raw: rawptr.to_vec()};

    // trim using scrappie's internal method
    // parameters taken directly from scrappie defaults
    let trim_start: usize = 200;
    let trim_end: usize = 10;
    let varsegchunk: usize = 100;
    let varseg_thresh = 0.0;

    match trim_and_segment_raw(&mut rt, trim_start, trim_end, varsegchunk, varseg_thresh) {
        Ok(_) => (),
        Err(_) => return Ok(et),
    }

    let mut ed_params: &DetectorParam = &EVENT_DETECTION_DEFAULTS;
    if rna {
        ed_params = &EVENT_DETECTION_RNA;
    }

    et = match detect_events(rt, *ed_params) {
        Ok(x) => x,
        Err(_) => et,
    };

    Ok(et)
}



#[cfg(test)]
mod tests {
    use super::*;
    use std::io::prelude::*;
    use npy::NpyData;

    #[test]
    fn test_eventdetection() {
        let data: Vec<f32> = vec![
            1.0, 1.0, 2.0, 2.0, 3.0,
            3.0, 4.0, 4.0, 5.0, 5.0,
            6.0, 6.0, 7.0, 7.0, 8.0,
            8.0, 9.0, 9.0, 10.0, 10.0];
        let n: usize = 20;
        let mut sum = vec![0.0f64; n+1];
        let mut sumsq = vec![0.0f64; n+1];
        compute_sum_sumsq(&data, &mut sum, &mut sumsq, n).unwrap();

        let peaks = vec![
            2, 4, 6, 8, 10, 12, 14, 16, 18, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        let et = create_events(peaks, sum, sumsq, n).unwrap();
        for i in 0 .. et.event.len() {
            println!("{:?}", et.event[i]);
        }
    }

    #[test]
    fn test_cumulative_sums() {
        let data: Vec<f32> = vec![
            1.0, 2.0, 3.0, 4.0, 5.0,
            6.0, 7.0, 8.0, 9.0, 10.0];
        let expt_sum: Vec<f64> = vec![
            0.0, 1.0, 3.0, 6.0, 10.0, 15.0,
            21.0, 28.0, 36.0, 45.0, 55.0,
        ];
        let expt_sumsq: Vec<f64> = vec![
            0.0, 1.0, 5.0, 14.0, 30.0, 55.0,
            91.0, 140.0, 204.0, 285.0, 385.0,
        ];
        let n: usize = 10;

        let mut sum = vec![0.0f64; n+1];
        let mut sumsq = vec![0.0f64; n+1];
        let _ret = compute_sum_sumsq(&data, &mut sum, &mut sumsq, n).unwrap();

        assert_eq!(sum, expt_sum);
        assert_eq!(sumsq, expt_sumsq);
    }


    #[test]
    fn test_calculation_tstat() {
        let _boundary: Vec<f32> = vec![1.15470054, 2.0, 3.46410162, 100.0, 3.46410162, 2.0, 1.15470054];
        let winlen: usize = 4;
        let data: Vec<f32> = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
            3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
            2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        ];
        let expt: Vec<f32> = vec![
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            1.15470054, 2.0, 3.46410162, 100.0, 3.46410162, 2.0, 1.15470054,
            0.0, 0.0, 0.0,
            1.15470054, 2.0, 3.46410162, 100.0, 3.46410162, 2.0, 1.15470054,
            0.0, 0.0, 0.0,
            1.15470054, 2.0, 3.46410162, 100.0, 3.46410162, 2.0, 1.15470054,
            0.0, 0.0, 0.0,
            1.15470054, 2.0, 3.46410162, 100.0, 3.46410162, 2.0, 1.15470054,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        ];

        let n: usize = 50;
        let mut sum = vec![0.0f64; n+1];
        let mut sumsq = vec![0.0f64; n+1];
        let _ret = compute_sum_sumsq(&data, &mut sum, &mut sumsq, n).unwrap();

        let mut tstat = compute_tstat(&sum, &sumsq, n, winlen).unwrap();
        for i in 0 .. n {
            if tstat[i] > 100.0 {
                tstat[i] = 100.0;
            }
        }

        for i in 0 .. expt.len() {
            assert!(tstat[i] - expt[i] < 1e-5);
        }
    }

    #[test]
    fn shift_scale_helper() {
        let shift: f32 = 0.25;
        let scale: f32 = 0.5;

        let data: Vec<f32> = vec![
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
            3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
            2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
        ];
        let mut data2 = data.clone();
        let nsample = data.len();

        let rt: RawTable = RawTable { n: nsample, start: 0, end: nsample, raw: data};
        let ed_params = &EVENT_DETECTION_DEFAULTS;

        let et1:EventTable = detect_events(rt, *ed_params).unwrap();

        // Scaled
        for i in 0 .. data2.len() {
            data2[i] = data2[i] * scale + shift;
        }
        let rt2: RawTable = RawTable { n: nsample, start: 0, end: nsample, raw: data2};
        let et2: EventTable = detect_events(rt2, *ed_params).unwrap();

        for ev in 0 .. 5 {
            assert_eq!(et1.event[ev].length, et2.event[ev].length);
            assert!(et1.event[ev].mean * scale + shift - et2.event[ev].mean < 1e-5);
        }
    }

    #[test]
    fn test_rna_read() {
        let mut buf = vec![];
        std::fs::File::open("tests/dRNA.npy").unwrap()
            .read_to_end(&mut buf).unwrap();
        let data = NpyData::from_bytes(&buf).unwrap().to_vec();

        let nsample = data.len();
        let rna = true;

        let et:EventTable = getevents(nsample, &data, rna).unwrap();
        println!("{:?}", (et.start, et.end));

        for i in 0 .. 10 {
            println!("{:?}", et.event[i]);
        }

        for i in et.event.len() - 10 .. et.event.len() {
            println!("{:?}", et.event[i]);
        }
    }
}
