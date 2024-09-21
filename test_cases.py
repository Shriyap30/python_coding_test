import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture(scope="module")
def driver():
    """Set up the Chrome WebDriver."""
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()


def test_navigate_products(driver):
    """Test to navigate to the homepage and verify the title."""

    driver.get("https://www.entrata.com/")
    driver.fullscreen_window()

    # Close cookies popup
    close = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[text()='X']")))
    close.click()

   # Products menu
    button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@id,'w-dropdown-toggle-')]")))
    actions = ActionChains(driver)

    # Hover over the element
    actions.move_to_element(button).perform()
    assert "Property Management" in driver.page_source

    # Close products dropdown
    button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@id,'w-dropdown-toggle-') and .//text()='Products']")))
    button.click()


def test_web_accessibility_visible(driver):

    # Scroll to the bottom of the page using JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Optionally, wait for a while to observe the scroll effect
    driver.implicitly_wait(5)  # Wait for 5 seconds

    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Web Accessibility Statement']")))

    assert element.is_displayed()
    time.sleep(10)


def test_navigate_property_management(driver):
    """Test to navigate to the Property Management page and verify content."""

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[@class='footer-heading' and .//text()='Property Management']")))

    button.click()
    element_property_management = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,"//h1[@class='color-white property' and .//text()='Property Management']")))
    assert element_property_management.is_displayed()


def test_interact_with_watch_demo_form(driver):
    """Test to interact with a form without submitting."""

    watch_demo_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='nav-button']//a[@href='https://go.entrata.com/watch-demo.html']"))
    )

    watch_demo_button.click()

    # Verify title
    title = driver.find_element(By.XPATH,"//h1[text()='Optimize Property Management with One Platform']")
    assert title.is_displayed()

    # Input first name
    input_name = driver.find_element(By.XPATH,"//input[@id='FirstName']")
    input_name.send_keys("Jerry")


