# project/tests/test_entry_model.py

import unittest
from datetime import datetime

from project.server import db
from project.server.models import Entry, User
from project.tests.base import BaseTestCase

TEXT = """ Bacon ipsum dolor amet t-bone pastrami chicken, sirloin bacon corned beef beef ribs jerky burgdoggen
    picanha. Drumstick leberkas chicken ball tip pork belly shoulder salami doner tongue rump corned beef beef ribs
    tail ham frankfurter. Salami brisket venison bacon. Meatball short ribs prosciutto picanha, biltong alcatra
    hamburger pork belly venison chicken rump meatloaf shank. Pork chop strip steak turducken tongue biltong bresaola,
    flank porchetta kielbasa."""


class TestEntryModel(BaseTestCase):
    """ Tests that an Entry gets created successfully"""

    def test_create_entry(self):
        user = User(
                name='Billy Bob',
                email='test@test.com',
                password='test'
        )
        db.session.add(user)
        db.session.commit()
        pub_date = datetime.utcnow()

        entry = Entry(user_id=user.id,
                      text=TEXT,
                      created_on=pub_date,
                      keywords="yankees, sports, baseball",
                      url="https://www.yankees.com",
                      title="The Yankees Win")
        db.session.add(entry)
        db.session.commit()
        stored_entry = Entry.query.filter_by(user_id=user.id).first()
        assert stored_entry.text == TEXT
        assert stored_entry.created_on == pub_date
        assert stored_entry.keywords == "yankees, sports, baseball"
        assert stored_entry.url == "https://www.yankees.com"
        assert stored_entry.title == "The Yankees Win"

    def test_no_pub_date_provided(self):
        """ Tests Entry creation when no publication date is provided"""
        user = User(
                name='Billy Bob',
                email='test@test.com',
                password='test'
        )
        db.session.add(user)
        db.session.commit()
        entry = Entry(user_id=user.id,
                      text=TEXT,
                      keywords="yankees, sports, baseball",
                      url="https://www.yankees.com",
                      title="The Yankees Win")
        db.session.add(entry)
        db.session.commit()
        stored_entry = Entry.query.filter_by(user_id=user.id).first()
        assert stored_entry.created_on


if __name__ == '__main__':
    unittest.main()
