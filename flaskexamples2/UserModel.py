from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)

    def __repr__(self):
        return str({
            'username':self.username,
            'password':self.password
        })

    def username_password_match(param_username,param_user_password):
        user = User.query.filter_by(username=param_username).filter_by(password=param_user_password).first()
        return user is not None


    def get_all_users():
        return User.query.all()


    def create_user(param_user_name,param_user_password):
        new_user = User(username=param_user_name,password=param_user_password)
        db.session.add(new_user)
        db.session.commit()
