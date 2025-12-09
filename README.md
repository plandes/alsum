# ALignment SUMmarization

[![PyPI][pypi-badge]][pypi-link]
[![Python 3.11][python311-badge]][python311-link]
[![Python 3.12][python311-badge]][python312-link]
[![Build Status][build-badge]][build-link]

Summarize text using Component ALignment Abstract Meaning Representation (CALAMR) alignment.

**Important**: This project is now deprecated in favor of the
[FlowGraphResult.reduce] method.  See the [Aligning Ad hoc Documents] example
of how to use it in the new version of [Calamr].


## Documentation

See the [full documentation](https://plandes.github.io/alsum/index.html).  The
[API reference](https://plandes.github.io/alsum/api.html) is also available.


## Obtaining

The library can be installed with pip from the [pypi] repository:
```bash
pip3 install zensols.alsum
```


## Changelog

An extensive changelog is available [here](CHANGELOG.md).


## Community

Please star this repository and let me know how and where you use this API.
Contributions as pull requests, feedback and any input is welcome.


## License

[MIT License](LICENSE.md)

Copyright (c) 2024 - 2025 Paul Landes


<!-- links -->
[pypi]: https://pypi.org/project/zensols.alsum/
[pypi-link]: https://pypi.python.org/pypi/zensols.alsum
[pypi-badge]: https://img.shields.io/pypi/v/zensols.alsum.svg
[python3100-badge]: https://img.shields.io/badge/python-3.10-blue.svg
[python3100-link]: https://www.python.org/downloads/release/python-3100
[python311-badge]: https://img.shields.io/badge/python-3.11-blue.svg
[python311-link]: https://www.python.org/downloads/release/python-3110
[build-badge]: https://github.com/plandes/alsum/workflows/CI/badge.svg
[build-link]: https://github.com/plandes/alsum/actions

[FlowGraphResult.reduce]: https://plandes.github.io/calamr/api/zensols.calamr.html#zensols.calamr.flow.FlowGraphResult.reduce
[Aligning Ad hoc Documents]: https://github.com/plandes/calamr?tab=readme-ov-file#aligning-ad-hoc-documents
[Calamr]: https://github.com/plandes/calamr
