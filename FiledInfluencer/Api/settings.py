from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="filed", name="influencer", kind="api")
    port = 47850
    mongo = core.replace_in_class(
        get_env_model(env, "mongo"),
        influencer_profiles_collection_name="instagram_influencers",
        influencer_database_name="influencer_db",
    )
