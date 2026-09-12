# MeiCan 美餐
fork的[美餐地址](https://github.com/LKI/meican), 改为自己使用的抢餐脚本.

> **本项目代码由 AI 生成。** 主要逻辑、修复与重构均由 AI 编程助手完成，
> 仅在本地按个人订餐需求做过少量调整，未经过充分测试，请自行审阅后再使用。

# 使用
1. 换取 cookie（只需一次，账号密码只在内存里用一次，不落盘）

   ```bash
   python -m meican.login
   ```

2. 配置 order.json 文件

3. 在根目录下运行

   ```bash
   python -m meican.meican_order
   ```

# 凭证说明
- 凭证是登录后下发的 `remember` cookie，保存在 `.meicancookie`
  （权限 600，已加入 .gitignore）。
- 也可用环境变量 `MEICAN_COOKIE` 提供 cookie，优先级高于文件，适合容器/定时任务。
- 实测 `remember` 在多次登录之间取值保持不变，与设备无关，所以**不存在「定时换新
  cookie」的问题**：存一次即可长期复用，只有服务端主动失效（例如改了密码）才需要
  重新执行 `python -m meican.login`。
- cookie 失效时美餐接口返回的是 `200 + HTML` 而不是 401，代码已按响应类型识别，
  会明确提示重新登录。

# TODO
- [] 接入bot通知消息
- [] 代码优化维护
