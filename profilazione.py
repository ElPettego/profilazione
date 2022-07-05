from typing import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium

import logging
import time
import traceback
from telegram.ext import Updater
import telegram
import tqdm


PATH = "/usr/bin/chromedriver"

numero_di_telefono = "3248020317"

counter = 49010

BOT_TOKEN = '5493530397:AAGyFqoTxBVbyPQDwheE-ET3UOnSqiNJYx0'

CHAT_ID_TARGET = '-601811465'
CHAT_ID_BOT_ESTERNO = "-1455649998"

def emit(mex, bot_token, chat_id):

        global str_to_send              
        full_mex = mex
        print(full_mex.splitlines()[1])        

        if 'Bet365' in  full_mex.splitlines()[1] and float(full_mex.splitlines()[0].split(':')[1].replace('%','').replace(' ', '')) > 0 :            
            split_n = full_mex.split('\n')
            print('############################################' + str(split_n) + '######################################')
            header = '🚀 ' + split_n[0] + '\n➡️ ' + split_n[1] + '\n\n'
            info = split_n[3] + '\n🆚 ' + split_n[4] + '\n📅 ' + split_n[5] + '\n\n'
            if 'MLS' in split_n[3] or 'Série A' in split_n[3] or 'UEFA' in split_n[3]:
                info = '⚽ ' + info
            if 'ATP' in split_n[3] or 'WTA' in split_n[3]:
                info = '🎾 ' + info    
            if 'NBA' in split_n[3]:
                info = '🎾 ' + info
            split__ = full_mex.split('---------------------------------------')[1]
            split__ = split__[2:len(split__)]
            book_1 = '💰 ' + split__.split('\n\n')[0].splitlines()[0] + '\n👉 ' + split__.split('\n\n')[0].splitlines()[1] + '\n\n'
            book_2 = '💰 ' + split__.split('\n\n')[1].splitlines()[0] + '\n👉 ' + split__.split('\n\n')[1].splitlines()[1] + '\n\n'
            split__2 = full_mex.split('---------------------------------------')[2]
            split__2 = split__2[2:len(split__2)]
            guadagno = '💸 ' + split__2.splitlines()[0]
            str_to_send = header + info + book_1 + book_2 + guadagno
        else:
            str_to_send = ''
            
               
        bot = telegram.Bot(token=bot_token)
        status = bot.send_message(chat_id=chat_id, text= str_to_send, parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=True )

        time.sleep(0.2)

        print(status)
            

def telegram_bot(bot_token):

    global link_stream

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    logger = logging.getLogger(__name__)

    
    def main():
        """Start the bot."""
        
        updater = Updater(bot_token, use_context=True)

        dp = updater.dispatcher
        updater.start_polling()
        while True:
            try:
                crawler()
        
            except Exception: 
                print(traceback.format_exc())
        

        # updater.stop()

    if __name__ == '__main__':
        main()

def crawler():

    global num_id
    global counter
    while True:

        try:

            #for sec in tqdm(range(3)):
            time.sleep(3)
                        
            num_id = 'message' + str(counter)

            last_mex = driver.find_element(By.ID, num_id).text

            print('############################')
            print(last_mex)
            print('############################')

            counter = counter + 1
            emit(last_mex, bot_token= BOT_TOKEN, chat_id=CHAT_ID_TARGET)                      

        except telegram.error.BadRequest :
            print('messaggio vuoto')

        except selenium.common.exceptions.NoSuchElementException:
            print('no new mex')

        except:
            print('################################################################################')
            print('meassageid: ' + num_id)
            print('no new mex')
            print(traceback.format_exc())

            print('no last mex')

try:

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    options.add_argument('--disable-notifications')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=PATH, options=options)
    actionChains = ActionChains(driver)
    driver.get('https://web.telegram.org/z/#' + CHAT_ID_BOT_ESTERNO)

    time.sleep(5)

    cwpn = driver.find_element(By.XPATH, '//*[@id="auth-qr-form"]/div/button[1]').click()

    time.sleep(2)

    driver.find_element(By.XPATH, '//*[@id="sign-in-phone-number"]').send_keys(numero_di_telefono)

    time.sleep(1)
    
    driver.find_element(By.XPATH, '//*[@id="auth-phone-number-form"]/div/form/button[1]').click()

    verification_code = input("Verification code: ")

    ver_code_input = driver.find_element(By.XPATH, '//*[@id="sign-in-code"]').send_keys(verification_code)

    time.sleep(1)

    driver.get('https://web.telegram.org/z/#' + CHAT_ID_BOT_ESTERNO)

    time.sleep(1)

    driver.refresh()

    time.sleep(6)

    while True:
        crawler()
     
except:

    print(traceback.format_exc())


telegram_bot(BOT_TOKEN)
