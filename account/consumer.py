import json
import logging

import pika
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import User
from db import session

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
params = pika.URLParameters(settings.RABBITMQ_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="accounting")


def callback(ch, method, properties, body):
    data = json.loads(body)  # convert to string
    data = json.loads(data)  # convert to dictionary

    if properties.content_type == "user_created":
        """A new user has been created"""

        new_user = User(
            user_id=data["id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            identification=data["identification"],
            email=data["email"],
            password=data["password"],
        )
        session.add(new_user)
        session.commit()
        session.close()
        logging.info("User created successfully")

    elif properties.content_type == "user_updated":
        """A user has been updated"""

        user = session.query(User).filter(User.user_id == data["id"]).first()
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        session.add(user)
        session.commit()
        session.close()
        logging.info("User updated successfully")

    elif properties.content_type == "user_deleted":
        """A user has been deleted"""

        user = session.query(User).filter(User.user_id == data["id"])
        user.delete(synchronize_session=False)
        session.commit()
        session.close
        logging.info("User deleted successfully")


channel.basic_consume(queue="accounting", on_message_callback=callback, auto_ack=True)
logging.info("Started Consuming")

channel.start_consuming()

channel.close()
