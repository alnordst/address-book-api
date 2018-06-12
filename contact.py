import json


class Contact(object):
    """
    Contact object to provide validation of form data.
    """

    def __init__(self, form):
        """
        Initialize contact and populate fields using form data.
        """
        self.data = {}
        self.update(form)


    def __str__(self):
        """
        Output contact in json format.
        """
        return json.dumps(self.data, sort_keys = True)


    def update(self, form):
        """
        Populate fields using form data.
        """
        if 'name' in form:
            self.data['name'] = form['name']
        if 'address' in form:
            self.data['address'] = form['address']
        if 'city' in form:
            self.data['city'] = form['city']
        if 'state' in form:
            self.verify_state(form['state'])
        if 'zip_code' in form:
            self.verify_zip_code(form['zip_code'])
        if 'phone' in form:
            self.verify_phone(form['phone'])

        self.remove_empties()


    def remove_empties(self):
        """
        Remove unused keys (keys with value set to None)
        """
        for key in dict(self.data):
            if self.data[key] is None:
                del self.data[key]


    def verify_state(self, state):
        """
        Verify state is 2 character string, store it if valid
        """
        if state and state.isalpha() and len(state) == 2:
            self.data['state'] = state.upper()
        else:
            self.data['state'] = None


    def verify_zip_code(self, zip_code):
        """
        Verify zip code is 5 digit integer, store it if valid
        """
        if zip_code and str(zip_code).isdecimal() and len(str(zip_code)) == 5:
            self.data['zip_code'] = zip_code
        else:
            self.data['zip_code'] = None


    def verify_phone(self, phone):
        """
        Verify phone number is valid, store it if so
        """
        valid_phone = False

        if phone:
            phone_digits = ''.join(c for c in str(phone) if c not in '().-+')
            if phone_digits.isdecimal():
                if len(phone_digits) == 10:
                    self.data['phone'] = '({set1}){set2}-{set3}'.format(
                        set1 = phone_digits[:3],
                        set2 = phone_digits[3:6],
                        set3 = phone_digits[6:]
                    )
                    valid_phone = True
                elif len(phone_digits) >= 11 and len(phone_digits) <= 13:
                    self.data['phone'] = '+{set1}({set2}){set3}-{set4}'.format(
                        set1 = phone_digits[:-10],
                        set2 = phone_digits[-10:-7],
                        set3 = phone_digits[-7:-4],
                        set4 = phone_digits[-4:]
                    )
                    valid_phone = True

        if not valid_phone:
            self.data['phone'] = None
