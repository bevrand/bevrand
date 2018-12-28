import argparse
import yaml

parser = argparse.ArgumentParser(description='Create a docker-compose file based on arguments given')

parser.add_argument('--build', type=bool, default=True,
                    help='Whether you want to build your images or you want to use an image (Default is True')

parser.add_argument('--tag', type=str,
                    help='The tag to use for your images, will only be set if build is True!')

parser.add_argument('--jaeger', type=bool, default=False,
                    help='Whether you want jaeger included (Default is false, any value will result in True)')

parser.add_argument('--jaegerdb', type=str, default='es', choices=['es', 'cas'],
                    help='jaeger db to use (Default is es (elastic) other option is cas (cassandra will only be '
                         'set if jaeger flag is True!')

parser.add_argument('--volume', type=bool, default=False,
                    help='Whether you want to use volumes(Default is false, any value will result in True)')

parser.add_argument('--tests', type=bool, default=False,
                    help='Whether you want componenttests included (Default is false, any value will result in True)')

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
tests = args.tests
create_password = args.password


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


print_values_at_startup()