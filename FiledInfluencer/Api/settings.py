from Core import settings as core
from Core.settings import get_env_model

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="filed", name="influencer", kind="api")
    port = 47850

    sql_server = core.replace_in_class(
        get_env_model(env, "sql_server"),
        host="dev-zone.ctonnmgtbe2i.eu-west-1.rds.amazonaws.com",
        username="filed_admin",
        password="dvserv3#rathena",
        name="Dev3.Filed.SMI.Influencers",
        port=1433,
    )

    # Local Testing
    # sql_server = core.replace_in_class(
    #     get_env_model(env, "sql_server"),
    #     host="localhost",
    #     username="sa",
    #     password="",
    #     name="Localhost.Filed.SMI.Influencers",
    #     port=1433,
    # )

    # Local Testing 2
    # sql_server = core.replace_in_class(
    #     get_env_model(env, "sql_server"),
    #     host="DESKTOP-JDD3RNF",
    #     username="sa",
    #     password="123456",
    #     name="Filed.SMI.Influencers",
    #     port=1433,
    #     driver="SQL Server Native Client 11.0",
    # )
