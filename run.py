from booking.booking import Booking # import the Booking class from booking/booking.py

try:
    with Booking() as bot: # create an instance of the Booking class
        bot.land_first_page() # call the land_first_page method from the Booking class
        bot.change_currency(currency='EUR') 
        bot.select_place_to_go(input("Where are you going? ")) 
        bot.select_dates(check_in_date = (input("Check-in date? YYYY-MM-DD: ")),
                         check_out_date= (input("Check-out date? YYYY-MM-DD: ")))
        bot.select_adults(int(input("How many adults? "))) 
        bot.click_search()
        bot.apply_filtrations()
        bot.refresh()
        bot.report_results()

except Exception as e:
    print("There is an issue in the program:", e)
