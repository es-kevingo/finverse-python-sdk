# Finverse Python SDK (Community-Driven)

A community-driven Python SDK for interacting with the [Finverse](https://www.finverse.com/) API, providing easy access to financial data and payment functionalities.

**Note:** This is an unofficial SDK. Please refer to the [official Finverse API documentation](https://docs.finverse.com/) for the most accurate and up-to-date information.

## About Finverse

Finverse is a financial data and payments platform.
- Website: [https://www.finverse.com/](https://www.finverse.com/)
- API Documentation: [https://docs.finverse.com/](https://docs.finverse.com/)

## Installation

### From PyPI (when published)
```bash
pip install finverse-python-sdk
```

### From GitHub (development)
```bash
pip install -e git+https://github.com/es-kevingo/finverse-python-sdk.git#egg=finverse-python-sdk
```

### Local development
```bash
git clone https://github.com/es-kevingo/finverse-python-sdk.git
cd finverse-python-sdk
pip install -e .
```

## Quick Start

```python
from finverse_sdk import FinverseClient

# Initialize the client
client = FinverseClient(api_key="your-api-key")

```

## Requirements

- Python 3.7+
- requests >= 2.20.0

## Contributing

Contributions are welcome! This is a community-driven project.

## License

MIT License