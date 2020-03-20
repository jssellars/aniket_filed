import humps
from flask_jwt_simple import jwt_required
from flask_restful import Resource, abort

from Turing.Api.Dtos.AdsManagerCatalogsBreakdownsCombinationsDto import AdsManagerCatalogsBreakdownsCombinationsDto
from Turing.Api.Dtos.AdsManagerCatalogsBreakdownsDto import AdsManagerCatalogsBreakdownsDto
from Turing.Api.Dtos.AdsManagerCatalogsMetacolumnsDto import AdsManagerCatalogsMetacolumnsDto
from Turing.Api.Dtos.AdsManagerCatalogsViewsByLevelDto import AdsManagerCatalogsViewsByLevelDto
from Turing.Api.Dtos.AdsManagerCatalogsViewsDto import AdsManagerCatalogsViewsDto


class AdsManagerCatalogsViewsEndpoint(Resource):

    @jwt_required
    def get(self):
        try:
            response = AdsManagerCatalogsViewsDto.get()
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid views definition request. Error {str(e)}")


class AdsManagerCatalogsViewsByLevelEndpoint(Resource):

    @jwt_required
    def get(self, level):
        try:
            response = AdsManagerCatalogsViewsByLevelDto.get(level)
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid views definition request. Error {str(e)}")


class AdsManagerCatalogsMetacolumnsEndpoint(Resource):

    @jwt_required
    def get(self):
        try:
            response = AdsManagerCatalogsMetacolumnsDto.get()
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid metacolumns definition request. Error {str(e)}")


class AdsManagerCatalogsBreakdownsEndpoint(Resource):

    @jwt_required
    def get(self):
        try:
            response = AdsManagerCatalogsBreakdownsDto.get()
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid breakdowns definition request. Error {str(e)}")


class AdsManagerCatalogsBreakdownsCombinationsEndpoint(Resource):

    @jwt_required
    def get(self):
        try:
            response = AdsManagerCatalogsBreakdownsCombinationsDto.get()
            return humps.camelize(response)
        except Exception as e:
            abort(400, message=f"Invalid breakdowns definition request. Error {str(e)}")
