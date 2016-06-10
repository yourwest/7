__author__ = 'angelinaprisyazhnaya'

import re
import csv
import pymorphy2
from pymystem3 import Mystem

morph = pymorphy2.MorphAnalyzer()
m = Mystem()

f = open('test_corpus.xml', 'r', encoding='utf8')
f = f.read()


def find_male_names(text):
    names = []
    male_names = open('male_names.csv', 'r', encoding='utf8')
    male_names = male_names.read()
    csv_iter = csv.reader(male_names.split('\n'), delimiter=';')
    for row in csv_iter:
        for name in row:
            names.append(name)

    capitals = re.compile('\\b[А-Я][а-я]+?\\b', flags=re.S)
    finds = capitals.findall(text)

    found_names = open('found_names.txt', 'w', encoding='utf8')
    for word in finds:
        # Здесь я пробую морфанализаторы, чтобы находились имена не только в номинативе,
        # но находятся отчества, потому что их начальная форма - это имя, от которого они образованы.
        # Поэтому если нам нужны только имена, лучше без морфанализатора.
        # word_pymorphy = morph.parse(word)[0]
        # word_nom = word_pymorphy.normal_form.capitalize()
        # word_mystem = m.lemmatize(word)[0].capitalize()
        if word in names:
            found_names.write(word + '\n')
    found_names.close()


def find_companies(text):
    companies = []
    labels = re.compile('\\b(пометк|тем)(а|и|ы|е|у|ой)\\b', flags=re.S | re.I)
    vacancies = re.compile('((ваканси|позици)(я|и|ю|ей))|(должност(ь|и|ью))', flags=re.S | re.I)
    metro = re.compile('м(\.|етро)?', flags=re.S | re.I)
    # Здесь учитываются аббревиатуры типа ТЦ и ТРЦ, которые могут быть и не просто местом,
    # а компанией, которая ищет сотрудников (в тестовом тексте есть несколько таких примеров).
    abbreviations = re.compile('(ТР?(К|Ц))|((СТ|Б)Ц)|ЖК|(О(О|А)О)|(З?АО)|(ТОО)|(ГК)|(ПС)')

    company_1 = re.compile('(\\w+) ("[^а-я].*?")', flags=re.S)
    finds_1 = company_1.findall(text)
    for i in finds_1:
        if vacancies.search(i[0]) is None \
                and labels.search(i[0]) is None \
                and metro.search(i[0]) is None \
                and len(i[1]) > 3:
            if abbreviations.search(i[0]) is not None:
                companies.append(i[0] + ' ' + i[1])
            else:
                companies.append(i[1])

    # Здесь находится какое-то количество мусора. Не очень представляю, по какому принципу можно
    # отсеивать неподходящие случаи, потому что мало ли как компания называется.
    company_2 = re.compile('((к|К)омпани(я|и|е?й|ю) (([А-ЯA-Z][А-ЯA-Zа-яa-z]+?\\s){1,3}))', flags=re.S)
    finds_2 = company_2.findall(text)
    for i in finds_2:
        if abbreviations.search(i[0]) is None:
            companies.append(i[3])

    found_companies = open('found_companies.txt', 'w', encoding='utf8')
    for i in companies:
        found_companies.write(i + '\n')
    found_companies.close()


def find_addresses(text):
    # Я считала, что для адреса обязательно должны быть указаны улица и дом, поэтому здесь
    # не находятся отдельно станции метро или города, например.
    city = '(г\. ?\\w+, )'
    metro = '(м(етро)?\.? ?\\w+( \\w+)?,? )'
    # Здесь можно добавлять еще всякие сокращения для бульваров, проспектов и т.д.
    street = '((ул(ица)?)|(пр(оезд)?)|ш)\.? \\w+( \\w+)?( \\w+)?,?'
    street_2 = '(\\w+ ((пр(оезд)?)|(пр-т))(,|\.)?)'
    house = '(д(ом)?\.?)? ?\\d+(/\\d+)?-?\\w?(\.|,)?'
    building = '(стр\. ?\\d+)'
    address = re.compile('({0}?{1}?({2}|{3}) ?{4} ?{5}?)'.format(city, metro, street, street_2, house, building))
    finds = address.findall(text)

    found_addresses = open('found_addresses.txt', 'w', encoding='utf8')
    for i in finds:
        found_addresses.write(i[0] + '\n')
    found_addresses.close()


find_companies(f)
