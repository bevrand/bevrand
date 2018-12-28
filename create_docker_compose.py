import argparse
import yaml
import string
import random
import os

parser = argparse.ArgumentParser(description='Create a docker-compose file based on arguments given')

parser.add_argument('--build', type=bool, default=True,
                    help='Whether you want to build your images or you want to use an image (Default is True')

parser.add_argument('--tag', type=str,
                    help='The tag to use for your images, will only be set if build is True!')

parser.add_argument('--jaeger', type=bool, default=False,
                    help='Whether you want jaeger included (Default is false, any value will result in True)')

parser.add_argument('--jaegerdb', type=str, default='els', choices=['els', 'cas'],
                    help='jaeger db to use (Default is els (elastic) other option is cas (cassandra will only be '
                         'set if jaeger flag is True!')

parser.add_argument('--version', type=str, default='2', choices=["2", "3", "3.1"],
                    help='docker-compose version you want to use')

parser.add_argument('--volume', type=bool, default=False,
                    help='Whether you want to use volumes(Default is false, any value will result in True)')

parser.add_argument('--tests', type=bool, default=False,
                    help='Whether you want componenttests included (Default is false, any value will result in True)')

parser.add_argument('--databaseonly', type=bool, default=False,
                    help='Whether you want only the databases and a dataseeder for local development'
                         '(Default is false, any value will result in True)')

parser.add_argument('--dataseeder', type=bool, default=True,
                    help='Whether you want only the dataseeder (Default is true)')

parser.add_argument('--password', type=bool, default=False,
                    help='Whether you want to create a password (production) or use test passwords'
                         '(Default is false, any value will result in True)')

args = parser.parse_args()

BUILD = args.build
if BUILD is False:
    TAG = args.tag
JAEGER = args.jaeger
if JAEGER is True:
    JAEGERDB = args.jaegerdb
VOLUME = args.volume
VERSION = args.version
TESTS = args.tests
CREATE_PASSWORD = args.password
DATABASE_ONLY = args.databaseonly
DATASEEDER = args.dataseeder

yaml_file = {}
service_yaml_file = {}
databases_services = ['dockergres', 'dockermongo', 'redis']
test_services = ['componenttest']
api_services = ['authenticationapi', 'highscoreapi', 'randomizerapi', 'playlistapi', 'proxyapi', 'reactapp']
data_seeder_service = ['dataseeder']
jaeger_services_cas = ['jaeger-collector-cas', 'jaeger-query-cas', 'jaeger-agent-cas', 'cassandra', 'cassandra-schema']
jaeger_services_es = ['els', 'kibana', 'jaeger-collector-els', 'jaeger-agent-els', 'jaeger-query-els']

def print_values_at_startup():
    print('Build = ' + str(BUILD))
    if BUILD is False:
        print('tag = ' + TAG)
    print('Jaeger = ' + str(JAEGER))
    if JAEGER is True:
        print('Jaegerdb = ' + JAEGERDB)
    print('Volume = ' + str(VOLUME))
    print('Tests = ' + str(TESTS))
    print('Password creation = ' + str(CREATE_PASSWORD))
    print('Version = ' + VERSION)
    print('Databases only = ' + str(DATABASE_ONLY))
    print('Dataseeder = ' + str(DATASEEDER))


def create_password_and_users():
    chars = string.ascii_letters + string.digits + '!@#$%^&*()/\{}[]<>'
    return ''.join(random.sample(chars, 32))


def load_docker_compose_file():
    stream = open("docker-compose-base.yml", "r")
    docs = yaml.load_all(stream)
    for doc in docs:
        for k, v in doc.items():
            if k == 'services':
                start_creation_of_yaml(v)


def write_a_test_compose_file(data):
    with open('docker-compose-test.yml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def set_version_for_yaml(yaml_version):
    yaml_file.update(version=yaml_version, services=service_yaml_file)
    return


def start_creation_of_yaml(yaml_services):
    for service in yaml_services:
        handle_service_creation(service, yaml_services[service])
    if BUILD is True:
        remove_build_or_images('image')
    else:
        remove_build_or_images('build')
    return


def handle_service_creation(service_name, service_yaml):
    if DATASEEDER is True:
        if service_name in data_seeder_service:
            service_yaml_file[service_name] = service_yaml
    if DATABASE_ONLY is True:
        if service_name in databases_services:
            service_yaml_file[service_name] = service_yaml
        return
    if JAEGER is True:
        if JAEGERDB == 'els':
            if service_name in jaeger_services_es:
                service_name = remove_jaeger_db_extension_from_name(service_name)
                service_yaml_file[service_name] = service_yaml
        elif JAEGERDB == 'cas':
            if service_name in jaeger_services_cas:
                service_name = remove_jaeger_db_extension_from_name(service_name)
                service_yaml_file[service_name] = service_yaml
    if TESTS is True:
        if service_name in test_services:
            service_yaml_file[service_name] = service_yaml
    if service_name in api_services:
        service_yaml_file[service_name] = service_yaml
    if service_name in databases_services:
        service_yaml_file[service_name] = service_yaml
    return


def remove_build_or_images(field):
    to_remove = []
    for service in service_yaml_file:
        for f in service_yaml_file[service]:
            if f == 'build':
                to_remove.append(service)
    for item in to_remove:
        service_yaml_file[item].pop(field, None)
    return


def remove_jaeger_db_extension_from_name(service_name):
    if '-els' in service_name or '-cas' in service_name:
        stripped_name = service_name.split('-')
        service_name = '-'.join(stripped_name[:2])
    return service_name


print_values_at_startup()
load_docker_compose_file()
set_version_for_yaml(VERSION)
write_a_test_compose_file(yaml_file)
