# modules/__init__.py
# modules 這個 package 裡面包含了一些主要的功能模組，如下：
#   login.py: 控制、處理網站登入流程
#   form.py: ??
#   discord.py: 裡面主要是用來發送 Discord 通知的模組
#   captcha.py: 用來破解驗證碼的模組（目前仍在開發中）

from . import form, login, discord, captcha

__all__ = ["form", "login", "discord", "captcha"]
