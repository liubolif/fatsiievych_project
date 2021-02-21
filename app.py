# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, request
from datetime import datetime
import os
import sys

app = Flask(__name__)

# записуємо початкову інформацію для футера. Так як дані про час і юзер агента
# (можуть переходити на різні сторінки сайту із різних браузерів) можуть динамічно змінюватись -
# то ці дані ініціалізуємо перед відкриття власне самої сторінки
footer_info = {
    'time': None,
    'os': os.uname(),
    'python': sys.version,
    'user_agent': None
}


@app.route("/")
@app.route("/about")
def about():
    footer_info['time'] = datetime.now().strftime("%H:%M:%S")
    footer_info['user_agent'] = request.headers.get('User-Agent')

    return render_template('about.html', title='Про сторінку', footer_info=footer_info)


@app.route("/bio")
def bio():
    footer_info['time'] = datetime.now().strftime("%H:%M:%S")
    footer_info['user_agent'] = request.headers.get('User-Agent')

    return render_template('bio.html', title='Біографія', footer_info=footer_info)


@app.route("/achievements")
def achievements():
    achievs_lst = ['<b>Рівень володіння англійською мовою</b>: <i> вмію користуватися Google Translate</i>',
                   'Вмію писати <i>`Hello World`</i> на <b>шістьох мовах програмування</b>',
                   '<b>Найкращий програміст</b> <i>за версією мами</i>',
                   '<b>Найкращий студент</b> <i>за версією бабусі</i>',
                   '<b>Найкращий брат</b> <i>за версією молодшого брата</i>',
                   '<b>Найкращий комп\'ютерний майсетр</b> <i>за версією сусідки знизу</i>',
                   'Отримав <b>похвальну грамоту</b> <i>в другому класі</i>',
                   '<b>Напам\'ять</b> знаю <i>таблицю Мендєлєва</i>',
                   'Отримав <b>98 балів</b> <i>з ОБЖ</i>']
    footer_info['time'] = datetime.now().strftime("%H:%M:%S")
    footer_info['user_agent'] = request.headers.get('User-Agent')
    return render_template('achievements.html', title='Досягнення', achievs_lst=achievs_lst, flag=True,
                           footer_info=footer_info)


@app.route("/photo")
def photo():
    footer_info['time'] = datetime.now().strftime("%H:%M:%S")
    footer_info['user_agent'] = request.headers.get('User-Agent')
    return render_template('photo.html', title='Фото', footer_info=footer_info, makeLittle=False)


if __name__ == '__main__':
    app.run(debug=True)
