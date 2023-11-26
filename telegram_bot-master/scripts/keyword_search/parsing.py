import requests
from bs4 import BeautifulSoup

class parsing():
    """Класс, находящий синонимы"""
    def __init__(self):
        self.header = {'user-agent': "hjkhjkhjhkjhkjh"}

    def go_syn(self, word):
        """Получаем массив синонимов по заданному слову"""
        link1 = f"https://sin.slovaronline.com/search?s={word}"
        responce1 = requests.get(link1, headers=self.header).text
        soup1 = BeautifulSoup(responce1, 'lxml')
        block = soup1.find('div', class_="search-result highlight")

        link2 = block.find('a').get('href')
        responce2 = requests.get(link2, headers=self.header).text
        soup2 = BeautifulSoup(responce2, 'lxml')

        str_with_key_word = soup2.find('div', itemprop="content", class_="blockquote").text
        list = str_with_key_word.split(",")
        list[0] = list[0].split()[1]

        res = []
        for i in range(min(4, len(list))):
            res.append(list[i])

        """block = soup.find('div', class_="synonyms prnt")
        for indx in range(len(block.find_all('span'))):
            list.append(block.find_all('span')[indx].text)"""
        return res

#p = parsing()
#p.go_syn('отчаяние')
