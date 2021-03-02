# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, request, redirect, flash, session
from app import app
from app.forms import ContactForm
from datetime import datetime
import os
import sys
import json


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


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    form = ContactForm()
    session_name = session.get('name')
    session_email = session.get('email')
    print(f'contact-form is using by {session_name}')
    # якщо користувач передає дані
    if request.method == 'POST':
        # і форма до того не була заповнена у поточній сесії (адже ім'я збережен в сесії відсутнє)
        if session_name is None:
            if form.validate_on_submit():
                # дістаємо дані із форм
                name = form.name.data
                email = form.email.data
                message = form.message.data
                # і записуємо ім'я та мейл у змінні сесії
                session['name'] = name
                session['email'] = email
                # зібрані дані із форми записуємо у json файл
                with open('data.json', 'a') as f:
                    json.dump({'name': name, 'email': email, 'message': message}, f,
                              indent=4, ensure_ascii=False)
                flash(f'Повідомлення від {name} було успішно надіслано', 'success')
                # виконуємо перенаправлення на сторінку 'контакт' із методом get
                return redirect(url_for('contact'))
            else:
                flash('Деякі поля не пройшли валідацію, будь ласка, введіть дані ще раз', 'danger')
        else:  # якщо форма до того ВЖЕ БУЛА заповнена у поточній сесії - то:
            # значення полів ім'я та емейлу для проходження валідації беремо із змінних сесії
            form.name.data = session_name
            form.email.data = session_email
            if form.validate_on_submit():
                # і нові дані зчитуємо лише з полля message
                message = form.message.data
                # зібрані дані із форми записуємо у json файл
                with open('data.json', 'a') as f:
                    json.dump({'name': session_name, 'email': session_email, 'message': message}, f,
                              indent=4, ensure_ascii=False)
                flash(f'Повідомлення від {form.name.data} було успішно надіслано', 'success')
                # виконуємо перенаправлення на сторінку 'контакт' із методом get
                return redirect(url_for('contact'))
            else:
                flash('Деякі поля не пройшли валідацію, будь ласка, введіть дані ще раз', 'danger')
    return render_template('contact.html', title='Контактна форма', form=form, session_name=session_name)
