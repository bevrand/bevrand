import argparse

parser = argparse.ArgumentParser(description='Create a docker-compose file based on arguments given')

parser.add_argument('--override', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

for arg in args:
    print(arg)
