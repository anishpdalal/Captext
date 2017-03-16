# project/tests/test_entries.py


import unittest
import json
import datetime

from project.tests.base import BaseTestCase
from project.server.models import Entry
from helpers import create_test_entries

TEXT = """ Bacon ipsum dolor amet t-bone pastrami chicken, sirloin bacon corned beef beef ribs jerky burgdoggen
    picanha. Drumstick leberkas chicken ball tip pork belly shoulder salami doner tongue rump corned beef beef ribs
    tail ham frankfurter. Salami brisket venison bacon. Meatball short ribs prosciutto picanha, biltong alcatra
    hamburger pork belly venison chicken rump meatloaf shank. Pork chop strip steak turducken tongue biltong bresaola,
    flank porchetta kielbasa."""


def register_user(self, email, password):
    return self.client.post(
            '/auth/register',
            data=json.dumps(dict(
                    email=email,
                    password=password
            )),
            content_type='application/json',
    )


class TestEntryBlueprint(BaseTestCase):
    """ Tests that user can create entry """

    def test_entry_creation(self):
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                    '/entries',
                    headers=dict(
                            Authorization='Bearer ' + json.loads(
                                    resp_register.data.decode()
                            )['auth_token'],
                    ),
                    data=json.dumps(dict(
                            text=TEXT,
                            url="https://www.yankees.com",
                            keywords="yankees, sports, baseball",
                            title="The Yankees Win"
                    )),
                    content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'created new entry')
            self.assertEqual(data['url'], "https://www.yankees.com")
            self.assertEqual(data['text'], TEXT)
            self.assertEqual(data['keywords'], "yankees, sports, baseball")
            self.assertEqual(data['title'], "The Yankees Win")
            self.assertTrue(data['user_id'] is not None)
            self.assertTrue(data['created_on'] is not None)
            self.assertEqual(isinstance(data['created_on'], unicode), True)
            entry = Entry.query.filter_by(title=data.get('title')).first()
            self.assertTrue(entry is not None)

    def test_create_entry_with_no_auth_header(self):
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                    '/entries',
                    data=json.dumps(dict(
                            text=TEXT,
                            url="https://www.yankees.com",
                            keywords="yankees, sports, baseball",
                            title="The Yankees Win"
                    )),
                    content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide a valid auth token.')
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(response.status_code, 403)

    def test_create_entry_with_empty_auth_token(self):
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                    '/entries',
                    headers=dict(
                            Authorization=''
                    ),
                    data=json.dumps(dict(
                            text=TEXT,
                            url="https://www.yankees.com",
                            keywords="yankees, sports, baseball",
                            title="The Yankees Win"
                    )),
                    content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], 'Provide a valid auth token.')
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(response.status_code, 403)

    def test_create_entry_without_url(self):
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            response = self.client.post(
                    '/entries',
                    headers=dict(
                            Authorization='Bearer ' + json.loads(
                                    resp_register.data.decode()
                            )['auth_token'],
                    ),
                    data=json.dumps(dict(
                            text=TEXT,
                            keywords="yankees, sports, baseball",
                            title="The Yankees Win"
                    )),
                    content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertEqual(data['message'], 'Please provide url, title, and text')
            self.assertEqual(response.status_code, 200)

    def test_get_entries(self):
        with self.client:
            resp_register = register_user(self, 'joe@gmail.com', '123456')
            create_test_entries()
            response = self.client.get(
                    '/entries',
                    headers=dict(
                            Authorization='Bearer ' + json.loads(
                                    resp_register.data.decode()
                            )['auth_token'],
                    )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['message'], 'retrieved entries')
            self.assertEqual(len(data['results']), 2)
            self.assertEqual(isinstance(data['results'][0]['created_on'], unicode), True)
            self.assertTrue(
                datetime.datetime.strptime(data['results'][0]['created_on'], '%m/%d/%Y') >= datetime.datetime.strptime(
                        data['results'][1]['created_on'], '%m/%d/%Y'))
            self.assertTrue(len(data['results'][0]['categories']), 3)
            self.assertTrue(data['results'][0]['user_id'] == data['results'][1]['user_id'])


if __name__ == '__main__':
    unittest.main()
