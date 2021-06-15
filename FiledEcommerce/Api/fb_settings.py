from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()

class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="filed", name="ecommerce", kind="api")
    port = 47650

    sql_server = core.replace_in_class(get_env_model(env, "sql_server"), name="Dev3.Filed.Facebook.Accounts")
    
    mongo = core.replace_in_class(get_env_model(env, "mongo"), ecommerce_database_name="dev3_ecommerce")
