"""交互式登录，用账号密码换取可长期复用的 cookie。

用法::

    python -m meican.login

账号密码只在本次运行中使用，不会写入磁盘；落盘的只有 cookie。
"""
import getpass
import sys

from .exceptions import MeiCanLoginFail
from .settings import MeiCanSetting, cookie_file
from .tools import MeiCan


def execute(argv=None):
    print("本次输入的账号密码只用于换取 cookie，不会被保存。")
    username = input("meican username: ").strip()
    password = getpass.getpass("meican password: ")
    if not username or not password:
        print("账号或密码为空，已取消。")
        return 1

    try:
        cookie = MeiCan.login_cookie(username, password)
    except MeiCanLoginFail as error:
        print("登录失败：{}".format(error))
        return 1
    except Exception as error:  # 网络异常等
        print("登录出错：{}".format(error))
        return 1

    MeiCanSetting().save_cookie(cookie)
    print("cookie 已保存到 {}（权限 600）".format(cookie_file))
    return 0


if __name__ == "__main__":
    sys.exit(execute())
