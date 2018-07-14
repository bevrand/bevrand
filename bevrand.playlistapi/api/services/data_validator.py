from cerberus import Validator
from api.error_handler.error_model import InvalidUsage


def validate_json_for_post(dict_file):
    schema = {'user': {'type': 'string', 'required': True, 'minlength': 3},
              'list': {'type': 'string', 'required': True, 'minlength': 2},
              'displayName': {'type': 'string'},
              'imageUrl': {'type': 'string'},
              'beverages': {'type': 'list', 'required': True, 'minlength' : 2,'schema': {'type': 'string', 'minlength': 2}}}
    validate_schema(schema, dict_file)
    return


def validate_json_for_list(list):
    schema = {'list': {'type': 'string', 'required': True, 'minlength': 2}}
    list_to_validate = {'list': list}
    validate_schema(schema, list_to_validate)
    return


def validate_json_for_user(user):
    schema = {'user': {'type': 'string', 'required': True, 'minlength': 3}}
    list_to_validate = {'user': user}
    validate_schema(schema, list_to_validate)
    return


def validate_schema(schema, file):
    v = Validator(schema)
    valid = v.validate(file, schema)
    if not valid:
        raise InvalidUsage('Errors occured when validating', status_code=400, meta=v.errors)
    return