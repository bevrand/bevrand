import subprocess
import json
import time
import argparse

parser = argparse.ArgumentParser(description='Create a docker-compose file based on arguments given')

tests_action_arg = parser.add_argument('--tests', type=str, default='component_tests',
                                     help='Test set to valdidate (default: %(default)s)')

args = parser.parse_args()
TESTS = args.tests

print(TESTS)

def wait_for_container_to_finish():
    running = True
    while running:
        status = subprocess.check_output("docker inspect " + TESTS, shell=True)
        status_json = json.loads(status)
        state = status_json[0]['State']
        running = state['Running']
        time.sleep(2)


def check_logs_for_backend():
    logs = subprocess.check_output("docker logs " + TESTS, shell=True)
    logs = str(logs)
    output = logs.replace("\\n", "\n")
    print(output)
    return logs


def validate_test_results():
    wait_for_container_to_finish()
    logs = str(check_logs_for_backend()).rstrip().replace(",", "")
    words = logs.split()
    terms = ['failed', 'FAILURES']
    for term in terms:
        if term in words:
                exit(1)
        else:
                exit(0)


validate_test_results()
