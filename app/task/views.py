# -*- coding: utf-8 -*-
from sqlalchemy import case
from flask import render_template, url_for, request, redirect, flash

from app.task import task_bp
from .forms import *
from .models import *
from app import db


@task_bp.route("/task")
def task_all():
    print("task_all")
    all_tasks = Task.query.order_by(case(value=Task.priority, whens={'low': 0, 'medium': 1, 'high': 2}).desc(),
                                    Task.created).all()
    #print(','.join(t.name for t in all_tasks[0].for_empl))
    return render_template('task_all.html', title='Завдання', all_tasks=all_tasks)


@task_bp.route("/task/create", methods=['POST', 'GET'])
def task_create():
    form = TaskForm().new()
    print("task_create")

    if form.validate_on_submit():
        print("validate_on_submit")

        # дістаємо дані із форм
        title = form.title.data
        description = form.description.data
        created = form.created.data
        priority = form.priority.data
        category_id = form.category.data
        employee_list = form.employee.data
        is_done = form.is_done.data

        try:
            category_obj = Category.query.get_or_404(category_id)
            new_task = Task(title=title, description=description, created=created, priority=priority,
                            categor=category_obj, is_done=is_done)
            print(new_task)

            for empl in employee_list:
                new_task.for_empl.append(Employee.query.get(int(empl)))

            db.session.add(new_task)
            db.session.commit()
            flash(f'Завдання "{new_task.title}" успішно додане', 'success')
        except:
            db.session.rollback()
            flash(f'Помилка під час запису завдання "{new_task.title}" до БД', 'danger')

        return redirect(url_for('task_bp_in.task_all'))

    elif request.method == 'POST':
        flash(form.errors, 'danger')
        return redirect(url_for('task_bp_in.task_create'))

    return render_template('task_create.html', title='Завдання', form=form)


@task_bp.route("/task/<int:id>")
def task_detail(id):
    task = Task.query.get(id)
    return render_template('task_detail.html', title='Завдання', task=task)


@task_bp.route("/task/<int:id>/delete")
def task_delete(id):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash(f'Завдання "{task.title}" видалено', 'warning')
    except:
        flash(f'Під час видалення завдання "{task.title}" трапилась помилка.', 'danger')
    return redirect(url_for('task_bp_in.task_all'))


@task_bp.route("/task/<int:id>/update", methods=['POST', 'GET'])
def task_update(id):
    form = TaskForm().new()
    print("task_update")
    # дістаємо необхідний об'єкт завдання для редагування
    task = Task.query.get_or_404(id)

    if request.method == 'GET':
        # зчитування списку усіх робітників, яким доручено дане завдання
        lst_of_empl = []
        for t in task.for_empl:
            lst_of_empl.append(t.id)
        print(lst_of_empl)

        form.title.data = task.title
        form.description.data = task.description
        form.created.data = task.created
        form.priority.data = task.priority
        form.category.data = task.categor.id
        form.employee.data = lst_of_empl
        form.is_done.data = task.is_done
        print(task.priority.name)
        print(type(task.priority.name))
        print(task.categor.id)
        print(type(task.categor.id))
        return render_template('task_update.html', title='Завдання', form=form)

    else:
        if form.validate_on_submit():
            print("task_update validate_on_submit")

            # дістаємо дані із форм і відразу записуємо їх в БД
            task.title = form.title.data
            task.description = form.description.data
            task.created = form.created.data
            task.priority = form.priority.data
            category_name = form.category.data
            task.categor = Category.query.get_or_404(category_name)
            employee_list = form.employee.data
            task.for_empl.clear()  # очищаємо всі існуючі вязаємозвязки перед новим записом
            for empl in employee_list:
                task.for_empl.append(Employee.query.get(int(empl)))
            task.is_done = form.is_done.data

            print("/*/*/*/*/*/*//*/*/*/*")
            print(task)

            try:
                db.session.commit()
                flash(f'Завдання "{task.title}" успішно змінене', 'info')
            except:
                db.session.rollback()
                flash(f'Помилка під час запису завдання "{task.title}" до БД', 'danger')

            return redirect(url_for('task_bp_in.task_all'))

        else:
            flash(form.errors, 'danger')
            return redirect(f'/task/{id}/update')


@task_bp.route("/employee/<int:id>")
def employee_profile(id):
    employee = Employee.query.get(id)
    all_tasks = Task.query.filter(Task.for_empl.contains(employee)).order_by(
        case(value=Task.priority, whens={'low': 0, 'medium': 1, 'high': 2}).desc(), Task.created)

    # рахуємо кількість виконаних завдань
    counter = 0
    for t in all_tasks:
        if t.is_done:
            counter += 1

    try:
        employee.count_of_compltd_task = counter
        db.session.commit()
    except:
        pass

    return render_template('employee_profile.html', title='Профіль працівника', employee=employee, all_tasks=all_tasks,
                           tasks_count=all_tasks.count())


@task_bp.route("/employee/create", methods=['POST', 'GET'])
def employee_create():
    print("employee_create")

    form = EmployeeForm()

    employees = Employee.query.all()

    if form.validate_on_submit():
        name = form.name.data

        new_empl = Employee(name=name)
        print(new_empl)
        try:
            db.session.add(new_empl)
            db.session.commit()
            flash(f'Працівника "{new_empl.name}" успішно додано', 'success')
        except:
            db.session.rollback()
            flash(f'Помилка під час запису працівника "{new_empl.name}" до БД', 'danger')

        return redirect(url_for('task_bp_in.task_all'))

    return render_template('employee_create.html', title='Додавання новго працівника', form=form, employees=employees)


@task_bp.route("/employee/<int:id>/delete", methods=['POST', 'GET'])
def employee_delete(id):
    print("employee_delete")
    empl = Employee.query.get_or_404(id)
    try:
        db.session.delete(empl)
        db.session.commit()
        flash(f'Працівника "{empl.name}" видалено', 'warning')
    except:
        flash(f'Під час видалення працівника "{empl.name}" трапилась помилка.', 'danger')
    return redirect(url_for('task_bp_in.task_all'))


@task_bp.route("/category", methods=['POST', 'GET'])
def category():
    print("category")

    all_categories = Category.query.all()

    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        print('category name =', name)
        new_categ = Category(name=name)
        print(new_categ)
        try:
            db.session.add(new_categ)
            db.session.commit()
            flash(f'Категорію "{new_categ.name}" успішно додано', 'success')
        except:
            db.session.rollback()
            flash(f'Помилка під час запису категорії "{new_categ.name}" до БД\n '
                  f'Можливо ви ввели ввели вже існуючу назву завдання', 'danger')

        return redirect(url_for('task_bp_in.category'))

    return render_template('category.html', title='Категорії', form=form, all_categories=all_categories)


@task_bp.route("/category/<int:id>/delete")
def category_delete(id):
    print("category_delete")
    categ = Category.query.get_or_404(id)
    try:
        db.session.delete(categ)
        db.session.commit()
        flash(f'Категорія "{categ.name}" видалена', 'warning')
    except:
        flash(f'Під час видалення категорії "{categ.name}" трапилась помилка.', 'danger')
    return redirect(url_for('task_bp_in.category'))


@task_bp.route("/category/<int:id>/update", methods=['POST', 'GET'])
def category_update(id):
    form = CategoryForm()
    print("category_update")
    # дістаємо необхідний об'єкт завдання для редагування
    categ = Category.query.get_or_404(id)

    if request.method == 'GET':
        form.name.data = categ.name

        return render_template('category_update.html', title='Зміна категорії', form=form)

    else:
        if form.validate_on_submit():
            print("category_update validate_on_submit")

            # дістаємо дані із форм і відразу записуємо їх в БД
            categ.name = form.name.data

            print(categ)
            try:
                db.session.commit()
                flash(f'Категорія "{categ.name}" успішно змінена', 'info')
            except:
                db.session.rollback()
                flash(f'Помилка під час запису категорії "{categ.name}" до БД', 'danger')

            return redirect(url_for('task_bp_in.category'))

        flash('Помилка під час валідації.', 'danger')
        return redirect({{url_for('task_bp_in.category_update', id=id)}})