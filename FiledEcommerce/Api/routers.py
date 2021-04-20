import json
import logging

import flask_restful
from flask import Response, request
from products_poc import ProductsData
from sets_poc import SetsData
from shopify_poc import shopify_data_receiver
from variables_poc import VariablesData

from Core.flask_extensions import log_request
from Core.logging_config import request_as_log_dict

logger = logging.getLogger(__name__)


class Resource(flask_restful.Resource):
    method_decorators = [log_request(logger)]


class ShopifyPrivateApp(Resource):
    def post(self, level):
        # spread the data
        data = {
            "api_key": "f7904ec7ec01a0a5f489ed3e6406ffb8",
            "api_password": "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",
            "shop_name": "filed-com",
            "endpoint": "shop",
        }
        req_body = request.get_json()
        api_key = req_body["api_key"]
        api_password = req_body["api_password"]
        shop_name = req_body["shop_name"]
        endpoint = req_body["endpoint"]
        resource_url = req_body.get("resource_url", None)
        # send the request
        shopify_data = shopify_data_receiver(api_key, api_password, shop_name, endpoint, resource_url=resource_url)
        if shopify_data["status"]:
            res = json.dumps({"result": shopify_data, "status": True})
            return Response(response=res, status=200, mimetype="application/json")
        else:
            res = json.dumps({"result": shopify_data, "status": False})
            return Response(response=res, status=200, mimetype="application/json")

    def get(self):
        filed_data = [
            {
                "filed": {"name": "id", "disabled": True, "type": "number"},
                "ecommerce": {"name": "entry__id", "disabled": True, "type": "number"},
            },
            {
                "filed": {"name": "age", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__published", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "brand", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__updated", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "category", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__link__rel", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "description", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__link__type", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "gender", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__link__href", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "gtin", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__title", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "image", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__s:type", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "margin", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__vendor", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "title", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__summary__type", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "price", "disabled": True, "type": "number"},
                "ecommerce": {"name": "entry__summary__#Text", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "sale_price", "disabled": True, "type": "number"},
                "ecommerce": {"name": "entry__s:tag__001", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "size", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__s:tag__002", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "availablity", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__s:variant__id", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "stock", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__s:variant__title", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "link", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__s:variant__s:price__currency", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "currency", "disabled": True, "type": "string"},
                "ecommerce": {"name": "entry__s:variant__s:price__#Text", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "Custom 1", "disabled": False, "type": "string"},
                "ecommerce": {"name": "entry__s:variant__s:sku", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "Custom 2", "disabled": False, "type": "string"},
                "ecommerce": {"name": "entry__s:variant__s:grams", "disabled": True, "type": "string"},
            },
            {
                "filed": {"name": "Custom 3", "disabled": False, "type": "string"},
                "ecommerce": {"name": "entry__s:variant__title", "disabled": True, "type": "string"},
            },
        ]
        res = json.dumps({"result": filed_data, "status": True})
        return Response(response=res, status=200, mimetype="application/json")


class SetHeader(Resource):
    def get(self):
        columns = SetsData.column_header()
        data = {
            "category": "Sets",
            "setsViews": {"columns": columns, "id": 1, "name": "Sets Header", "isDefault": True, "isSelected": True},
        }
        res = json.dumps(data)
        return Response(response=res, status=200, mimetype="application/json")


class ProductHeader(Resource):
    def get(self):
        columns = ProductsData.column_header()
        data = {
            "category": "Products",
            "productsViews": {
                "columns": columns,
                "id": 1,
                "name": "Products Header",
                "isDefault": True,
                "isSelected": True,
            },
        }
        res = json.dumps(data)
        return Response(response=res, status=200, mimetype="application/json")


class VariableHeader(Resource):
    def get(self):
        columns = VariablesData.column_header()
        data = {
            "category": "Variables",
            "variablesViews": {
                "columns": columns,
                "id": 1,
                "name": "Variants Header",
                "isDefault": True,
                "isSelected": True,
            },
        }
        res = json.dumps(data)
        return Response(response=res, status=200, mimetype="application/json")


class FiledSets(Resource):
    def post(self):
        try:
            res = Commons.generate_filed_data_response(request.get_json(force=True), SetsData.set_main_data())
            return Response(response=res, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": "Failed to process request."}, 400


class FiledProducts(Resource):
    def post(self):
        try:
            res = Commons.generate_filed_data_response(request.get_json(force=True), ProductsData.set_main_data())
            return Response(response=res, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": "Failed to process request."}, 400


class FiledVariables(Resource):
    def post(self):
        try:
            res = Commons.generate_filed_data_response(request.get_json(force=True), VariablesData.set_main_data())
            return Response(response=res, status=200, mimetype="application/json")
        except Exception as e:
            logger.exception(repr(e), extra=request_as_log_dict(request))
            return {"message": "Failed to process request."}, 400


class Commons:
    @staticmethod
    def generate_filed_data_response(
        req_body,
        all_value,
    ):
        start_row = req_body["startRow"]
        end_row = req_body["endRow"]
        data = all_value[int(start_row) : int(end_row)]
        if len(all_value) > (len(data) + start_row):
            next_page_cursor = "eee"
        else:
            next_page_cursor = None

        summary = {"total_nr_of_product": 15000, "total_nr_of_variable": 15000}
        return json.dumps({"data": data, "nextPageCursor": next_page_cursor, "summary": summary})
