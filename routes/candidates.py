import flask as flask
import controllers.candidates as candidate

candidate_blp = flask.Blueprint("candidate", __name__)


@candidate_blp.route("/candidates", methods=["POST"])
def add_candidate():
    return candidate.AddCandidateController(flask.request).create()


@candidate_blp.route("/candidates", methods=["GET"])
def get_candidates():
    return candidate.ReadAllCandidatesController(flask.request).read_all()


@candidate_blp.route("/candidates/<int:candidate_id>", methods=["GET"])
def get_candidate(candidate_id):
    return candidate.ReadCandidateController(flask.request).read(candidate_id)


@candidate_blp.route("/candidates/<int:candidate_id>", methods=["PUT"])
def update_candidate(candidate_id):
    return candidate.UpdateCandidateController(flask.request).update(candidate_id)


@candidate_blp.route("/candidates/<int:candidate_id>", methods=["DELETE"])
def delete_candidate(candidate_id):
    return candidate.DeleteCandidateController(flask.request).delete(candidate_id)
