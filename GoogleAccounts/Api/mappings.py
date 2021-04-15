from marshmallow import fields

from Core.mapper import MapperBase


class GetAccountsCommandMapping(MapperBase):
    authorization_code = fields.String(required=True)


class GoogleHeadersMapping(MapperBase):
    client_id = fields.String(required=True)
    client_secret: fields.String(required=True)
    token: fields.String(required=True)
    refresh_token: fields.String(required=True)
    scopes: fields.String(required=True)
    token_uri: fields.String(required=True)


class AdAccountInsightsCommandMapping(MapperBase):
    from_date = fields.String(required=True)
    to_date = fields.String(required=True)
