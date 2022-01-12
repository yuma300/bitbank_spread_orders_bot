import time
import os
from decimal import Decimal 
import python_bitbankcc

API_KEY = os.environ['BITBANK_API_KEY']
API_SECRET = os.environ['BITBANK_API_SECRET']

prv = python_bitbankcc.private(API_KEY, API_SECRET)
pub = python_bitbankcc.public()

# -------- 設定項目 ここから
pair = 'xrp_jpy' # 取引ペア
side = 'sell' # 買いか売りか (buy|sell)
max_filled_amount = Decimal('200') # いくら以上約定したら停止するか
order_amount = Decimal('20') # 注文1個あたりの数量
interval = 500 # 何秒ごとに注文を出し直すか
step_ratio = Decimal('0.001') # 値段をバラけさせて注文出す際の値段の間隔
# -------- 設定項目 ここまで


if side == 'buy': step_ratio = -step_ratio 
order_id_list = [] # 注文IDのリスト
filled_amount = Decimal('0') # 現在いくら約定してるか

# 全注文キャンセルする関数
def close_all_orders():
  global order_id_list

  if len(order_id_list) > 0:
    # 全注文キャンセルする
    value = prv.cancel_orders(
      pair,
      order_id_list
    )

# ラストプライスに近いところで複数に価格をバラけさせて注文いれる関数
def put_orders():
  global order_id_list
  global order_amount
  global step_ratio

  # ラストプライスの取得
  value = pub.get_ticker(pair)
  last = Decimal(pub.get_ticker(pair)['last'])
  # 注文する価格を決める
  order_prices = [
    last * (1 + step_ratio * 1),
    last * (1 + step_ratio * 2),
    last * (1 + step_ratio * 3),
    last * (1 + step_ratio * 4),
    last * (1 + step_ratio * 5)
  ]
  # 注文を出す
  for price in order_prices:
    value = prv.order(
        pair, # 取引ペア
        str(price), # 価格 (成行注文の場合は None にする)
        str(order_amount), # 注文枚数
        side, # 注文サイド (buy|sell)
        'limit' # 注文タイプ (limit|market|stop|stop_limit)
    )
    order_id_list.append(str(value['order_id']))

# 約定した数量を取得する関数
def get_filled_amount():
  global filled_amount
  global order_id_list
  global max_filled_amount

  for order_id in order_id_list:
    value = prv.get_trade_history(
        pair,
        '1000',
        order_id
    )

    for trade in value['trades']:
      filled_amount += Decimal(trade['amount'])


if __name__== '__main__':
  while True: #無限ループ
    close_all_orders()
    get_filled_amount()
    # max_filled_amountで指定した数量以上に約定していれば終了
    if max_filled_amount <= filled_amount:
      print('completed more than max_completed_amount')
      exit()
    put_orders()

    time.sleep(interval) #intervalで指定した秒数待つ
