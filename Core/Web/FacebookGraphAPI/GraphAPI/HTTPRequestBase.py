import requests


class HTTPRequestBase:
    _timeout = 10000

    @classmethod
    def get(cls, url=None, fields=None, pagination=True):
        response = None
        page = None
        summary = None
        try:
            page = cls.__get(url)
            if pagination:
                response, summary = cls.loop_pages(page, url)
            else:
                return page

            return response, summary
        except Exception as e:
            # Log exception
            if response:
                return response, summary
            elif page:
                return page, summary
            else:
                return e, None

    @classmethod
    def __get(cls, url):
        response = requests.get(url=url, timeout=cls._timeout)
        if response.status_code == 200:
            response = response.json()
        else:
            response = response.json()

            if 'error_user_msg' in response['error'].keys():
                raise Exception(response['error']['error_user_msg'])
            else:
                raise Exception(response['error']['message'])

        return response

    @classmethod
    def loop_pages(cls, page, url, field=None):
        raw_response = cls.__extract_data_from_page(page, field)
        response = []
        summary = []
        try:
            response = raw_response.get('data') if 'data' in raw_response.keys() else raw_response
            summary = raw_response.get('summary')
        except KeyError:
            pass
        except Exception as e:
            raise e

        if page and "paging" in page.keys():
            try:
                while page and 'data' in page.keys() and len(page['data']):
                    page = cls.__next_page_from_cursor(page, url)
                    page = cls.__extract_data_from_page(page, field)
                    if page and 'data' in page.keys():
                        response.extend(page['data'])
            except Exception as e:
                # TODO: Log error and continue. This is a common error when looping through all the pages
                pass
        return response, summary

    @staticmethod
    def __extract_data_from_page(page, field=None):
        if field and field not in page.keys():
            data = page
        elif field and field in page.keys():
            data = page[field]
        else:
            data = page

        return data

    @classmethod
    def __next_page_from_cursor(cls, page, url):
        if 'cursors' in page['paging'].keys():
            next_page_string = page['paging']['cursors']['after']
            url = url + '&after=%s' % next_page_string
        else:
            url = page['paging']['next']

        response = requests.get(url, timeout=cls._timeout)
        if response.status_code == 200:
            response = response.json()
        else:
            response = response.json()
            if 'error_user_msg' in response['error'].keys():
                raise Exception(response['error']['error_user_msg'])
            else:
                raise Exception(response['error']['message'])

        return response

    @staticmethod
    def post(url, params=None):
        if params:
            response = requests.post(url, json=params)
        else:
            response = requests.post(url)

        if response.status_code == 200:
            response = response.json()
        else:
            response = response.json()
            if 'error_user_msg' in response['error'].keys():
                raise Exception(response['error']['error_user_msg'])
            else:
                raise Exception(response['error']['message'])

        return response

    @staticmethod
    def put(url, params=None):
        if params:
            response = requests.put(url, json=params)
        else:
            response = requests.put(url)

        if response.status_code == 200:
            response = response.json()
        else:
            response = response.json()
            if 'error_user_msg' in response['error'].keys():
                raise Exception(response['error']['error_user_msg'])
            else:
                raise Exception(response['error']['message'])

        return response

    @staticmethod
    def delete(url):
        response = requests.delete(url)
        if response.status_code == 200:
            response = response.json()
        else:
            response = response.json()
            if 'error_user_msg' in response['error'].keys():
                raise Exception(response['error']['error_user_msg'])
            else:
                raise Exception(response['error']['message'])

        return response
