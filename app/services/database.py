from app.models import db
from app.models import Candidate


class DB():
    def __init__(self, model):
        self.model = model

    @staticmethod
    def get_candidates():
        Candidate.query.all()

    @staticmethod
    def get_candidate(candidate_id):
        return Candidate.query.get(candidate_id)

    @staticmethod
    def create_candidate(data):
        try:
            new_candidate = Candidate(
                name=data['name'], age=data['age'], address=data['address'], phone=data['phone'])
            db.session.add(new_candidate)
            db.session.commit()
            return new_candidate
        except:
            return False

    @classmethod
    def delete_candidate(cls, candidate_id):
        try:
            candidate = cls.get_candidate(candidate_id)
            db.session.delete(candidate)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def update_candidate(cls, candidate_id, data):
        try:
            candidate = cls.get_candidate(candidate_id)
            candidate.firstname = data.get('firstname', candidate.firstname)
            candidate.lastname = data.get('lastname', candidate.lastname)
            candidate.email = data.get('email', candidate.email)
            db.session.commit()
            return candidate
        except:
            return False
