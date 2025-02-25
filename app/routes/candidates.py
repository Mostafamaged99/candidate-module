from flask import Blueprint
from app.controllers import candidates as candidate_controller

candidates_api = Blueprint('candidates', __name__, url_prefix='/candidates')


@candidates_api.route('/', methods=['GET'])
def get_all_candidates():
    return candidate_controller.get_all_candidates()


@candidates_api.route('/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    return candidate_controller.get_candidate(candidate_id)


@candidates_api.route('/', methods=['POST'])
def create_candidate():
    return candidate_controller.create_candidate()


@candidates_api.route('/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    return candidate_controller.update_candidate(candidate_id)


@candidates_api.route('/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    return candidate_controller.delete_candidate(candidate_id)
