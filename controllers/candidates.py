from sqlalchemy.exc import IntegrityError
import helpers.exceptions as exceptions
import http
import services.database as crud
import models
import re
import services.token as token


class AddCandidateController:
    def __init__(self, test_request=None):
        self.request = test_request
        self.body_request = self.request.get_json()
        self.token = self.request.headers.get('Authorization')

    @property
    def validator(self):
        return _AddCandidateValidator()

    @property
    def handler(self):
        return _CandidateBusinessHandler()

    @property
    def serializer(self):
        return _CandidateSerializer()

    def create(self):
        """
        Validates input and creates a new candidate.
        Returns: Repersents the candidate details and status code
        """
        try:
            self.validator.validate(self.token, self.body_request)
            response = self.handler.post(self.body_request)
            return self.serializer.serialize_list(response), http.HTTPStatus.CREATED
        except exceptions.NotFoundError as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError, exceptions.DuplicateFieldError, exceptions.DatabaseIntegrityError) as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class UpdateCandidateController:
    def __init__(self, request):
        self.request = request
        self.body_request = self.request.get_json()
        self.token = self.request.headers.get('Authorization')

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _CandidateBusinessHandler()

    @property
    def serializer(self):
        return _CandidateSerializer()

    def update(self, id):
        """
        Validates input and update candidate
        :param id: The id of the candidate to update
        Returns: Represents the candidate details and status code
        """
        try:
            self.validator.validate(self.token)
            response = self.handler.update(id, self.body_request)
            return self.serializer.serialize_list(response), http.HTTPStatus.OK
        except exceptions.NotFoundError as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError, exceptions.DuplicateFieldError) as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class ReadAllCandidatesController:
    def __init__(self, request):
        self.request = request
        self.token = self.request.headers.get('Authorization')

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _CandidateBusinessHandler()

    @property
    def serializer(self):
        return _CandidateSerializer()

    def read_all(self):
        """
        Validates token and retrieves all candidates.
        Returns: Represents all candidates details and status code
        """
        try:
            self.validator.validate(self.token)
            response = self.handler.get_all()
            return self.serializer.serialize_list(response), http.HTTPStatus.OK
        except exceptions.NotFoundError as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError, exceptions.DuplicateFieldError) as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


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


class ReadCandidateController:
    def __init__(self, request):
        self.request = request
        self.token = self.request.headers.get("Authorization")

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _CandidateBusinessHandler()

    @property
    def serializer(self):
        return _CandidateSerializer()

    def read(self, id):
        """
        Validates token and retrieves a candidate data by Id
        :Params id: The id of the candidates to retrieve
        Returns: Represents candidate data and status code
        """
        try:
            self.validator.validate(self.token)
            response = self.handler.get(id)
            return self.serializer.serialize_list(response)
        except exceptions.NotFoundError as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)


class DeleteCandidateController:
    def __init__(self, request):
        self.request = request
        self.token = self.request.headers.get('Authorization')

    @property
    def validator(self):
        return _TokenValidator()

    @property
    def handler(self):
        return _CandidateBusinessHandler()

    @property
    def serializer(self):
        return _DeleteSerializer()

    def delete(self, id):
        try:
            self.validator.validate(self.token)
            response = self.handler.delete(id)
            return self.serializer.serialize_list(response)
        except exceptions.NotFoundError as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.NOT_FOUND)
        except (exceptions.InvalidFieldError, exceptions.RequiredInputError) as exp:
            return _ErrorSerialize().core_error_serialize(exp, http.HTTPStatus.BAD_REQUEST)

# BusinessHandler


class _CandidateBusinessHandler:
    def __init__(self, candidate_test=None, token_test=None):
        self.operator = candidate_test or crud.CrudOperator(
            models.Candidate)
        # self.token = token_test or tk.Token()

    def post(self, request_body):
        """
        Creates a new candidate.
        :param request_body: The data for the new candidate.
        :return: The created candidate record.
        """
        # token = self.token.verify_token()
        # self.operator.get_one(token['user_id'])
        record = self.operator.create(request_body)
        return record

    def update(self, id, request_body):
        """
        Updates a candidate by ID.
        :param id: The ID of the candidate to update.
        :param request_body: The updated data for the candidate.
        :return: The updated candidate record.
        """
        # token = self.token.verify_token()
        # self.operator.get_one(token['user_id'])
        record = self.operator.update(id, request_body)
        return record

    def get_all(self):
        """
        Retrieves all candidates.
        :return: A list of candidate records.
        """
        # token = self.token.verify_token()
        # self.operator.get_one(token['user_id'])
        records = self.operator.get_all()
        if not records:
            raise exceptions.NotFoundError("Records does not exist")
        return records

    def get(self, _id):
        """
        Retrieves a candidate by ID.
        :param _id: The ID of the candidate to retrieve.
        :return: The candidate record.
        """
        # token = self.token.verify_token()
        # self.operator.get_one(token['user_id'])
        record = self.operator.get_one(_id)
        if not record:
            raise exceptions.NotFoundError("Record does not exist")
        return record

    def delete(self, id):
        """
        Deletes a candidate by ID.
        :param id: The ID of the candidate to delete.
        :return: The deleted candidate record.
        """
        # token = self.token.verify_token()
        # self.operator.get_one(token['user_id'])
        record = self.operator.delete(id)
        return record


# Validation
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


class _AddCandidateValidator:
    def validate(self, token, body):
        """
        Validates the token and candidate data.
        :param token: The user token.
        :param body: The candidate data to validate.
        """
        self.is_valid_token(token)
        self.is_valid_name(body.get("name"))
        self.is_valid_email(body.get("email"))
        self.is_valid_phone(body.get("phone"))
        self.is_valid_title(body.get("title"))

    def is_valid_token(self, token):
        if not token:
            raise exceptions.RequiredInputError("token is missing")

    def is_valid_name(self, name):
        if not name:
            raise exceptions.RequiredInputError("name is required")
        self._is_valid_name(name)

    def _is_valid_name(self, name):
        if not isinstance(name, str):
            raise exceptions.InvalidInputError("name is not valid string")

    def is_valid_title(self, title):
        if not title:
            raise exceptions.RequiredInputError("title is required")
        self._is_valid_title(title)

    def _is_valid_title(self, title):
        if not isinstance(title, str):
            raise exceptions.InvalidInputError("title is not valid int")

    def is_valid_email(self, email):
        if not email:
            raise exceptions.RequiredInputError("email is required")
        self._is_valid_email(email)

    def _is_valid_email(self, email):
        if not re.match(EMAIL_REGEX, email):
            raise exceptions.InvalidInputError("email is not valid")

    def is_valid_phone(self, phone):
        if not phone:
            raise exceptions.RequiredInputError("phone is required")
        self._is_valid_phone(phone)

    def _is_valid_phone(self, phone):
        if not isinstance(phone, str):
            raise exceptions.InvalidInputError("phone must be a string number")

# serializer


class _DeleteSerializer:
    def serialize(self, id):
        return {
            "message": f"User id {id} deleted successfully!"
        }


class _CandidateSerializer:
    def serialize_list(self, candidate):
        if not candidate:
            return []
        if isinstance(candidate, list):
            return [self.serialize(user) for user in candidate]
        return self.serialize(candidate)

    def serialize(self, candidate):
        """
        Serializes a candidate.
        :param candidate: The candidate to serialize.
        :return: Serialized candidate data.
        """
        return {
            "id": candidate.id,
            "name": candidate.name,
            "title": candidate.title,
            "email": candidate.email,
            "phone": candidate.phone,
            "created_at": candidate.created_at,
            "updated_at": candidate.updated_at,
            # "skills": ", ".join(skill.name for skill in candidate.skills),
            # "degree": ", ".join(education.degree for education in candidate.education),
            # "graduation_year": ", ".join(str(education.graduation_year) for education in candidate.education),
            # "institution": ", ".join(education.institution for education in candidate.education),
            # "company": ", ".join(experience.company for experience in candidate.experience),
            # "position": ", ".join(experience.position for experience in candidate.experience),
            # "start_date": ", ".join(experience.start_date for experience in candidate.experience),
            # "end_date": ", ".join(experience.end_date for experience in candidate.experience),
            # "date": ", ".join(applications.date for applications in candidate.applications),
        }

# ErrorSerialize


class _ErrorSerialize:
    def core_error_serialize(self, error, status):
        return self._get_serialized_response(error, status), status

    def _get_serialized_response(self, error, status):
        """
        Serializes an error response.
        :param error: The error to serialize.
        :param status: The HTTP status code.
        :return: Serialized error response.
        """
        return {
            "status": status.phrase,
            "description": status.description,
            "message": error.message,
        }
