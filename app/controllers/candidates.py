from flask import request
from app.models import Candidate, db


def get_all_candidates():
    candidates = Candidate.query.all()
    return {"data": [candidate.to_dict() for candidate in candidates]}, 200


def get_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return {"data": candidate.to_dict()}, 200


def create_candidate():
    data = request.get_json()
    new_candidate = Candidate(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        title=data['title']
    )
    db.session.add(new_candidate)
    db.session.commit()
    return {"data": new_candidate.to_dict()}, 201


def update_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()
    candidate.name = data['name']
    candidate.email = data['email']
    candidate.phone = data['phone']
    candidate.title = data['title']
    db.session.commit()
    return {"data": candidate.to_dict()}, 200


def delete_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    db.session.delete(candidate)
    db.session.commit()
    return '', 204
