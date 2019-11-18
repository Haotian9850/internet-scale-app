from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select


def test_search_bar(driver, keyword):
    search_bar = driver.find_element_by_name("keyword")
    search_bar.clear()
    search_bar.send_keys(keyword)
    search_bar.send_keys(Keys.RETURN)
    print("searching for: ", keyword)

    assert "No matching pets found in our database." not in driver.page_source

    print("passing search bar test")

    pass


def test_registration(driver, user_data):


    register_button = driver.find_element_by_id("registerButton")
    register_button.click()

    print("adding ", user_data["Username"], " to the database....")

    username_field = driver.find_element_by_id("id_username")
    first_name_field = driver.find_element_by_id("id_first_name")
    last_name_field = driver.find_element_by_id("id_last_name")
    age_field = driver.find_element_by_id("id_age")
    gender_field = driver.find_element_by_id("id_gender")
    email_field = driver.find_element_by_id("id_email_address")
    zip_field = driver.find_element_by_id("id_zipcode")
    pwd_field = driver.find_element_by_id("id_password")
    confirm_pwd_field = driver.find_element_by_id("id_confirm_password")

    username = user_data["Username"]
    first_name = user_data["First_name"]
    last_name = user_data["Last_name"]
    age = user_data["Age"]
    gender = user_data["Gender"]
    email = user_data["Email_address"]
    zipcode = user_data["Zipcode"]
    pwd = user_data["Password"]

    username_field.clear()
    username_field.send_keys(username)

    first_name_field.clear()
    first_name_field.send_keys(first_name)

    last_name_field.clear()
    last_name_field.send_keys(last_name)

    age_field.clear()
    age_field.send_keys(age)

    gender_field.click()
    select = Select(gender_field)
    select.select_by_visible_text(gender)

    email_field.clear()
    email_field.send_keys(email)


    zip_field.clear()
    zip_field.send_keys(zipcode)

    pwd_field.clear()
    pwd_field.send_keys(pwd)

    confirm_pwd_field.clear()
    confirm_pwd_field.send_keys(pwd)

    submit_button = driver.find_element_by_id("id_register_submit")
    submit_button.click()

    assert "successfully created!" in driver.page_source

    print("passing register test")

    pass

def test_login(driver, user_data):
    login_button = driver.find_element_by_id("id_login_button")
    login_button.click()

    print("logging in as ", user_data["Username"])

    username_field = driver.find_element_by_id("id_username")
    pwd_field = driver.find_element_by_id("id_password")

    username_field.clear()
    username_field.send_keys(user_data["Username"])

    pwd_field.clear()
    pwd_field.send_keys(user_data["Password"])

    submit_button = driver.find_element_by_id("id_login_submit")
    submit_button.click()

    assert "Successfully logged in" in driver.page_source

    print("passing login test")

    pass


def test_create_pet(driver, pet_data):
    create_pet_button = driver.find_element_by_id("id_create_pet_button")
    create_pet_button.click()

    print("adding ", pet_data["Name"], " to the database....")

    pet_name_field = driver.find_element_by_id("id_name")
    pet_type_field = driver.find_element_by_id("id_pet_type")
    pet_descr_field = driver.find_element_by_id("id_description")
    price_field = driver.find_element_by_id("id_price")

    pet_name_field.clear()
    pet_name_field.send_keys(pet_data["Name"])

    pet_type_field.clear()
    pet_type_field.send_keys(pet_data["Pet_type"])

    pet_descr_field.clear()
    pet_descr_field.send_keys(pet_data["Description"])

    price_field.clear()
    price_field.send_keys(pet_data["Price"])

    submit_button = driver.find_element_by_id("id_create_pet_submit")
    submit_button.click()

    assert "successfully created" in driver.page_source

    print("passing create pet test")

    pass 



if __name__ == "__main__":
    driver = webdriver.Remote("http://selenium-chrome:4444/wd/hub", DesiredCapabilities.CHROME)

    driver.get("http:presentation-0:8000/homepage")
    assert "Portia" in driver.title

    user_data = {"Username": "test_username1", "First_name": "test_firstname1", "Last_name": "test_lastname1", 
    "Age": "23", "Gender": "Other", "Email_address": "test_emailaddress1@test.com", "Zipcode": "22904", 
    "Password": "Test_password1"}
    
    test_registration(driver, user_data)

    test_login(driver, user_data)

    driver.get("http:presentation-0:8000/homepage")
    assert "Portia" in driver.title

    pet_data = {"Name": "bagelbunny", "Pet_type":"dog", "Description": "not a bunny", "Price": "18.00"}

    test_create_pet(driver, pet_data)

    driver.get("http:presentation-0:8000/homepage")
    assert "Portia" in driver.title

    test_search_bar(driver, "dog")

    driver.close()