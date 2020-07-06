from FacebookDexter.Api.Tools.ImportanceMapper import ImportanceMapper


class DexterApiRecommendationsPageCommandValidator():
    def validate(self, request_json):
        permitted_filters = ['campaign_id', 'channel', 'category', 'optimization_type', 'level', 'importance',
                             'confidence', 'recommendation_type', 'source', 'structure_id', 'ad_account_id',
                             'search_term', 'parent_id']

        permitted_sort_criteria = ['recommendation_type', 'optimization_type', 'created_at', 'importance', 'confidence']
        data = request_json

        errors = []

        page_number = data['PageNumber'] if 'PageNumber' in data else 1
        if page_number is None:
            page_number = 1

        page_size = data['PageSize'] if 'PageSize' in data else 10
        if page_size is None:
            page_size = 10

        _filter = data['Filter'] if 'Filter' in data else {}

        bad_filters = []
        if _filter:
            if not isinstance(_filter, dict):
                errors.append('invalid filter')
            else:
                for key in _filter:
                    if key not in permitted_filters:
                        errors.append(f"invalid filter criterion {key}")
                    else:
                        if not _filter[key]:
                            bad_filters.append(key)
                        if key in ['importance']:
                            mapped_values = []
                            for value in _filter[key]:
                                mapped_values.append(ImportanceMapper.get_importance_value(value))
                            _filter[key] = mapped_values

                for key in bad_filters:
                    del _filter[key]

        excluded_ids = data['ExcludedIds'] if 'ExcludedIds' in data else []

        sort = []
        if 'Sort' in data:
            sort = data['Sort']

        mongo_sort = None
        if sort:
            mongo_sort = []
            if not isinstance(sort, dict):
                errors.append('invalid sort')
            else:
                for key in sort:
                    if key not in permitted_sort_criteria:
                        errors.append(f'invalid sort criterion {key}')
                    else:
                        if sort[key] not in ['Ascending', 'Descending']:
                            errors.append(f'invalid sort order, {sort[key]}')
                        else:
                            if sort[key] == 'Ascending':
                                mongo_sort.append((key, 1))
                            else:
                                mongo_sort.append((key, -1))

        _filter['confidence'] = {'$gte': 0.5}

        if len(errors) > 0:
            return False, errors

        command_json = {
            "page_size": page_size,
            "page_number": page_number,
            "recommendations_filter": _filter,
            "recommendations_sort": mongo_sort,
            "excluded_ids": excluded_ids
        }

        return True, command_json
