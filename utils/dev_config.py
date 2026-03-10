# development configuration file

import logging

# Enable debug mode (global)
DEBUG_MODE = True

## logger configuration
## see: https://docs.python.org/3/library/logging.html#logging.basicConfig
logging.basicConfig(
    level=logging.INFO if not DEBUG_MODE else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


## WebDriver configuration
WEBDRIVER_CONFIG = {
    "webdriver_debug": DEBUG_MODE,  # 是否啟用 WebDriver debug 模式: True or False
    "user_agent": "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",  # 自定義 User-Agent: string or None
}
