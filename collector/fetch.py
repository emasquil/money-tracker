from typing import Tuple

from requests_html import HTMLSession

def itau_fetch(url: str) -> Tuple[int, int]:
    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    buy_str= r.html.xpath('//*[@id="USD-compra"]')[0].text.split(",")
    sell_str = r.html.xpath('//*[@id="USD-venta"]')[0].text.split(",")
    buy = int(buy_str[0]+ buy_str[1])
    sell = int(sell_str[0]+ sell_str[1])
    return buy, sell

def brou_fetch(url: str) -> Tuple[int, int]:
    session = HTMLSession()
    r = session.get(url)
    buy_str = r.html.xpath('//*[@id="p_p_id_cotizacionfull_WAR_broutmfportlet_INSTANCE_otHfewh1klyS_"]/div/div/div/table/tbody/tr[1]/td[3]/div/p')[0].text.split(",")
    sell_str = r.html.xpath('//*[@id="p_p_id_cotizacionfull_WAR_broutmfportlet_INSTANCE_otHfewh1klyS_"]/div/div/div/table/tbody/tr[1]/td[5]/div/p')[0].text.split(",")
    buy = int(buy_str[0]+ buy_str[1]) / 1000
    sell = int(sell_str[0]+ sell_str[1]) / 1000
    return buy, sell


    