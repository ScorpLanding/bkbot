import tkinter as tk
import time
from datetime import datetime, timedelta
from selenium import webdriver
import cfscrape
from bs4 import BeautifulSoup
from threading import Thread

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.main_app()

    def main_app(self):
        btn_run = tk.Button(root, text='Запуск', padx='15', pady='4', font='16', background='#bdbdbd',
                            activebackground='#3f3f3f')
        btn_run.bind('<Button-1>',
                     lambda exe: self.send_keys())
        btn_run.place(x=140, y=350)
        label_site = tk.Label(root, text='https://parimatch.com/', font='Arial 10 bold')
        label_site.place(x=250, y=355)

    def send_keys(self):
        t1 = Thread(target=self.bet, args=(entry_user.get(), entry_pass.get(), entry_koef.get(), entry_sum.get(), entry_time.get()))
        t1.start()

    def bet(self, username, password, coef_bet, bet_sum, time_per_bet):
        delay_bet_time = time_per_bet * 60
        scrape = cfscrape.create_scraper()
        html = scrape.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        while True:
            try:
                for link in soup.find_all('td', class_='td_n'):
                    match_link = link.find('a').get('href')
                    html_match = scrape.get(main_link + match_link).content
                    soup_m = BeautifulSoup(html_match, 'html.parser')
                    for coef in soup_m.find_all('i', class_='blank'):
                        coef_if = coef.text
                        coef_id = coef.find_parent('a').get('id')
                        if float(coef_if) == coef_bet:
                            driver = webdriver.Firefox()
                            driver.get('https://www.parimatch.com/?login=1')
                            time.sleep(6)
                            driver.find_element_by_css_selector(
                                '.loginForm > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)').send_keys(
                                username)
                            driver.find_element_by_css_selector(
                                '.loginForm > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3) > input:nth-child(1)').send_keys(
                                password)
                            driver.find_element_by_css_selector('button.btn_orange:nth-child(1)').click()
                            driver.get(main_link + match_link)
                            driver.find_element_by_id(coef_id).click()
                            driver.find_element_by_css_selector('button.btn_orange:nth-child(1)').click()
                            time.sleep(2)
                            for handle in driver.window_handles:
                                driver.switch_to_window(handle)
                            driver.find_element_by_css_selector('.enbl').send_keys(bet_sum)
                            driver.find_element_by_css_selector('#do_stake').click()
                            time.sleep(5)
                            driver.close()
                            for handle_main in driver.window_handles:
                                driver.switch_to_window(handle_main)
                            driver.close()
                            lable_text = datetime.now() + timedelta(minutes=time_per_bet)
                            logs_text.configure(foreground='green')
                            logs_text.insert('1.0', 'Ваша ставка принята! Следующаябудет в ' + str(lable_text)[10:19] + '\n')
                            root.update()
                            time.sleep(delay_bet_time)
            except:
                try:
                    driver.close()
                    lable_erorr = datetime.now() + timedelta(seconds=30)
                    logs_text.configure(foreground='red')
                    logs_text.insert('1.0', 'Ошибка! Следующая попытка в\n' + str(lable_erorr)[10:19] + '\n')
                    root.update()
                    time.sleep(30)
                except:
                    lable_erorr = datetime.now() + timedelta(seconds=30)
                    logs_text.configure(foreground='red')
                    logs_text.insert('1.0', 'Ошибка! Следующая попытка в\n' + str(lable_erorr)[10:19] + '\n')
                    root.update()
                    time.sleep(30)

if __name__ == '__main__':
    url = 'https://www.parimatch.com/live.html'
    main_link = 'https://www.parimatch.com/'
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.geometry('400x400')
    root.resizable(False, False)
    root.title('PariMatch Bot by M.E.')
    label_user = tk.Label(root, text='Логин')
    label_user.place(x=105, y=25)
    entry_user = tk.Entry(root)
    entry_user.place(x=35, y=45)
    label_pass = tk.Label(root, text='Пароль')
    label_pass.place(x=265, y=25)
    entry_pass = tk.Entry(root, show='*')
    entry_pass.place(x=205, y=45)
    label_koef = tk.Label(root, text='Коэффициент')
    label_koef.place(x=70, y=75)
    entry_koef = tk.Entry(root)
    entry_koef.place(x=35, y=95)
    label_time = tk.Label(root, text='Время между ставками')
    label_time.place(x=215, y=75)
    entry_time = tk.Entry(root)
    entry_time.place(x=205, y=95)
    label_sum = tk.Label(root, text='Сумма ставки')
    label_sum.place(x=155, y=125)
    entry_sum = tk.Entry(root)
    entry_sum.place(x=115, y=145)
    logs_text = tk.Text(root, height=10, width=30)
    logs_text.place(x=90, y=185)
    root.mainloop()