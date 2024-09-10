[![Dry Run](https://github.com/d33p0st/python-rust-mix-build/actions/workflows/test.yml/badge.svg)](https://github.com/d33p0st/python-rust-mix-build/actions/workflows/test.yml)

# Overview

`python-rust-mix-build` is a GitHub Action that checks if the Python-Rust mix project passes build or not.

## Usage

Test case usage for `python-rust-mix-build`.

```yaml
name: Build Test

on: [push]

jobs:
    Test:
        runs-on: ubuntu-latest # multiple can be added
        steps:
            - name: Checkout Repo
              uses: actions/checkout@v3

            - name: Run Build Test
              uses: d33p0st/python-rust-mix-build@v1
              with:
                python-version: 3.9 # set python version. default: 3.12
                miniconda-version: # set miniconda version. default: "latest"
```

## Requirements

For this action to work on your Python-Rust mix project, make sure you have `Cargo.toml` and `pyproject.toml` intact and follows the proper rules.

> For Example, the following entries should be there in your Cargo.toml

```toml
[lib]
crate-type = ["cdylib"]

[build-dependencies]
cc = "1.0"
```

> Note: This will not work in pure rust or pure python projects. Make sure you are using `pyo3` crate in rust to create binaries that can be called from a python script or file. Additionaly, `maturin` is being used to test the build which means `pyproject.toml` should have an entry about it.

> A demo [`pyproject.toml`](https://github.com/d33p0st/python-rust-mix-build/blob/main/pyproject.toml) and [`Cargo.toml`](https://github.com/d33p0st/python-rust-mix-build/blob/main/Cargo.toml) is provided [here](https://github.com/d33p0st/python-rust-mix-build).

## Inputs

`python-rust-mix-build` has three inputs:

- `python-version`: specify the python version. Default is `3.12`
- `miniconda-version`: specify the miniconda version to use as `maturin` needs either venv or miniconda to work. Default is `"latest"`
- `replace`: Takes boolean values. Default is `false`. This builds and pushes that built binary back to the repository.
  
  For this to work, add an addition line to your workflow file:
  ```yaml
  permissions: write-all
  ``` 
- `GH_TOKEN`: This takes GITHUB API TOKEN as input, if `permissions: write-all` line is provided, The action will automatically get the GITHUB TOKEN from your account. However, If not provided, `GH_TOKEN` needs to be set with proper permissions.

## Caution

You need to pull auto-generated commits in case of using `replace` input, Else your repo will mess up.

## Issues

Feel free to submit any issues [here](https://github.com/d33p0st/python-rust-mix-build/issues).

## Pull Requests

Create any relevant pull requests [here](https://github.com/d33p0st/python-rust-mix-build/pulls).