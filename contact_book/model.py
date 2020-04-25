class ContactInformation(object):

    def __init__(self, contact_id=None, first_name=None, phone_number=None, email_address=None, last_name=None):
        self._contact_id = contact_id
        self._first_name = first_name
        self._phone_number = phone_number
        self._email_address = email_address
        self._last_name = last_name

    @property
    def contact_id(self):
        return self._contact_id

    @contact_id.setter
    def contact_id(self, value):
        self._contact_id = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def email_address(self):
        return self._email_address

    @email_address.setter
    def email_address(self, value):
        self._email_address = value

    def __repr__(self, *args, **kwargs):
        return 'Student [id : {4}, first_name: {0}, phone_number: {1}, last_name: {2}, email_address: {3} ]' \
            .format(self._first_name, self._phone_number, self._last_name, self._email_address, self._contact_id)
