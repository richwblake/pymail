from faker import Faker
from app import app
from models import db, Message

fake = Faker()

def create_messages():

    Message.query.delete()

    messages = []

    for i in range(20):
        m = Message(
                name = fake.name(),
                email = fake.email(),
                content = fake.sentence(),
                )

        messages.append(m)

    db.session.add_all(messages)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_messages()
