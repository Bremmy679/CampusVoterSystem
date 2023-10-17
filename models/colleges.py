#The model for the students various colleges within the campus

class College(Base):
    __tablename__ = 'colleges'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    location = Column(String(50))
    students = relationship('Student', backref='college', lazy=True)

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __repr__(self):
        return '<College %r>' % self.name