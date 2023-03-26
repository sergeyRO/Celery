import app
import pytest

@pytest.fixture(scope='module')
def test_client():
    flask_app = app.app
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()