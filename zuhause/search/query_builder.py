class QueryBuilder:

    def __init__(self, params):
        self._params = params

    def build(self):
        es_query = self._query_template()
        should_match = es_query['query']['bool']['should']
        must_not_match = es_query['query']['bool']['must_not']
        filter_match = es_query['query']['bool']['filter']

        self._add_query_terms(should_match)
        self._add_pet_filter(must_not_match)
        self._add_max_price_filter(filter_match)
        self._add_available_from_filter(filter_match)
        self._add_geo_location_filter(filter_match)

        return es_query

    def _add_query_terms(self, should_match):
        if ('q' in self._params):
            should_match.append({'match': {'all': self._params['q']}})

    def _add_pet_filter(self, must_not_match):
        if ('pets_allowed' in self._params and self._params['pets_allowed'] == 'yes'):
            must_not_match.append({'match_phrase': {'description.english': 'pet not allowed'}})

    def _add_max_price_filter(self, filter_match):
        if ('max_price' in self._params):
            filter_match.append({'range': {'rent_price': {'lte': self._params['max_price']}}})

    def _add_available_from_filter(self, filter_match):
        if ('available_from' in self._params):
            filter_match.append({'range': {'available_at': {'gte': self._params['available_from']}}})

    def _add_geo_location_filter(self, filter_match):
        if ('base_location' in self._params):
            filter_match.append({'geo_distance': {'distance': self._params['base_location']['radius'],
                                    'geolocation' : {
                                        'lat' : self._params['base_location']['lat'],
                                        'lon' : self._params['base_location']['long']}}})

    def _query_template(self):
        return {
                'query': {
                    'bool': {
                        'should': [
                           {'match_all': {}
                           }
                        ],
                        'must_not': [],
                        'filter': []
                      }
                    }, 'size': 1000
                }
