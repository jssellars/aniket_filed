from flask_jwt_simple import jwt_required
from flask_restful import Resource, abort

from Potter.FacebookPixels.Api.Dtos.PixelsInsightsCatalogsDto import PixelsInsightsCatalogsDto


class PixelsInsightsCatalogsEndpoint(Resource):

    @jwt_required
    def get(self):
        try:
            return PixelsInsightsCatalogsDto.pixels
        except Exception as e:
            abort(400, message=f"Failed to retrieve pixel insights breakdowns. Error {str(e)}")


class CustomConversionsInsightsCatalogsEndpoint(Resource):

    @jwt_required
    def get(self):
        try:
            return PixelsInsightsCatalogsDto.custom_conversions
        except Exception as e:
            abort(400, message=f"Failed to retrieve custom conversion insights breakdowns. Error {str(e)}")

