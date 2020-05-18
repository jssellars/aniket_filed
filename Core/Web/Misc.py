import humps


def load_raw_request(request):
    return humps.decamelize(request.get_json(force=True))


def dump_response(response):
    return humps.camelize(response)


def snake_to_camelcase(data):
    if isinstance(data, list):
        camelcase = [{humps.camelize(key): value for key, value in entry.items()} for entry in data]
    else:
        camelcase = {humps.camelize(key): value for key, value in data.items()}

    return camelcase
