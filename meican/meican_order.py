import argparse
import sys
import time
import json

from tools import MeiCan
from settings import MeiCanSetting, OrderSetting
from exceptions import NoOrderAvailable
from commands import get_dishes, get_restaurants, get_tabs
from models import Restaurant, Tab, Dish, Section, Order

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
settings = MeiCanSetting()
settings.load_credentials()
order_list = OrderSetting()

# print(f"{settings.username}, {settings.password}, {settings.cookie}")
meican = MeiCan(settings.username, settings.password, settings.cookie)
def debug_print_json(data):
    print("data: ", json.dumps(data, indent=4, ensure_ascii=False))

def print_time():
    timer = time.time() - start_time
    hours = int(timer // 3600)
    minutes = int(timer // 60 - hours * 60)
    seconds = int(timer - hours * 3600 - minutes)
    print(f"meican bot for {hours}h {minutes}m {seconds}s")

def check_order(data_list, title):
    is_order = False # 是否已下单
    for calenar in data_list:
        # print(type(calenar))
        # debug_print_json(calenar)
        date = calenar["date"]
        for tar in calenar["calendarItemList"]:
            order_title = tar["title"]
            if tar["status"] == "ORDER" and tar["corpOrderUser"]:
                first_order_name = tar["corpOrderUser"]["restaurantItemList"][0]["dishItemList"][0]["dish"]["name"]
                print(f"{date}: {order_title}.已有订单: {first_order_name}")
                if order_title.find(title) != -1:
                    is_order = True
    return is_order 


def find_dish_and_order(data_list, order_config):
    # debug_print_json(data_list)
    tar_cal = None
    for calenar in data_list:
        date = calenar["date"]
        for tar in calenar["calendarItemList"]:
            order_title = tar["title"]
            if order_title.find(order_config.title) != -1:
                tar_cal = tar
                break
    if tar_cal is None:
        print("找到不到目标")
        return
    
    # print("============================")
    # debug_print_json(tar_cal)
    tab = Tab(tar_cal)
    restaurants = meican.get_restaurants(tab)
    dishes_list = None
    # print(restaurants)
    for y in restaurants:
        if y.name.find(order_config.restuantname) != -1:
            dishes_list = meican.get_dishes(y)
    # print(dishes_list)
    for i in order_config.dishname:
        for y in dishes_list: 
            # print(f"{i.restaurant.name}, {i.name}, {i.price}, ")
            if y.name.find(i) != -1:
                meican.order(y)
                print(f"下单成功, {y.restaurant}, {y.name}, {y.price}")
                return


def execute(argv=None):

    while True: 
        print_time()
        meican.load_tabs(True)
        try:
            for i in order_list._order:
                # print(repr(i))
                # test_data = meican.get_day(i.weekday)
                test_data = meican.get_wed_dateList()
                is_order = check_order(test_data, i.title)
                if not is_order:
                    find_dish_and_order(test_data, i)
        except NoOrderAvailable:
            print("别急，下一顿还没开放订餐")
            return
        time.sleep(SCAN_TICK)


if __name__ == "__main__":
    execute()
