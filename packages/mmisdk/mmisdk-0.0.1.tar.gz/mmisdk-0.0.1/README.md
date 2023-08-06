# MMI Custodian SDK

A Python library to create and submit EVM transactions to custodians connected with MetaMask Institutional.

## User documentation and examples

For documentation on how to use the library, please visit the page [MetaMask Institutional SDK](https://consensys.gitlab.io/codefi/products/mmi/mmi-sdk-py/sdk-python/), or [`docs/sdk-python.md`](docs/sdk-python.md).

You can also explore various usage examples in the directory [`./examples`](./examples).

## Developer documentation

🚨 The commands we list below use `python` and `pip`. Depending on your local setup, you might need to replace them by `python3` and `pip3`.

### Requirements

- Python 3.7 or above

### Installing dependencies

To install `mmisdk`, along with the tools you need to develop and run tests, run the following:

```bash
pip install -e .[dev]
```

### Unit tests

```bash
./run_tests.sh
```

### Building the package

```bash
python3 setup.py bdist_wheel sdist
```

### Creating / Updating the manifest

```bash
pip install check-manifest
check-manifest --create
```
