from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def test_search_bar(driver, keyword):
    pass 

def test_registration(driver):
    pass

def test_create_pet(driver):
    pass 



if __name__ == "__main__":
    driver = webdriver.Remote("http://selenium-chrome:4444/wd/hub", DesiredCapabilities.CHROME)
    driver.get("http:presentation:8000/homepage")
    
    elem = driver.find_element_by_id("registerButton")
    elem.click()