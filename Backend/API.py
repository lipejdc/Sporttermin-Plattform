import json
import SQL_Alchemy_Stuff as ORM
from SQL_Alchemy_Stuff import User, Appointment, Comment, Friendzone
from sqlalchemy import select

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
            
        return "{}"


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
    with Session(engine) as session:
        try:
            user = session.scalars(select(User).where(User.id == id)).one()
            
            if(user):
                session.delete(user)
                session.commit()
                return Response("OK", status=200)
            else:
                return Response("invalid request", status=400)
            
        except Exception as e:
            print(f"Exception in delete_user: {e}")
            return Response("invalid request", status=400)


def fz_get(user_id: str, fz_id: str = "") -> str:
    print("hi000er!")


def apt_get(user_id: str, apt_id: str = "") -> str:
    print("hi000er!")


def comment_get(user_id: str, apt_id: str = "") -> str:
    print("hi000er!")