from cerberus import Validator
from api.error_handler.error_model import InvalidUsage


def validate_play_list(play_list):
    schema = {'playlist': {'type': 'string', 'required': True, 'minlength': 2}}
    list_to_validate = {'playlist': play_list}
    validate_schema(schema, list_to_validate)


def validate_user_name(user):
    schema = {'user': {'type': 'string', 'required': True, 'minlength': 3}}
    list_to_validate = {'user': user}
    validate_schema(schema, list_to_validate)


def validate_beverages(beverages):
    schema = {'beverages': {'type': 'list', 'required': True, 'minlength' : 2,'schema': {'type': 'string', 'minlength': 2}}}
    beverages_to_validate = {'beverages': beverages}
    validate_schema(schema, beverages_to_validate)


def validate_schema(schema, file):
    v = Validator(schema)
    valid = v.validate(file, schema)
    if not valid:
        raise InvalidUsage('Errors occured when validating', meta=v.errors)
    return
