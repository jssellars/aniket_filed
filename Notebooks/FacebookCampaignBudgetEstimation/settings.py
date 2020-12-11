from Core import settings as core


class Default:
    # WARNING: this must not inherit BaseModel and must be name "Default"
    environment = "dev"
    name = core.Name(domain="facebook", name="campaignbudgetestimation", kind="bt")
    port = 47350
