from api.tests.base import BaseTestCase
from api.services import data_validator
from api.error_handler.error_model import InvalidUsage
import pytest
from _pytest.monkeypatch import MonkeyPatch


class TestService(BaseTestCase):
    """Tests for the Randomize Service."""
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_valid_model_user_returns_none(self):
        sut = {'user' : 'test'}
        result = data_validator.validate_user_name(sut)
        assert result == None

    def test_valid_model_list_returns_none(self):
        sut = {'list' : 'validlist'}
        result = data_validator.validate_play_list(sut)
        assert result == None

    def test_valid_model_beverages_returns_none(self):
        sut = {'beverages': ['beer', 'wine', 'cola']}
        result = data_validator.validate_beverages(sut)
        assert result == None

    def test_invalid_user_raises_error(self):
        sut = {'user': 'te'}
        with pytest.raises(InvalidUsage):
            data_validator.validate_user_name(sut)

    def test_invalid_list_raises_error(self):
        sut = {'list': 't'}
        with pytest.raises(InvalidUsage):
            data_validator.validate_play_list(sut)

    def test_invalid_beverage_list_length_raises_error(self):
        sut = {'beverages': ['cola']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_beverages(sut)

    def test_invalid_beverage_in_beverage_list_raises_error(self):
        sut = {'beverages': ['cola', 'beer', 'f']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_beverages(sut)