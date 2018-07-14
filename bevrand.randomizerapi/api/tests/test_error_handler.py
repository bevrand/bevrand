from api.tests.base import BaseTestCase
from api.error_handler.error_model import InvalidUsage
from api.controllers import randomize_controller, redis_controller
import pytest


def raise_error(message, status, meta=None):
    raise InvalidUsage(message=message, status_code=status, meta=meta)


class TestErrorHandler(BaseTestCase):
    """Tests for the Randomize ErrorHandling."""

    def test_error_raised(self):
        with pytest.raises(InvalidUsage):
            raise_error('hello from pytest', 400)

    def test_error_raised_with_meta(self):
        with pytest.raises(InvalidUsage):
            meta = {'hello', 'world'}
            raise_error('hello from pytest', 400, meta)

    def test_no_status_code_gives_back_400(self):
        sut = InvalidUsage('hello from pytest')
        assert sut.status_code == 400

    def test_invalid_usage_randomize(self):
        error = InvalidUsage('hello from pytest', 400)
        sut = randomize_controller.handle_invalid_usage(error)
        message = sut.response
        status = sut.status_code
        assert 'pytest' in message[0]
        assert status == 400

    def test_invalid_usage_redis(self):
        error = InvalidUsage('hello from pytest', 400)
        sut = redis_controller.handle_invalid_usage(error)
        message = sut.response
        status = sut.status_code
        assert 'pytest' in message[0]
        assert status == 400