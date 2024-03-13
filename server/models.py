from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(metadata=metadata)

class Receiver(db.Model, SerializerMixin):
    __tablename__ = 'receivers'

    serialize_rules = ('-messages.receiver',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    messages = db.relationship('Message', back_populates='receiver')

    def __repr__(self):
        return f'<Receiver {self.id} {self.name} {self.email}>'

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    serializer_rules = ('-receiver.messages', '-message_fields.message',)

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    receiver_id = db.Column(db.Integer, db.ForeignKey('receivers.id'))

    receiver = db.relationship('Receiver', back_populates='messages')
    message_fields = db.relationship('MessageField', back_populates='message')

    def __repr__(self):
        return f'<Message {self.id} {len(self.message_fields)} message fields>'

class MessageField(db.Model, SerializerMixin):
    __tablename__ = 'message_fields'

    serializer_rules = ('-message.message_fields',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))

    message = db.relationship('Message', back_populates='message_fields')

    def __repr__(self):
        return f'<MessageField {self.id} {self.title} {self.content[0:10]}...>'
