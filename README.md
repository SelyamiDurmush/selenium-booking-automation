# Selenium Booking Automation

## Project Overview

This project automates booking operations on a booking website using Selenium WebDriver. It features functionality to change currency, search for destinations, set travel dates, define the number of adults, filter results based on criteria, and generate reports. The project is designed to allow users to customize inputs through terminal prompts.

### Project Structure

Below is an overview of each module and its functionality:

- **`run.py`**: The main script to initiate the booking automation. This script:
  - Prompts the user for input on travel destination, dates, and the number of adults.
  - Calls various methods from the `Booking` class to execute the booking search, apply filters, and generate a results report.

#### Booking Module (`booking/`)
- **`booking.py`**: 
  - This is the main automation driver for booking operations. It inherits from `webdriver.Chrome` to manage the browser session.
  - Contains methods to change the currency, enter destination, select dates, define guest count, initiate searches, and display results.
  - Key methods include:
    - `land_first_page()`: Loads the booking website.
    - `change_currency(currency)`: Selects the currency specified by the user.
    - `select_place_to_go(place_to_go)`: Enters a destination and confirms the search input.
    - `select_dates(check_in_date, check_out_date)`: Sets the check-in and check-out dates.
    - `select_adults(adults)`: Configures the number of adults for the booking.
    - `click_search()`: Initiates the search based on the selected criteria.
    - `apply_filtrations()`: Calls the `BookingFiltration` class to apply rating and price filters.
    - `report_results()`: Generates a formatted report of the search results using the `BookingReport` class.

- **`booking_filtration.py`**:
  - This module manages search filtration:
    - `apply_star_rating()`: Filters results by the specified star ratings (e.g., 3, 4, 5 stars).
    - `sort_price_lowest_first()`: Sorts results by lowest price to facilitate budget-friendly choices.
  - These methods enable a more targeted search experience by refining the displayed options based on rating and price.

- **`booking_report.py`**:
  - Responsible for extracting and organizing data from search results:
    - `pull_deal_boxes()`: Retrieves all deal elements on the results page.
    - `pull_deal_box_attributes()`: Collects data on each hotel, including name, price, and rating score, and formats it into a structured list.
  - Uses this information to generate a user-friendly report displaying hotel name, price, and rating, outputted via a table format.

- **`constants.py`**:
  - Stores essential constants, like the website's base URL (`https://www.booking.com`). By centralizing these values, this file facilitates easy updates to key configurations.

### Requirements

- Python 3.x
- Selenium WebDriver
- WebDriver for the target browser (e.g., ChromeDriver for Chrome)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SelyamiDurmush/selenium-booking-automation.git
   cd selenium-booking-automation
