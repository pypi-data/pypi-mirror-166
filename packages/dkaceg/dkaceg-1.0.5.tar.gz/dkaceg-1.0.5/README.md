A library to find elements through an easy way

### Installation
```sh
pip install dkaceg
```

### Example 1
It searches a keyword on google
```sh
from dkaceg.webdriver.chrome.options import Options
from dkaceg.webdriver.common.desired_capabilities import DesiredCapabilities
from dkaceg.webdriver.common.keys import Keys
from dkaceg import webdriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage ')
chrome_options.add_argument('--disable-dev-shm-usage ')
chrome_options.add_experimental_option("excludeSwitches",["disable-popup-blocking"])
driver = webdriver.Chrome("E:\\studio\\Developer-DataKund\\chromedriver104.exe",chrome_options=chrome_options)
driver.get("https://google.com")
search_element=driver.find_element_by_dkaceg("google_search")
search_element.send_keys("datakund",Keys.ENTER)
driver.quit()
```

### Example 2
It fetches the titles of packages on pypi
```sh
from dkaceg.webdriver.chrome.options import Options
from dkaceg.webdriver.common.desired_capabilities import DesiredCapabilities
from dkaceg.webdriver.common.keys import Keys
from dkaceg import webdriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage ')
chrome_options.add_argument('--disable-dev-shm-usage ')
chrome_options.add_experimental_option("excludeSwitches",["disable-popup-blocking"])
driver = webdriver.Chrome("E:\\studio\\Developer-DataKund\\chromedriver104.exe",chrome_options=chrome_options)
driver.get("https://pypi.org/search/?q=firebase")
title_elements=driver.find_elements_by_dkaceg("pypi_title")
for ele in title_elements:
	print(ele.text)
driver.quit()
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

