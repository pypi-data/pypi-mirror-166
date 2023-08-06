![This is an image](https://firebasestorage.googleapis.com/v0/b/datakund-studio.appspot.com/o/selenium%20pro1.png?alt=media&token=45a2f1cd-b577-4bb5-9ff8-8e91ac7c9aec)

# selenium pro - intelligent & powerful cloud native selenium
[![PyPI version](https://badge.fury.io/py/selenium-pro.svg)](https://badge.fury.io/py/selenium-pro)

### Benefits of selenium-pro over selenium
- All the capabilities of Selenium + 
- Auto write scripts using Selenium Script Generator
- No Inspection of HTML Elements required
- Intelligent Element Handling Automatically in case of HTML changes
- Auto Setup Chromedrivers based on Operating System & Browser versions
- Run scripts in Cloud with single function call
- Bypass Automated Browser Detection
- Coming Up - Convert your old selenium scripts to selenium pro so that they never fail due to element errors

### [Selenium Pro Auto Code Generator Chrome Extension](https://chrome.google.com/webstore/detail/selenium-auto-code-genera/ocimgcpcnobcnmclomhhmjidgoiekeaf)

### Installation
```sh
pip install selenium-pro
```

### Import
```sh
from selenium_pro.webdriver.common.keys import Keys
from selenium_pro import webdriver
```

### Start Browser
```sh
driver = webdriver.Start()
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

### Find Elements By Pro
- This is one of the advanced methods added in this library aside from the conventional methods in selenium.
- This method finds element without you having to mention selectors or locators
- Also this ensures that whenever HTML element changes, its able to adapt to changes & work fine without you having to do any code change
- Use this [Selenium Pro Auto Code Generator Chrome Extension](https://chrome.google.com/webstore/detail/selenium-auto-code-genera/ocimgcpcnobcnmclomhhmjidgoiekeaf) to get pro-id for any element on the web

### Webdriver-Start
- This method will check your operating system, default browser & its version & install driver accordingly
- You can still use conventional methods if you want  specific configuration


### All Default Selenium Functions Work Well
```sh
#find elements by conventional methods
driver.find_elements(By.XPATH, '//button')

#close window
driver.close()

#set cookies in browser
driver.add_cookie({})

....
```

#### All your selenium scripts will work fine with selenium pro. Just import selenium pro instead

### [Complete Selenium Documentation Available here](https://www.selenium.dev/documentation/)
### [Selenium Python Docs](https://selenium-python.readthedocs.io/)

### Contact Us
* [Telegram](https://t.me/datakund)

