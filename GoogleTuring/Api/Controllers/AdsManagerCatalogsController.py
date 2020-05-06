import humps
from flask_jwt_simple import jwt_required
from flask_restful import Resource, abort

from GoogleTuring.Api.Dtos.AdsManagerCatalogsInsightsReportByLevelDto import AdsManagerCatalogsInsightsReportByLevelDto
from GoogleTuring.Api.Dtos.AdsManagerCatalogsViewsByLevelDto import AdsManagerCatalogsViewsByLevelDto


class AdsManagerCatalogsViewsByLevelEndpoint(Resource):
    @jwt_required
    def get(self, level):
        try:
            response = AdsManagerCatalogsViewsByLevelDto.get(level)
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid views definition request. Error {str(e)}")


class AdsManagerCatalogsMetaColumnsEndpoint(Resource):
    @jwt_required
    def get(self, level):
        try:
            response = AdsManagerCatalogsInsightsReportByLevelDto.get(level)
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid metacolumns definition request. Error {str(e)}")
