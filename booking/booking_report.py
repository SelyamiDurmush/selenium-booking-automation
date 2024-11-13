# The specific data that we need from each one o fthe deal boxes:

import re
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        deal_boxes = self.boxes_section_element.find_elements(By.XPATH, './/div[@data-testid="property-card-container"]')
        return deal_boxes
    
    def pull_deal_box_attributes(self):
        collected_data = []

        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(By.XPATH, './/div[@data-testid="title"]')
            hotel_name = hotel_name.get_attribute('innerHTML').strip()
            
            hotel_price = deal_box.find_element(By.XPATH, './/span[@data-testid="price-and-discounted-price"]').text.strip()
            
            hotel_score = deal_box.find_element(By.XPATH, './/div[@data-testid="review-score"]')
            score_text = hotel_score.find_element(By.XPATH, './/div').text.strip()          
            score_text = re.search(r'\d+\.\d+', score_text)
            if score_text:
                score_text = score_text.group()
            else:
                score_text = None  # Handle the case if no score is found

            collected_data.append([hotel_name, hotel_price, score_text])
        print("Number of hotel numbers:", len(self.deal_boxes))
        return collected_data
