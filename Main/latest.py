import logging

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import re
from pathlib import Path
logging.basicConfig(format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s', \
                    level = logging.DEBUG)
options = webdriver.ChromeOptions()
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],  # Disable Chrome's PDF Viewer
           "download.default_directory": "/home/user/Downloads", "download.prompt_for_download": "false",
           "download.directory_upgrade": True, "plugins.always_open_pdf_externally": True,
           "download.extensions_to_open": "applications/pdf"}

options.add_experimental_option("prefs", profile)
wd = webdriver.Chrome("/home/user/PycharmProjects/test1/Drivers/chromedriver.exe", chrome_options=options)
URL = 'https://delhihighcourt.nic.in/'
wd.get(URL)
logging.info("A Info Logging Message")
time.sleep(3)
judgement = wd.find_element_by_link_text('Judgements')
judgement.click()
judgement.click()
time.sleep(3)

wd.find_element_by_link_text('PDF Judgement').click()

wd.switch_to.window(wd.window_handles[1])

partyname = wd.find_element_by_name('Submit4')

partyname.send_keys(Keys.ENTER)
time.sleep(3)

wd.switch_to.frame("dynfr")

wait = WebDriverWait(wd, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name=\"p_name\"]')))
wd.find_element_by_xpath('//input[@name="p_name"]').send_keys(' ')
time.sleep(3)

wd.execute_script("arguments[0].removeAttribute('readonly')",
                  WebDriverWait(wd, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='frdate']"))))
wd.execute_script("arguments[0].removeAttribute('readonly')",
                  WebDriverWait(wd, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='todate']"))))

wd.find_element_by_xpath("//input[@name='frdate']").clear()
time.sleep(3)
wd.find_element_by_id('frdate').send_keys('02/10/2019')
time.sleep(3)

wd.find_element_by_xpath("//input[@name='todate']").clear()
time.sleep(3)
wd.find_element_by_id('todate').send_keys('02/10/2020')
time.sleep(3)

wd.find_element_by_name('Submit').send_keys(Keys.ENTER)

wait.until(EC.presence_of_element_located((By.XPATH, '//a[@target="_blank"]')))
wd.find_element_by_xpath("//a[@target='_blank']").click()
time.sleep(5)
for dir in os.scandir('/home/user/Downloads'):
    try:
        if dir.is_dir():
            os.rmdir(dir)
        else:
            data = str(Path(dir))
            res1 = " ".join(re.findall("[0-9]+", data))
            ls = str(res1).split()
            a = ls[0]
            a = a[:2] + "-" + a[2:4] + "-" + a[4:]
            b = ls[1]
            b = b[:-4] + " of " + b[-4:] + ".pdf"
            c = a + " DEL " + b
            os.rename(str(Path(dir)), str(Path(c)))
    except:
        pass
