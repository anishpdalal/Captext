# project/tests/helpers.py

from project.server.models import Entry, db


def create_test_entries():
    entry1 = Entry(1, "The sky is blue.", "https://www.facts.com", "Sky is Blue", keywords="sky, color, nature")
    db.session.add(entry1)
    db.session.commit()
    entry2 = Entry(1, "Outer space is empty.", "https://www.space.com", "Empty Outer Space", keywords="space, nature, astronomy")
    db.session.add(entry2)
    db.session.commit()
