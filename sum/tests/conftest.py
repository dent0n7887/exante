import pytest
from asyncio import new_event_loop, set_event_loop
from aiohttp import web
from consts import SETTINGS, DATA_SERVICE
from settings import Settings
from os import remove
from services import DataService
from models import DataModel
from dao import DataDAO
from views_manager import ViewsManager
from utils.AppMiddleware import error_middleware


@pytest.fixture
def loop():
    loop = new_event_loop()
    set_event_loop(loop)
    return loop


@pytest.fixture
def get_app():
    app = web.Application()
    return app


@pytest.fixture
def f_test_client(get_app, aiohttp_client, loop, f_data_service):
    manager = ViewsManager(app=get_app)
    manager.register_routes()
    get_app.middlewares.append(error_middleware)
    get_app[DATA_SERVICE] = f_data_service
    return loop.run_until_complete(aiohttp_client(get_app))


@pytest.fixture
def env_settings(env_setup, get_app):
    settings = Settings(_env_file=".env_test")
    get_app[SETTINGS] = settings
    return settings


@pytest.fixture
def env_setup(request, env_data):
    with open('.env_test', 'w') as file:
        file.writelines([f"{key} = {env_data[key]}\n" for key in env_data])

    def env_teardown():
        remove(".env_test")

    request.addfinalizer(env_teardown)


@pytest.fixture
def env_data():
    return {
        "DB_NAME": "test_db_name",
        "DB_USER": "test_db_user",
        "DB_PASSWORD": "test_db_pass",
        "DB_HOST": "test_db_host",
    }


@pytest.fixture
def f_data_dao():
    return DataDAO(app=get_app)


@pytest.fixture
def f_data_service(f_data_dao):
    return DataService(data_dao=f_data_dao)


@pytest.fixture
def f_data_model():
    return [DataModel(
        id=1,
        js='{"z": [1, "a", 0.5, 1], "": True}',
        sum=2
    )]