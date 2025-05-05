import argparse
import sys
import time
import json

from settings import MeiCanSetting, OrderSetting

#----- todo 做成配置形式
TARGET_WEEK_DAY = 2 #周三是2
TARGET_RESTUANTS = ["麦当劳", "肯德基", "越南菜"] #目标餐馆
TARGET_DISH = [["板烧鸡腿汉堡套餐"], [], ["菌菇"]] #目标ORDER
SECOND_PRICE = 40 #找不到目标定单直接用价格

#-- config --
ORDER_FLAG = True #直接下单
SCAN_TICK = 5 * 60 # 扫描时间
TARGET_TILE = "午餐" #目标晚餐会直接下单 上面目标


start_time = time.time()
order_list = OrderSetting()
print("-------------------------")
print(type(order_list))
print(len(order_list._order))
for i in order_list._order:
    print("----- ", repr(i))