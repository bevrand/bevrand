from cerberus import Validator


def validate_json_for_randomize(dict_file):
    schema = {'user': {'type': 'string', 'required': True, 'minlength': 3},
              'list': {'type': 'string', 'required': True, 'minlength': 2},
              'beverages': {'type': 'list', 'required': True, 'minlength' : 2,'schema': {'type': 'string'}}}
    return validate_schema(schema, dict_file)


def validate_json_for_list(list):
    schema = {'list': {'type': 'string', 'required': True, 'minlength': 2}}
    list_to_validate = {'list': list}
    return validate_schema(schema, list_to_validate)


def validate_json_for_user(user):
    schema = {'user': {'type': 'string', 'required': True, 'minlength': 3}}
    list_to_validate = {'user': user}
    return validate_schema(schema, list_to_validate)


def validate_schema(schema, file):
    v = Validator(schema)
    valid = v.validate(file, schema)
    json_data = {'valid': valid, 'errors': v.errors}
    return json_data
