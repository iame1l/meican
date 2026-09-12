import json
import os
from os.path import abspath, dirname, exists, join

from .models import Order

# 配置固定放在工程根目录，避免受启动时的工作目录影响
_project_root = dirname(dirname(abspath(__file__)))
cookie_file = join(_project_root, ".meicancookie")
order_file = join(_project_root, "order.json")


class MeiCanSetting(object):
    """美餐凭证：只从环境变量或 cookie 文件读取，不涉及账号密码。"""

    def load_cookie(self):
        """优先取环境变量 MEICAN_COOKIE，其次读 .meicancookie 文件。"""
        cookie = os.environ.get("MEICAN_COOKIE")
        if cookie:
            return cookie.strip()
        if exists(cookie_file):
            with open(cookie_file, encoding="utf-8") as f:
                return f.read().strip() or None
        return None

    def save_cookie(self, cookie):
        """写入 cookie 文件并收紧权限，只有当前用户可读写。"""
        with open(cookie_file, "w", encoding="utf-8") as f:
            f.write(cookie.strip() + "\n")
        os.chmod(cookie_file, 0o600)


class OrderSetting(object):
    def __init__(self):
        self._order = []
        if not exists(order_file):
            print("order_file not exists !")
            return
        with open(order_file, encoding="utf-8") as f:
            order_data = json.load(f)
            self._order.extend([Order(_) for _ in order_data["orders"]])
