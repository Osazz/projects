from sqlite3 import OperationalError

from util import DatabaseUtil, Log
from exceptions import MissingVariable
from model import ContactInformation

LOG = Log('business_logic').log


class Management(DatabaseUtil):

    def save_information(self, first_name, phone_number, email_address, last_name=None):
        """
        This saves contact information to the database
        :param first_name: First name of the customer/friend that you want to save his/her contact in string
        :param phone_number: The phone number of your contact all in integer
        :param email_address: The email address of contact
        :param last_name: Last name of contact
        :return: success code (0)
        """
        LOG.info('Creating new contact information')

        def _create_information(conn, cur, _first_name, _phone_number, _email_address, _last_name=None):
            LOG.debug('Creating information for {0}'.format(_first_name))

            cur.execute("INSERT INTO contacts(first_name, phone_number, email_address, last_name)"
                        "values('{0}', '{1}', '{2}', '{3}')"
                        .format(_first_name, _phone_number, _email_address, _last_name))

            conn.commit()

            LOG.info("Successfully create contact information for {0}".format(_first_name))

        return self.do_db_transaction(_create_information, first_name, phone_number, email_address, last_name)

    def delete_information(self, contact_id):
        """
        This the function that carries out the delete operation
        :param contact_id: unique id of the contact you want to delete
        :return: 0
        """
        if not contact_id:
            raise MissingVariable("To delete contact information, we need either contact's phone number or email address")

        LOG.info('Deleting contact information ')

        def _delete_information(conn, cur, _contact_id):
            msg = "Deleting information for"
            customize_log(msg, contact_id, 'debug')

            query = "Delete from contacts where true and id={0}".format(_contact_id)

            cur.execute(query)
            conn.commit()
            customize_log("Successfully delete information for ", _contact_id, 'info')

        return self.do_db_transaction(_delete_information, contact_id)

    def update_information(self, contact_id, first_name=None, phone_number=None, email_address=None, last_name=None):
        """
        update contact information. since phone number and email must be unique they must be passed
        :param contact_id: ID pf info you wish to edit
        :param first_name: First name of the customer/friend that you want to update his/her contact in string
        :param phone_number: The phone number of your contact all in integer
        :param email_address: The email address of contact
        :param last_name: Last name of contact
        :return: 0
        """

        def _update_information(conn, cur, _first_name=None, _phone_number=None, _email_address=None, _last_name=None):
            condition = []
            set_statement = []
            if _email_address:
                condition.append(" and email_address='{0}'".format(_email_address))
            if _phone_number:
                condition.append(" and phone_number='{0}'".format(_phone_number))

            if _first_name:
                set_statement.append(" first_name = '{0}'".format(_first_name))
            if _last_name:
                set_statement.append(" last_name = '{0}'".format(_last_name))

            query = "update contacts set {0} where id={2} {1}".format(', '.join(set_statement), ', '.join(condition), contact_id)
            customize_log("updating contact information for ", _phone_number, _email_address, 'debug')
            cur.execute(query)
            conn.commit()

            customize_log("Successfully update contact information for ", _phone_number, _email_address)

        return self.do_db_transaction(_update_information, first_name, phone_number, email_address, last_name)

    def search_information(self, contact_id=None, first_name=None, phone_number=None, email_address=None, last_name=None):
        """
        Seacrh data base for contact information.
        :param contact_id: id of contact
        :param first_name: First name of the customer/friend that you want to update his/her contact in string
        :param phone_number: The phone number of your contact all in integer
        :param email_address: The email address of contact
        :param last_name: Last name of contact
        :return: 0
        """

        def _get_information(conn, cur, _id=None, _first_name=None, _phone_number=None, _email_address=None, _last_name=None):
            query = "Select id, first_name, phone_number, email_address, last_name from contacts where true "
            if id:
                query += " and id={0}".format(id)
            if first_name:
                query += " and first_name='{0}'".format(first_name)
            if phone_number:
                query += " and phone_number='{0}'".format(phone_number)
            if email_address:
                query += " and email_address='{0}'".format(email_address)
            if last_name:
                query += " and last_name='{0}'".format(last_name)
            cur.execute(query)
            record = [
                ContactInformation(record[0], record[1], record[2], record[3], record[4], record[5])
                for record in cur.fetchall()
            ]
            conn.commit()
            return record

        return self.do_db_transaction(_get_information, contact_id, first_name, phone_number, email_address, last_name)

    def create_db_table(self):
        def _create_table(conn, cur):
            # check if table exist
            try:
                cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'""")
                if not cur.fetchone():
                    raise OperationalError("Table does not exist")
            except OperationalError as e:
                self.log.error(e)
                cur.execute('''CREATE TABLE contacts
                                                (   
                                                    id INTEGER,
                                                    first_name character(128) NOT NULL,
                                                    last_name character(128),
                                                    phone_number character(1), 
                                                    email_address VARCHAR NOT NULL,
                                                    CONSTRAINT contacts_pkey PRIMARY KEY (id)
                                                )
                                            ''')

            conn.commit()
            LOG.debug('contacts table exist')

        return self.do_db_transaction(_create_table)


def customize_log(msg, phone_num, email, level='info'):
    if level == 'info':
        log = LOG.info
    else:
        log = LOG.debug

    if phone_num and not email:
        log('{0} {1}'.format(msg, phone_num))
    elif email and not phone_num:
        log('{0} {1}'.format(msg, email))
    else:
        log('{0} {1} and {2}'.format(msg, phone_num, email))
