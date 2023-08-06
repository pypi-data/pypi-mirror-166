# Evmospy

[![PyPI version](https://badge.fury.io/py/evmoswallet.svg)](https://badge.fury.io/py/evmoswallet) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/hanchon-live/evmoswallet/master.svg)](https://results.pre-commit.ci/latest/github/hanchon-live/evmoswallet/master)

Python3.9+ utils for the Evmos Blockchain.

## Requirements

The cryptocurve dependency requires some libs to be built:

```sh
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev autoconf libtool pkgconf
```

MacOS:

```sh
brew install autoconf automake libtool
```

## Installation

```sh
pip install evmospy
```

## MacOS openssl error

If you get the error that says something like `the libcrypto is running on unsafe mode` and the process is aborted:

```sh
brew install openssl
sudo ln -s /opt/homebrew/opt/openssl@1.1/lib/libcrypto.1.1.dylib /usr/local/lib
sudo ln -s /opt/homebrew/opt/openssl@1.1/lib/libssl.1.1.dylib /usr/local/lib
cd /usr/local/lib
sudo ln -s libcrypto.3.dylib libcrypto.dylib
sudo ln -s libssl.3.dylib libssl.dylib
```

## Usage

Inside each `./evmospy/<module>/` there is a README file with an example on how to use the module.
