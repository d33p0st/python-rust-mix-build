use pyo3::prelude::*;

#[pyfunction]
fn demo() -> PyResult<()> {
    Ok(())
}

#[pymodule]
fn rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(demo, m)?)?;
    Ok(())
}