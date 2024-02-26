import json
import dbclasses as ORM
from dbclasses import User, Appointment, Comment, Friendzone
from sqlalchemy import select
from datetime import datetime

ORM.create_db_if_not_exists()

def user_get(id: str = "", email: str = "", passwd:str = "") -> set:
    with ORM.get_session() as session:
        if id != "":
            user = session.scalars(select(User).where(User.id == id)).one()
            
            if user:
                return user.to_json()
            
        elif email != "" and passwd != "":
            user = session.scalars(select(User).where(User.id == id)).one()
            
            if user:
                return user.to_json()
        else:
            users = session.scalars(select(User)).all()
        
            users_dict = {}
            for user in users:
                users_dict[user.id] = user.to_dict()
                
            return json.dumps(users_dict)
            
        return ("{}")


def user_update(id: str, first_name: str, last_name: str, email: str, passwd: str, gender: int, age: int, city: str):
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).one()
        
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.passwd = passwd
            user.gender = gender
            user.age = age
            user.city = city
            
            session.commit()
            
            return user.to_json()
            
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
            
            return user.to_json()
            
    return ("{}")


def user_delete(id: str):
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).one()
        
        if(user):
            session.delete(user)
            session.commit()
            return ("{}")
        else:
            return ("{}")


def fz_get(user_id: str, fz_id: str = "") -> str:
    with ORM.get_session() as session:
        if fz_id != "":
            fz = session.scalars(select(Friendzone).where(Friendzone.id == fz_id)).one()
            
            if fz:
                return fz.to_json()
            
        elif user_id != "":
            user = session.scalars(select(User).where(User.id == id)).one()
            
            if user:
                fzs = user.friendzones
                
                if fzs and len(fzs) > 0:
                    fzs_dict = {}
                    
                    for fz in fzs:
                        fzs_dict[fz.id] = fz
                
                    return json.dumps(fzs_dict)
            
        return ("{}")


def fz_create(user_id: str, name: str) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == id)).one()
        
        if user:
            fz = Friendzone()
            fz.creator = user.id
            fz.name = name
            
            user.friendzones.append(fz)
            
            session.commit()
            
            return fz.to_json()
            
    return ("{}")


def fz_update(fz_id: str, name) -> str:
    with ORM.get_session() as session:
        if fz_id and fz_id != "":
            fz = session.scalars(select(Friendzone).where(Friendzone.id == fz_id)).one()
            
            if fz:
                fz.name = name
                
                session.commit()
                
                return fz.to_json()
            
        return ("{}")


def fz_delete(fz_id: str = "") -> str:
    with ORM.get_session() as session:
        fz = session.scalars(select(Friendzone).where(Friendzone.id == fz_id)).one()
        
        if(fz):
            session.delete(fz)
            session.commit()
            return ("{}")
        else:
            return ("{}")


def apt_get(user_id: str, apt_id: str = "") -> str:
    with ORM.get_session() as session:
        if apt_id != "":
            apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).one()
            
            if apt:
                return apt.to_json()
            
        elif user_id != "":
            user = session.scalars(select(User).where(User.id == id)).one()
            
            if user:
                apts = user.appointments
                
                if apts and len(apts) > 0:
                    apts_dict = {}
                    
                    for apt in apts:
                        apts_dict[apt.id] = apt
                
                    return json.dumps(apts_dict)
            
        return ("{}")
    
    
def apt_create(user_id: str, name: str, date: datetime, time_start: str, time_stop: str, citycode: int, city: str, maxUser: int, notice: str) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).one()
        
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
            
            return apt.to_json()
            
    return ("{}")


def apt_update(apt_id: str, name: str, date: datetime, time_start: str, time_stop: str, citycode: int, city: str, maxUser: int, notice: str) -> str:
    with ORM.get_session() as session:
        if apt_id and apt_id != "":
            apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).one()
            
            if apt:
                apt.date = date
                apt.time_start = time_start
                apt.time_stop = time_stop
                apt.citycode = citycode
                apt.city = city
                apt.maxUser = maxUser
                apt.notice = notice
                
                session.commit()
                
                return apt.to_json()
            
        return ("{}")


def apt_delete(apt_id: str = "") -> str:
    with ORM.get_session() as session:
        apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).one()
        
        if(apt):
            session.delete(apt)
            session.commit()
            return ("{}")
        else:
            return ("{}")


def comment_get(user_id: str = "", apt_id: str = "", comment_id: str = "") -> str:
    with ORM.get_session() as session:
        if comment_id != "":
            comment = session.scalars(select(Comment).where(Comment.id == comment_id)).one()
            
            if comment:
                return comment.to_json()
            
        elif user_id != "":
            user = session.scalars(select(User).where(User.id == user_id)).one()
            
            if user:
                comments = user.comments
                
                if comments and len(comments) > 0:
                    comments_dict = {}
                    
                    for comment in comments:
                        comments_dict[comment.id] = comment
                
                    return json.dumps(comments_dict)
        elif apt_id != "":
            apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).one()
            
            if apt:
                comments = apt.comments
                
                if comments and len(comments) > 0:
                    comments_dict = {}
                    
                    for comment in comments:
                        comments_dict[comment.id] = comment
                
                    return json.dumps(comments_dict)
            
        return ("{}")
    
    
def comment_create(user_id: str, apt_id: str, timestamp: str, comment_value) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).one()
        apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).one()
        
        if user and apt:
            comment = Comment()
            comment.appointment_id = apt.id
            comment.user_id = user.id
            comment.timestamp = timestamp
            comment.comment_value = comment_value
            
            user.Comments.append(comment)
            
            session.commit()
            
            return comment.to_json()
            
    return ("{}")


def comment_update(user_id: str, apt_id: str, timestamp: str, comment_value) -> str:
    with ORM.get_session() as session:
        user = session.scalars(select(User).where(User.id == user_id)).one()
        apt = session.scalars(select(Appointment).where(Appointment.id == apt_id)).one()
        
        if user and apt:
            comment = Comment()
            comment.appointment_id = apt.id
            comment.user_id = user.id
            comment.timestamp = timestamp
            comment.comment_value = comment_value
            
            user.Comments.append(comment)
            
            session.commit()
            
            return comment.to_json()
            
    return ("{}")


def comment_delete(comment_id: str = "") -> str:
    with ORM.get_session() as session:
        comment = session.scalars(select(Comment).where(Comment.id == comment_id)).one()
        
        if(comment):
            session.delete(comment)
            session.commit()
            return ("{}")
        else:
            return ("{}")