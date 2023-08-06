# Orijin-SDK for Python 3.10
Originally intended for internal use and just called python-tools, this SDK can act as a frontend client and allow you to replicate calls made by the brand platform and mobile apps.  This project was built on top of the Old-Orijin data migration tool, but has since had significant overhauls.

## Package Description
This repo contains the Orijin SDK for Python. **This library was built for python-3.10.1**

Install the latest release with `pip install --upgrade orijin-sdk` or clone this repo and install with `pip install -e /path/to/repo/`

See the scripts in `/scripts/` for simple examples or the demon in `/demo/` for a more in-depth guide to fully utilize this package.

## Usage

This package doesn't have a specific usage, rather it is a collection of helpful functions to make building python apps that connect to the Orijin system easier.

See `/scripts/` and `/demo/` for examples.

## Development Setup

To contribute to this sdk, clone this repo and run the following from the clone's root folder.

### Create or enter a virtual environment (Optional):
```
py -m venv .venv         # Run once
./venv/Scripts/activate  # Run every time
```

### Install requirements:
```
pip install -r requirements.txt
```

### Compile from source

To install the orijin-sdk from source, run:
```
pip install -e .
```
> Replace `.` with `/path/to/repo` to install from another directory

Go into a Python cli (run `py`) and test frequently that everything is working as expected during development.
Run `exit()` or `[Ctrl-Z], [enter]` to leave the cli.

## Release Development Setup

These additional steps are only requiered if you're contributing to a distributable build.

See https://packaging.python.org/en/latest/tutorials/packaging-projects/ for full instrutctions.
The guide below has instructions written for Windows, though the main difference is just using the command `py` instead of `python3`.

### First Time Setup

Inside your environment, install the following additional tools:

Python Build Tool: `py -m pip install --upgrade build`

PyPi Upload Tool: `py -m pip install --upgrade twine`

And set up a second venv for testing: `py -m venv testing`

### Build

Increment the version number (\<major>.\<minor>.\<patch>) in `setup.py`

To build a new distributable, run:
```
py -m build
```
> You can see your builds in the `/dist/` folder, though you don't need to use them locally.

### Test Upload

Test your build by uploading it to Test PyPi first:
```
py -m twine upload --repository testpypi dist/*
```
And install that upload in your testing environment:
```
testing/Scripts/activate
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade orijin-sdk
py -m pip install -r requirements.txt
```

Go into a Python cli (run `py`) and test everything is still working as expected.

Once you're done testing remember to return to your project venv: `.venv/Scripts/activate`
### Release

Upload to PyPi:
```
py -m twine upload dist/*
```