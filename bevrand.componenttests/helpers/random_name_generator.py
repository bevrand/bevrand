import random
import string


class HelperClass(object):

    @staticmethod
    def random_word_special_signs_included(word_length):
        sb = ''
        chars = string.ascii_letters + string.digits + '!@#$%^&*(){}[]<>'
        for x in range(0, word_length):
            sb += chars
        return ''.join(random.sample(sb, word_length))

    @staticmethod
    def random_word_letters_only(word_length):
        sb = ''
        chars = string.ascii_letters
        for x in range(0, word_length):
            sb += chars
        return ''.join(random.sample(sb, word_length))

    @staticmethod
    def random_int_generator(word_length):
        sb = ''
        chars = string.digits
        for x in range(0, word_length):
            sb += chars
        return ''.join(random.sample(sb, word_length))

    @staticmethod
    def create_random_email():
        first_part = HelperClass.random_word_letters_only(15)
        second_part = HelperClass.random_word_letters_only(5)
        return f'{first_part}@{second_part}.com'
