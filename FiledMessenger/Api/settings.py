from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="filed", name="messenger", kind="api")
    port = 47734
    mongo = core.replace_in_class(
        get_env_model(env, "mongo"),
        message_collection_name="messages",
        message_database_name="message_db",
    )
