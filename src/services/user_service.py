import bcrypt
import jwt
from datetime import datetime, timedelta
from src.database.user_model import UserModel
from src.config import JWT_SECRET, JWT_ALGORITHM

class UserService:
    def __init__(self, db_session):
        """
        Initialize the UserService with a database session.
        :param db_session: Database session for interacting with the user model.
        """
        self.db_session = db_session

    def create_user(self, username, email, password):
        """
        Create a new user in the database.
        :param username: Username of the user.
        :param email: Email of the user.
        :param password: Plain text password of the user.
        :return: Created user object or None if the user already exists.
        """
        existing_user = self.db_session.query(UserModel).filter_by(email=email).first()
        if existing_user:
            return None  # User already exists

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = UserModel(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def authenticate_user(self, email, password):
        """
        Authenticate a user using email and password.
        :param email: Email of the user.
        :param password: Plain text password of the user.
        :return: JWT token if authentication is successful, None otherwise.
        """
        user = self.db_session.query(UserModel).filter_by(email=email).first()
        if not user:
            return None

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = self._generate_jwt_token(user)
            return token
        return None

    def update_user_profile(self, user_id, username=None, email=None, password=None):
        """
        Update the user's profile information.
        :param user_id: ID of the user to update.
        :param username: New username (optional).
        :param email: New email (optional).
        :param password: New password (optional).
        :return: Updated user object or None if user does not exist.
        """
        user = self.db_session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return None

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user.updated_at = datetime.utcnow()
        self.db_session.commit()
        return user

    def get_user_by_id(self, user_id):
        """
        Retrieve a user by their ID.
        :param user_id: ID of the user.
        :return: User object or None if user does not exist.
        """
        return self.db_session.query(UserModel).filter_by(id=user_id).first()

    def get_user_by_email(self, email):
        """
        Retrieve a user by their email.
        :param email: Email of the user.
        :return: User object or None if user does not exist.
        """
        return self.db_session.query(UserModel).filter_by(email=email).first()

    def _generate_jwt_token(self, user):
        """
        Generate a JWT token for the authenticated user.
        :param user: User object.
        :return: JWT token as a string.
        """
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=7)  # Token valid for 7 days
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token

    def delete_user(self, user_id):
        """
        Delete a user from the database.
        :param user_id: ID of the user to delete.
        :return: True if deletion was successful, False otherwise.
        """
        user = self.db_session.query(UserModel).filter_by(id=user_id).first()
        if not user:
            return False

        self.db_session.delete(user)
        self.db_session.commit()
        return True