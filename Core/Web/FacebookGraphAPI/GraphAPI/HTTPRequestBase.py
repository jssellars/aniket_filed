import requests
from retry import retry


class HTTPRequestBase:
    _timeout = 10000
    __RETRY_LIMIT = 3

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
    @retry(exceptions=Exception, tries=__RETRY_LIMIT, delay=1)
    def get_page(cls, url=None):
        response = None
        next_page_cursor = None

        try:
            page = cls.__get(url)
            raw_response = cls.__extract_data_from_page(page)
            response = raw_response.get('data') if 'data' in raw_response.keys() else None
            # TODO send summary only on the first page
            summary = raw_response.get('summary') if 'summary' in raw_response.keys() else None
            pagination = raw_response.get('paging') if 'paging' in raw_response.keys() else None
            if pagination:
                next_link = pagination.get('next') if 'cursors' in pagination.keys() else None
                if next_link:
                    cursors = pagination.get('cursors') if 'cursors' in pagination.keys() else None
                    if cursors:
                        next_page_cursor = cursors.get('after') if 'after' in cursors.keys() else None

            return response, next_page_cursor, summary
        except Exception as e:
            # Log exception
            if response or next_page_cursor:
                return response, next_page_cursor
            else:
                return e, None

    @classmethod
    @retry(exceptions=Exception, tries=__RETRY_LIMIT, delay=1)
    def __get(cls, url):
        response = requests.get(url, timeout=cls._timeout)
        response_as_dict = response.json()
        if response.status_code == 200:
            return response_as_dict

        error = response_as_dict['error']

        raise Exception(error.get('error_user_msg', error.get('message')))

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
    @retry(exceptions=Exception, tries=__RETRY_LIMIT, delay=1)
    def __next_page_from_cursor(cls, page, url):
        if 'cursors' in page['paging'].keys():
            next_page_string = page['paging']['cursors']['after']
            url = url + '&after=%s' % next_page_string
        else:
            url = page['paging']['next']

        response = requests.get(url, timeout=cls._timeout)
        response_as_dict = response.json()
        if response.status_code == 200:
            return response_as_dict

        error = response_as_dict['error']

        raise Exception(error.get('error_user_msg', error.get('message')))

    @staticmethod
    @retry(exceptions=Exception, tries=__RETRY_LIMIT, delay=1)
    def post(url, params=None):
        if params:
            response = requests.post(url, json=params)
        else:
            response = requests.post(url)

        response_as_dict = response.json()
        if response.status_code == 200:
            return response_as_dict

        error = response_as_dict['error']

        raise Exception(error.get('error_user_msg', error.get('message')))

    @staticmethod
    @retry(exceptions=Exception, tries=__RETRY_LIMIT, delay=1)
    def put(url, params=None):
        if params:
            response = requests.put(url, json=params)
        else:
            response = requests.put(url)

        response_as_dict = response.json()
        if response.status_code == 200:
            return response_as_dict

        error = response_as_dict['error']

        raise Exception(error.get('error_user_msg', error.get('message')))

    @staticmethod
    @retry(exceptions=Exception, tries=__RETRY_LIMIT, delay=1)
    def delete(url):
        response = requests.delete(url)
        response_as_dict = response.json()
        if response.status_code == 200:
            return response_as_dict

        error = response_as_dict['error']

        raise Exception(error.get('error_user_msg', error.get('message')))
