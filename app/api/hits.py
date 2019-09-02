from app.api import bp
from flask import jsonify, request, url_for
from sqlalchemy import desc
from app.api.errors import bad_request, error_response
from app.models import Hits, Artists
from app import db

# [GET] wyświetla listę 20 hitów
@bp.route("/v1/hits", methods=["GET"])
def get_hits():
    hits = Hits.query.order_by(desc("created_at")).limit(20)
    return jsonify(Hits.to_dict_collection(hits))


# [POST] tworzy nowy hit na podstawie przekazanego obiektu: artistID, title
@bp.route("/v1/hits", methods=["POST"])
def create_hit():
    data = request.get_json() or {}
    if "artist_id" not in data or "title" not in data:
        return bad_request("must include artist and title fields")
    hit = Hits()
    hit.from_dict(data)
    db.session.add(hit)
    db.session.commit()
    response = jsonify(hit.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_title", title_url=hit.title_url)
    return response


# [GET] wyświetla szczegóły pojedynczego hitu
@bp.route("/v1/hits/<string:title_url>", methods=["GET"])
def get_title(title_url):
    hits = Hits.query.filter_by(title_url=title_url)
    if hits.count() > 0:
        for hit in hits:
            return jsonify(Hits.query.get_or_404(hit.id).to_dict())
    return error_response(404, "NOT FOUND")


# [PUT] aktualizuje wybrany hit (tylko pola artist_id, title, title_url
# i automatycznie wypełnia pole updated_at
@bp.route("/v1/hits/<string:title_url>", methods=["PUT"])
def update_title(title_url):
    try:
        mod_hit = Hits.query.filter_by(title_url=title_url).first()
        data = request.get_json() or {}
        mod_hit.from_dict(data)
        db.session.commit()
        return jsonify(mod_hit.to_dict())
    except:
        return bad_request("BAD REQUEST")


# [DELETE] usuwa wybrany hit
@bp.route("/v1/hits/<string:title_url>", methods=["DELETE"])
def delete_title(title_url):
    hits = Hits.query.filter_by(title_url=title_url)
    response = []
    if hits.count() > 0:
        for hit in hits:
            db.session.delete(hit)
            message = f"Hit '{hit.title}' has been deleted. ID number: {hit.id}"
            response.append({"message": message})
        db.session.commit()
        return jsonify(response)
    else:
        return error_response(204, "NO CONTENT")
