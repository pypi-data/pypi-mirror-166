from typing import List, Dict, Any, Optional, Union
from aiohttp import ClientSession, TCPConnector
from asyncio import sleep, Semaphore
from urllib.parse import urlencode
from datetime import datetime
from . import types
import logging
import hashlib
import hmac
import time

try:
    import ujson as json
except ImportError:
    import json


class Zixi:
    _class_instances: int = 0

    def __init__(self, api_key: str, user_id: str, disable_rate_limiting: bool = False):
        """
        Initialize Zixi class
        :param api_key: ZixiPay API key
        :param user_id: ZixiPay user ID
        :param disable_rate_limiting: Set True if you want to manage rate limits on your own
        """
        self.api_key: str = api_key
        self.user_id: str = user_id
        self._semaphore: Semaphore = Semaphore(2)
        self._disable_rate_limiting: bool = disable_rate_limiting
        Zixi._class_instances += 1
        if Zixi._class_instances == 2:
            logging.warning('Creating multiple instances of Zixi may lead to rate limit hits')

    def _sign_request(self, params: Dict[str, Any]) -> str:
        """
        Sign the request with HMAC signature
        :param params: Request parameters
        :return: HMAC signed request
        """
        return hmac.new(self.api_key.encode('utf-8'), urlencode(params).encode('utf-8'),
                        digestmod=hashlib.sha256).hexdigest()

    async def _request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Make a request to API endpoint
        :param endpoint: Endpoint to send a request to
        :param params: Request parameters
        :return: API response on success
        """
        if not self._disable_rate_limiting:
            await self._semaphore.acquire()  # API endpoints calls are limited to 2 requests/second per IP address

        if params is None:
            params = dict()
        params['uid'] = self.user_id
        params['ts'] = int(time.time())
        params['sig'] = self._sign_request(params=params)
        async with ClientSession(connector=TCPConnector(ssl=True), json_serialize=json.dumps) as session:
            result = await (await session.post(f'https://api.zixipay.com/apiv2{endpoint}', data=params)).json()
            if result['result'] != 'ok':
                raise ValueError(f'Error while performing a request to /apiv2{endpoint}: {result["payload"]}')
        await sleep(1)

        if not self._disable_rate_limiting:
            self._semaphore.release()

        return result

    async def get_balances(self) -> List[types.Balance]:
        """
        Get all wallet balances
        :return: List of types.Balance objects
        """
        result = await self._request(endpoint='/getbalances')
        to_return: List[types.Balance] = list()

        for item in result['payload']:
            to_return.append(types.Balance(name=item['name'], code=item['code'], balance=float(item['balance'])))
        return to_return

    async def get_wallets(self, currency: str) -> Union[types.Wallet, types.USDTWallet]:
        """
        Get the wallet address of a specific currency
        :param currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :return: types.Wallet or types.USDTWallet object
        """
        result = await self._request(endpoint='/getwallet', params={'currency': currency})
        wallets: dict = dict()
        if currency == 'USDT':
            for wallet in result['payload']:
                name: str = wallet['name'].split(' ')[1].lower()
                wallets[name] = types.Wallet(address=wallet['address'], name=wallet['name'], code=wallet['name'],
                                             confirm=int(wallet['confirm']))
            return types.USDTWallet(**wallets)
        result = result['payload'][0]
        return types.Wallet(address=result['address'], name=result['name'],
                            code=result['code'], confirm=int(result['confirm']))

    async def get_rates(self) -> types.Rates:
        """
        Get live exchange rates
        :return: types.Rates object
        """
        result = await self._request(endpoint='/getrates')
        rates: dict = dict()
        for rate in result['payload']:
            rates[rate['code'].lower()] = types.Rate(code=rate['code'], decimal=int(rate['decimal']),
                                                     rate=float(rate['rate']))
        return types.Rates(**rates)

    async def get_fees(self) -> types.Fees:
        """
        Get all the applicable fees and limits
        :return: types.Fees object
        """
        result = await self._request(endpoint='/getfees')
        fees = dict()
        for key, value in {'deposit': 'deposit', 'withdrawal': 'withdrawal', 'internaltransfer': 'internal_transfer',
                           'exchange': 'exchange'}.items():
            items = dict()
            for fee in result['payload'][key]:
                items[fee['symbol'].lower()] = types.Fee(name=fee['name'], symbol=fee['symbol'],
                                                         min_amount=float(fee['min_amount']),
                                                         max_amount=float(fee['max_amount']), fee=float(fee['fee']))
            fees[value] = types.FeeGroup(**items)
        return types.Fees(**fees)

    async def statement(self, txid: Optional[str] = None, time_from: Optional[datetime] = None,
                        time_to: Optional[datetime] = None, currency: Optional[str] = None,
                        status: Optional[str] = None, transaction_type: Optional[str] = None,
                        sender: Optional[str] = None, recipient: Optional[str] = None) -> List[types.Transaction]:
        """
        Get transaction(s) history with optional filters, maximum number of transactions returned is 2000
        :param txid: ZixiPay transaction ID
        :param time_from: From date
        :param time_to: To date
        :param currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param status: Transaction status (pending, processed, cancelled or blocked)
        :param transaction_type: Transaction type (deposit, withdrawal, transfer, exchange or payment)
        :param sender: Sender, could be user id or email address
        :param recipient: Recipient, could be user id, email address or crypto wallet address
        :return: types.Transaction object
        """
        params = dict()
        for key, value in locals().items():
            if value is None or key == 'self' or key == 'params':
                continue
            if key == 'time_from':
                params['timefrom'] = value.strftime('%Y-%m-%d')
            elif key == 'time_to':
                params['timeto'] = value.strftime('%Y-%m-%d')
            else:
                params[key] = value

        result = await self._request(endpoint='/statement', params=params)
        to_return: List[types.Transaction] = list()
        for transaction in result['payload']['transactions']:
            to_return.append(types.Transaction(txid=transaction['txid'],
                                               time=datetime.strptime(transaction['time'], '%Y-%m-%d %H:%M:%S'),
                                               type=transaction['type'], status=transaction['status'],
                                               amount=float(transaction['amount']), fee=float(transaction['fee']),
                                               currency=transaction['currency'], sender=transaction['sender'],
                                               recipient=transaction['recipient'], details=transaction['details'],
                                               extras=transaction['extras'], merchant_ref=transaction['merchant_ref']))
        return to_return

    async def withdraw(self, amount: float, currency: str, recipient: str, fee_in: bool = False) -> types.Transaction:
        """
        Withdraw any of the supported cryptocurrencies.
        This endpoint is used for sending funds to another wallet address on the blockchain.
        :param amount: Amount to be withdrawn
        :param currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param recipient: Recipient’s wallet address (for USDT withdrawal: TRC20, ERC20, OMNI addresses are acceptable)
        :param fee_in: Fee inclusive, deduct the fee from the withdrawal amount
        :return: types.Transaction object
        """
        params: dict = {'amount': amount, 'currency': currency, 'recipient': recipient, 'feein': int(fee_in)}
        result = await self._request(endpoint='/withdraw', params=params)
        transaction = result['payload'][0]
        return types.Transaction(txid=transaction['txid'], status=transaction['status'],
                                 amount=float(transaction['amount']), fee=float(transaction['fee']),
                                 currency=transaction['currency'], total=transaction['total'])

    async def transfer(self, amount: float, currency: str, recipient: str, note: Optional[str] = None,
                       passcode: Optional[int] = None, fee_in: bool = False) -> types.Transaction:
        """
        Internal transfer any of the supported cryptocurrencies.
        This endpoint is used for transferring funds to another ZixiPay wallet holder internally.
        Internal transfers are instant and irrevocable.
        :param amount: Amount to be transferred
        :param currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param recipient: Recipient’s email address or user id
        :param note: Internal comment for the transfer
        :param passcode: 4 digit pin if the transfer needs to be passcode protected
        :param fee_in: Fee inclusive, deduct the fee from the transfer amount
        :return: types.Transaction object
        """
        params = dict()
        for key, value in locals().items():
            if value is None or key == 'self' or key == 'params':
                continue
            if key == 'fee_in':
                params['feein'] = int(fee_in)
            else:
                params[key] = value
        result = await self._request(endpoint='/transfer', params=params)
        transaction = result['payload'][0]
        return types.Transaction(txid=transaction['txid'], status=transaction['status'],
                                 amount=float(transaction['amount']), fee=float(transaction['fee']),
                                 currency=transaction['currency'], recipient=transaction['recipient'],
                                 passcode=int(transaction['passcode']))

    async def exchange(self, amount: float, from_currency: str, to_currency: str,
                       fee_in: bool = False) -> types.Exchange:
        """
        Inter-wallet exchange is used for exchanging funds between USDZ and other currencies
        :param amount: Amount to be exchanged
        :param from_currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param to_currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param fee_in: Fee inclusive, deduct the fee from the exchange amount
        :return: types.Exchange object
        """
        params = {'amount': amount, 'from': from_currency, 'to': to_currency, 'feein': fee_in}
        result = await self._request(endpoint='/exchange', params=params)
        exc = result['payload'][0]
        return types.Exchange(from_amount=float(exc['fromamount']), from_currency=exc['fromcurrency'],
                              from_txid=exc['fromtxid'], to_amount=float(exc['toamount']),
                              to_currency=exc['tocurrency'], to_txid=exc['totxid'], rate=float(exc['rate']),
                              fee=float(exc['fee']))

    async def get_payment_wallet(self, currency: str, ref: str) -> Union[types.Wallet, types.USDTWallet]:
        """
        Get payment wallet address
        :param currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param ref: A reference tag to this payment wallet
        :return: A new wallet address everytime it is called (types.Wallet or types.USDTWallet object)
        """
        result = await self._request(endpoint='/getpaymentwallet', params={'currency': currency, 'ref': ref})
        wallets: dict = dict()

        if currency == 'USDT':
            for wallet in result['payload']:
                name: str = wallet['name'].split(' ')[1].lower()
                wallets[name] = types.Wallet(address=wallet['address'], name=wallet['name'], code=wallet['name'],
                                             confirm=int(wallet['confirm']), qr_code=wallet['qr-code'])
            return types.USDTWallet(**wallets)
        result = result['payload'][0]
        return types.Wallet(address=result['address'], name=result['name'],
                            code=result['code'], confirm=int(result['confirm']), qr_code=result['qr-code'])

    async def create_invoice(self, amount: float, currency: str, ref: str, multi_currency: bool = False,
                             validity: int = 0) -> types.Invoice:
        """
        Create a payment invoice
        :param amount: Invoice amount
        :param currency: Any of the supported currencies (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param ref: A reference tag to this invoice
        :param multi_currency: Can the invoice be paid by any of the supported cryptocurrencies?
        :param validity: Invoice validity in minutes, valid for 7 days by default
        :return: types.Invoice object
        """
        result = await self._request(endpoint='/createinvoice', params={'amount': amount, 'currency': currency,
                                                                        'ref': ref, 'multicurrency': multi_currency,
                                                                        'validity': validity})
        result = result['payload']
        return types.Invoice(invoice_id=result['invoice_id'], amount=amount, currency=currency, ref=ref,
                             accept_multi=multi_currency, validity=validity, url=result['invoice_url'],
                             qr_url=result['invoice_url_qrcode'])

    async def cancel_invoice(self, invoice_id: str) -> bool:
        """
        Cancel a payment invoice
        :param invoice_id: The invoice_id of the invoice to be cancelled
        :return: True on success
        """
        result = await self._request(endpoint='/cancelinvoice', params={'invoice_id': invoice_id})
        return result['result'] == 'ok'

    async def get_invoice(self, invoice_id: str) -> types.Invoice:
        """
        Get invoice details
        :param invoice_id: The invoice_id of the invoice
        :return: types.Invoice object
        """
        result = await self._request(endpoint='/getinvoice', params={'invoice_id': invoice_id})
        result = result['payload']
        return types.Invoice(invoice_id=result['invoice_id'], amount=float(result['amount']),
                             currency=result['currency'], date=datetime.strptime(result['date'], '%Y-%m-%d %H:%M:%S'),
                             status=result['status'], ref=result['ref'], accept_multi=bool(int(result['accept_multi'])),
                             validity=int(result['validity']))

    async def list_invoices(self, invoice_id: Optional[str] = None, ref: Optional[str] = None,
                            date_from: Optional[datetime] = None, date_to: Optional[datetime] = None,
                            currency: Optional[str] = None, status: Optional[str] = None) -> List[types.Invoice]:
        """
        Get all the invoices, optional filters could be used to narrow down the search
        :param invoice_id: The invoice_id of the invoice
        :param ref: Reference tag to the invoice
        :param date_from: From this issue date
        :param date_to: To this issue date
        :param currency: Invoice currency (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :param status: Invoice currency (USDZ, EURZ, LTC, BTC, ETH or USDT)
        :return: list of types.Invoice objects
        """
        params = dict()
        for key, value in locals().items():
            if value is None or key == 'self' or key == 'params':
                continue
            if key == 'date_from':
                params['datefrom'] = value.strftime('%Y-%m-%d')
            elif key == 'date_to':
                params['dateto'] = value.strftime('%Y-%m-%d')
            else:
                params[key] = value

        result = await self._request(endpoint='/listinvoices', params=params)
        invoices: List[types.Invoice] = list()
        for invoice in result['payload']['invoices']:
            invoices.append(types.Invoice(invoice_id=invoice['invoice_id'], amount=float(invoice['amount']),
                                          currency=invoice['currency'],
                                          date=datetime.strptime(invoice['date'], '%Y-%m-%d %H:%M:%S'),
                                          status=invoice['status'], ref=invoice['ref'],
                                          accept_multi=bool(int(invoice['accept_multi'])),
                                          validity=int(invoice['validity'])))
        return invoices
