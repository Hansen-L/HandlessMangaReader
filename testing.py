# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Chrome('./chromedriver')
# driver.get("http://www.mangareader.net/haikyu/39")
# element=driver.find_element_by_tag_name('body')
# element.send_keys(Keys.ARROW_RIGHT)
# element.send_keys(Keys.ARROW_RIGHT)


from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

time.sleep(3)

keyboard.press(Key.right)
keyboard.release(Key.right)
keyboard.press(Key.right)
keyboard.release(Key.right)
