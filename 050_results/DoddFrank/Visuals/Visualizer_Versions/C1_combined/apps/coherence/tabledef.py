from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# Local:
#engine = create_engine('sqlite:///apps/coherence/static/users/users.db', echo=True)

# Pythonanywhere:
engine = create_engine('sqlite:////home/RegulatoryComplexity/RegulatoryComplexity/050_results/DoddFrank/Visuals/Visualizer_Versions/C1_combined/apps/coherence/static/users/users.db', echo=True)

Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    afiliation = Column(String)
    authenticated = Column(Boolean, default=False)

    #----------------------------------------------------------------------
    def __init__(self, username, password, email,afiliation, authenticated):
        """"""
        self.username = username
        self.password = password
        self.email = email
        self.afiliation = afiliation
        self.authenticated = authenticated

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False



# create tables
Base.metadata.create_all(engine)
