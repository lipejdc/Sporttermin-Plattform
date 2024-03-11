import json  # Import JSON library for data interchange.
# Import custom ORM (Object-Relational Mapping) module for database interactions.
import dbclasses as ORM
# Import specific ORM classes.
from dbclasses import User, Appointment, Comment, Friendzone, FriendzoneInvitation
# Import select function from SQLAlchemy for querying the database.
from sqlalchemy import select
from datetime import datetime  # Import datetime for handling date and time.
# Import MIMEMultipart for constructing email messages.
from email.mime.multipart import MIMEMultipart
# Import MIMEText for adding text content to emails.
from email.mime.text import MIMEText
import smtplib  # Import smtplib for sending emails via SMTP.
import secrets  # Import secrets for generating secure tokens.
 
# Ensure the database exists before starting the application.
ORM.create_db_if_not_exists()
 
 
# Function to retrieve user information by ID, email, or password.
def user_get(id: str = "", email: str = "", passwd: str = "") -> set:
    with ORM.get_session() as session:
        if id != "":
            user = session.scalars(select(User).where(User.id == id)).first()
 
            if user:
                return json.dumps(user.to_dict())
 
        elif email != "" and passwd != "":
            user = session.scalars(select(User).where(
                User.email == email).where(User.passwd == passwd)).first()
 
            if user:
                return json.dumps(user.to_dict())
        elif email != "":
            user = session.scalars(
                select(User).where(User.email == email)).first()
 
            if user:
                return json.dumps(user.to_dict())
        else:
            users = session.scalars(select(User)).all()
 
            users_list = []
            for user in users:
                users_list.append(user.to_dict())
 
            return json.dumps(users_list)
 
        return ("[]")
 
 
# Function to update existing user information in the database.
def user_update(id: str, first_name: str, last_name: str, email: str, passwd: str, age: int, city: str):
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).first()
 
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.passwd = passwd
            user.age = age
            user.city = city
 
            session.commit()
 
            return json.dumps(user.to_dict())
 
    return ("{}")
 
# Function to create a new user in the database.
 
 
def user_create(first_name: str, last_name: str, email: str, passwd: str, age: int, city: str):
    with ORM.get_session() as session:
        user = User()
 
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.passwd = passwd
            user.age = age
            user.city = city
 
            session.add(user)
            session.commit()
 
            return json.dumps(user.to_dict())
 
    return ("{}")
 
# Function to delete a user from the database by their ID.
 
 
def user_delete(id: str):
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).first()
 
        if (user):
            session.delete(user)
            session.commit()
            return ("{}")
        else:
            return ("{}")
 
# Function to retrieve friendzone(s) information by user ID or friendzone ID.
 
 
def fz_get(user_id: str, fz_id: str = "") -> str:
    with ORM.get_session() as session:
        if fz_id != "":
            fz = session.scalars(select(Friendzone).where(
                Friendzone.id == fz_id)).first()
 
            if fz:
                return json.dumps(fz.to_dict())
 
        elif user_id != "":
            user = session.scalars(
                select(User).where(User.id == user_id)).first()
 
            if user:
                fzs = user.friendzones
 
                if fzs and len(fzs) > 0:
                    fzs_list = []
 
                    for fz in fzs:
                        fzs_list.append(fz)
 
                    return json.dumps(fzs_list)
 
        return ("[]")
 
# Function to create a new friendzone and associate it with a user.
 
 
def fz_create(user_id: int, name: str) -> str:
    with ORM.get_session() as session:
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return "Benutzer nicht gefunden."
 
            # Erstelle eine neue Friendzone
            new_friendzone = Friendzone(name=name, creator_id=user_id)
 
            # Füge den Benutzer der Friendzone hinzu
            new_friendzone.users.append(user)
 
            # Speichere die Friendzone und die Beziehung in der Datenbank
            session.add(new_friendzone)
            session.commit()
 
            return f"Benutzer {user_id} wurde erfolgreich zur Friendzone '{name}' hinzugefügt."
 
        except Exception as e:
            session.rollback()
            return f"Ein Fehler ist aufgetreten: {str(e)}"
        finally:
            session.close()
 
# Function to update the name of an existing friendzone.
 
 
def fz_update(fz_id: str, name) -> str:
    with ORM.get_session() as session:
        if fz_id and fz_id != "":
            fz = session.scalars(select(Friendzone).where(
                Friendzone.id == fz_id)).first()
 
            if fz:
                fz.name = name
 
                session.commit()
 
                return json.dumps(fz.to_dict())
 
        return ("{}")
 
# Function to delete a friendzone from the database by its ID.
 
 
def fz_delete(fz_id: str = "") -> str:
    with ORM.get_session() as session:
        fz = session.scalars(select(Friendzone).where(
            Friendzone.id == fz_id)).first()
 
        if (fz):
            session.delete(fz)
            session.commit()
            return ("{}")
        else:
            return ("{}")
 
# Function to retrieve appointment(s) information by user ID or appointment ID.
 
 
def apt_get(user_id: str, apt_id: str = "") -> str:
    with ORM.get_session() as session:
        print(f"\tIn apt_get with user_id: {user_id} and apt_id: {apt_id}")
        if apt_id != "":
            apt = session.scalars(select(Appointment).where(
                Appointment.id == apt_id)).first()
 
            if apt:
                return json.dumps(apt.to_dict())
 
        elif user_id != "":
            print("\tIn apt_get in has user_id")
            user = session.scalars(
                select(User).where(User.id == user_id)).first()
            print("\tFound User!")
            if user:
                apts = user.appointments
 
                if apts and len(apts) > 0:
                    apts_list = []
 
                    for apt in apts:
                        apts_list.append(apt)
 
                    return json.dumps(apts_list)
 
        return ("[]")
 
# Function to create a new appointment and associate it with a user and possibly a friendzone.
 
 
def apt_create(user_id: str, name: str, date: datetime, time_start: str, time_stop: str, citycode: int, city: str, street: str, house_nr: str, maxUser: int, notice: str, friendzone_id: str) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).first()
        fz = session.scalars(select(Friendzone).where(
            Friendzone.id == friendzone_id)).first()
 
        if user:
            apt = Appointment()
            apt.creator = user.id
            apt.name = name
            apt.date = date
            apt.time_start = time_start
            apt.time_stop = time_stop
            apt.citycode = citycode
            apt.city = city
            apt.street = street
            apt.house_nr = house_nr
            apt.maxUser = maxUser
            apt.notice = notice
 
            user.appointments.append(apt)
            fz.appointments.append(apt)
 
            session.commit()
 
            return json.dumps(apt.to_dict())
 
    return ("{}")
 
# Function to update existing appointment information in the database.
 
 
def apt_update(apt_id: str, name: str, date: datetime, time_start: str, time_stop: str, citycode: int, city: str, street: str, house_nr: str, maxUser: int, notice: str) -> str:
    with ORM.get_session() as session:
        if apt_id and apt_id != "":
            apt = session.scalars(select(Appointment).where(
                Appointment.id == apt_id)).first()
 
            if apt:
                apt.date = date
                apt.time_start = time_start
                apt.time_stop = time_stop
                apt.citycode = citycode
                apt.city = city
                apt.street = street
                apt.house_nr = house_nr
                apt.maxUser = maxUser
                apt.notice = notice
 
                session.commit()
 
                return json.dumps(apt.to_dict())
 
        return ("{}")
 
# Function to delete an appointment from the database by its ID.
 
 
def apt_delete(apt_id: str = "") -> str:
    with ORM.get_session() as session:
        apt = session.scalars(select(Appointment).where(
            Appointment.id == apt_id)).first()
 
        if (apt):
            session.delete(apt)
            session.commit()
            return ("{}")
        else:
            return ("{}")
 
# Function to retrieve comment(s) information by user ID, appointment ID, or comment ID.
 
 
def comment_get(user_id: str = "", apt_id: str = "", comment_id: str = "") -> str:
    with ORM.get_session() as session:
        if comment_id != "":
            comment = session.scalars(select(Comment).where(
                Comment.id == comment_id)).first()
 
            if comment:
                return json.dumps(comment.to_dict())
 
        elif user_id != "":
            user = session.scalars(
                select(User).where(User.id == user_id)).first()
 
            if user:
                comments = user.comments
 
                if comments and len(comments) > 0:
                    comments_list = []
 
                    for comment in comments:
                        comments_list.append(comment)
 
                    return json.dumps(comments_list)
        elif apt_id != "":
            apt = session.scalars(select(Appointment).where(
                Appointment.id == apt_id)).first()
 
            if apt:
                comments = apt.comments
 
                if comments and len(comments) > 0:
                    comments_list = []
 
                    for comment in comments:
                        comments_list.append(comment)
 
                    return json.dumps(comments_list)
 
        return ("{}")
 
# Function to create a new comment and associate it with a user and an appointment.
 
 
def comment_create(user_id: str, apt_id: str, timestamp: str, comment_value) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).first()
        apt = session.scalars(select(Appointment).where(
            Appointment.id == apt_id)).first()
 
        if user and apt:
            comment = Comment()
            comment.appointment_id = apt.id
            comment.user_id = user.id
            comment.timestamp = timestamp
            comment.comment_value = comment_value
 
            user.Comments.append(comment)
 
            session.commit()
 
            return json.dumps(comment.to_dict())
 
    return ("{}")
 
# Function to update existing comment information in the database.
 
 
def comment_update(user_id: str, apt_id: str, timestamp: str, comment_value) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).first()
        apt = session.scalars(select(Appointment).where(
            Appointment.id == apt_id)).first()
 
        if user and apt:
            comment = Comment()
            comment.appointment_id = apt.id
            comment.user_id = user.id
            comment.timestamp = timestamp
            comment.comment_value = comment_value
 
            user.Comments.append(comment)
 
            session.commit()
 
            return json.dumps(comment.to_dict())
 
    return ("{}")
 
# Function to delete a comment from the database by its ID.
 
 
def comment_delete(comment_id: str = "") -> str:
    with ORM.get_session() as session:
        comment = session.scalars(select(Comment).where(
            Comment.id == comment_id)).first()
 
        if (comment):
            session.delete(comment)
            session.commit()
            return ("{}")
        else:
            return ("{}")
 
# Function to handle the process of creating and sending an invitation to join a friendzone.
 
 
def create_and_send_invitation(friendzone_id, user_email):
    with ORM.get_session() as session:
        friendzone = session.scalars(
            select(Friendzone).where(Friendzone.id == friendzone_id)).first()
        friendzone_name = friendzone.name
 
    token = generate_secure_token()
    save_invitation_to_db(friendzone_id, user_email, token)
    send_invitation_email(user_email, friendzone_name, token, friendzone_id)
 
# Utility function to generate a secure token for friendzone invitations.
 
 
def generate_secure_token():
    return secrets.token_urlsafe()
 
# Utility function to save a friendzone invitation to the database.
 
 
def save_invitation_to_db(friendzone_id, user_email, token):
    new_invitation = FriendzoneInvitation(
        friendzone_id=friendzone_id,
        user_email=user_email,
        token=token,
        accepted=False
    )
    with ORM.get_session() as session:
        session.add(new_invitation)
        session.commit()
        return new_invitation
 
# Function to construct and send an email invitation for a friendzone.
 
 
def send_invitation_email(user_email, friendzone_name, token, friendzone_id):
    msg = MIMEMultipart()
    msg['From'] = 'SportApp.Service@gmail.com'
    msg['To'] = user_email
    msg['Subject'] = f'Einladung zur Friendzone: {friendzone_name}'
 
    # TODO: Server anpassen, falls es gehostet wird.
    body = (f'Klicke auf diesen Link, um der Friendzone "{friendzone_name}" beizutreten: '
            f'https://http://127.0.0.1:8000/accept-invitation?token={token}&friendzone_id={friendzone_id}')
    msg.attach(MIMEText(body, 'plain'))
 
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login('SportApp.Service@gmail.com', 'fnaedvabprtufixc')
    smtpserver.sendmail('SportApp.Service@gmail.com',
                        user_email, msg.as_string())
 
# Function to validate an invitation token and add the user to the corresponding friendzone.
 
 
def check_token_fz(token):
    with ORM.get_session() as session:
        invitation = session.query(
            FriendzoneInvitation).filter_by(token=token).first()
        if not invitation or invitation.accepted:
            return 'Ungültige oder bereits akzeptierte Einladung.'
 
        user = session.query(User).filter_by(
            email=invitation.user_email).first()
        if not user:
            return 'Benutzer nicht gefunden.'
 
        # Finde die zugehörige Friendzone
        friendzone = session.query(Friendzone).filter_by(
            id=invitation.friendzone_id).first()
        if not friendzone:
            return 'Friendzone nicht gefunden.'
 
        # Überprüfe, ob der Benutzer bereits Mitglied der Friendzone ist
        if user in friendzone.users:
            return 'Benutzer ist bereits Mitglied der Friendzone.'
 
        # Füge den Benutzer zur Friendzone hinzu
        friendzone.users.append(user)
        invitation.accepted = True  # Markiere die Einladung als angenommen
        session.commit()
 
        return 'Du wurdest erfolgreich zur Friendzone hinzugefügt!'