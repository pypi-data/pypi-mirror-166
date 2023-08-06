from ..extensions import db


class SQLMixin(object):

    def save(self):
        """
        Save the current instance of the model.

        Args:
            self: The current instance of the model.

        Returns:
            None
        """
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        """
        Update the current instance of the model.

        Args:
            self: The current instance of the model.

        Returns:
            None
        """
        db.session.commit()
        return self

    def delete(self):
        """
        Delete the current instance of the model.

        Args:
            self: The current instance of the model.

        Returns:
            db.session.commit()'s result
        """
        db.session.delete(self)
        return db.session.commit()
