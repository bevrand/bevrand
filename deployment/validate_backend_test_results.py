import subprocess
import json
import time


def wait_for_container_to_finish():
    running = True
    while running:
        status = subprocess.check_output("docker inspect component_tests", shell=True)
        status_json = json.loads(status)
        state = status_json[0]['State']
        running = state['Running']
        time.sleep(2)
    return


def check_logs_for_backend():
    logs = subprocess.check_output("docker logs component_tests", shell=True)
    logs = str(logs)
    output = logs.replace("\\n", "\n")
    print(output)
    return logs


def validate_test_results():
    wait_for_container_to_finish()
    logs = str(check_logs_for_backend()).rstrip()
    words = logs.split()
    term = 'FAILURES'
    if term in words:
        exit(1)
    else:
        exit(0)
    return


validate_test_results()
