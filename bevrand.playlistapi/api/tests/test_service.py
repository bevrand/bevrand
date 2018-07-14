from api.tests.base import BaseTestCase
from api.services import data_validator
from api.error_handler.error_model import InvalidUsage
import pytest
from _pytest.monkeypatch import MonkeyPatch


class TestService(BaseTestCase):
    """Tests for the Randomize Service."""
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_valid_model_returns_none(self):
        sut = {'user' : 'test', 'list': 'test', 'beverages': ['beer', 'wine', 'cola']}
        result = data_validator.validate_json_for_post(sut)
        assert result == None


    def test_invalid_user_raises_error(self):
        sut = {'user': 'te', 'list': 'test', 'beverages': ['beer', 'wine', 'cola']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_post(sut)


    def test_invalid_list_raises_error(self):
        sut = {'user': 'test', 'list': 't', 'beverages': ['beer', 'wine', 'cola']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_post(sut)

    def test_invalid_beverage_list_length_raises_error(self):
        sut = {'user': 'test', 'list': 'test', 'beverages': ['cola']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_post(sut)

    def test_invalid_beverage_in_beverage_list_raises_error(self):
        sut = {'user': 'test', 'list': 'test', 'beverages': ['cola', 'beer', 'f']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_post(sut)