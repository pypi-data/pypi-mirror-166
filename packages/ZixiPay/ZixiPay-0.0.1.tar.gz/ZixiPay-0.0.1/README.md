# ZixiPay
This library is an asynchronous [ZixiPay API](https://zixipay.github.io/) wrapper.\
All methods were renamed to snake_case, some function parameters as well.


### Installation
```shell
pip install zixipay
```
##### Speedups
```shell
pip install ujson
```


### Example usage
```python
from ZixiPay import Zixi, types
ZIXI: Zixi = Zixi(api_key='API_KEY', user_id='USER_ID')


invoice: types.Invoice = await ZIXI.create_invoice(amount=10, currency='USDZ', ref='TEST', multi_currency=True)
```