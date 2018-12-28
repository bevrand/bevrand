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

parser.add_argument('--version', type=str, default='2', choices=['2', '3', '3.1'],
                    help='docker-compose version you want to use')

parser.add_argument('--volume', type=bool, default=False,
                    help='Whether you want to use volumes(Default is false, any value will result in True)')

parser.add_argument('--tests', type=bool, default=False,
                    help='Whether you want componenttests included (Default is false, any value will result in True)')

parser.add_argument('--databaseonly', type=bool, default=False,
                    help='Whether you want only the databases and a dataseeder for local development '
                         '(Default is false, any value will result in True)')

parser.add_argument('--password', type=bool, default=False,
                    help='Whether you want to create a password (production) or use test passwords'
                         '(Default is false, any value will result in True)')

args = parser.parse_args()

build = args.build
if build is False:
    tag = args.tag
jaeger = args.jaeger
if jaeger is True:
    jaegerdb = args.jaegerdb
volume = args.volume
version = args.version
tests = args.tests
create_password = args.password
database_only = args.databaseonly


def print_values_at_startup():
    print('Build = ' + str(build))
    if build is False:
        print('tag = ' + tag)
    print('Jaeger = ' + str(jaeger))
    if jaeger is True:
        print('Jaegerdb = ' + jaegerdb)
    print('Volume = ' + str(volume))
    print('Tests = ' + str(tests))
    print('Password creation = ' + str(create_password))
    print('Version = ' + version)
    print('Databases only = ' + str(database_only))


def create_password_and_users():
    chars = string.ascii_letters + string.digits + '!@#$%^&*()/\{}[]<>'
    return ''.join(random.sample(chars, 32))


def load_docker_compose_file():
    print(os.getcwd())
    stream = open("docker-compose-base.yml", "r")
    docs = yaml.load_all(stream)
    for doc in docs:
        for k, v in doc.items():
            print(k, "->", v)
        print("\n",)


def write_a_test_compose_file(data):
    with open('docker-test.yml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


print_values_at_startup()
load_docker_compose_file()
data = dict(Version=version)
write_a_test_compose_file(data)
