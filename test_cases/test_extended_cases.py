import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    yield driver
    driver.quit()

def test_valid_login(setup):
    setup.find_element(By.ID, "user-name").send_keys("standard_user")
    setup.find_element(By.ID, "password").send_keys("secret_sauce")
    setup.find_element(By.ID, "login-button").click()
    assert "inventory" in setup.current_url

def test_invalid_login(setup):
    setup.find_element(By.ID, "user-name").send_keys("wrong_user")
    setup.find_element(By.ID, "password").send_keys("wrong_pass")
    setup.find_element(By.ID, "login-button").click()
    error = setup.find_element(By.CSS_SELECTOR, ".error-message-container").text
    assert "Epic sadface" in error

def test_add_to_cart(setup):
    setup.find_element(By.ID, "user-name").send_keys("standard_user")
    setup.find_element(By.ID, "password").send_keys("secret_sauce")
    setup.find_element(By.ID, "login-button").click()
    setup.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    cart_count = setup.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == "1"
    setup.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    product_name = setup.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert "Sauce Labs Backpack" in product_name

def test_search_product(setup):
    setup.find_element(By.ID, "user-name").send_keys("standard_user")
    setup.find_element(By.ID, "password").send_keys("secret_sauce")
    setup.find_element(By.ID, "login-button").click()
    setup.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    setup.find_element(By.ID, "inventory_sidebar_link").click()
    products = setup.find_elements(By.CLASS_NAME, "inventory_item_name")
    product_names = [p.text for p in products]
    assert len(product_names) > 0
