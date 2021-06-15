from typing import List, Optional, Dict

from Core.mongo_adapter import MongoRepositoryBase, MongoOperator
from FiledMessenger.Api.model import MessageModel
from FiledMessenger.Api.startup import config


class MessageHandler:
    messages = MongoRepositoryBase(
        config=config.mongo,
        collection_name=config.mongo.message_collection_name,
        database_name=config.mongo.message_database_name,
    )

    @staticmethod
    def convert_to_pydantic(object: Dict) -> MessageModel:
        """
        Convert dict to pydantic model
        """
        return MessageModel.parse_obj(object)

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


# TODO: remove duplicacy
class ConversationHandler:
    messages = MongoRepositoryBase(
        config=config.mongo,
        collection_name=config.mongo.message_collection_name,
        database_name=config.mongo.message_database_name,
    )

    @staticmethod
    def convert_to_pydantic(object: Dict) -> MessageModel:
        """
        Convert dict to pydantic model
        """
        return MessageModel.parse_obj(object)

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
