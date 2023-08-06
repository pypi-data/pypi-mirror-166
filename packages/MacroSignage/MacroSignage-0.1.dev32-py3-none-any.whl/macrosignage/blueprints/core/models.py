from slugify import slugify

from macrosignage.extensions import db
from macrosignage.utils.sql import SQLMixin
from macrosignage.utils import generate_random_string, allowed_file, \
    get_file_extension


class Display(SQLMixin, db.Model):
    """
    Display Model.

    Args:
        db.Model: SQLAlchemy model class.
        SQLMixin: SQL mixin class.

    Returns:
        None
    """
    __tablename__ = 'displays'

    public_key = db.Column(db.String(10))
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    slides = db.relationship('Slide', backref='display', lazy='dynamic')

    @staticmethod
    def insert_default_displays():
        """
        Insert default displays.

        Args:
            None

        Returns:
            None
        """
        displays = [
            {
                'name': 'Default',
                'description': 'Default display.',
            }
        ]
        for display in displays:
            Display(**display).save()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.public_key is None:
            self.public_key = generate_random_string(8)


class Slide(SQLMixin, db.Model):
    """
    Slide Model.
    Args:
        SQLMixin: SQL mixin class.
        db.Model: SQLAlchemy model class.
    Returns:
        None
    """
    __tablename__ = 'slides'

    public_key = db.Column(db.String(32), unique=True)
    background = db.Column(db.String(120))
    foreground = db.Column(db.String(120))
    title = db.Column(db.String(20))
    show_logo = db.Column(db.Boolean, default=True)
    display_id = db.Column(db.Integer, db.ForeignKey('displays.id'))

    @staticmethod
    def generate_public_key():
        """
        Generate public key.
        Args:
            None
        Returns:
            str: Public key.
        """
        return generate_random_string(32)

    def __init__(self, **kwargs):
        super(Slide, self).__init__(**kwargs)

        if self.public_key is None:
            self.public_key = generate_random_string(12)

        if self.background:
            self.background = slugify(
                self.public_key) + '.' + get_file_extension(
                self.background)

        if self.foreground:
            self.foreground = slugify(
                self.public_key) + '.' + get_file_extension(
                self.foreground)
