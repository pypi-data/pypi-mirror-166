# pymt5pure

MetaTrader 5 WebAPI implementation in Python.

## Installation

```
pip install pymt5pure
```

## Usage

Create a client:

```python
from pymt5pure import MT5Client, MT5Api

client = MT5Client(host="111.111.111.111", port=443)
client.connect(username="33007", password="112233")
print("Connected!")

# Basic command call
response = client('SYMBOL_NEXT', INDEX=0)
print(response.params)
print(response.json)

# Using MT5's Official objects
mt5 = MT5Api(client)

result = mt5.symbol_total()
print(result)

result = mt5.symbol_next(0)
print(
    result.CurrencyBase,
    result.CurrencyProfit,
    result.Description
)
```

## Features

* [x] Basic socket connection
* [x] Authentication
* [x] Connection KeepAlive
* [x] AES Encryption
* [~] MT5API interfaces (incomplete)
