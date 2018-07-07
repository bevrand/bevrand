import subprocess
import json
import time


def wait_for_container_to_finish():
    running = True
    while running:
        status = subprocess.check_output("docker inspect backend_tests", shell=True)
        status_json = json.loads(status)
        state = status_json[0]['State']
        running = state['Running']
        time.sleep(5)
    return


def check_logs_for_backend():
    logs = subprocess.check_output("docker logs backend_tests", shell=True)
    return logs


def normalize_list(list_to_normalize):
    corrected_list = []
    for word in list_to_normalize:
        word = word.replace('\\n', '')
        word = word.split('.')[0]
        corrected_list.append(word)
    return corrected_list


def print_success_and_failed_tests(list_to_print):
    passed_index = list_to_print.index("Passed:")
    failed_index = list_to_print.index("Failed:")
    skipped_index = list_to_print.index("Skipped:")
    print('%s %s' %(list_to_print[passed_index], list_to_print[passed_index + 1])) 
    print('%s %s' %(list_to_print[failed_index], list_to_print[failed_index + 1]))
    print('%s %s' %(list_to_print[skipped_index], list_to_print[skipped_index + 1]))
    return


def validate_test_results():
    wait_for_container_to_finish()
    logs = str(check_logs_for_backend()).rstrip()
    words = logs.split()
    split_word = "tests:"
    split_list = words[words.index(split_word):len(words)]
    corrected_list = normalize_list(split_list)
    print_success_and_failed_tests(corrected_list)
    term = 'Successful'
    if term in corrected_list:
        print("Tests successful")
        exit(0)
    else:
        print("One or more tests failed printing logs for more details")
        print(logs)
        exit(1)
    return


validate_test_results()
