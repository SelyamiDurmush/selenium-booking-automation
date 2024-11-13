# This file will include a class with instance methods.
# That will be responsible to interact with our website.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        

    def apply_star_rating(self, *star_values):
        for star_value in star_values:
            star_filtration_box = self.driver.find_elements(By.XPATH, '//div[@data-filters-group="class"]/fieldset//input[@type="checkbox"]')[star_value - 1]
            star_filtration_box.click()
            print(f"Selected {star_value} star(s) rating.")
        # wait for the page to load after applying the filtration
        time.sleep(2)
        return
    
    def sort_price_lowest_first(self):
        sort_by_button = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="sorters-dropdown-trigger"]')
        sort_by_button.click()
        
        lowest_price_button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Price (lowest first)"]')
        lowest_price_button.click()
        print("Sorted by price lowest first.")
        #input("Press Enter to continue...")
        time.sleep(3)
        return


