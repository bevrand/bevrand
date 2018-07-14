from api.tests.base import BaseTestCase
from api.service import redis_service, data_validator, view_models
from api.error_handler.error_model import InvalidUsage
from api.db.redis_connection import RedisConnection
from api.db.data_models import SuccessModelRedis
import pytest
from _pytest.monkeypatch import MonkeyPatch


class TestService(BaseTestCase):
    """Tests for the Randomize Service."""
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test_valid_model_returns_none(self):
        sut = {'user' : 'test', 'list': 'test', 'beverages': ['beer', 'wine', 'cola']}
        result = data_validator.validate_json_for_randomize(sut)
        assert result == None


    def test_invalid_user_raises_error(self):
        sut = {'user': 'te', 'list': 'test', 'beverages': ['beer', 'wine', 'cola']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_randomize(sut)


    def test_invalid_list_raises_error(self):
        sut = {'user': 'test', 'list': 't', 'beverages': ['beer', 'wine', 'cola']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_randomize(sut)

    def test_invalid_beverage_list_length_raises_error(self):
        sut = {'user': 'test', 'list': 'test', 'beverages': ['cola']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_randomize(sut)

    def test_invalid_beverage_in_beverage_list_raises_error(self):
        sut = {'user': 'test', 'list': 'test', 'beverages': ['cola', 'beer', 'f']}
        with pytest.raises(InvalidUsage):
            data_validator.validate_json_for_randomize(sut)

    def test_model_created_correctly(self):
        test_list = ['beer', 'wine']
        message = 'hello from the tests'
        model = view_models.ErrorModel(list_to_return=test_list, message=message)
        assert message == model.message
        assert 'beer' in model.list


    def test_random_drink_return(self):
        def mockreturn(self, redis_col, drink_to_incr):
            return
        self.monkeypatch.setattr(RedisConnection, 'count_rolled_drinks', mockreturn)
        drink_list = ['wine', 'beer', 'cola']
        user = 'pytest'
        sut = redis_service.randomize_drink_from_list(drink_list, user)
        assert sut in drink_list

    def test_lists_are_returned_in_the_correct_format(self):
        drink_list = []
        first_drink = 'beer'
        first_rolled = 10
        second_drink = 'wine'
        second_rolled = 9
        drink_list.append({'drink': 'montypytest:' + first_drink, 'rolled': first_rolled})
        drink_list.append({'drink': 'montypytest:' + second_drink, 'rolled': second_rolled})
        mock_model = SuccessModelRedis(drink_list)

        def mockreturn(self, redis_col):
            return mock_model

        self.monkeypatch.setattr(RedisConnection, 'get_top_list', mockreturn)
        sut = redis_service.get_all_rolled_drinks_from_redis(user='monthy', desc_list='pytest', topfive_bool=False)
        returned_list = sut['body']['monthy:pytest']
        assert len(returned_list) == 2
        assert first_drink == returned_list[0]['drink']
        assert second_drink == returned_list[1]['drink']
        assert first_rolled == returned_list[0]['rolled']
        assert second_rolled == returned_list[1]['rolled']

    def test_lists_are_limited_to_five_when_bool_is_true(self):
        drink_list = []
        drink_list.append({'drink': 'montypytest:beer', 'rolled': 10})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 9})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 8})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 7})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 6})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 5})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 4})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 3})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 2})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 1})
        mock_model = SuccessModelRedis(drink_list)

        def mockreturn(self, redis_col):
            return mock_model

        self.monkeypatch.setattr(RedisConnection, 'get_top_list', mockreturn)
        sut = redis_service.get_all_rolled_drinks_from_redis(user='monthy', desc_list='pytest', topfive_bool=True)
        returned_list = sut['body']['monthy:pytest']
        assert len(returned_list) == 5

    def test_lists_are_complete_when_bool_is_false(self):
        drink_list = []
        drink_list.append({'drink': 'montypytest:beer', 'rolled': 10})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 9})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 8})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 7})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 6})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 5})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 4})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 3})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 2})
        drink_list.append({'drink': 'montypytest:wine', 'rolled': 1})
        mock_model = SuccessModelRedis(drink_list)

        def mockreturn(self, redis_col):
            return mock_model

        self.monkeypatch.setattr(RedisConnection, 'get_top_list', mockreturn)
        sut = redis_service.get_all_rolled_drinks_from_redis(user='monthy', desc_list='pytest', topfive_bool=False)
        returned_list = sut['body']['monthy:pytest']
        assert len(returned_list) == len(drink_list)
