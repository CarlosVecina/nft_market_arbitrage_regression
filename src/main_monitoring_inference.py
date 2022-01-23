
import json
import pandas as pd
from requests import post
from discord import Webhook, RequestsWebhookAdapter

from utils import get_driver, price_my_axie, open_axie_if_true, notify_axie_if_true, export_axie_if_true


class MarketData():
  def __init__(self):
    self.driver = get_driver(False)

  def __parse_axie_detail_dict(self, dict_raw_axie_detail: dict) -> pd.DataFrame:
    """"""
    dict_detail_data = {
      'axie_id': dict_raw_axie_detail['data']['axie']['id'],
      'genes': dict_raw_axie_detail['data']['axie']['genes'],
      'hp': dict_raw_axie_detail['data']['axie']['stats']['hp'],
      'speed':  dict_raw_axie_detail['data']['axie']['stats']['speed'],
      'skill': dict_raw_axie_detail['data']['axie']['stats']['skill'],
      'morale': dict_raw_axie_detail['data']['axie']['stats']['morale'],
      'eyes': dict_raw_axie_detail['data']['axie']['parts'][0]['id'],  # eyes
      'ears': dict_raw_axie_detail['data']['axie']['parts'][1]['id'],  # ears
      'back': dict_raw_axie_detail['data']['axie']['parts'][2]['id'],  # back
      'back_attack': dict_raw_axie_detail['data']['axie']['parts'][2]['abilities'][0]['attack'],  # back a
      'back_def': dict_raw_axie_detail['data']['axie']['parts'][2]['abilities'][0]['defense'],  # back d
      'mouth': dict_raw_axie_detail['data']['axie']['parts'][3]['id'],  # mouth
      'mouth_attack':  dict_raw_axie_detail['data']['axie']['parts'][3]['abilities'][0]['attack'],  # mouth a
      'mounth_def': dict_raw_axie_detail['data']['axie']['parts'][3]['abilities'][0]['defense'],  # mouth d
      'head': dict_raw_axie_detail['data']['axie']['parts'][4]['id'],  # head
      'head_attack': dict_raw_axie_detail['data']['axie']['parts'][4]['abilities'][0]['attack'],  # head a
      'head_def': dict_raw_axie_detail['data']['axie']['parts'][4]['abilities'][0]['defense'],  # head d
      'tail': dict_raw_axie_detail['data']['axie']['parts'][5]['id'],  # tail
      'tail:attack': dict_raw_axie_detail['data']['axie']['parts'][5]['abilities'][0]['attack'],  # tail a
      'tail_def': dict_raw_axie_detail['data']['axie']['parts'][5]['abilities'][0]['defense']  # tail d
    }

    df_axie_detail = pd.DataFrame([dict_detail_data])
    return df_axie_detail

  def get_last_axie_last_listings(self, size: str, criteria: str) -> json:
    r = post("https://graphql-gateway.axieinfinity.com/graphql",
          json={
    "operationName": "GetAxieLatest",
    "variables": {
      "from": 0,
      "size": size,
      "sort": criteria,
      "auctionType": "Sale",
      "criteria": {}
    },
    "query": "query GetAxieLatest($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieRowData\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieRowData on Axie {\n  id\n  image\n  class\n  name\n  genes\n  owner\n  class\n  stage\n  title\n  breedCount\n  level\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
      })
    return r.json()

  def get_axie_detail(self, id: str) -> json:
      """"""
      r = post("https://graphql-gateway.axieinfinity.com/graphql",
      json={
                  "operationName": "GetAxieDetail",
                  "variables": {
                  "axieId": id
                  },
        "query": "query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"
                  })

      return r.json()

  def start_monitoring(self):
    while True:
      try:
        ## GET AXIE LAST LISTINGS
        result = self.get_last_axie_last_listings(150, criteria="Latest")
        #result = get_last_axie_last_listings(150, criteria="PriceAsc")
        for axie_dict in result['data']['axies']['results'][0:1000]:
          ## AXIE IN MY WISHLIST CRITERIA
          i_dict_axie_detail = self.get_axie_detail(axie_dict['id'])
          i_df_axie_detail = self.__parse_axie_detail_dict(i_dict_axie_detail)
          i_df_axie_detail['price_eth_parsed'] = float(axie_dict['auction']['currentPrice'])/10**18
          i_df_axie_detail['axie_type'] = axie_dict['class']
          i_df_axie_detail['breed'] = axie_dict['breedCount']

          axie_estimated_price = price_my_axie(i_df_axie_detail)
          ind_price_estimation = [True] * len(i_df_axie_detail)
          ind_price_estimation = ind_price_estimation & (axie_estimated_price*0.75 > i_df_axie_detail.loc[0,'price_eth_parsed'])
          print(axie_estimated_price*0.65, i_df_axie_detail.loc[0,'price_eth_parsed'])
          notify_axie_if_true(axie_dict['id'],
           ind_price_estimation[0],
            "Estimated price: "+str(axie_estimated_price)+" . Actual price: "+str(i_df_axie_detail.loc[0,'price_eth_parsed'])+ " DIFF IS: "+str(axie_estimated_price-i_df_axie_detail.loc[0,'price_eth_parsed'])+" RATIO: "+str((axie_estimated_price-i_df_axie_detail.loc[0,'price_eth_parsed'])/i_df_axie_detail.loc[0,'price_eth_parsed']))
          open_axie_if_true(self.driver, axie_dict['id'], ind_price_estimation[0])
          export_axie_if_true(
            axie_dict['id'],
            pd.to_datetime(axie_dict['auction']['startingTimestamp'], unit='s'),
            str(axie_estimated_price),
            str(i_df_axie_detail.loc[0,'price_eth_parsed']),
            ind_price_estimation[0])

          print(axie_dict['id'], pd.to_datetime(axie_dict['auction']['startingTimestamp'], unit='s'))

      except BaseException as ex:
        print('Axie Detail Excpt')
        print(axie_dict['id'])
        print(ex)
