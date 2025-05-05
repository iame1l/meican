import json
from os.path import exists, expanduser, join
from models import Order

setting_file = join(expanduser("~"), ".meicanrc")
order_file = join(expanduser("./"), "order.json")


class MeiCanSetting(object):
    def __init__(self):
        self._settings = {}
        if not exists(setting_file):
            return
        with open(setting_file, encoding="utf-8") as f:
            self._settings = json.load(f)

    def save(self):
        with open(setting_file, str("w"), encoding="utf-8") as f:
            f.write(json.dumps(self._settings, ensure_ascii=False, indent=2))

    def load_credentials(self):
        for key in ["username", "password"]:
            if key not in self._settings:
                self._settings[key] = input("please input your meican {}: ".format(key))
        self.save()

    def __getattr__(self, item):
        return self._settings[item]

class OrderSetting(object):
    def __init__(self):
        self._order = []
        if not exists(order_file):
            print("order_file not exists !")
            return
        with open(order_file, encoding="utf-8") as f:
            order_data = json.load(f)
            self._order.extend([Order(_) for _ in order_data["orders"]])