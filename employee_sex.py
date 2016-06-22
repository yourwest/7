__author__ = 'angelinaprisyazhnaya'

import numpy as np
from sklearn.naive_bayes import GaussianNB

f = open('test_corpus.xml', 'r', encoding='utf8')
f = f.read()
# Пустая строка - разделитель вакансий.
vacancies = f.split(sep='\n\n')

feature_words = ['мужчина', 'женщина', 'мужской', 'женский']

# Сбор признаков.
all_data = []
for vacancy in vacancies:
    vacancy_data = []
    vacancy = vacancy.lower()
    for word in feature_words:
        if word in vacancy:
            vacancy_data.append(1)
        else:
            vacancy_data.append(0)
    all_data.append(vacancy_data)

# Вычисление пола сотрудника.
labels = []
for i in all_data:
    if (i[0] == 1 and i[1] == 1) or (i[2] == 1 and i[3] == 1):
        labels.append('both')
    elif i[0] == 1 or i[2] == 1:
        labels.append('male')
    elif i[1] == 1 or i[3] == 1:
        labels.append('female')
    else:
        labels.append('not defined')

# Naive Bayes.
all_data = np.array(all_data)
labels = np.array(labels)
clf = GaussianNB()
clf.fit(all_data[:500], labels[:500])
print(clf.score(all_data[:500], labels[:500]))
print(clf.score(all_data[500:], labels[500:]))
