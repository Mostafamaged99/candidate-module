import flask
import controllers.auth as auth

auth_blp = flask.Blueprint("auth", __name__)


@auth_blp.route("/auth/register", methods=["post"])
def register():
    return auth.RegisterController(flask.request).register()


@auth_blp.route("/auth/login", methods=["post"])
def login():
    return auth.LoginController(flask.request).login()


@auth_blp.route("/users", methods=["GET"])
def read_all():
    return auth.ReadAllUsersController(flask.request).read_all()


@auth_blp.route("/users/<int:user_id>", methods=["GET"])
def read(user_id):
    return auth.ReadUserController(flask.request).read(user_id)


@auth_blp.route("/users/<int:user_id>", methods=["PUT"])
def update(user_id):
    return auth.UpdateUserController(flask.request).update(user_id)


@auth_blp.route("/users/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    return auth.DeleteUserController(flask.request).delete(user_id)
