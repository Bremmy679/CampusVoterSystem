#The database model for the application

#The declarative base for  the database

Base = declarative_base()

#The User model

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50), unique=True)
    password = Column(String(50))
    is_admin = Column(Boolean, default=False)
    is_voted = Column(Boolean, default=False)

    def __init__(self, firstname, lastname, email, password, is_admin=False, is_voted=False):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_voted = is_voted

    def __repr__(self):
        return '<User %r>' % self.email