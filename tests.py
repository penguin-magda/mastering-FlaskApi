#!/usr/bin/env python
import unittest
import json
from config import Config
from app import create_app, db
from app.models import Artists, Hits
from faker import Faker
from tqdm import tqdm
from random import randint

fake = Faker()


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


def populate_database():
    """Populate database with fake aritsts and fake hits"""
    for i in tqdm(range(50)):
        a = Artists(first_name=fake.first_name(), last_name=fake.last_name())
        db.session.add(a)
        db.session.commit()
    for i in tqdm(range(200)):
        h = Hits(artist_id=randint(1, 50), title=fake.sentence())
        db.session.add(h)
        db.session.commit()


class HitsModelCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.test_client = cls.app.test_client()

        from app.api import bp as bp_api

        cls.app.register_blueprint(bp_api)

        db.create_all()
        populate_database()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test1_get_hits(self):
        """Test API can lists hits"""
        response = self.test_client.get("/api/v1/hits")
        self.assertEqual(response.status_code, 200)

    def test2_create_hit(self):
        """Test API can create hit"""
        data = dict(title="Jakiś losowy tytuł", artist_id=12)
        response = self.test_client.post(
            "/api/v1/hits", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = {"title": "test"}
        response = self.test_client.post("/api/v1/hits", data=data)
        self.assertEqual(response.status_code, 400)

    def test3_get_one_hit(self):
        """Test API can detail specific hit"""
        response = self.test_client.get("/api/v1/hits/jakis-losowy-tytul")
        self.assertEqual(response.status_code, 200)
        response = self.test_client.get("/api/v1/hits/aaa")
        self.assertEqual(response.status_code, 404)

    def test4_update_hit(self):
        """Test API can modify specific hit"""
        data = dict(title="rest")
        response = self.test_client.put(
            "/api/v1/hits/jakis-losowy-tytul",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = dict(artist_id=17, title="Inny tytuł")
        response = self.test_client.put(
            "/api/v1/hits/rest", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = dict(artist_id=5)
        response = self.test_client.put(
            "/api/v1/hits/rest", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = dict(artist_id=58)
        response = self.test_client.put(
            "/api/v1/hits/rest", data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = dict(artist_id=58)
        response = self.test_client.put(
            "/api/v1/hits/inny-tytul",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test5_delete_hit(self):
        """Test API can delete hit"""
        response = self.test_client.delete("/api/v1/hits/rest")
        self.assertEqual(response.status_code, 204)
        response = self.test_client.delete("/api/v1/hits/inny-tytul")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
