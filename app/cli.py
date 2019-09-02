from faker import Faker
from app.models import Artists, Hits
from app import db
from random import randint
from tqdm import tqdm

fake = Faker()


def register(app):
    @app.cli.group()
    def populatedb():
        """Create Artists and Hits"""
        pass

    @populatedb.command()
    def artists():
        for i in tqdm(range(50)):
            a = Artists(first_name=fake.first_name(), last_name=fake.last_name())
            db.session.add(a)
            db.session.commit()

    @populatedb.command()
    def hits():
        if len(Artists.query.all()) == 0:
            raise RuntimeError("Populate hits failed. First populate Artists.")
        for i in tqdm(range(200)):
            h = Hits(artist_id=randint(1, 50), title=fake.sentence())
            db.session.add(h)
            db.session.commit()
