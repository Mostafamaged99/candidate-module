import helpers.exceptions as exceptions
import re
import services.database as crud
import models
import services.token as token
import hashlib
import http
import datetime as datetime


class RegisterController:
    def __init__(self, request):
        self.request = request
        self.body_request = self.request.get_json()

    @property
    def validator(self):
        return _UserValidator()

    @property
    def handler(self):
        return _UserBusinessHandler()

    @property
    def serializer(self):
        return _RegisterSerializer()

    def register(self):
        """
        Validates user data
        Returns: User details and status code
        """
        try:
            self.validator.validate(self.body_request)
            response = self.handler.post(self.body_request)
            return self.serializer.serialize(response), http.HTTPStatus.CREATED
        except exceptions.NotFoundError as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class LoginController:
    def __init__(self, request):
        self.request = request
        self.body_request = request.get_json()

    @property
    def validator(self):
        return _LoginValidator()

    @property
    def handler(self):
        return _LoginBusinessHandler()

    @property
    def serializer(self):
        return _LoginSerializer()

    def login(self):
        try:
            self.serializer.serialize(self.body_request)
            response = self.handler.post(self.body_request)
            return self.serializer.serialize(response), http.HTTPStatus.OK
        except exceptions.NotFoundError as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class UpdateUserController:
    def __init__(self, request):
        self.request = request
        self.body_request = self.request.get_json()
        self.token = self.request.headers.get("Authorization")

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _UserBusinessHandler()

    @property
    def serializer(self):
        return _UserSerializer()

    def update(self, id):
        """
        Update user.
        :Params id: The id for user to update.
        Returns: The updated user.
        """
        try:
            self.validator.validate(self.token)
            response = self.handler.update(id, self.body_request)
            return self.serializer.serialize(response), http.HTTPStatus.OK
        except exceptions.NotFoundError as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class ReadAllUsersController:
    def __init__(self, request):
        self.request = request
        self.body_request = self.request.get_json
        self.token = self.request.headers.get("Authorization")

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _UserBusinessHandler()

    @property
    def serializer(self):
        return _UserSerializer()

    def read_all(self):
        """
        Retreives all users.
        Returns: Users data.
        """
        try:
            self.validator.validate(self.token)
            response = self.handler.get_all()
            return self.serializer.list_serialize(response)
        except exceptions.NotFoundError as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class ReadUserController:
    def __init__(self, request):
        self.request = request
        self.body_request = self.request.get_json
        self.token = self.request.headers.get("Authorization")

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _UserBusinessHandler()

    @property
    def serializer(self):
        return _UserSerializer()

    def read(self, id):
        """
        Retrieves user by id.
        :Params id: The id of user for update.
        Returns: User data.
        """
        try:
            self.validator.validate(self.token)
            response = self.handler.get(id)
            return self.serializer.list_serialize(response)
        except exceptions.NotFoundError as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class DeleteUserController:
    def __init__(self, request):
        self.request = request
        self.body_request = self.request.get_json
        self.token = self.request.headers.get("Authorization")

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _UserBusinessHandler()

    @property
    def serializer(self):
        return _DeleteSerializer()

    def delete(self, id):
        """
        Delete user by id.
        :Params id: The id of user for delete.
        Returns: Success message.
        """
        try:
            self.validator.validate(self.token)
            response = self.handler.delete(id)
            return self.serializer.serialize(response)
        except exceptions.NotFoundError as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerializer().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class _DeleteSerializer:
    def serialize(self, id):
        return {
            "message": f"User id {id} deleted successfully!"
        }


class _UserSerializer:
    def list_serialize(self, users):
        if isinstance(users, list):
            return [self.serialize(user)for user in users]
        return self.serialize(users)

    def serialize(self, user):
        """
        Serialize updated user.
        :Params user: The user data to seriaize.
        """
        return {
            "user": user.id,
            "email": user.email,
            "role": user.role,
            "createdAt": user.created_at,
            "updateddAt": user.updated_at,
        }


class _TokenValidator:
    def __init__(self):
        self.token_service = token.Token()

    def validate(self, token):
        """
        Validates the provided JWT.
        :param token: The JWT to validate.
        :raises exceptions.RequiredInputError: If the token is missing.
        :raises exceptions.InvalidFieldError: If the token is invalid or expired.
        """
        self._is_valid_token(token)

    def _is_valid_token(self, token):
        if not token:
            raise exceptions.RequiredInputError("Token is missing")
        self.token_service.verify_token()


class _LoginSerializer:
    def serialize(self, token):
        """
        Serialize login response
        Returns: Token
        """
        return {
            "token": token,
            "message": f"user logged in successfully!"
        }


class _LoginBusinessHandler:
    def __init__(self):
        self.operator = crud.CrudOperator(models.User)
        self.token = token.Token()

    def post(self, request_body):
        """
        Create token to login
        :Params request_body: The user data to login
        Returns: Token
        """
        email = request_body.get("email")
        encoded_password = request_body.get("password").encode("utf-8")
        role = request_body.get("role")
        user = self.operator.user_filter_data(email=email).first()
        if not user:
            raise exceptions.InvalidFieldError("Email isn't valid")
        hashed_password = hashlib.sha256(encoded_password).hexdigest()
        if hashed_password != user.password:
            raise exceptions.InvalidFieldError("Password isn't valid")
        payload = {
            'user_id': user.id,
            'role': role,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
        }
        token = self.token.create_token(payload)
        return token


class _LoginValidator:
    def validate(self, body):
        """
        Validates login data
        :Params body: The login user data to validate
        Returns: validated data
        """
        self._is_valid_email(body.get("email"))
        self._is_valid_password(body.get("password"))

    def _is_valid_email(self, email):
        if not email:
            raise exceptions.RequiredInputError("Email is required")
        if not re.match(EMAIL_REGEX, email):
            raise exceptions.InvalidFieldError("Email isn't in match")

    def _is_valid_password(self, password):
        if not password:
            raise exceptions.RequiredInputError("Password is required")
        if not re.match(PASSWORD_REGEX, password):
            raise exceptions.InvalidFieldError("Password isn't in match")


class _RegisterSerializer:
    def serialize(self, user):
        """
        Serialize user data
        :Params user: The user data to serialize
        Returns: Serialized format for user
        """
        return {
            "user": user.id,
            "email": user.email,
            "role": user.role,
            "createdAt": user.created_at,
            "updatedAt": user.updated_at,
            "message": f"user id {user.id} registered successfully!"
        }


class _ErrorSerializer:
    def core_error_serialize(self, error, status):
        return self._get_serialized_response(error, status), status

    def _get_serialized_response(self, error, status):
        """
        Serialize error response
        :Params error: The error body
        :Params status: The status code
        Returns: The serialized error
        """
        return {
            "status": status.phrase,
            "description": status.description,
            "message": error.message,
        }


class _UserBusinessHandler:
    def __init__(self):
        self.operator = crud.CrudOperator(models.User)
        self.token = token.Token()

    def post(self, request_body):
        """
        Register user
        :Params request_body: The data for new user
        Returns: The regestered user record
        """
        user_email = request_body.get("email")
        user = self.operator.user_filter_data(email=user_email).first()
        print("User Email:", user_email)
        print("Filtered user:", user)
        print("Creating new user:", request_body)
        if user:
            raise exceptions.InvalidFieldError("User already exsits")
        decoded_password = request_body.get("password").encode("utf-8")
        request_body['password'] = hashlib.sha256(decoded_password).hexdigest()
        new_user = self.operator.create(request_body)
        return new_user

    def update(self, id, request_body):
        """
        Update user by id
        :Params id: The id for user
        :Params request_body: The updated data for user
        Returns: The updated user data
        """
        decoded_password = request_body.get("password")
        if decoded_password:
            hashed_password = hashlib.sha256(decoded_password).hexdigest()
            request_body['password'] = hashed_password
        record = self.operator.update(id, request_body)
        return record

    def delete(self, id):
        """
        Delete user by id
        :Params id: The id for user
        Returns: The deleted record
        """
        record = self.operator.delete(id)
        return record

    def get_all(self):
        """
        Retrieves all users
        Returns: A list of users
        """
        records = self.operator.get_all()
        if not records:
            raise exceptions.NotFoundError("Not found users")
        return records

    def get(self, id):
        """
        Retrieves user by id
        :Params id: The id for user
        Returns: A list of users
        """
        record = self.operator.get_one(id)
        if not record:
            raise exceptions.NotFoundError("Not found user")
        return record


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
PASSWORD_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"


class _UserValidator:
    def __init__(self):
        self.required_attr = ["email", "password", "role"]

    def validate(self, body):
        """
        Validates user data
        :Params body: The user data to validate
        """
        self._check_required(body)
        self._is_valid_email(body.get("email"))

    def _check_required(self, body):
        for attr in self.required_attr:
            if not (body and body.get(attr)):
                raise exceptions.InvalidFieldError(f"{attr} is required")

    def _is_valid_email(self, email):
        if not re.match(EMAIL_REGEX, email):
            raise exceptions.InvalidFieldError("email is not valid")
