import argparse
import yaml
import string
import random
import os


parser = argparse.ArgumentParser(description='Create a docker-compose file based on arguments given')

# jaeger_group = parser.add_argument_group('jaeger', 'jaeger related settings')
image_action_group = parser.add_mutually_exclusive_group()

image_action_group.add_argument('--pull-images', dest='image_action', action='store_const',
                                const='pull', default='build',
                                help='set image action to perform to pull, skips the build stage (default: %(default)s)')

image_action_group.add_argument('--build-images', dest='image_action', action='store_const',
                                const='build', default='build',
                                help='set image action to perform to build, ensures the build stage is executed even if the profile would have set it to pull (default: %(default)s)')

parser.add_argument('--tag', type=str, default='latest',
                    help='The tag to set for your build images, or the tag that will be used to pull the custom images if --pull-images flag is set (default: %(default)s)')

jaeger_group = parser.add_argument_group('jaeger', 'jaeger related settings')

jaeger_group.add_argument('--include-jaeger', action='store_true',
                          help='Jaeger containers will be included if this flag is set (default: %(default)s)')

jaeger_group.add_argument('--jaeger-backend-db', type=str, default='els', choices=['els', 'cas'],
                          help='jaeger db to use (Default is els (elastic) other option is cas (cassandra will only be '
                               'used if --include-jaeger flag is set!')

parser.add_argument('--version', type=str, default='2', choices=["2", "3", "3.1"],
                    help='docker-compose version you want to use')

parser.add_argument('--use-volumes', action='store_true',
                    help='When this flag is set, docker will use volumes for persistent data storage (default: %(default)s)')

parser.add_argument('--run-component-tests', action='store_true',
                    help='Whether you want componenttests included (default %(default)s)')

profile_group = parser.add_mutually_exclusive_group()

profile_group.add_argument('--no-profile', action='store_const', dest='profile', const='none',
                           help='Same as "--profile none". Contains no images by default, the base profile to use for setting all flags and setings manually')

profile_group.add_argument('--profile', type=str, default='dev', choices=['dev', 'database-only', 'none'],
                           help='Sets the default action based on a particular purpose. All configurations can be made by setting all flags manually, the profiles just give an easier way to achieve this. [dev] builds all services and supporting systems with static passwords, for local development and demos. [database-only] runs only the database containers with data from database seeder, from images, for local development. [none] contains no images by default, the base profile to use for setting all flags and setings manually')

parser.add_argument('--databaseonly', type=bool, default=False,
                    help='Whether you want only the databases and a dataseeder for local development'
                         '(Default is false, any value will result in True)')

dataseeder_arg = parser.add_argument('--dataseeder', type=bool, default=False,
                                     help='Whether you want only the dataseeder (Default is true)')

parser.add_argument('--generate-passwords', action='store_true',
                    help='Whether you want to create a password (production) or use test passwords'
                         '(default: %(default)s)')
# TODO Support stdin
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default='docker-compose.yml',
                    help='Select the docker-compose.yml base file %(default)s')

# TODO Set output to quiet if using stdout
# Output (file or stdout)
output_group = parser.add_mutually_exclusive_group()

output_group.add_argument('--stdout', action='store_true')
outfile_arg = output_group.add_argument('--out', dest='outfile', nargs='?', type=argparse.FileType('w'),
                                        default='docker-compose-test2.yml')
parser.print_help()
args = parser.parse_args()

PROFILE = args.profile

if PROFILE == 'database-only':
    dataseeder_arg.default = True

USE_STDOUT = args.stdout
if USE_STDOUT:
    outfile_arg.default = sys.stdout

# After setting the defaults, re-read the arguments
args = parser.parse_args()

BUILD = args.image_action == 'build'
TAG = args.tag
JAEGER = args.include_jaeger
if JAEGER is True:
    JAEGERDB = args.jaeger_backend_db
VOLUME = args.use_volumes
VERSION = args.version
TESTS = args.run_component_tests
CREATE_PASSWORD = args.generate_passwords
DATABASE_ONLY = args.databaseonly
DATASEEDER = args.dataseeder
INFILE = args.infile
OUTFILE = args.outfile

yaml_file = {}
service_yaml_file = {}
databases_services = ['dockergres', 'dockermongo', 'redis']
test_services = ['componenttest']
api_services = ['authenticationapi', 'highscoreapi', 'randomizerapi', 'playlistapi', 'proxyapi', 'frontendapi']
data_seeder_service = ['dataseeder']
password_services = {'authenticationapi': 'dockergres', 'playlistapi': 'dockermongo'}
volume_services = ['dockergres', 'dockermongo']
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


def create_password(length):
    chars = string.ascii_letters + string.digits + '!'
    return ''.join(random.sample(chars, length))


def create_user(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.sample(chars, length))


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
    if CREATE_PASSWORD is True:
        set_random_passwords()
    if VOLUME is True:
        set_volumes()
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
    else:
        remove_jaeger_from_env()
    if TESTS is True:
        if service_name in test_services:
            service_yaml_file[service_name] = service_yaml
    if service_name in api_services:
        service_yaml_file[service_name] = service_yaml
    if service_name in databases_services:
        service_yaml_file[service_name] = service_yaml
    return


def remove_jaeger_from_env():
    for service in service_yaml_file:
        for field in service_yaml_file[service]:
            if field == 'environment':
                for env in service_yaml_file[service][field]:
                    if env == "JAEGER_AGENT_HOST=jaeger-agent":
                        service_yaml_file[service][field].remove(env)
                    if env == "JAEGER_AGENT_PORT=6831":
                        service_yaml_file[service][field].remove(env)
            if field == 'depends_on':
                for depends in service_yaml_file[service][field]:
                    if depends == "jaeger-agent":
                        service_yaml_file[service][field].remove(depends)

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


def set_random_passwords():
    for k, v in password_services.items():

        password = create_password(25)
        user_name = create_user(15)
        password_object = PassWordObjects()

        auth_str = password_object.authenticationapi
        auth_str = auth_str.replace("PLACEHOLDER_PASS", password)
        auth_str = auth_str.replace("PLACEHOLDER_USER", user_name)

        gres_str = []
        for str in password_object.dockergres:
            str = str.replace("PLACEHOLDER_PASS", password)
            str = str.replace("PLACEHOLDER_USER", user_name)
            gres_str.append(str)

        play_str = password_object.playlistapi
        play_str = play_str.replace("PLACEHOLDER_PASS", password)
        play_str = play_str.replace("PLACEHOLDER_USER", user_name)

        mon_str = []
        for str in password_object.dockermongo:
            str = str.replace("PLACEHOLDER_PASS", password)
            str = str.replace("PLACEHOLDER_USER", user_name)
            mon_str.append(str)

        if k == 'authenticationapi':
            service_yaml_file[k]['environment'].append(auth_str)
            for field in service_yaml_file[k]['environment']:
                if field == 'ASPNETCORE_ENVIRONMENT="Development"':
                    service_yaml_file[k]['environment'].remove('ASPNETCORE_ENVIRONMENT="Development"')
                    service_yaml_file[k]['environment'].append('ASPNETCORE_ENVIRONMENT="Production"')
            service_yaml_file[v]['environment'].remove('POSTGRES_PASSWORD=postgres')
            service_yaml_file[v]['environment'].remove('POSTGRES_USER=postgres')
            for str in gres_str:
                service_yaml_file[v]['environment'].append(str)
        elif k == 'playlistapi':
            service_yaml_file[k]['environment'].remove('MONGO_URL=mongodb://dockermongo:27017/admin')
            service_yaml_file[k]['environment'].append(play_str)
            if DATASEEDER is True:
                service_yaml_file['dataseeder']['environment'].remove('MONGO_URL=mongodb://dockermongo:27017/admin')
                service_yaml_file['dataseeder']['environment'].append(play_str)
            for str in mon_str:
                service_yaml_file[v]['environment'].append(str)
    return


def set_volumes():
    for service in volume_services:
        service_yaml_file[service]['volumes'].append('test')
    return


def remove_jaeger_db_extension_from_name(service_name):
    if '-els' in service_name or '-cas' in service_name:
        stripped_name = service_name.split('-')
        service_name = '-'.join(stripped_name[:2])
    return service_name


class PassWordObjects(object):

    authenticationapi = 'ConnectionStrings:PostGres=Host=dockergres;Port=5432;Database=bevrand;Uid=PLACEHOLDER_USER;Pwd=PLACEHOLDER_PASS;'
    dockergres = ['POSTGRES_PASSWORD=PLACEHOLDER_PASS', 'POSTGRES_USER=PLACEHOLDER_USER']
    dockermongo = ['MONGO_INITDB_ROOT_USERNAME=PLACEHOLDER_USER', 'MONGO_INITDB_ROOT_PASSWORD=PLACEHOLDER_PASS']
    playlistapi = 'MONGO_URL=mongodb://PLACEHOLDER_USER:PLACEHOLDER_PASS@dockermongo:27017/admin'

print_values_at_startup()
load_docker_compose_file()
set_version_for_yaml(VERSION)
write_a_test_compose_file(yaml_file)
