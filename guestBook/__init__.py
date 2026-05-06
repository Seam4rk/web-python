import os

from flask import Flask

def create_app():
    # Создаем экземпляр Flask для инициализации web-приложения
    app = Flask(__name__, instance_relative_config=True)

    app.instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')

    # Проставляем глобальные параметры нашего приложения
    app.config.from_mapping(
        # Обязательный параметр для защиты данных
        SECRET_KEY='dev',
        # Путь до файла базы данных SQLite
        DATABASE=os.path.join(app.instance_path, 'guestBook.sqlite'),
    )

    # Загружаем конфигурацию из файла "config.py"
    # app.config.from_pyfile('config.py', silent=True)

    # Создаем папки по пути "app.instance_path"
    os.makedirs(app.instance_path, exist_ok=True)

    # Инициализируем подключение к базе данных
    from . import db
    db.init_app(app)

    # Инициализируем маршруты (blueprints)

    from . import guestBook
    app.register_blueprint(guestBook.bp)
    app.add_url_rule('/', endpoint='index')

    return app
