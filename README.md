# TTS Code Sample - SLCSP

The prompt for this code sample is in PROMPT.md.

## Installation

This was written on Python 3.10.1.

(todo: test on earlier versions of Python)

Everything is in the standard library, but if you want to run static type analysis or linting you'll need `mypy` and `black` respectively. These are included in the `requirements-dev.txt` for your convenience - you'll probably want to install those into a virtual environment, too.

```bash
$ # Optional, but helps you not mess up your Python environment
$ python -m venv .venv
$ source .venv/bin/activate
$ # Actually install
(.venv) $ pip install -r requirements-dev.txt
```

## Testing

We have some automated tests:

```bash
$ ./test_slcsp.py
```

## Usage

```bash
$ ./slcsp.py -h 
usage: [-h] slcsp plans zips

Output the second-lowest-cost Silver plan for each ZIP code to stdout in CSV format.

positional arguments:
  slcsp       File containing ZIP codes to calculate SLCSP for.
  plans       File containing plan information.
  zips        File containing a ZIP code to rate area mapping.

options:
  -h, --help  show this help message and exit
```