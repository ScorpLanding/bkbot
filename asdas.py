from bs4 import BeautifulSoup
from urllib.request import *
from selenium import webdriver
import time

print('''
                                      ┌─────────────────────────┐
                                      │▞▀▖▞▀▖▞▀▖▛▀▖▛▀▖ ▛▀▖▛▀▘▌ ▌│
                                      │▚▄ ▌  ▌ ▌▙▄▘▙▄▘ ▌ ▌▙▄ ▚▗▘│
                                      │▖ ▌▌ ▖▌ ▌▌▚ ▌ ▗▖▌ ▌▌  ▝▞ │
                                      │▝▀ ▝▀ ▝▀ ▘ ▘▘ ▝▘▀▀ ▀▀▘ ▘ │
                                      └─────────────────────────┘
    ''')

username = input('Введите логин: ')
password = input('Введите пароль: ')
bet_sum = input('Введите сумму ставки: ')
coef_usl = float(input('Введите коэф: '))

main_link = 'https://olimp.kz/'

url = 'https://olimp.kz/betting'

while True:
    opener = build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
    install_opener(opener)
    html_doc = urlopen(url).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    try:
        for n in range(1, 12):
            for a in soup.find_all('tr', class_='sportIdOfMatchTr-'+str(n)+' forLiveFilter'):
                catch_href = a.find('a').next_element.next_element.next_element
                match_href = catch_href.find('a').get('href')
                html_match = urlopen(main_link+match_href).read()
                soup_m = BeautifulSoup(html_match, 'html.parser')
                for coef in soup_m.find_all('b', class_='value_js'):
                    coef_if = coef.next
                    coef_id_if = coef.next_element.next_element
                    find_coef = coef_if.find_parent('span')
                    id_c = str(find_coef.get('id'))
                    if float(coef_id_if) == coef_usl:
                        m = webdriver.Firefox()
                        m.get(main_link + match_href)
                        m.find_element_by_css_selector('div.onoffswitch:nth-child(2) > label:nth-child(2) > span:nth-child(1)').click()
                        m.find_element_by_css_selector(
                            '.enter-block > form:nth-child(1) > div:nth-child(1) > input:nth-child(2)').send_keys(username)
                        m.find_element_by_css_selector(
                            '.enter-block > form:nth-child(1) > div:nth-child(1) > input:nth-child(3)').send_keys(password)
                        m.find_element_by_css_selector('.enterBtn').click()
                        m.find_element_by_css_selector('#oc_summ').send_keys(bet_sum)
                        m.find_element_by_css_selector('#b_ever').click()
                        m.find_element_by_css_selector('#sah_no').click()
                        m.find_element_by_css_selector('#save-oc-button').click()
                        time.sleep(3)
                        m.find_element_by_id(id_c).click()
                        time.sleep(15)
                        m.close()
                        print('\n                               [' + time.strftime('%X') + ']'+'Ставка принята!!!')
                        time.sleep(1740)
    except:
        print('Ошибка!!!')
        m.close()
        time.sleep(1740)
