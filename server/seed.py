from faker import Faker
from app import app
from models import db, Receiver, Message, MessageField

fake = Faker()

def create_messages():

    Receiver.query.delete()
    Message.query.delete()
    MessageField.query.delete()

    messages = []

    r1 = Receiver(name=fake.name(), origin='https://www.willsblake.tech', email=fake.email())
    r2 = Receiver(name=fake.name(), origin=fake.url(), email=fake.email())

    db.session.add(r1)
    db.session.add(r2)

    r1.messages = [Message() for i in range(0, 5)]
    r2.messages = [Message() for i in range(0, 5)]

    for receiver in Receiver.query.all():
        for message in receiver.messages:
            message.message_fields = [MessageField(title=fake.word(), content=fake.sentence()) for i in range(0, 3)]

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_messages()
