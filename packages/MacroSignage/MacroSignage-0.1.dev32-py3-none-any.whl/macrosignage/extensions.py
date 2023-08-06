from flask_sqlalchemy import Model, SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table


class MSModel(Model):
    """
    MACRO SIGNAGE MODEL

    This class is used to provide a common interface for all models.

    Args:
        Model: SQLAlchemy model class.

    Returns:
        None
    """

    @declared_attr
    def __tablename__(cls):
        """
        Get the table name for the current model.

        Args:
            cls: The current model class.

        Returns:
            Table name in lowercase.
        """
        return cls.__name__.lower()

    @declared_attr
    def id(cls):
        """
        Primary key.

        Args:
            cls: Class.

        Returns:
            Primary key.
        """
        for base in cls.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                rtype = sa.ForeignKey(base.id, ondelete='CASCADE')
                break
        else:
            rtype = sa.Integer()
        return sa.Column(rtype, primary_key=True)

    @declared_attr
    def created_at(cls):
        """
        Adds created_at column to model.

        Args:
            cls: Class.

        Returns:
            Created column with default value of current timestamp.
        """
        return sa.Column(sa.DateTime, default=sa.func.now())

    @declared_attr
    def updated_at(cls):
        """
        Adds updated_at column to model.

        Args:
            cls: Class.

        Returns:
            Updated column with default value of current timestamp and onupdate value of current timestamp.
        """
        return sa.Column(sa.DateTime, default=sa.func.now(), onupdate=sa.func.now())


db = SQLAlchemy(model_class=MSModel)

extensions = [
    db,
]
