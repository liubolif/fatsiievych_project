import click
from flask.cli import with_appcontext
from app import db
from app.profile.models import User
from app.task.models import Task, Category, Employee

@click.group()
def cli():
    pass

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()
    click.echo("tables created!!!")


@click.command(name='create_admin')
@with_appcontext
def create_admin():
    username = "test_admin"
    email = "test_admin@gmail.com"
    password = "11111111"
    admin = True
    user = User(username=username, email=email, password=password, admin=admin)
    #print("superadmin created", u)
    db.session.add(user)
    db.session.commit()
    click.echo("admin created!!!")

cli.add_command(create_tables)
cli.add_command(create_admin)


if __name__ == '__main__':
    cli()
# @click.command(name="create_user")
# @with_appcontext
# def create_user():
#     user = User(username='username', email='email', password='password')
#     db.session.add(user)
#     db.session.commit()