from flask import Flask
from elasticsearch import Elasticsearch
from contact import Contact


class Handler(object):
    """
    Handles operations on elasticsearch.
    """

    def __init__(self, index_name, port = 9200, wipe_index = False):
        self.index_name = index_name
        self.es = Elasticsearch(port = port)

        if wipe_index and self.es.indices.exists(self.index_name):
            self.es.indices.delete(index = self.index_name)

        if not self.es.indices.exists(self.index_name):
            self.es.indices.create(index = self.index_name)


    def list_contacts(self, arguments):
        """
        Returns a list of contacts or False.
        """
        try:
            self.es.indices.refresh(index = self.index_name)
            res = self.es.search(index = self.index_name, body = {
                "from": arguments["page"] * arguments["pageSize"],
                "size": arguments["pageSize"],
                "query": arguments["query"]
            })
            return res['hits']['hits']

        except:
            return False


    def create_contact(self, form):
        """
        Creates contact from form data. Returns True if successful.
        """
        try:
            if self._get_contact(form['name']): #contact by that name exists
                return False
            else:
                contact = Contact(form)
                res = self.es.index(index = self.index_name, doc_type = '_doc',
                                     body = str(contact))
                return res['result'] == 'created'

        except:
            return False


    def list_a_contact(self, name):
        """
        Returns data on a single contact identified by name.
        """
        try:
            return  self._get_contact(name)['_source']
        except:
            return False


    def update_contact(self, form):
        """
        Update a contact using form data. Returns True if successful.
        """
        try:
            if self.delete_contact(form['name']):
                return self.create_contact(form)
            else:
                return False
        except:
            return False

    def delete_contact(self, name):
        """
        Delete a contact identified by name. Returns True if successful.
        """
        try:
            contact_id = self._get_contact(name)['_id']
            res = self.es.delete(index = self.index_name, doc_type = '_doc',
                                 id = contact_id)
            return res['result'] == 'deleted'
        except:
            return False

    def _get_contact(self, name):
        try:
            self.es.indices.refresh(index = self.index_name)
            res = self.es.search(index = self.index_name, body = {
                "query": {
                    "match": {
                        "name": name
                    }
                }
            })
            return res['hits']['hits'][0]
        except:
            return False
