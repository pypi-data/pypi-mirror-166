use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use numpy::{IntoPyArray, PyArray1};
// use ndarray;

use crate::events::{EventTable, EventT, getevents};
use crate::eventalign::time_series_search;

// Interface for scrappie functions
#[pyfunction(is_rna = true)]
#[pyo3(text_signature = "(data, is_rna)")]
fn split_signals(
    // py: Python,
    data: &PyArray1<f32>,
    is_rna: bool,
) -> Result<EventTable, PyErr> {
    let nsample = data.len();
    let data = data.to_vec()?;

    let et: EventTable = match getevents(nsample, &data, is_rna) {
        Ok(x) => x,
        Err(_) => EventTable::default(),
    };
    Ok(et)
}

// Interface for DTW alignment
#[pyfunction(number=1, alpha = "0.5")]
#[pyo3(text_signature = "(query, reference, alpha)")]
fn search_signals <'py>(
    py: Python<'py>,
    query: &PyArray1<f32>,
    reference: &PyArray1<f32>,
    output: usize,
    alpha: f32,
) -> Result<(
    &'py PyArray1<usize>,
    &'py PyArray1<usize>,
    &'py PyArray1<f32>,
    Vec<(&'py PyArray1<usize>, &'py PyArray1<usize>)>
), PyErr> {
    let ret = unsafe {
        let q = query.as_array();
        let r = reference.as_array();
        py.allow_threads(|| {
            time_series_search(&q, &r, output, alpha)
        })
    }?;

    Ok((
        ret.0.into_pyarray(py),
        ret.1.into_pyarray(py),
        ret.2.into_pyarray(py),
        ret.3.mapv(|a| (a.0.into_pyarray(py), a.1.into_pyarray(py))).to_vec(),
    ))
}

// Python module
#[pymodule]
fn event_tools(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(split_signals, m)?)?;
    m.add_function(wrap_pyfunction!(search_signals, m)?)?;
    m.add_class::<EventTable>()?;
    m.add_class::<EventT>()?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    Ok(())
}
