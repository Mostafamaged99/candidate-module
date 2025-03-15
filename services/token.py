import jwt
import extensions
import flask
import helpers.exceptions as exception


class Token:
    def create_token(self, paylod):
        """
        Creates a JWT token
        :Params paylod: The data to encode with the token
        :Return: return a JWT encoded token
        """
        token = jwt.encode(
            paylod, extensions.app.config["JWT_SECRET_KEY"], algorithm="HS256")
        return token

    def verify_token(self):
        """
        Verify JWT token
        :Return: The decoded token payload
        :Raise: If token is expired or invalid
        """
        try:
            auth_header = flask.request.headers.get("Authorization")
            if not auth_header:
                raise exception.InvalidFieldError("Authorization header is missing")
        
            # Assuming the header is in the format "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise exception.InvalidFieldError("Authorization header must be in the format 'Bearer <token>'")
        
            token = parts[1]
            return jwt.decode(token, extensions.app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exception.InvalidFieldError("Token has expired")
        except jwt.InvalidTokenError:
            raise exception.InvalidFieldError("Token is invalid")

