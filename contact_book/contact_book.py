#!/usr/bin/python
import argparse
import re

from business_logic import Management
from util import Logger, program_name

log = Logger(program_name()).log


class WrongVariable(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class TooLongVariable(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def alphanumeric(var, variable_name):
    if not var.isalnum():
        raise WrongVariable("{0} must be a alphanumeric".format(variable_name))
    too_long_val(var, variable_name)


def email_val(var, variable_name):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", var):
        raise WrongVariable("{0} must be an email".format(variable_name))
    too_long_val(var, variable_name)


def string_validation(var, variable_name):
    if not var.isalpha():
        raise WrongVariable("{0} must be a string".format(variable_name))

    too_long_val(var, variable_name)


def integer(var, variable_name):
    if not int(var):
        raise WrongVariable("{0} must be a int".format(variable_name))

    too_long_val(var, variable_name)


def too_long_val(var, variable_name):
    if len(var) > 256:
        raise TooLongVariable("{0} is too long, max length is 256".format(variable_name))


def _input_validation(variable, data_type):
    var_input = ''
    count = 2
    while count > 0:
        count -= 1
        try:
            msg = 'Please enter {0} of your contact : '.format(variable)
            var_input = input(msg)
            if data_type == 'string':
                string_validation(var_input, variable)
            if data_type == 'alphanumeric':
                alphanumeric(var_input, variable)
            if data_type == 'int':
                integer(var_input, variable)
            if data_type == 'email':
                email_val(var_input, variable)
            break
        except TooLongVariable as e:
            log.warning(e)
            continue
        except WrongVariable as e:
            log.warning(e)
            continue

    if count == 0:
        log.error("Problem getting input for {0}. please follow the rule")
        raise SystemExit(2)
    return var_input


def input_var(numbers):
    contact_id, first_name, last_name, phone_number, email_address = None, None, None, None, None
    for num in numbers:
        if num == 0:
            contact_id = _input_validation('contact id', 'int')
        if num == 1:
            first_name = _input_validation('first name', 'string')
        if num == 2:
            last_name = _input_validation('last name', 'string')
        if num == 3:
            phone_number = _input_validation('phone number', 'int')
        if num == 4:
            email_address = _input_validation('email address', 'email')

    return contact_id, first_name, last_name, phone_number, email_address


def save_info():
    num = [1, 2, 3, 4]
    __, first_name, last_name, phone_number, email_address = input_var(num)

    ma = Management()
    ma.save_information(first_name, str(phone_number), email_address, last_name)


def delete_info():
    contact_id = _input_validation('contact id', 'int')

    ma = Management()
    ma.delete_information(contact_id)


def search_info():
    def _do_search(_contact_id=None, _first_name=None, _last_name=None, _phone_number=None, _email_address=None):
        ma = Management()
        return ma.search_information()

    def _search_res(search):
        log.info("Contact result is : \n {0}".format(search))

    user_question = input("What do you want to search with. Select number \n"
                          "0 Return all values"
                          "1 Search with contact id"
                          "2 Search with last name"
                          "3 Search with first name"
                          "4 Search with phone number"
                          "5 Search with email")

    if int(user_question) == 5:
        _search_res(_do_search())
    if int(user_question) == 0:
        contact_id, __, __, __, __ = input_var([int(user_question)])
        _search_res(_do_search(_contact_id=contact_id))
    if int(user_question) == 1:
        __, first_name, __, __, __ = input_var([int(user_question)])
        _search_res(_do_search(_first_name=first_name))
    if int(user_question) == 2:
        __, __, last_name, __, __ = input_var([int(user_question)])
        _search_res(_do_search(_last_name=last_name))
    if int(user_question) == 3:
        __, __, __, phone_number, __ = input_var([int(user_question)])
        _search_res(_do_search(_phone_number=phone_number))
    if int(user_question) == 4:
        __, __, __, __, email_address = input_var([int(user_question)])
        _search_res(_do_search(_email_address=email_address))


def edit_info():
    log.info('Editing user information')
    first_name, email_address, last_name, phone_number = None, None, None, None
    edit_question = []
    expected_input = [1, 2, 3, 4, 0]
    ma = Management()
    contact_id, __, __, __, __ = input_var([0])
    ma.update_information(contact_id=contact_id)
    answer = 'No'
    count = 5
    while answer != 'done' and count > 0:
        edit_answer = input("Please select a number of information you wish to update \n"
                            "1. Search with last name"
                            "2. Search with first name"
                            "3. Search with phone number"
                            "4. Search with email\n"
                            "if you are done type 0"
                            )
        try:
            if int(edit_answer) == 0:
                answer = 'done'
                continue
            if int(edit_answer) in expected_input and int(edit_answer) not in edit_question:
                edit_question.append(int(edit_answer))
        except ValueError:
            log.error("We only accept integer value in {0}".format(expected_input))
            raise SystemExit(2)
        count -= 1

    for num in edit_question:
        if num == 1:
            __, first_name, __, __, __ = input_var([num])
        elif num == 2:
            __, __, last_name, __, __ = input_var([num])
        elif num == 3:
            __, __, __, phone_number, __ = input_var([num])
        elif num == 4:
            __, __, __, __, email_address = input_var([num])
    ma.update_information(contact_id=contact_id, first_name=first_name, last_name=last_name, phone_number=phone_number,
                          email_address=email_address)
    log.info("User information successfully updated")


if __name__ == "__main__":
    log.info("Starting contact management process")
    Management().create_db_table()
    parser = argparse.ArgumentParser(prog='contact_book',
                                     description='contact book management for storing, deleting and searching address book',
                                     usage='%(prog)s path')
    parser.add_argument('action', type=str, choices=['save', 'delete', 'edit', 'search'], help='Select one of the actions '
                                                                                               'you want to perform')
    args = parser.parse_args()

    if args.action == 'save':
        save_info()
    elif args.action == 'delete':
        delete_info()
    elif args.action == 'edit':
        edit_info()
    elif args.action == 'search':
        search_info()
    else:
        log.error("Action Value can only be one of this: ['save', 'delete', 'edit', 'search']")
        raise SystemExit(2)
    args = parser.parse_args()
