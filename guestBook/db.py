import sqlite3
from datetime import datetime

import click

# g - специальный объект для временного хранения данных в рамках одного запроса
# current_app - экземпляр Flask, занимающийся обработкой текущего запроса
from flask import current_app, g

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

# PostgreSQL - psycopg, psycopg2, asyncpg, pg8000

# Используется везде, где нужен доступ к БД
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            # Путь до файла нашей базы данных
            current_app.config['DATABASE'],
            # Используем типы колонок в таблицах для определения, какой тип данных вернуть из базы в Python
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Возвращаемые строки будут словарями, к столбцам можно будет обращаться по имени
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    # Достаем подключение к базе данных
    db = get_db()
    # Открываем SQL-файл, читаем его в кодировке utf-8 и выполняем.
    #
    # После завершения работы файл закрываем.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """
    Clear the existing data and create new tables.
    """
    init_db()
    click.echo('Initialized the database.')

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    # Регистрируем действия по завершению обработки запроса.
    #
    # В частности, закрываем подключение к базе данных
    app.teardown_appcontext(close_db)
    # Регистрируем команду по инициализации базы данных
    app.cli.add_command(init_db_command)
