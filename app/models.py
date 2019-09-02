from sqlalchemy import event
from app import db
from datetime import datetime
from slugify import slugify


class Artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hits = db.relationship("Hits", backref="artist", lazy="dynamic")

    def __repr__(self):
        return f"<Artist {self.first_name} {self.last_name}>"


class Hits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    title = db.Column(db.String(255))
    title_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @staticmethod
    def generate_title_url(target, value, oldvalue, initializator):
        if value and (not target.title_url or value != oldvalue):
            target.title_url = slugify(value)

    def __repr__(self):
        return f"<{self.title}>"

    @staticmethod
    def to_dict_collection(query):
        data = []
        temp_dict = {}
        for hit in query:
            temp_dict["id"] = hit.id
            temp_dict["title"] = hit.title
            temp_dict["title_url"] = hit.title_url
            data.append(temp_dict)
            temp_dict = {}
        return data

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "title_url": self.title_url,
            "created_at": self.created_at,
            "artists": {
                "id": self.artist.id,
                "first_name": self.artist.first_name,
                "last_name": self.artist.last_name,
            },
        }
        return data

    def from_dict(self, data):
        for field in ["artist_id", "title"]:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def delete_hit(hit):
        data = {
            "id": hit.id,
            "title": hit.title,
            "message": f"Hit {hit.title} has been deleted",
        }
        return data


event.listen(Hits.title, "set", Hits.generate_title_url, retval=False)
