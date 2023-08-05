A library to find elements through an easy way

### Installation
```sh
pip install dkaceg
```

### Example 1
It searches a keyword on google
```sh
from dkaceg.webdriver.common.keys import Keys
from dkaceg import webdriver
driver = webdriver.Start()
driver.get("https://google.com")
search_element=driver.find_element_by_dkaceg("google_search")
search_element.send_keys("datakund",Keys.ENTER)
driver.quit()
```

### Example 2
It fetches the titles of packages on pypi
```sh
from dkaceg.webdriver.common.keys import Keys
from dkaceg import webdriver
driver = webdriver.Start()
driver.get("https://pypi.org/search/?q=firebase")
title_elements=driver.find_elements_by_dkaceg("pypi_title")
for ele in title_elements:
	print(ele.text)
driver.quit()
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

