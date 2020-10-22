from marshmallow import fields

from Core.Tools.Mapper.MapperBase import MapperBase, MapperNestedField
from FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto


class GraphAPIAdAccountMapping(MapperBase):
    id = fields.String(data_key="id")
    account_id = fields.String(data_key="account_id")
    name = fields.String(data_key="name")
    account_status = fields.Integer(data_key="account_status")
    currency = fields.String(data_key="currency")
    business = MapperNestedField(GraphAPIBusinessDto, data_key="business")
