#The base model where all the other models inherit from
from flask import  session, declarative_base

Base = declarative_base()

class BaseModel():

    def __init__(self):
        self.session = session
        
    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()
