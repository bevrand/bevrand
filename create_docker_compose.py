import argparse
import yaml
import string
import random
import sys
import os

parser = argparse.ArgumentParser(description='Create a docker-compose file based on arguments given')

image_action_group = parser.add_mutually_exclusive_group()

image_action_arg = image_action_group.add_argument('--pull-images', dest='image_action', action='store_const',
                                                   const='pull', default='build',
                                                   help='set image action to perform to pull, skips the build stage (default: %(default)s)')

image_action_group.add_argument('--build-images', dest='image_action', action='store_const',
                                const='build', default='build',
                                help='set image action to perform to build, ensures the build stage is executed even if the profile would have set it to pull (default: %(default)s)')

tag_action_arg = parser.add_argument('--tag', type=str, default='latest',
                                     help='The tag to set for your build images, or the tag that will be used to pull the custom images if --pull-images flag is set (default: %(default)s)')

jaeger_group = parser.add_argument_group('jaeger', 'jaeger related settings')

exclude_jaeger_arg = jaeger_group.add_argument('--exclude-jaeger', action='store_true',
                                               help='Jaeger containers will NOT be included if this flag is set (default: %(default)s)')

jaeger_group.add_argument('--jaeger-backend-db', type=str, default='els', choices=['els', 'cas'],
                          help='jaeger db to use (Default is els (elastic) other option is cas (cassandra will only be '
                               'used if --include-jaeger flag is set!')

parser.add_argument('--version', type=str, default='3.1', choices=["2", "3", "3.1"],
                    help='docker-compose version you want to use')

use_volume_arg = parser.add_argument('--use-volumes', action='store_true',
                                     help='When this flag is set, docker will use volumes for persistent data storage (default: %(default)s)')

run_component_arg = parser.add_argument('--run-component-tests', action='store_true',
                                        help='Whether you want componenttests included (default %(default)s)')

profile_group = parser.add_mutually_exclusive_group()

profile_group.add_argument('--no-profile', action='store_const', dest='profile', const='none',
                           help='Same as "--profile none". Contains no images by default, the base profile to use for setting all flags and setings manually')

profile_group.add_argument('--profile', type=str, default='dev',
                           choices=['prod', 'dev', 'database-only', 'ui-tests', 'component-tests', 'none'],
                           help='Sets the default action based on a particular purpose. All configurations can be made by setting all flags manually, the profiles just give an easier way to achieve this. [dev] builds all services and supporting systems with static passwords, for local development and demos. [database-only] runs only the database containers with data from database seeder, from images, for local development. [none] contains no images by default, the base profile to use for setting all flags and setings manually')

dataseeder_arg = parser.add_argument('--dataseeder', type=bool, default=True,
                                     help='Whether you want only the dataseeder (Default is True)')

pass_generation_arg = parser.add_argument('--generate-passwords', action='store_true',
                                          help='Whether you want to create a password (production) or use test passwords'
                                               '(default: %(default)s)')
# TODO Support stdin
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default='docker-compose-base.yml',
                    help='Select the docker-compose.yml base file %(default)s')

# TODO Set output to quiet if using stdout
# Output (file or stdout)
output_group = parser.add_mutually_exclusive_group()

output_group.add_argument('--stdout', action='store_true')
outfile_arg = output_group.add_argument('--out', dest='outfile', nargs='?', type=argparse.FileType('w'),
                                        default='docker-compose-created.yml')
parser.print_help()
args = parser.parse_args()

PROFILE = args.profile

DATABASE_ONLY = False

# All databases plus the dataseeder for local development
if PROFILE == 'database-only':
    dataseeder_arg.default = True
    exclude_jaeger_arg.default = True
    DATABASE_ONLY = True
# For local development
if PROFILE == 'dev':
    dataseeder_arg.default = False
    run_component_arg.default = True
    pass_generation_arg.default = True
# For Circle component tests environment
if PROFILE == 'component-tests':
    dataseeder_arg.default = True
    image_action_arg.default = 'pull'
    tag_action_arg.default = os.environ.get('CIRCLE_SHA1')
    exclude_jaeger_arg.default = True
    run_component_arg.default = True
    pass_generation_arg.default = True
# For Circle ui tests environment
if PROFILE == 'ui-tests':
    dataseeder_arg.default = True
    image_action_arg.default = 'pull'
    tag_action_arg.default = os.environ.get('CIRCLE_SHA1')
    exclude_jaeger_arg.default = True
    pass_generation_arg.default = True
# For production environment
if PROFILE == 'prod':
    dataseeder_arg.default = False
    image_action_arg.default = 'build'
    tag_action_arg.default = os.environ.get('CIRCLE_SHA1')
    use_volume_arg.default = True

USE_STDOUT = args.stdout
if USE_STDOUT:
    outfile_arg.default = sys.stdout

# After setting the defaults, re-read the arguments
args = parser.parse_args()

BUILD = args.image_action == 'build'
TAG = args.tag
JAEGER = args.exclude_jaeger is False
if JAEGER is True:
    JAEGERDB = args.jaeger_backend_db
VOLUME = args.use_volumes
VERSION = args.version
TESTS = args.run_component_tests
GENERATE_PASSWORD = args.generate_passwords
DATASEEDER = args.dataseeder
INFILE = args.infile
OUTFILE = args.outfile

yaml_file = {}
service_yaml_file = {}
databases_services = ['dockergres', 'dockermongo', 'redis']
test_services = ['componenttest']
api_services = ['authenticationapi', 'highscoreapi', 'randomizerapi', 'playlistapi', 'proxyapi', 'frontendapi',
                'dockernginx']
data_seeder_service = ['dataseeder']
password_services = {'authenticationapi': 'dockergres', 'playlistapi': 'dockermongo'}
volume_services = ['dockermongo', 'dockergres']
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
    print('Password creation = ' + str(GENERATE_PASSWORD))
    print('Version = ' + VERSION)
    print('Databases only = ' + str(DATABASE_ONLY))
    print('Dataseeder = ' + str(DATASEEDER))
    print('Outfile = ' + str(OUTFILE))


def create_password(length):
    chars = string.ascii_letters + string.digits + '!'
    return ''.join(random.sample(chars, length))


def create_user(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.sample(chars, length))


def load_docker_compose_file():
    stream = INFILE
    docs = yaml.load_all(stream)
    for doc in docs:
        for k, v in doc.items():
            if k == 'services':
                start_creation_of_yaml(v)


def write_a_test_compose_file(data):
    yaml.dump(data, OUTFILE, default_flow_style=False)


def set_version_for_yaml(yaml_version):
    yaml_file.update(version=yaml_version, services=service_yaml_file)


def replace_circle_sha_with_tag(tag):
    for service in service_yaml_file:
        for image in service_yaml_file[service]:
            if image == 'image':
                test = service_yaml_file[service][image]
                service_yaml_file[service][image] = test.replace("${CIRCLE_SHA1}", tag)


def start_creation_of_yaml(yaml_services):
    for service in yaml_services:
        handle_service_creation(service, yaml_services[service])
    if BUILD is True:
        remove_build_or_images('image')
    else:
        remove_build_or_images('build')
    if GENERATE_PASSWORD is True:
        password = create_password(25)
        user_name = create_user(15)
        for client, server in password_services.items():
            set_passwords(client, server, user_name, password)
    else:
        if os.environ.get('MONGO_USERNAME') is not None:
            mongo_username = os.environ.get('MONGO_USERNAME')
            mongo_password = os.environ.get('MONGO_PASSWORD')
            set_passwords('playlistapi', 'dockermongo', mongo_username, mongo_password)
        if os.environ.get('POSTGRES_USERNAME') is not None:
            postgres_username = os.environ.get('POSTGRES_USERNAME')
            postgres_password = os.environ.get('POSTGRES_PASSWORD')
            set_passwords('authenticationapi', 'dockergres', postgres_username, postgres_password)
    if VOLUME is False:
        remove_volumes()

    if TAG is not None and BUILD is False:
        replace_circle_sha_with_tag(TAG)


def handle_service_creation(service_name, service_yaml):
    if DATASEEDER is True and service_name in data_seeder_service:
        service_yaml_file[service_name] = service_yaml
    if DATABASE_ONLY is True:
        if service_name in databases_services:
            service_yaml_file[service_name] = service_yaml
        return
    if JAEGER is True:
        service_name = select_jaeger_database(service_name, service_yaml)
    else:
        remove_jaeger_from_env()
    if TESTS is True and service_name in test_services:
        service_yaml_file[service_name] = service_yaml
    if service_name in api_services:
        service_yaml_file[service_name] = service_yaml
    if service_name in databases_services:
        service_yaml_file[service_name] = service_yaml
    return


def select_jaeger_database(service_name, service_yaml):
    if (JAEGERDB == 'els' and service_name in jaeger_services_es) \
            or (JAEGERDB == 'cas' and service_name in jaeger_services_cas):
        service_name = remove_jaeger_db_extension_from_name(service_name)
        service_yaml_file[service_name] = service_yaml
    return service_name


def remove_jaeger_from_env():
    """" Removes all Jaeger related environment variables """
    for service in service_yaml_file:
        for field in service_yaml_file[service]:
            if field == 'environment' or field == 'depends_on':
                remove_jaeger_entries(field, service)


def remove_jaeger_entries(field, service):
    """ If the service with given field's entry is "jaeger-agent"
    or starts with "JAEGER_AGENT",
    then it is removed from the service yaml """

    for env in service_yaml_file[service][field]:
        if env == "jaeger-agent" or env.startswith("JAEGER_AGENT"):
            service_yaml_file[service][field].remove(env)


def remove_build_or_images(field):
    to_remove = []
    for service in service_yaml_file:
        for f in service_yaml_file[service]:
            if f == 'build':
                to_remove.append(service)
    for item in to_remove:
        service_yaml_file[item].pop(field, None)


def set_passwords(client, server, user_name, password):
    password_object = PassWordObjects()

    auth_str = password_object.authenticationapi
    auth_str = auth_str.replace("PLACEHOLDER_PASS", password)
    auth_str = auth_str.replace("PLACEHOLDER_USER", user_name)

    gres_str = []
    for password_placeholder in password_object.dockergres:
        password_placeholder = password_placeholder.replace("PLACEHOLDER_PASS", password)
        password_placeholder = password_placeholder.replace("PLACEHOLDER_USER", user_name)
        gres_str.append(password_placeholder)

    play_str = password_object.playlistapi
    play_str = play_str.replace("PLACEHOLDER_PASS", password)
    play_str = play_str.replace("PLACEHOLDER_USER", user_name)

    mon_str = []
    for password_placeholder in password_object.dockermongo:
        password_placeholder = password_placeholder.replace("PLACEHOLDER_PASS", password)
        password_placeholder = password_placeholder.replace("PLACEHOLDER_USER", user_name)
        mon_str.append(password_placeholder)

    if client == 'authenticationapi':
        service_yaml_file[client]['environment'].append(auth_str)
        for field in service_yaml_file[client]['environment']:
            if field == 'ASPNETCORE_ENVIRONMENT="Development"':
                service_yaml_file[client]['environment'].remove('ASPNETCORE_ENVIRONMENT="Development"')
                service_yaml_file[client]['environment'].append('ASPNETCORE_ENVIRONMENT="Production"')
        service_yaml_file[server]['environment'].remove('POSTGRES_PASSWORD=postgres')
        service_yaml_file[server]['environment'].remove('POSTGRES_USER=postgres')
        for environment in gres_str:
            service_yaml_file[server]['environment'].append(environment)
    elif client == 'playlistapi':
        service_yaml_file[client]['environment'].remove('MONGO_URL=mongodb://dockermongo:27017/admin')
        service_yaml_file[client]['environment'].append(play_str)
        if DATASEEDER is True:
            service_yaml_file['dataseeder']['environment'].remove('MONGO_URL=mongodb://dockermongo:27017/admin')
            service_yaml_file['dataseeder']['environment'].append(play_str)
        for environment in mon_str:
            service_yaml_file[server]['environment'].append(environment)


def remove_volumes():
    for service in volume_services:
        service_yaml_file[service].pop('volumes', None)


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
