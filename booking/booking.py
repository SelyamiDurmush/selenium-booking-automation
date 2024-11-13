from selenium import webdriver
import booking.constants as const
import os
import time
import sys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable
 


class Booking(webdriver.Chrome):
    def __init__(self, driver_path = os.pathsep + os.path.dirname(os.path.realpath(__file__)) + '/chromedriver', teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown # if teardown is True, the browser will close after the context manager block
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Booking, self).__init__(options=options) # This will call the __init__ method of the parent class (webdriver.Chrome)
        self.implicitly_wait(4) # wait for 5 seconds before throwing an exception
        self.maximize_window() 

    def __exit__(self, exc_type, exc_val, exc_tb): # This method is called when the context manager block exits
        if self.teardown: # if teardown is True, close the browser
            self.quit()

    def land_first_page(self):
        print(f"Landing first page ... {const.BASE_URL}")
        self.get(const.BASE_URL) # full access to the webdriver.Chrome methods with Self keyword
        time.sleep(1)

    def change_currency(self, currency=None):
        # Close the cookie banner if it appears
        self.close_cookie_banner()
        
        # Locate and click the currency picker button
        currency_element = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()
        time.sleep(1)  # Wait for the dropdown to load
        
        # Find the currency list and locate the currency item by matching its text
        currency_options = self.find_elements(By.CLASS_NAME, "CurrencyPicker_currency")
        for option in currency_options:
            if currency in option.text:  # Check if the currency code (e.g., 'USD', 'GBP') is in the text
                try:
                    option.click()  # Try clicking on the matching currency option
                    print(f"Currency changed to: {currency}")
                    break
                except ElementClickInterceptedException:
                    # In case another element intercepts the click
                    print("Click intercepted, retrying...")
                    self.execute_script("arguments[0].scrollIntoView(true);", option)  # Scroll to the element
                    option.click()
                    break
        else:
            print(f"Currency '{currency}' not found in the dropdown.")
        
        time.sleep(1)  # Optional: wait for UI updates


    def close_cookie_banner(self):
        try:
            # Attempt to locate and click the "Accept Cookies" button if it appears
            cookie_accept_button = self.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_accept_button.click()
            time.sleep(1)  # Wait briefly to ensure the banner is closed
        except NoSuchElementException:
            # If the cookie banner is not found, continue without any issues
            print("Cookie banner not found, proceeding.")

    def select_place_to_go(self, place_to_go):
        # Locate the search box and enter the destination
        search_box = self.find_element(By.CSS_SELECTOR, 'input[aria-label="Where are you going?"]')
        search_box.clear()  # Clear the search box
        self.close_popup()  # Close the pop-up if it appears
        search_box.send_keys(place_to_go)
        print(f"Searching for {place_to_go} ...")
        
        # Use WebDriverWait to wait until the autocomplete result is clickable
        try:
            time.sleep(1)  # Optional: wait for UI updates
            WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.ID, 'autocomplete-result-0'))
            )
            #time.sleep(1)  # Optional: wait for UI updates
            self.find_element(By.ID, 'autocomplete-result-0').click()
            print("Selected the first search option..")   
        except Exception as e:
            print(f"Error selecting the place: {e}")
            sys.exit(1)

    def close_popup(self):
        try:
            close_popup = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')
            close_popup.click()
            print("Closed the popup.")
        except NoSuchElementException:
            print("Popup not found, proceeding.")

    def select_dates(self, check_in_date, check_out_date):
        # Locate the date picker elements
        check_in_element  = self.find_element(By.CSS_SELECTOR, 'span[data-date="' + check_in_date + '"]')
        check_in_element.click()
        check_out_element = self.find_element(By.CSS_SELECTOR, 'span[data-date="' + check_out_date + '"]')
        check_out_element.click()
        time.sleep(1)
        print(f"Selected dates: {check_in_date} to {check_out_date}")

    def select_adults(self, adults):
        # Locate the guest selection dropdown
        guest_dropdown = self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')
        guest_dropdown.click()
               
        while True:
            decrease_adults = self.find_element(By.CSS_SELECTOR, 'button[class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 bb803d8689 e91c91fa93"]')
            decrease_adults.click()
            print("Decreased button clicked")
            time.sleep(1)
            adults_value = self.find_element(By.ID, 'group_adults')
            adults_count = int(adults_value.get_attribute('value'))

            if adults_count == 1:
                break

        increase_adults = self.find_element(By.CSS_SELECTOR, 'button[class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 bb803d8689 f4d78af12a"]')
        for _ in range(adults - 1):
            increase_adults.click()
            print("Increased button clicked")
        time.sleep(1)

    def click_search(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()
        print("Search button clicked.")
        # Wait for the new page or results to load fully after selecting the option
        try:
            WebDriverWait(self, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="filters-sidebar"]'))
            )
        except Exception as e:
            print(f"Error selecting the place: {e}")

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self) # Create an instance of the BookingFiltration class
        filtration.apply_star_rating(3, 4, 5) # Apply the star rating filter
        filtration.sort_price_lowest_first() # Sort the results by price from lowest to highest

    def report_results(self):
        # Find the section containing the hotel boxes
        hotel_boxes = self.find_element(By.XPATH, '//div[@data-results-container="1"]') # Find the hotel boxes
        report = BookingReport(hotel_boxes) # Create an instance of the BookingReport class
        time.sleep(0.5)
        table = PrettyTable(
            field_names=["Hotel Name", "Price", "Score"] 
        )
        table.add_rows(report.pull_deal_box_attributes()) # Add the rows to the table
        print(table)