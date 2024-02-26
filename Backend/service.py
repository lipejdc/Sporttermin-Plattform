import json
import dbclasses as ORM
from dbclasses import User, Appointment, Comment, Friendzone
from sqlalchemy import select
from datetime import datetime

ORM.create_db_if_not_exists()

def user_get(id: str = "", email: str = "", passwd:str = "") -> set:
    with ORM.get_session() as session:
        if id != "":
            user = session.scalars(select(User).where(User.id == id)).first()
            
            if user:
                return json.dumps(user.to_dict())
            
        elif email != "" and passwd != "":
            user = session.scalars(select(User).where(User.email == email).where(User.passwd == passwd)).first()
            
            if user:
                return json.dumps(user.to_dict())
        else:
            users = session.scalars(select(User)).all()
        
            users_list = []
            for user in users:
                users_list.append(user.to_dict())
                
            return json.dumps(users_list)
            
        return ("[]")


def user_update(id: str, first_name: str, last_name: str, email: str, passwd: str, gender: int, age: int, city: str):
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).first()
        
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.passwd = passwd
            user.gender = gender
            user.age = age
            user.city = city
            
            session.commit()
            
            return json.dumps(user.to_dict())
            
    return ("{}")


def user_create(first_name: str, last_name: str, email: str, passwd: str, gender: int, age: int, city: str):
    with ORM.get_session() as session:
        user = User()
        
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.passwd = passwd
            user.gender = gender
            user.age = age
            user.city = city
            
            session.add(user)
            session.commit()
            
            return json.dumps(user.to_dict())
            
    return ("{}")


def user_delete(id: str):
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).first()
        
        if(user):
            session.delete(user)
            session.commit()
            return ("{}")
        else:
            return ("{}")


def fz_get(user_id: str, fz_id: str = "") -> str:
    with ORM.get_session() as session:
        if fz_id != "":
            fz = session.scalars(select(Friendzone).where(Friendzone.id == fz_id)).first()
            
            if fz:
                return json.dumps(fz.to_dict())
            
        elif user_id != "":
            user = session.scalars(select(User).where(User.id == id)).first()
            
            if user:
                fzs = user.friendzones
                
                if fzs and len(fzs) > 0:
                    fzs_list = []
                    
                    for fz in fzs:
                        fzs_list.append(fz)
                
                    return json.dumps(fzs_list)
            
        return ("[]")


def fz_create(user_id: str, name: str) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).first()
        
        if user:
            fz = Friendzone()
            fz.creator = user.id
            fz.name = name
            
            user.friendzones.append(fz)
            
            session.commit()
            
            return json.dumps(fz.to_dict())
            
    return ("{}")


def fz_update(fz_id: str, name) -> str:
    with ORM.get_session() as session:
        if fz_id and fz_id != "":
            fz = session.scalars(select(Friendzone).where(Friendzone.id == fz_id)).first()
            
            if fz:
                fz.name = name
                
                session.commit()
                
                return json.dumps(fz.to_dict())
            
        return ("{}")


def fz_delete(fz_id: str = "") -> str:
    with ORM.get_session() as session:
        fz = session.scalars(select(Friendzone).where(Friendzone.id == fz_id)).first()
        
        if(fz):
            session.delete(fz)
            session.commit()
            return ("{}")
        else:
            return ("{}")


def apt_get(user_id: str, apt_id: str = "") -> str:
    with ORM.get_session() as session:
        if apt_id != "":
            apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).first()
            
            if apt:
                return json.dumps(apt.to_dict())
            
        elif user_id != "":
            user = session.scalars(select(User).where(User.id == id)).first()
            
            if user:
                apts = user.appointments
                
                if apts and len(apts) > 0:
                    apts_list = []
                    
                    for apt in apts:
                        apts_list.append(apt)
                
                    return json.dumps(apts_list)
            
        return ("[]")
    
    
def apt_create(user_id: str, name: str, date: datetime, time_start: str, time_stop: str, citycode: int, city: str, maxUser: int, notice: str) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).first()
        
        if user:
            apt = Appointment()
            apt.creator = user.id
            apt.name = name
            apt.date = date
            apt.time_start = time_start
            apt.time_stop = time_stop
            apt.citycode = citycode
            apt.city = city
            apt.maxUser = maxUser
            apt.notice = notice
            
            user.appointments.append(apt)
            
            session.commit()
            
            return json.dumps(apt.to_dict())
            
    return ("{}")


def apt_update(apt_id: str, name: str, date: datetime, time_start: str, time_stop: str, citycode: int, city: str, maxUser: int, notice: str) -> str:
    with ORM.get_session() as session:
        if apt_id and apt_id != "":
            apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).first()
            
            if apt:
                apt.date = date
                apt.time_start = time_start
                apt.time_stop = time_stop
                apt.citycode = citycode
                apt.city = city
                apt.maxUser = maxUser
                apt.notice = notice
                
                session.commit()
                
                return json.dumps(apt.to_dict())
            
        return ("{}")


def apt_delete(apt_id: str = "") -> str:
    with ORM.get_session() as session:
        apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).first()
        
        if(apt):
            session.delete(apt)
            session.commit()
            return ("{}")
        else:
            return ("{}")


def comment_get(user_id: str = "", apt_id: str = "", comment_id: str = "") -> str:
    with ORM.get_session() as session:
        if comment_id != "":
            comment = session.scalars(select(Comment).where(Comment.id == comment_id)).first()
            
            if comment:
                return json.dumps(comment.to_dict())
            
        elif user_id != "":
            user = session.scalars(select(User).where(User.id == user_id)).first()
            
            if user:
                comments = user.comments
                
                if comments and len(comments) > 0:
                    comments_list = []
                    
                    for comment in comments:
                        comments_list.append(comment)
                
                    return json.dumps(comments_list)
        elif apt_id != "":
            apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).first()
            
            if apt:
                comments = apt.comments
                
                if comments and len(comments) > 0:
                    comments_list = []
                    
                    for comment in comments:
                        comments_list.append(comment)
                
                    return json.dumps(comments_list)
            
        return ("{}")
    
    
def comment_create(user_id: str, apt_id: str, timestamp: str, comment_value) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).first()
        apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).first()
        
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


def comment_update(user_id: str, apt_id: str, timestamp: str, comment_value) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).first()
        apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).first()
        
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


def comment_delete(comment_id: str = "") -> str:
    with ORM.get_session() as session:
        comment = session.scalars(select(Comment).where(Comment.id == comment_id)).first()
        
        if(comment):
            session.delete(comment)
            session.commit()
            return ("{}")
        else:
            return ("{}")