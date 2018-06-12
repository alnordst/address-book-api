import unittest
from contact import Contact
import json
from handling import Handler

def toJson(form):
    return json.dumps(form, sort_keys = True)

class TestContactClass(unittest.TestCase):

    def test_input_output(self):
        form = {'name': 'Alex'}
        contact = Contact(form)
        self.assertEqual(toJson(form), str(contact))

    def test_update(self):
        form = {'name': 'Alex'}
        form2 = {'name': 'Alli'}
        contact = Contact(form)
        contact.update(form2)
        self.assertEqual(toJson(form2), str(contact))

    def test_remove_empties(self):
        form = {'name': 'Alex', 'last_name': None}
        contact = Contact(form)
        del form['last_name']
        self.assertEqual(toJson(form), str(contact))

    def test_verify_state(self):
        form = {'state': 'MD'}
        form2 = {'state': 'md'}
        form3 = {'state': 'Maryland'}
        form4 = {}
        contact = Contact(form)
        contact2 = Contact(form2)
        contact3 = Contact(form3)
        self.assertEqual(toJson(form), str(contact))
        self.assertEqual(toJson(form), str(contact2))
        self.assertEqual(toJson(form4), str(contact3))

    def test_verify_zip_code(self):
        form = {'zip_code': 12345}
        form2 = {'zip_code': 1234}
        form3 = {'zip_code': 123456}
        form4 = {}
        contact = Contact(form)
        contact2 = Contact(form2)
        contact3 = Contact(form3)
        self.assertEqual(toJson(form), str(contact))
        self.assertEqual(toJson(form4), str(contact2))
        self.assertEqual(toJson(form4), str(contact3))

    def test_verify_phone(self):
        form = {'phone': 1234567890}
        form2 = {'phone': 12345678901}
        form3 = {'phone': 12345678901234}
        form4 = {'phone': '(123)456-7890'}
        form5 = {'phone': '+1(234)567-8901'}
        form6 = {}
        contact = Contact(form)
        contact2 = Contact(form2)
        contact3 = Contact(form3)
        contact4 = Contact(form4)
        contact5 = Contact(form5)
        self.assertEqual(toJson(form4), str(contact))
        self.assertEqual(toJson(form5), str(contact2))
        self.assertEqual(toJson(form6), str(contact3))
        self.assertEqual(toJson(form4), str(contact4))
        self.assertEqual(toJson(form5), str(contact5))

class TestHandling(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.handler = Handler('test', wipe_index = True)

    def test_create_contact(self):
        form = {'name': 'Alex', 'city': 'Laurel', 'state': 'MD'}
        self.assertTrue(self.handler.create_contact(form))
        self.assertFalse(self.handler.create_contact(form))
        form2 = {'city': 'New York'}
        self.assertFalse(self.handler.create_contact(form2))

    def test_list_a_contact(self):
        form = {'name': 'Alex', 'city': 'Laurel', 'state': 'MD'}
        es_contact = self.handler.list_a_contact('Alex')
        self.assertEqual(es_contact, form)

    def test_list_contacts(self):
        form = {'name': 'Alli', 'state': 'MD'}
        form2 = {'name': 'son'}
        self.handler.create_contact(form)
        self.handler.create_contact(form)
        res = self.handler.list_contacts({"query": {"match": {"state": "MD"}},
            "page": 0, "pageSize": 1})
        res2 = self.handler.list_contacts({"query": {"match": {"state": "MD"}},
            "page": 1, "pageSize": 1})
        self.assertTrue(res)
        self.assertTrue(res2)
        self.assertTrue(len(res) == 1)
        self.assertFalse(res[0]['_source'] == res2[0]['_source'])

    def test_update_contact(self):
        form = {'name': 'Corinne', 'city': 'Laurel'}
        form2 = {'name': 'Corinne', 'city': 'Baltimore'}
        self.assertFalse(self.handler.update_contact(form))
        self.handler.create_contact(form)
        #self.assertTrue(self.handler.update_contact(form2))
        #self.assertEqual(self.handler.list_a_contact('Corinne'), form2)

    def test_delete_contact(self):
        form = {'name': 'a ghost'}
        self.handler.create_contact(form)
        self.assertTrue(self.handler.delete_contact('a ghost'))
        self.assertFalse(self.handler.list_a_contact('a ghost'))
