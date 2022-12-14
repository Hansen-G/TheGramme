from email.policy import default
from .db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
from .following import follows
from .comments_likes import CommentsLikes
from .images_likes import Imageslikes
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(64), nullable=False)
    profile_img = db.Column(db.String(1000), nullable=True, default='https://res.cloudinary.com/hansenguo/image/upload/v1660950302/TheGramme/user_yiqxol.png')
    website = db.Column(db.String(64), nullable=True)
    bio = db.Column(db.String(150), nullable=True)
    phone_number = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(50), nullable=True)
    public = db.Column(db.Boolean, nullable=False, default=True)
    createdAt = db.Column(db.DateTime(timezone=True), nullable=True, server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=func.now())


    images = db.relationship("Image", back_populates="user", cascade="all, delete-orphan")
    # images = db.relationship("Image", back_populates="user")
    images_likes = db.relationship(
        "Image",
        secondary=Imageslikes,
        back_populates="user_image_likes",
        # cascade="all,delete"
    )

    comments = db.relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    # comments = db.relationship("Comment", back_populates="user")

    comments_likes = db.relationship(
        "Comment",
        secondary=CommentsLikes,
        back_populates="user_comment_likes",
        # cascade="all, delete"
    )

    followers = db.relationship(
        "User",
        secondary=follows,
        primaryjoin=(follows.c.follower_id == id),
        secondaryjoin=(follows.c.following_id == id),
        # cascade="all, delete",
        backref=db.backref("following", lazy="dynamic"),
        lazy="dynamic"
    )

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "email": self.email,
            "following": [{"following_id": i.id, "username": i.name, "profile_img": i.profile_img} for i in self.followers],
            "followers": [{"follower_id": i.id, "username": i.name, "profile_img": i.profile_img} for i in self.following],
            "profile_img": self.profile_img,
            "bio": self.bio,
            "gender": self.gender,
            "website": self.website
        }

    @property
    def for_following(self):
        return {
            "following": [i.id for i in self.followers]
        }
