from typing import Dict

from twitter_app.models.user import User


class UserStore:
    """Database wrapper."""

    def __init__(self, db):
        """Constructor.

        Args:
            db: SQLAlchemy - database object
        """
        self.__db = db

    def create_user(self, user_json: Dict) -> User:
        """Create a user given json data for it.

        Args:
            user_json: Dict - json with user specific data
        """
        return User(
            id=user_json["id"],
            name=user_json["name"],
            screen_name=user_json["screen_name"],
            number_of_followers=user_json["followers_count"],
        )

    def upsert(self, user: User):
        """Update or insert a user into the database.

        Args:
            user: User - user object to update or insert.
        """
        existing_user = User.query.filter_by(id=user.id).first()
        if existing_user:
            self.__db.session.delete(existing_user)
        self.__db.session.add(user)
        self.__db.session.commit()
