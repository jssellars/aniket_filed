from Core import settings as core

env = core.get_environment()


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="filed", name="ecommerce", kind="api")
    port = 47650
