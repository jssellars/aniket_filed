from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    name = core.Name(domain="facebook", name="apps", kind="bt")
    port = 47231
