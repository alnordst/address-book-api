# address-book-api

## Notes

Project went a little rough. A lot of trouble with elasticsearch both in 
learning how to work with it and running it.

## Instructions

API for contact management using elasticsearch.

Install packages with `python setup.py install`

Runs on port 5000, expects elasticsearch on port 9200.
Start elasticsearch first.

Elasticsearch port can be changed by changing PORT on line 10 of app.py
(didn't have time to make it a command line argument)

Run with `flask run` from base directory.

Run tests with `python3 -m unittests tests.` 
(tests require elasticsearch to be running)

## Endpoints

GET /contact?pageSize={}&page={}&query={}

List contacts by search query.


POST /contact

Creates a contact.


GET /contact/{name}

Returns contact by unique name.


PUT /contact/{name}

Updates contact by unique name.


DELETE /contact/{name}

Deletes contact by unique name.