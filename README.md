# bitbank_spread_orders_bot

## 概要

ラストプライスを見て、ラストプライスから指定の刻み幅でプライスを散らばらせて一気に指値注文を出すbotです。
大量に利確したいときに成行注文や大量の数量で指値注文を入れたくないときに使われる事を想定しています


## 使い方

```
$ pip3 install git+https://github.com/bitbankinc/python-bitbankcc@3aee8a6ef9d4616e11f044c2a1574ec389671675\#egg=python-bitbankcc -t ./
$ export PYTHONPATH="./python_bitbankcc:$PYTHONPATH"
$ export BITBANK_API_KEY=xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
$ export BITBANK_API_SECRET=zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
$ python3 src/main.py
```