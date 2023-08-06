A library to find elements through an easy way

### Installation
```sh
pip install selenium_pro
```

### Example 1
It searches a keyword on google
```sh
from selenium_pro.webdriver.common.keys import Keys
from selenium_pro import webdriver
driver = webdriver.Start()
driver.get('https://www.google.com/')
driver.find_element_by_pro('QYQyyPtidm5_xqG').click()
driver.switch_to.active_element.send_keys('shoes')
driver.switch_to.active_element.send_keys(Keys.ENTER)
```

### Example 2
It fetches the titles of packages on pypi
```sh
from selenium_pro.webdriver.common.keys import Keys
from selenium_pro import webdriver
driver = webdriver.Start()
driver.get("https://pypi.org/search/?q=firebase")
title_elements=driver.find_elements_by_pro("ErZwU_jOEg0s4_9")
for ele in title_elements:
	print(ele.text)
driver.quit()
```

### Contact Us
* [Telegram](https://t.me/datakund)
* [Website](https://datakund.com)

