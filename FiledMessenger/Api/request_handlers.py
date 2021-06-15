import random
import string

from typing import List, Optional, Dict

from Core.mongo_adapter import MongoRepositoryBase, MongoOperator
from FiledMessenger.Api.model import MessageModel, ConversationIDModel
from FiledMessenger.Api.startup import config


class MessageHandler:
    messages = MongoRepositoryBase(
        config=config.mongo,
        collection_name=config.mongo.message_collection_name,
        database_name=config.mongo.message_database_name,
    )

    @staticmethod
    def convert_to_pydantic(dict_object: Dict) -> MessageModel:
        """
        Convert dict to pydantic model
        """
        return MessageModel.parse_obj(dict_object)

    @classmethod
    def add_message(cls, sender, recipient, message) -> MessageModel:
        msg = MessageModel(
            sender=sender,
            recipient=recipient,
            message=message,
        )
        cls.messages.add_one(msg.dict())

        return msg.json()

    @classmethod
    def get_message(cls, sender, recipient) -> Optional[List[MessageModel]]:
        msgs = cls.messages.get({"sender": sender, "recipient": recipient})

        if not msgs:
            return None

        results = [cls.convert_to_pydantic(msg) for msg in msgs]
        return [result.json() for result in results]


# TODO: remove duplicates
class ConversationHandler:
    messages = MongoRepositoryBase(
        config=config.mongo,
        collection_name=config.mongo.message_collection_name,
        database_name=config.mongo.message_database_name,
    )

    @staticmethod
    def convert_to_pydantic(dict_object: Dict) -> MessageModel:
        """
        Convert dict to pydantic model
        """
        return MessageModel.parse_obj(dict_object)

    @classmethod
    def get_conversation(cls, sender, recipient) -> Optional[List[MessageModel]]:
        query = {
            MongoOperator.OR.value: [
                {"sender": sender, "recipient": recipient},
                {"sender": recipient, "recipient": sender},
            ]
        }
        msgs = cls.messages.get_sorted(
            query=query,
            sort_query=[("timestamp", -1)],
        )

        if not msgs:
            return None

        results = [cls.convert_to_pydantic(msg) for msg in msgs]
        return [result.json() for result in results]


def create_conversation():
    len_string = 10
    random_string = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=len_string)
    )
    return random_string


# TODO: remove duplicates
class ConversationIDHandler:
    conversations = MongoRepositoryBase(
        config=config.mongo,
        collection_name=config.mongo.conversation_collection_name,
        database_name=config.mongo.message_database_name,
    )

    @staticmethod
    def convert_to_pydantic(dict_object: Dict) -> ConversationIDModel:
        """
        Convert dict to pydantic model
        """
        return ConversationIDModel.parse_obj(dict_object)

    @classmethod
    def get_conversation_id(cls, sender, recipient) -> Optional[ConversationIDModel]:
        msg = cls.query_conversation_id(recipient, sender)

        if not msg:
            return None

        return msg.json()

    @classmethod
    def query_conversation_id(cls, recipient, sender) -> Optional[ConversationIDModel]:
        query = {
            MongoOperator.OR.value: [
                {"sender": sender, "recipient": recipient},
                {"sender": recipient, "recipient": sender},
            ]
        }
        msgs = cls.conversations.get(query=query)

        if not msgs:
            return None

        return cls.convert_to_pydantic(msgs[0])

    @classmethod
    def add_conversation_id(cls, sender, recipient) -> ConversationIDModel:
        msg = cls.query_conversation_id(recipient, sender)

        if not msg:
            msg = ConversationIDModel(
                sender=sender,
                recipient=recipient,
                conversation_id=create_conversation(),
            )
            cls.conversations.add_one(msg.dict())

        return msg.json()
