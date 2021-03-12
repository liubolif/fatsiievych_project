# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect, flash, session
from app import app
from app.forms import ContactForm, TaskForm
from app.models import Task
from app import db
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


@app.route("/task")
def task_all():
    print("task_all")
    all_tasks = Task.query.all()
    return render_template('task_all.html', title='Завдання',  all_tasks=all_tasks)


@app.route("/task/create", methods=['POST', 'GET'])
def task_create():
    form = TaskForm()
    print("task_create")

    if form.validate_on_submit():
        print("validate_on_submit")

        # дістаємо дані із форм
        title = form.title.data
        description = form.description.data
        created = form.created.data
        priority = form.priority.data
        is_done = form.is_done.data

        new_task = Task(title=title, description=description, created=created, priority=priority, is_done=is_done)
        print(new_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash(f'Завдання "{new_task.title}" успішно додане', 'success')
        except:
            db.session.rollback()
            flash(f'Помилка під час запису завдання "{new_task.title}" до БД', 'danger')

        return redirect(url_for('task_all'))

    elif request.method == 'POST':
        flash('Помилка під час валідації', 'danger')
        return redirect(url_for('task_create'))

    return render_template('task_create.html', title='Завдання', form=form)


@app.route("/task/<int:id>")
def task_detail(id):
    task = Task.query.get(id)
    return render_template('task_detail.html', title='Завдання', task=task)


@app.route("/task/<int:id>/delete", methods=['POST', 'GET'])
def task_delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash(f'Завдання "{task.title}" видалено', 'warning')
    except:
        flash(f'Під час видалення завдання "{task.title}" трапилась помилка.', 'danger')
    return redirect(url_for('task_all'))


@app.route("/task/<int:id>/update", methods=['POST', 'GET'])
def task_update(id):
    form = TaskForm()
    print("task_update")
    # дістаємо необхідний об'єкт завдання для редагування
    task = Task.query.get_or_404(id)

    if request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.created.data = task.created
        form.priority.data = task.priority.name
        form.is_done.data = task.is_done

        return render_template('task_update.html', title='Завдання', form=form)

    else:
        if form.validate_on_submit():
            print("task_update validate_on_submit")

            # дістаємо дані із форм і відразу записуємо їх в БД
            task.title = form.title.data
            task.description = form.description.data
            task.created = form.created.data
            task.priority = form.priority.data
            task.is_done = form.is_done.data

            print(task)
            try:
                db.session.commit()
                flash(f'Завдання "{task.title}" успішно змінене', 'info')
            except:
                db.session.rollback()
                flash(f'Помилка під час запису завдання "{task.title}" до БД', 'danger')

            return redirect(url_for('task_all'))

        else:
            flash('Помилка під час валідації.', 'danger')
            return redirect(f'/task/{id}/update')


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
