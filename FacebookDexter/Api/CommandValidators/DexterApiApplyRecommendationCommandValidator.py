class DexterApiApplyRecommendationCommandValidator:
    def validate(self, request_args: dict, request_headers: dict):
        recommendation_id = request_args.get("id")
        if not recommendation_id:
            error_message = ['Please provide id']
            return False, error_message
        parameters = {
            "id": recommendation_id,
            "token": request_headers.get('HTTP_AUTHORIZATION')
        }
        return True, parameters
