# Sara SDK Python
<div>
    <img src="https://img.shields.io/badge/version-1.0.0-blue" /> <img src="https://img.shields.io/badge/python-%3E=%203.7-green" /> <img src="https://img.shields.io/badge/license-MIT-brightgreen" />
</div>

## Getting Started

Assuming that you have a supported version of Python installed, you can first
set up your environment with:

    $ python -m venv .venv
    $ . .venv/bin/activate

Then, you can install sara SDK from PyPI with:

    $ python -m pip install sara-sdk

or install from source with:

    $ git clone https://github.com/Synkar/Sara-SDK-Python.git
    $ cd sara_sdk
    $ python -m pip install -r requirements.txt
    $ python -m pip install .

## Using Sara SDK

After installing sara-sdk

First thing to do after importing to project is use the credentials to authenticate

    sara_sdk.auth("access_key", "secret_key")

After this you can call the function would like to run.

Example:

    sara_sdk.iam.apps.list()

## Running Tests

You can run test to all functions by running `pytest` in the project by using:

    $ pytest

Or run on a specific file (module)

    $ pytest -v tests/test_apps.py

## Getting Help

We use GitHub issues for tracking bugs and feature requests

## Contributing

We value feedback and contributions from our community. Whether it's a bug report, new feature, correction, or additional documentation, we welcome your issues and pull requests.
