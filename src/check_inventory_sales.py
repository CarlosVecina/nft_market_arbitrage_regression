import time
import numpy as np
from discord import Webhook, RequestsWebhookAdapter

from utils import get_driver


ACTUAL_AXIES = 6
BASE_URL = "https://marketplace.axieinfinity.com/profile/inventory/axie"
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/891089974315872276/KKGF7iNJlqMk2pzb_zq4xzCDZuyzsi2eoPukEATvtgPe8-AD0PHSIgPirZDMpt_i9kIH'

driver = get_driver(False)
webhook = Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=RequestsWebhookAdapter())

while True:
    driver.get(BASE_URL)
    time.sleep(1+np.random.random_sample())
    n_axis = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div[3]/div/div/div/div[1]/div[1]/h2/span').text.split(' ')[0]
    print(n_axis)
    time.sleep(60*5+np.random.random_sample())
    if int(n_axis) < ACTUAL_AXIES:
        webhook.send('Se ha producido una venta. El numero actual de Axies en cartera son :'+n_axis)


