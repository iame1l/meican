import sys
import time
import json

from .tools import MeiCan
from .settings import MeiCanSetting, OrderSetting
from .exceptions import MeiCanLoginFail, NoOrderAvailable
from .models import Tab

#-- config --
SCAN_TICK = 10 * 60 # 扫描时间


start_time = time.time()
settings = MeiCanSetting()
order_list = OrderSetting()


def build_meican():
    cookie = settings.load_cookie()
    if not cookie:
        print("没有找到 cookie，请先完成一次登录：")
        print("    python -m meican.login")
        sys.exit(1)
    return MeiCan(cookie=cookie)


def debug_print_json(data):
    print("data: ", json.dumps(data, indent=4, ensure_ascii=False))

def print_time():
    timer = time.time() - start_time
    hours = int(timer // 3600)
    minutes = int(timer // 60 - hours * 60)
    seconds = int(timer - hours * 3600 - minutes)
    print(f"meican bot for {hours}h {minutes}m {seconds}s")

def check_order(meican, data_list, title):
    is_order = False # 是否已下单
    for calenar in data_list:
        # print(type(calenar))
        # debug_print_json(calenar)
        date = calenar["date"]
        for tar in calenar["calendarItemList"]:
            order_title = tar["title"]
            if tar["status"] == "CLOSED":
                print(f"{date}: {order_title}.订单关闭!!!")
                is_order = True
            if tar["status"] == "ORDER" and tar["corpOrderUser"]:
                first_order_name = tar["corpOrderUser"]["restaurantItemList"][0]["dishItemList"][0]["dish"]["name"]
                print(f"{date}: {order_title}.已有订单: {first_order_name}")
                if order_title.find(title) != -1:
                    is_order = True
    return is_order 


def find_dish_and_order(meican, data_list, order_config):
    # debug_print_json(data_list)
    tar_cal = None
    for calenar in data_list:
        for tar in calenar["calendarItemList"]:
            order_title = tar["title"]
            if order_title.find(order_config.title) != -1:
                tar_cal = tar
                break
        if tar_cal is not None:
            break
    if tar_cal is None:
        print(f"找不到目标时段: {order_config.title}")
        return

    # debug_print_json(tar_cal)
    tab = Tab(tar_cal)
    restaurants = meican.get_restaurants(tab)
    dishes_list = None
    # print(restaurants)
    for restaurant in restaurants:
        if restaurant.name.find(order_config.restuantname) != -1:
            dishes_list = meican.get_dishes(restaurant)
            break
    # print(dishes_list)
    if dishes_list is None:
        print(f"餐馆没有可选: {order_config.restuantname}")
        return

    target_dishes = []
    for name in order_config.dishname:
        for dish in dishes_list:
            if dish.name.find(name) != -1:
                target_dishes.append(dish)
                break
    if not target_dishes:
        print(f"没有找到菜品: {', '.join(order_config.dishname)}")
        return

    data = meican.order(target_dishes)
    dishes_desc = "; ".join(
        f"{dish.restaurant}, {dish.name}, {dish.price}" for dish in target_dishes
    )
    print(f"下单结果: {data.get('message')}, {dishes_desc}")

def execute(argv=None):

    while True: 
        print_time()
        try:
            meican = build_meican()
            meican.load_tabs(True)
            for i in order_list._order:
                # print(repr(i))
                # test_data = meican.get_day(i.weekday)
                test_data = meican.get_day_dateList(i.weekday)
                is_order = check_order(meican, test_data, i.title)
                if not is_order:
                    find_dish_and_order(meican, test_data, i)
        except MeiCanLoginFail as error:
            print("登录凭证不可用：{}".format(error))
            print("请重新运行 `python -m meican.login` 更新 cookie")
            return
        except NoOrderAvailable:
            print("别急，下一顿还没开放订餐")
            return
        time.sleep(SCAN_TICK)


if __name__ == "__main__":
    execute()
