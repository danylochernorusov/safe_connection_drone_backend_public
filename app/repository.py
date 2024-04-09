from database import session, User, Message

class UserRepository:
    def add(self, username: str, password: str) -> None:
        user = User(username, password)
        session.add(user)
        session.commit()

    def get(self, id: int) -> User:
        user = session.query(User).filter_by(id=id).first()
        return user

    def get_all(self) -> list[User]:
        users = session.query(User).all()
        return users

    def update(self, id: int, new_username: str, new_password: str) -> None:
        user = session.query(User).filter_by(id=id).first()

        user.set_username(new_username)
        user.set_password(new_password)

        session.commit()

    def delete(self, id: int) -> None:
        user = session.query(User).filter_by(id=id).first()
        session.delete(user)
        session.commit()

    def search(self, username: str, password: str) -> User:
        users = session.query(User).all()
        for user in users:
            if user.get_username() == username:
                if user.password_check(password):
                    return user
                
        raise Exception()
    
class MessageRepository:
    def add(self, text: str, sender_id: int, recipient_id: int) -> None:
        message = Message(text, sender_id, recipient_id)
        session.add(message)
        session.commit()

    def get(self, id: int) -> User:
        message = session.query(Message).filter_by(id=id).first()
        return message

    def get_all(self) -> list[User]:
        messages = session.query(Message).all()
        return messages

    def update(self, id: int, new_text: str) -> None:
        message = session.query(Message).filter_by(id=id).first()

        message.set_text(new_text)

        session.commit()

    def delete(self, id: int) -> None:
        message = session.query(Message).filter_by(id=id).first()
        session.delete(message)
        session.commit()