use std::cmp::Ordering;
use std::f32::INFINITY as inf;

// use ndarray::prelude::*;
use ndarray::{array, s, Data, ArrayBase, Array, Ix1, Ix2};
// use ndarray_stats::QuantileExt;
use anyhow::{Result, ensure};

/**
  The following code taken from tssearch at https://github.com/fraunhoferportugal/tssearch
  The tssearch repository is under BSD-3-Clause license
*/

/**
 * np.diff
 *
 * Parameters
 * ----------
 * x: 1d-array with length n
 *
 * Returns
 * -------
 * x_diff: 1d-array with length n -1
 *
 **/
fn diff <D: Data<Elem = f32>>(
    x: &ArrayBase<D, Ix1>,
) -> Result<Array<f32, Ix1>> {
    let n = x.len();
    ensure!(n > 0, "Empty x for calculating diff");
    let mut x_diff = Array::zeros(n - 1);
    for i in 1 .. n {
        x_diff[i-1] = x[i] - x[i-1];
    }
    Ok(x_diff)
}

/**
 * Get standardization parameters
 *
 * Parameters
 * ----------
 * x: 1d-array with length n
 *
 * Returns
 * -------
 * x_mean: f32
 * x_std: f32
 */
fn stand_param <D: Data<Elem = f32>>(
    x: &ArrayBase<D, Ix1>
) -> Result<(f32, f32)> {
    let n = x.len();
    let x_mean: f32 = x.sum() / n as f32;
    let x_var: f32 = (x - x_mean).mapv(|a| a.powi(2)).sum() / n as f32;
    let x_std: f32 = x_var.sqrt();
    Ok((x_mean, x_std))
}

/**
 * Standardization with (x - mean) / stdv
 *
 * Parameters
 * ----------
 * x: 1d-array
 *
 * Returns
 * -------
 * x_stand: standardized x
 */
fn standardization <D: Data<Elem = f32>>(
    x: ArrayBase<D, Ix1>,
    mean: f32,
    std: f32,
) -> Result<Array<f32, Ix1>> {
    let x_stand = x.mapv(|a| a - mean) / std;
    Ok(x_stand)
}

/**
 * Cost matrix using (x - y) ** 2
 *
 * Parameters
 * ----------
 * x: nd-array
 *      Time series x (query).
 * y: nd-array
 *      Time series y.
 *
 * Returns
 * -------
 * c: nd-array
 *      The cost matrix.
 */
fn _cost_matrix <D: Data<Elem = f32>>(
    x: &ArrayBase<D, Ix1>,
    y: &ArrayBase<D, Ix1>,
) -> Result<Array<f32, Ix2>>{
    let l1 = x.len();
    let l2 = y.len();

    let mut c: Array<f32, Ix2> = Array::zeros((l1, l2));

    for i in 0 .. l1 {
        for j in 0 .. l2 {
            c[[i, j]] = (x[i] - y[j]).powi(2);
        }
    }

    Ok(c)
}

/**
 *  Computes cost matrix using a specified distance (dist) between two time series.
 *  Parameters
 *  ----------
 * x: nd-array
 *     Time series x (query).
 * y: nd-array
 *     Time series y.
 * alpha: weight of derivative / standardization cost
 * Returns
 * -------
 * c: nd-array
 **/
fn cost_matrix <D: Data<Elem = f32>>(
    x: &ArrayBase<D, Ix1>,
    y: &ArrayBase<D, Ix1>,
    alpha: f32,
) -> Result<Array<f32, Ix2>> {
    ensure!(x.len() > 0, "Invalid query");
    ensure!(y.len() > 0, "Invalid reference");

    let weights: Array<f32, Ix2> = Array::ones((x.len()-1, 1));

    // Derivative calculation
    let x_diff = diff(x)?;
    let y_diff = diff(y)?;

    // standardization parameters
    let abs_norm = stand_param(x)?;
    let diff_norm = stand_param(&x_diff)?;

    // Derivative calculation and standardization
    let d_x = standardization(x_diff, diff_norm.0, diff_norm.1)?;
    let d_y = standardization(y_diff, diff_norm.0, diff_norm.1)?;

    // same length of derivative
    let n_x = standardization(x.slice(s![0..x.len()-1]), abs_norm.0, abs_norm.1)?;
    let n_y = standardization(y.slice(s![0..y.len()-1]), abs_norm.0, abs_norm.1)?;

    // Cost matrix
    let cost_d = _cost_matrix(&d_x, &d_y)? * &weights;
    let cost_n = _cost_matrix(&n_x, &n_y)? * &weights;

    let c: Array<f32, Ix2> = alpha * cost_n + (1.0 - alpha) * cost_d;

    Ok(c)
}

/**
 * Initializes the cost matrix according to the dtw type.
 * Parameters
 * ----------
 * x: nd-array
 *      Time series x (query).
 * y: nd-array
 *      Time series y.
 * tolerance: int
 *      Tolerance value.
 *
 * Returns
 * -------
 * ac: nd-array
 *      The accumulated cost matrix.
 */
fn acc_initialization(
    x: usize,
    y: usize,
    _tolerance: f32,
) -> Result<Array<f32, Ix2>>{
    let mut ac: Array<f32, Ix2> = Array::zeros((x+1, y+1));
    ac.slice_mut(s![1.., 0]).fill(inf);
    Ok(ac)
}

/**
 * Fast computation of accumulated cost matrix using cost matrix.
 *
 * Parameters
 * ----------
 * ac: nd-array
 *      Given cost matrix c, ac = acc_initialization(...), ac[1:, 1:] = c.
 *
 * Returns
 * -------
 * ac : The accumulated cost matrix.
 */
fn _accumulated_cost_matrix(
    ac: &mut Array<f32, Ix2>
) -> Result<&mut Array<f32, Ix2>> {
    let shape = ac.shape().to_vec();
    for i in 0 .. shape[0] - 1 {
        for j in 0 .. shape[1] - 1 {
            ac[[i+1, j+1]] += f32::min(
                ac[[i, j+1]], f32::min(ac[[i+1, j]], ac[[i, j]])
            );
        }
    }

    Ok(ac)
}

/**
 * Get the accumulated cost matrix
 *
 * Parameters
 * ----------
 * c: nd-array
 *      The cost matrix
 *
 * Returns
 * -------
 * ac: nd-array
 *      The accumulated cost matrix
 */
fn accumulated_cost_matrix <D: Data<Elem = f32>>(
    c: ArrayBase<D, Ix2>,
    _factor: f32,
    tolerance: f32,
) -> Result<Array<f32, Ix2>>{
    let shape = c.shape();
    let mut ac: Array<f32, Ix2> = acc_initialization(shape[0], shape[1], tolerance)?;
    ac.slice_mut(s![1.., 1..]).assign(&c);
    let ret = _accumulated_cost_matrix(&mut ac)?.slice(s![1.., 1..]).to_owned();
    Ok(ret)
}

/**
 * Compute Dynamic Time Warping (DTW) of two time series.
 *
 * Parameters
 * ----------
 * x : 1d-array
 *      Time series x (query)
 * y : nd-array
 *      Time series y (reference)
 * alpha : float
 *      the cost matrix factor
 *
 * Returns
 * -------
 * d: float
 *      The DTW distance
 * ac : 2d-array
 *      The accumulated cost matrix
 */
fn dtw <D: Data<Elem = f32>>(
    x: &ArrayBase<D, Ix1>,
    y: &ArrayBase<D, Ix1>,
    alpha: f32,
) -> Result<(Array<f32, Ix1>, Array<f32, Ix2>)>{
    let xl = x.len();
    let yl = y.len();
    let factor = usize::min(xl, yl) as f32 * 0.5;
    let tolerance = 0f32;

    // cost matrix
    let c = cost_matrix(&x, &y, alpha)?;

    // accumulative cost matrix
    let ac = accumulated_cost_matrix(c, factor, tolerance)?;

    // Distance
    let d = ac.slice(s![-1, ..]).to_owned();

    Ok((d, ac))
}

/**
 * Find local maxima in a 1D array
 * From https://github.com/scipy/scipy/blob/4cf21e753cf937d1c6c2d2a0e372fbc1dbbeea81/scipy/signal/_peak_finding_utils.pyx
 *
 * This function finds all local maxima in a 1D array and returns the indices
 * for their edges and midpoints (rounded down for even plateau sizes).
 *
 * Parameters
 * ----------
 * x : ndarray
 *      The array to search for local maxima.
 *
 * Returns
 * -------
 * midpoints : ndarray
 *      Indices of midpoints of local maxima in `x`.
 * left_edges : ndarray
 *      Indices of edges to the left of local maxima in `x`.
 * right_edges : ndarray
 *      Indices of edges to the right of local maxima in `x`.
 *
 * Notes
 * -----
 * - Compared to `argrelmax` this function is significantly faster and can
 *   detect maxima that are more than one sample wide. However this comes at
 *   the cost of being only applicable to 1D arrays.
 * - A maxima is defined as one or more samples of equal value that are
 *   surrounded on both sides by at least one smaller sample.
 *
 * .. versionadded:: 1.1.0
 */
fn _local_maxima_1d <D: Data<Elem = f32>>(
    x: &ArrayBase<D, Ix1>,
) -> Result<(Array<usize, Ix1>, Array<usize, Ix1>, Array<usize, Ix1>)>{
    let n = x.len() / 2;

    // Preallocate, there can't be more maxima than half the size of `x`
    let mut midpoints: Array<usize, Ix1> = Array::zeros((n, ));
    let mut left_edges: Array<usize, Ix1> = Array::zeros((n, ));
    let mut right_edges: Array<usize, Ix1> = Array::zeros((n, ));
    let mut m = 0; // Pointer to the end of valid area in allocated arrays

    let mut i = 1; // Pointer to current sample, first one can't be maxima
    let i_max = x.len() - 1; // Last sample can't be maxima
    while i < i_max  {
        // Test if previous sample is smaller
        if x[i - 1] < x[i] {
            let mut i_ahead = i + 1; // Index to look ahead of current sample

            // Find next sample that is unequal to x[i]
            while i_ahead < i_max && x[i_ahead] == x[i] {
                i_ahead += 1;
            }

            // Maxima is found if next unequal sample is smaller than x[i]
            if x[i_ahead] < x[i] {
                left_edges[m] = i;
                right_edges[m] = i_ahead - 1;
                midpoints[m] = (left_edges[m] + right_edges[m]) / 2;
                m += 1;
                // Skip samples that can't be maximum
                i = i_ahead;
            }
        }
        i += 1;
    }

    midpoints = midpoints.slice(s![..m]).to_owned();
    left_edges = left_edges.slice(s![..m]).to_owned();
    right_edges = right_edges.slice(s![..m]).to_owned();

    Ok((midpoints, left_edges, right_edges))
}

/**
 * A simple argsort function from https://github.com/rust-ndarray/ndarray/issues/1145
 *
 * Parameters
 * ----------
 * arr : 1d-array for sort
 *
 * Returns
 * -------
 * indices : sorted indices
 */
fn argsort_by<S, F>(arr: &ArrayBase<S, Ix1>, mut compare: F) -> Vec<usize>
where
    S: Data,
    F: FnMut(&S::Elem, &S::Elem) -> Ordering,
{
    let mut indices: Vec<usize> = (0..arr.len()).collect();
    indices.sort_unstable_by(move |&i, &j| compare(&arr[i], &arr[j]));
    indices
}

/**
 * Evaluate which peaks fulfill the distance condition.
 *
 * Parameters
 * ----------
 * peaks : ndarray
 *      Indices of peaks in `vector`.
 * priority : ndarray
 *      An array matching `peaks` used to determine priority of each peak. A
 *      peak with a higher priority value is kept over one with a lower one.
 * distance : np.float64
 *      Minimal distance that peaks must be spaced.
 * Returns
 * -------
 * keep : ndarray[bool]
 *      A boolean mask evaluating to true where `peaks` fulfill the distance
 *      condition.
 * Notes
 * -----
 * Declaring the input arrays as C-contiguous doesn't seem to have performance
 * advantages.
 * .. versionadded:: 1.1.0
 */
fn _select_by_peak_distance <S, D>(
    peaks: &ArrayBase<S, Ix1>,
    priority: &ArrayBase<D, Ix1>,
    distance: usize,
) -> Result<Array<bool, Ix1>> where
    S: Data<Elem = usize>,
    D: Data<Elem = f32>
{
    let peaks_size = peaks.len();
    let mut keep: Array<bool, Ix1> = Array::from_elem((peaks_size,), true); // Prepare array of flags

    // Create map from `i` (index for `peaks` sorted by `priority`) to `j` (index
    // for `peaks` sorted by position). This allows to iterate `peaks` and `keep`
    // with `j` by order of `priority` while still maintaining the ability to
    // step to neighbouring peaks with (`j` + 1) or (`j` - 1).
    let priority_to_position = argsort_by(&priority, |a, b| a
        .partial_cmp(b)
        .expect("SortError: Elements must not be NaN."));

    // Highest priority first -> iterate in reverse order (decreasing)
    for i in (0 .. peaks_size).rev() {
        // "Translate" `i` to `j` which points to current peak whose
        // neighbours are to be evaluated
        let j = priority_to_position[i];
        if keep[j] == false {
            // Skip evaluation for peak already marked as "dont't keep"
            continue
        }

        if j > 0 { // Prevent overflow
            let mut k = j - 1;
            // Flag "earlier" peaks for removal until minimal distance is exceeded
            while peaks[j] - peaks[k] < distance {
                keep[k] = false;
                if k == 0 {
                    break; // Prevent overflow
                }
                k -= 1;
            }
        }

        let mut k = j + 1;
        // Flag "later" peaks for removal until minimal distance is exceeded
        while k < peaks_size && peaks[k] - peaks[j] < distance {
            keep[k] = false;
            k += 1;
        }
    }

    Ok(keep)
}

/**
 * Get new array using mask array
 *
 * Parameters
 * ----------
 * x : 1d-array
 *      Input data
 * mask : 1d-array[bool]
 *      Mask data
 *
 * Returns
 * -------
 * keep : 1d-array
 *      Masked array
 */
fn mask_array <S, D>(
    x: &ArrayBase<D, Ix1>,
    mask: &ArrayBase<S, Ix1>,
) -> Result<Array<usize, Ix1>> where
   S: Data<Elem = bool>,
    D: Data<Elem = usize>,
{
    let n = mask.mapv(|x| x as usize).sum();
    let mut keep: Array<usize, Ix1> = Array::zeros((n, ));

    let mut j = 0;
    for i in 0 .. mask.len() {
        if mask[i] {
            keep[j] = x[i];
            j += 1;
        }
    }

    Ok(keep)
}

/**
 * Find peaks inside a signal based on peak properties.
 *
 * This function takes a 1-D array and finds all local maxima by
 * simple comparison of neighboring values. Optionally, a subset of these
 * peaks can be selected by specifying conditions for a peak's properties.
 *
 * Parameters
 * ----------
 * x: sequence
 *      A signal with peaks
 * distance: number, optional
 *      Required minimal horizontal distance (>=1) in samples between
 *      neighbouring peaks. Smaller peaks are removed first until the condition
 *      is fulfilled for all remaining peaks
 *
 * Returns
 * -------
 * peaks: ndarray
 *      Indices of peaks in `x` that satisfy all given conditions
 */
fn find_peaks <D: Data<Elem = f32>>(
    x: &ArrayBase<D, Ix1>,
    distance: usize,
) -> Result<Array<usize, Ix1>> {
    ensure!(distance >= 1, "`distance` must be greater or equal to 1");

    let _ret = _local_maxima_1d(x)?;
    let peaks = _ret.0;
    let _left_edges = _ret.1;
    let _right_edges = _ret.2;

    let priority = peaks.mapv(|a| x[a]);
    let keep = _select_by_peak_distance(&peaks, &priority, distance)?;

    let ret = mask_array(&peaks, &keep)?;

    Ok(ret)
}

/**
 * Method to retrieve the k-best occurrences from a given vector distance
 *
 * Parameters
 * ----------
 * distance: nd-array
 *      distance values
 * output: tuple
 *      number of occurrences
 * overlap: float
 *      minimum distance between occurrences
 *
 * Returns
 * -------
 * id_s: nd-array
 *     indexes of k-best occurrences
 */
fn start_sequences_index <D: Data<Elem = f32>>(
    distance: &ArrayBase<D, Ix1>,
    output: usize,
    overlap: usize,
) -> Result<Array<usize, Ix1>> {
    let _neg_dis = distance.mapv(|a| a * -1.0);
    let pks = find_peaks(&_neg_dis, overlap)?;
    if pks.len() == 0 {
        return Ok(pks);
    }

    let pks_val = pks.mapv(|x| distance[x]);
    let pks_val_sort: Array<usize, Ix1> = Array::from(
        argsort_by(&pks_val, |a, b| a
        .partial_cmp(b)
        .expect("SortError: Elements must not be NaN.")));

    let n = output.min(pks_val_sort.len());
    Ok(pks_val_sort.slice(s![..n]).mapv(|a| pks[a]))
}

/**
 * Computes the adjusted traceback path of the matrix c.
 *
 * Parameters
 * ----------
 * ac : nd-array
 *      The accumulated cost matrix.
 *
 * Returns
 * -------
 * ret : (nd-array, nd-array)
 *      Coordinates of the minimum path adjusted.
 */
fn traceback_adj <D: Data<Elem = f32>>(
    ac:&ArrayBase<D, Ix2>,
) -> Result<(Array<usize, Ix1>, Array<usize, Ix1>)>{
    let mut i = ac.shape()[0] - 2;
    let mut j = ac.shape()[1] - 2;
    let mut p = vec![i];
    let mut q = vec![j];
    while i > 0 && j > 0 {
        let mut tb = 0;
        if ac[[i, j+1]] < ac[[i, j]] {
            tb = 1;
        }
        if ac[[i+1, j]] < ac[[i, j+tb]] {
            tb = 2;
        }
        if tb == 0 {
            i -= 1;
            j -= 1;
        } else if tb == 1 {
            i -= 1;
        } else {
            j -= 1;
        }
        p.push(i);
        q.push(j);
    }
    while i > 0 {
        i -= 1;
        p.push(i);
        q.push(j);
    }
    p.reverse();
    q.reverse();
    let _p = Array::from_vec(p);
    let _q = Array::from_vec(q);
    Ok((_p, _q))
}

/**
 * Time series search method locates the k-best occurrences of a given query on a more extended sequence based on a
 * distance measurement.
 *
 * Parameters
 * ----------
 * query : 1d-array
 *      Query signal
 * sequence : 1d-array
 *      Sequence signal
 *
 * Returns
 * -------
 * start_index : usize
 *      Start of aligned path
 * end_index : usize
 *      End of aligned path
 * path_dist : f32
 *      DTW distance of path
 * path : (p, q)
 *      Aligned path
 *
 */
pub fn time_series_search <D: Data<Elem = f32>>(
    query: &ArrayBase<D, Ix1>,
    sequence: &ArrayBase<D, Ix1>,
    output: usize,
    alpha: f32,
) -> Result<(
    Array<usize, Ix1>,
    Array<usize, Ix1>,
    Array<f32, Ix1>,
    Array<(Array<usize, Ix1>, Array<usize, Ix1>), Ix1>
)>
{
    let _ret = dtw(query, sequence, alpha)?;
    let distance = _ret.0;
    let ac = _ret.1;

    let end_index = start_sequences_index(&distance, output, query.len() / 2)?;

    let path: Array<(Array<usize, Ix1>, Array<usize, Ix1>), Ix1> = end_index.mapv(|a|
        traceback_adj(&ac.slice(s![.., ..a+1])).unwrap()
    );
    let path_dist = end_index.mapv(|a| distance[a]);
    let start_index: Array<usize, Ix1> = path.mapv(|a| a.1[0]);

    Ok((start_index, end_index, path_dist, path))
}


#[cfg(test)]
mod tests {
    use super::*;
    use std::io::prelude::*;
    use npy::NpyData;

    #[test]
    fn test_diff() {
        let x: Array<f32, Ix1> = array![1., 2., 3., 4., 5.];
        let _diff = diff(&x).unwrap();
        assert_eq!(_diff, array![1., 1., 1., 1.]);
    }

    #[test]
    fn test_standaridzation() {
        let x: Array<f32, Ix1> = array![1., 2., 1., 2., 1., 2.];
        let y = stand_param(&x).unwrap();
        let _stand = standardization(x, y.0, y.1).unwrap();
        assert_eq!(_stand, array![-1., 1., -1., 1., -1., 1.]);
    }

    #[test]
    fn test_acc_cost() {
        let x: Array<f32, Ix1> = array![1., 2., 3., 4., 3., 2., 1., 2., 1., 0., 1.];
        let y: Array<f32, Ix1> = array![1.5, 2.5, 1.5];
        let xl = x.len();
        let yl = y.len();
        let factor = usize::min(xl, yl) as f32 * 0.5;
        let tolerance = 0f32;
        let c =  cost_matrix(&x, &y, 0.5).unwrap();
        let ac = accumulated_cost_matrix(c, factor, tolerance).unwrap();

        let _ac = array![
            [0.10083334, 2.9075003],
            [0.20166668, 2.2016668],
            [1.1091669, 2.3025],
            [5.63, 2.016667],
            [8.5375, 2.1175003],
            [10.638334, 2.2183337],
            [10.739167, 5.125834],
            [12.84, 5.2266674],
            [14.940834, 6.1341677],
            [15.848334, 10.655001],
        ];
        assert_eq!(ac, _ac);
    }

    #[test]
    fn test_dtw() {
        let x: Array<f32, Ix1> = array![1., 2., 3., 4., 3., 2., 1., 2., 1., 0., 1.];
        let y: Array<f32, Ix1> = array![1.5, 2.5, 1.5];
        let _dtw = dtw(&x, &y, 0.5).unwrap();
        assert_eq!(_dtw.0, array![15.848334, 10.655001]);
    }

    #[test]
    fn test_search() {
        let t: Array<f32, Ix1> = Array::range(0., 20.*3.14, 0.1);
        let sequence: Array<f32, Ix1> = t.mapv(|x| x.sin());
        let query: Array<f32, Ix1> = t.slice(s![0usize..70usize]).mapv(|x| x.sin()) - 0.0;
        let ret = time_series_search(&query, &sequence, 5, 0.5).unwrap();
        assert_eq!(ret.0[0], 0);
        assert_eq!(ret.1[0], 68);
        assert_eq!(ret.2[0], 0.0);
    }

    #[test]
    fn test_fail() {
        let query: Array<f32, Ix1> = array![1., 2., 3., 4., 5.];
        let sequence: Array<f32, Ix1> = array![1., 2.];
        let ret = time_series_search(&query, &sequence, 1, 0.5).unwrap();
        assert_eq!(ret.0.len(), 0);
    }

    #[test]
    fn test_rna() {
        use crate::events::getevents;

        let mut buf: Vec<u8> = vec![];
        std::fs::File::open("tests/sequence.npy").unwrap()
            .read_to_end(&mut buf).unwrap();
        let sequence: Vec<f32> = NpyData::from_bytes(&buf).unwrap().to_vec();
        let sequence_et = getevents(sequence.len(), &sequence, true).unwrap();

        let mut buf2: Vec<u8> = vec![];
        std::fs::File::open("tests/query.npy").unwrap()
            .read_to_end(&mut buf2).unwrap();
        let query: Vec<f32> = NpyData::from_bytes(&buf2).unwrap().to_vec();
        let query_et = getevents(query.len(), &query, true).unwrap();

        // Create ndarray
        let p = sequence_et.event.iter().map(|x| x.mean).collect::<Vec<f32>>();
        let q = query_et.event.iter().map(|x| x.mean).collect::<Vec<f32>>();
        let x = Array::from_vec(p);
        let y = Array::from_vec(q);

        let ret = time_series_search(&x, &y, 1, 0.5).unwrap();

        assert_eq!(ret.0[0], 53);
        assert_eq!(ret.1[0], 167);
        assert_eq!(ret.2[0], 264.31802);
    }
}