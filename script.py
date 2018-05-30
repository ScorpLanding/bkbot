from bs4 import BeautifulSoup
from urllib.request import *
import time
from selenium import webdriver
from pyvirtualdisplay import Display

url = 'https://olimp.kz/betting'
main_link = 'https://olimp.kz/'

def get_html(url):
    req = Request(url)
    html = urlopen(req).read()
    return html

def main():
    opener = build_opener()
    opener.addheaders = [('User-Agent','Mozila/5.0')]
    install_opener (opener)
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    for n in range(0, 12):
        try:
            # парсер матчей
            for b in soup.find_all('tr', class_='sportIdOfMatchTr-' + str(n) + ' forLiveFilter'):
                matches = b.find('a').next_element.next_element.next_element
                m_par = matches.find('a')
                m_href = m_par.get('href')
            htmlmatches = get_html(main_link + m_href)
            soups = BeautifulSoup(htmlmatches, 'html.parser')
            # парсер коэфициентов
            for a in soups.find_all('b', class_='value_js'):
                coef_main = a.next_element
                span_id_find = a.find_parent().get('id')
                log_coef = open('logcoef.txt', 'a')
                log_coef.write(
                    '[' + time.strftime('%X') + ']' + coef_main + '  ==  ' + span_id_find + ' == ' + m_href + '\n')
                if float(coef_main) <= opr_coef:
                    log_coef_mensh = open('coefmensh.txt', 'a')
                    log_coef_mensh.write(coef_main + ' == ' + m_href + ' == ' + span_id_find+'\n')
                    print(coef_main + ' == ' + m_href + ' == ' + span_id_find)


        except:
            print('                               [' + time.strftime('%X') + ']' + 'Error')


if __name__ == "__main__":

    # меню





    print('''                                                ┌────────────┐
                                                │▞▀▖▌ ▌▀▛▘▌ ▌│
                                                │▙▄▌▌ ▌ ▌ ▙▄▌│
                                                │▌ ▌▌ ▌ ▌ ▌ ▌│
                                                │▘ ▘▝▀  ▘ ▘ ▘│
                                                └────────────┘
        ''')
    username = input('\n                               [' + time.strftime('%X') + ']' + 'Username: ')
    password = input('                               [' + time.strftime('%X') + ']' + 'Password: ')

    print('                               ##########################################')
    print('                               #         Задержка между ставками        #')
    print('                               ##########################################')
    timeout_ot = int(input('\n                               [' + time.strftime('%X') + ']' + 'От '))
    timeout_do = int(input('                               [' + time.strftime('%X') + ']' + 'До '))

    print('                               ##########################################')
    print('                               #         Выберите тип ставки            #')
    print('                               #       1 - Процент от баланса           #')
    print('                               #       2 - Фиксированная сумма          #')
    print('                               ##########################################')
    check__inp_money = input('\n                               [' + time.strftime('%X') + ']' + 'Ваш выбор: ')
    if check__inp_money == '1':
        check__inp_money = input('                               [' + time.strftime('%X') + ']' + 'Ваша ставка: ')
    elif check__inp_money == '2':
        check__inp_money = input('                               [' + time.strftime('%X') + ']' + 'Ваша ставка: ')
    else:
        print('ERROR! TRY AGAIN')
        quit()
    print('                               ##########################################')
    print('                               #      Ограничитель на коэффициент!      #')
    print('                               ##########################################')
    opr_coef = float(input('\n                               [' + time.strftime('%X') + ']' + 'Определённый коэф: '))
    main()


#sportIdOfMatchTr https://olimp.kz/betting bg sportIdOfMatchTr-1 forLiveFilter
