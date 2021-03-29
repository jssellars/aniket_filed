from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="campaignsbuilder", kind="api")
    port = 47220
    mongo = core.replace_in_class(
        get_env_model(env, "mongo"),
        publish_feedback_collection_name="publish_feedback",
        publish_feedback_database_name="{env}_campaign_builder_publish_feedback",
    )
