import python_bitbankcc
import time
import os, json
from decimal import Decimal 

API_KEY = os.environ['BITBANK_API_KEY']
API_SECRET = os.environ['BITBANK_API_SECRET']



prv = python_bitbankcc.private(API_KEY, API_SECRET)
pub = python_bitbankcc.public()

pair = 'btc_jpy' # 取引ペア
side = 'sell'
max_filled_amount = Decimal('100')
filled_amount = Decimal('0')
order_amount = Decimal('10')
interval = 10


order_id_list = [] # 注文IDのリスト


# 全注文キャンセルする関数
def close_all_orders():
  if len(order_id_list) > 0:
    # 全注文キャンセルする
    value = prv.cancel_orders(
      pair,
      order_id_list
    )
    if (value['success'] == 1):
      order_id_list = []
    else:
      print('failed to close orders')      
      exit()


# ラストプライスに近いところで複数に価格をバラけさせて注文いれる関数
def put_orders():
  # ラストプライスの取得
  value = Decimal(pub.get_ticker(pair)['data']['last'])
  # 注文する価格を決める
  order_prices = [
    value * 1.02, 
    value * 1.04, 
    value * 1.06, 
    value * 1.08,
    value * 1.10
  ]
  # 注文を出す
  for price in order_prices:
    value = prv.order(
        pair, # 取引ペア
        price, # 価格 (成行注文の場合は None にする)
        order_amount, # 注文枚数
        side, # 注文サイド (buy|sell)
        'limit' # 注文タイプ (limit|market|stop|stop_limit)
    )
    if (value['success'] == 1):
      order_id_list.append(value['data']['order_id'])
    else:
      print('failed to put orders')      
      exit()

# 約定した数量を取得する関数
def get_filled_amount():
  for order_id in order_id_list:
    value = prv.get_trade_history(
        pair, # ペア
        '1000', # 取得する約定数
        order_id
    )
    if (value['success'] == 1):
      for trade in value['data']['trades']:
        filled_amount += Decimal(trade['amount'])
    else:
      print('failed to get filled amount')      
      exit()
  pass

if __name__== '__main__':
  while True: #無限ループ
    # max_trade_amountで指定した数量以上に約定していれば終了
    if max_filled_amount <= filled_amount:
      print('completed more than max_completed_amount')
      exit()

    close_all_orders()
    get_filled_amount()
    put_orders()

    time.sleep(interval) #intervalで指定した秒数待つ
