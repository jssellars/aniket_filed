import cgi
import io
import json
import jwt
import humps


class RequestSerializer:

    def __init__(self, event):
        self.event = event

    def get_body(self):
        try:
            return humps.decamelize(json.loads(self.event.get("body")))
        except Exception:
            byte_body = io.BytesIO(self.event['body'].encode('utf-8'))
            byte_headers = cgi.parse_header(self.event['headers']['Content-Type'])[1]
            if 'boundary' in byte_headers:
                byte_headers['boundary'] = byte_headers['boundary'].encode('utf-8')
            byte_headers['CONTENT-LENGTH'] = len(self.event['body'])
            form_data = cgi.parse_multipart(byte_body, byte_headers)
            return {
                "mapping": humps.decamelize(json.loads(form_data['mapping'][0])),
                "file": form_data['file']
            }

    def get_query_params(self):
        return humps.decamelize(self.event.get("queryStringParameters"))

    def get_path_params(self):
        return humps.decamelize(self.event.get("pathParameters"))

    def get_headers(self):
        return humps.decamelize(self.event.get("headers"))

    def decode_jwt(self):
        bearer_token = self.get_headers().get('authorization')
        token = bearer_token.replace('Bearer ', '')
        jwt_data = jwt.decode(token, verify=False)
        return humps.decamelize(jwt_data)


class ResponseSerializer:

    @staticmethod
    def get_response(body, headers=None):
        return {
            "headers": {"Access-Control-Allow-Origin": "*"},
            "statusCode": 200,
            "body": json.dumps({"message": humps.camelize(body)})
        }

    @staticmethod
    def get_redirect(url):
        return {
            "headers": {"Location": url, "Access-Control-Allow-Origin": "*"},
            "statusCode": 301
        }
