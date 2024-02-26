from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey, Boolean, Table, create_engine
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import uuid

Base = declarative_base()

gEngine = None

# Association tables
user_appointment = Table(
    'user_appointment', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id')),
    Column('appointment_id', UUID(as_uuid=True), ForeignKey('appointment.id')),
    Column('status', Boolean)
)

user_friendzone = Table(
    'user_friendzone', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id')),
    Column('friendzone_id', UUID(as_uuid=True), ForeignKey('friendzone.id')),
    Column('status', Boolean)
)

# ORM-Classes


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    passwd = Column(String(256))  # Für gehashte Passwörter
    gender = Column(Integer)
    age = Column(Integer, nullable=False)
    city = Column(String(100))

    appointments = relationship(
        'Appointment', secondary=user_appointment, back_populates='users')
    comments = relationship('Comment', back_populates='user')
    friendzones = relationship(
        'Friendzone', secondary=user_friendzone, back_populates='users')

    def to_dict(self):
        return {
            "id": str(self.id),  # UUID in String konvertieren
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "gender": self.gender,
            "age": self.age,
            "city": self.city,
        }


class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    creator_id = Column(UUID(as_uuid=True),
                        ForeignKey('user.id'), nullable=False)
    name = Column(String(200), nullable=False)
    date = Column(DateTime)
    time_start = Column(DateTime)
    time_end = Column(DateTime)
    citycode = Column(Integer)
    city = Column(String(100))
    max_user = Column(Integer)
    notice = Column(String(500))

    users = relationship('User', secondary=user_appointment, back_populates='appointments')
    comments = relationship('Comment', back_populates='appointment')


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey('appointment.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    timestamp = Column(DateTime)  # Geändert zu DateTime
    comment_value = Column(String(250))

    user = relationship('User', back_populates='comments')
    appointment = relationship('Appointment', back_populates='comments')


class Friendzone(Base):
    __tablename__ = 'friendzone'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200))
    creator_id = Column(UUID(as_uuid=True),
                        ForeignKey('user.id'), nullable=False)

    users = relationship('User', secondary=user_friendzone, back_populates='friendzones')


def create_db_if_not_exists():
    # Hier setzt du den korrekten Connection String für deine MSSQL-Datenbank ein
    connection_string = "sqlite:///test.sqlite"
    engine = create_engine(connection_string, echo=True)

    # Überprüfe, ob die Datenbank existiert
    if not database_exists(engine.url):
        # Erstelle die Datenbank, wenn sie nicht existiert
        create_database(engine.url)
        print("Datenbank wurde erstellt.")

        # Hier wird die Datenbank mit den Tabellen aus dbclasses.py initialisiert
        Base.metadata.create_all(engine)
        print("Tabellen wurden erstellt.")
    else:
        print("DB exists")
        
    global gEngine
    gEngine = engine


def get_session():
    global gEngine
    if gEngine != None:
        return Session(gEngine)
    else:
        connection_string = "sqlite:///test.sqlite"
        engine = create_engine(connection_string, echo=True)
        
        gEngine = engine
        
        return Session(gEngine)