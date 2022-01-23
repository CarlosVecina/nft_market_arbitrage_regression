from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from discord import Webhook, RequestsWebhookAdapter
import catboost as cb
import json
import numpy as np
import pandas as pd

# TODO: Docstrings

def get_driver(use_proxy: bool = False) -> webdriver:
    """"""
    chrome_options = Options()

    if use_proxy:
        #driver =webdriver.Chrome()#,options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        driver.get('https://sslproxies.org/')
        driver.execute_script(
            'return arguments[0].scrollIntoView(true);',
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//th[contains(., 'IP Address')]"))
            )
        )
        ips = [my_elem.get_attribute('innerHTML') for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 1]")))]
        ports = [my_elem.get_attribute('innerHTML') for my_elem in WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-striped table-bordered dataTable']//tbody//tr[@role='row']/td[position() = 2]")))]

        proxies = []
        for i in range(0, len(ips)):
            proxies.append(ips[i]+':'+ports[i])
        chrome_options = webdriver.ChromeOptions()
        i = int(np.random.randint(low=0, high=5, size=(1,)))
        chrome_options.add_argument('--proxy-server={}'.format(proxies[i]))
        chrome_options.add_argument('start-maximized')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

    chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    return driver

def next_sold_page(driver: webdriver) -> None:
    """"""
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div[2]/div/div/button[2]').click()

    return None

def price_my_axie(df_axie_stats: pd.DataFrame) -> float:
    """"""
    mcatboos_price_eth = cb.CatBoostRegressor()  # TODO: Change to sklearn pipelines train and inference
    mcatboos_price_eth.load_model('./src/axie_market_tracker/eth_price_v0')
    with open('./src/axie_market_tracker/eth_price_v0_category_dict.txt', 'r') as data:
            s = data.read()
            s = s.replace('\t','')
            s = s.replace('\n','')
            s = s.replace(',}','}')
            s = s.replace(',]',']')
            s = s.replace('\'', '\'')
            dict_categorical = json.loads(s)

    df_axie_stats_parsed = df_axie_stats.loc[:, mcatboos_price_eth.feature_names_]
    df_axie_stats_parsed = df_axie_stats_parsed.replace(dict_categorical)
    df_axie_stats_parsed.loc[:, dict_categorical.keys()] = df_axie_stats_parsed.loc[:, dict_categorical.keys()].astype('category')

    return mcatboos_price_eth.predict(df_axie_stats_parsed)[0]

def open_axie_if_true(driver: webdriver, axie_id: str, interesting: bool) -> None:
    """"""
    if interesting:
        base_url = 'https://marketplace.axieinfinity.com/'
        driver.get(base_url+'axie/'+axie_id)

    return None

def notify_axie_if_true(axie_id: str, interesting: bool, extra_msg: str) -> None:
    """"""
    if interesting:
        base_url = 'https://marketplace.axieinfinity.com/'
        discord_webhook_url = 'https://discord.com/api/webhooks/891089974315872276/KKGF7iNJlqMk2pzb_zq4xzCDZuyzsi2eoPukEATvtgPe8-AD0PHSIgPirZDMpt_i9kIH'
        webhook = Webhook.from_url(discord_webhook_url, adapter=RequestsWebhookAdapter())
        webhook.send(extra_msg)
        webhook.send(base_url+'axie/'+axie_id)

    return None

def export_axie_if_true(axie_id: str, timestamp: str, price_est: str, price_actual: str, interesting: bool) -> None:
    """"""
    if interesting:
        df_export = pd.DataFrame({'axie_id':axie_id,
                    'timestamp': timestamp,
                    'price_est':price_est,
                    'price_actual':price_actual}, index=[0])
        df_export.to_csv('app_axie_alerts.csv', mode='a', header=False, index=False)

    return None