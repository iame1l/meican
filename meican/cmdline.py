import argparse
import sys

from tools import MeiCan
from settings import MeiCanSetting
from exceptions import NoOrderAvailable


def initialize_meican():
    settings = MeiCanSetting()
    settings.load_credentials()
    return MeiCan(settings.username, settings.password)


def execute(argv=None):
    if argv is None:
        argv = sys.argv[1:] or []
    parser = argparse.ArgumentParser(description="命令行点美餐的工具")
    parser.add_argument("-o", "--order", help="order meal")
    args = parser.parse_args(argv)

    meican = initialize_meican()
    meican.load_tabs(True)

    try:
        # print("AAAAAAAAAAAAAAAAAAAAAAAAaa: ", meican.tabs())
        # print(meican._calendar_items)
        # print(meican._wed_day_calendar)
        # print(meican._tabs)
        print(meican._wed_day_tab)
        dishes = meican.list_dishes()
    except NoOrderAvailable:
        print("别急，下一顿还没开放订餐")
        return
    if args.order:
        keyword = args.order.decode("utf-8")
        dishes = [_ for _ in dishes if keyword in _.name]
        if len(dishes) == 1:
            meican.order(dishes[0])
            print("done!")
        elif not dishes:
            print("没有找到 {} 的对应菜品".format(keyword))
        else:
            print("找到多于一个菜品，请指定更详细的关键词")
            print("\n".join(["{}".format(_) for _ in dishes]))


if __name__ == "__main__":
    execute()
