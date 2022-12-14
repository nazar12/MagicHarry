import numbers
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import telebot
import requests
import schedule


def telegram_bot_sendtext(bot_message):
    bot_token = 'MY_TOKEN' #add your token
    bot_chatID = 'MY_ID' #add your chat ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


#test = telegram_bot_sendtext("check")
#print(test)
def report():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    timer=str((current_time))

    is_queue = True
    url = "https://tickets.wbstudiotour.co.uk/webstore/shop/ViewItems.aspx?CG=HPTST2&C=TIX2&_ga=2.178305572.1851349500.1632157983-2010059077.1603341446"

    driver = webdriver.Chrome(executable_path= "/Users/danielrabinovich/Downloads/chromedriver")
    driver.get(url=url)
    time.sleep(2)
    if "Queue-it" in driver.title:
        while is_queue:
            if not "Queue-it" in driver.title:
                is_queue = False
                break
            else:
                print("Waiting.")
                time.sleep(1)
    time.sleep(3)
    #assert 'Warner Bros. Web Store :: Ticket Selection' in driver.title
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Select date and time')]"))).click()
    time.sleep(5)

    driver.find_element_by_name("ctl00$ContentPlaceHolder$SalesChannelDetailControl$EventsDateTimeSelectorModal$EventsDateTimeSelector$CalendarSelector$MonthDropDownList").send_keys(("December"))
    time.sleep(5)
    days_len = len(driver.find_elements_by_xpath("(//*[contains(@class, 'c c-14-all day ng-scope available')])"))
    time.sleep(5)
    #test2 = telegram_bot_sendtext(str(days_len))

    for number in range(days_len):
        try:
            element = driver.find_elements_by_xpath("(//*[contains(@class, 'c c-14-all day ng-scope available')])")[number]
            day_number = element.text
            if not 9 <= int(day_number) <= 11: continue
            element.click()
            time.sleep(2)
            hours_len = driver.find_elements_by_xpath("(//*[contains(@class, 'event_time ng-binding')])")
            for i in hours_len:
                # hour = driver.find_elements_by_xpath("(//*[contains(@class, 'time row m-t-all ng-scope')])")[i]
                hour_text = i.text
                print(f"Day: {day_number}, hour: {hour_text}")
                telegram_bot_sendtext(f"Day: {day_number}, hour: {hour_text}")

        except Exception as e:
            print(e)
            pass
        finally:
            time.sleep(2)
    telegram_bot_sendtext(f"Didn't find your turn: {timer}")
    driver.close()
    driver.quit()
#schedule.every().day.at("19:29").do(report)
schedule.every(10).minutes.do(report)
while True:
    schedule.run_pending()
    time.sleep(1)
