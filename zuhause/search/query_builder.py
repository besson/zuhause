class QueryBuilder:

    def __init__(self, params):
        self._params = params

    def build(self):
        es_query = self._query_template()
        function_score = es_query['query']['function_score']
        should_match = es_query['query']['function_score']['query']['bool']['should']
        must_match = es_query['query']['function_score']['query']['bool']['must']
        filter_match = es_query['query']['function_score']['query']['bool']['filter']

        self._add_query_terms(should_match)
        self._add_pet_filter(must_match)
        self._add_max_price_filter(filter_match)
        self._add_available_at_filter(filter_match)
        self._add_room_filter(filter_match)
        self._add_elevator_filter(must_match)
        self._add_groundfloor_filter(must_match)
        self._add_furnished_filter(must_match)
        self._add_geo_location_boost(function_score)

        return es_query

    def _add_query_terms(self, should_match):
        if ('q' in self._params):
            should_match.append({'match': {'all': self._params['q']}})

    def _add_pet_filter(self, must_match):
        if ('pets_allowed' in self._params and self._params['pets_allowed'] == True):
            must_match.append({'match': {'allows_pets': 'yes'}})
        elif('pets_allowed' in self._params and self._params['pets_allowed'] == False):
            must_match.append({'match': {'allows_pets': 'no'}})

    def _add_max_price_filter(self, filter_match):
        if ('max_price' in self._params):
            filter_match.append({'range': {'rent_price': {'to': self._params['max_price']}}})

    def _add_available_at_filter(self, filter_match):
        if ('available_at' in self._params):
            filter_match.append({'range': {'available_at': {'to': self._params['available_at']}}})

    def _add_room_filter(self, filter_match):
        if ('rooms' in self._params):
            filter_match.append({'range': {'rooms': {'from': self._params['rooms']}}})

    def _add_elevator_filter(self, must_match):
        if ('elevator' in self._params and self._params['elevator'] == True):
            must_match.append({'match': {'source': 'immobilienscout24-elevator'}})

    def _add_groundfloor_filter(self, must_match):
        if ('groundfloor' in self._params and self._params['groundfloor'] == True):
            must_match.append({'match': {'source': 'immobilienscout24-groundfloor'}})

    def _add_furnished_filter(self, must_match):
        if ('furnished' in self._params and self._params['furnished'] == True):
            must_match.append({'match': {'furnished': True}})

    def _add_geo_location_boost(self, function_score):
        if ('base_location' in self._params):
            function_score['gauss'] = {
                                        'geolocation': {
                                            'origin': '%s,%s' % (self._params['base_location']['lat'],
                                                                self._params['base_location']['long']),
                                            'scale': self._params['base_location']['radius']
                                        }
                                     }

    def _add_room_booster(self, should_match):
        if ('rooms' in self._params):
            should_match.append({ 'multi_match':
                                    {'query': '%d room' % self._params['rooms'],
                                     'type': 'phrase_prefix',
                                     'fields': [
                                        'description.english',
                                        'dimensions.english'
                                      ]
                                    }
                                })

    def _query_template(self):
        return {
                    'query': {
                        'function_score': {
                            'query': {
                                'bool': {
                                    'should': [
                                       {'match_all': {}
                                       }
                                    ],
                                    'must_not': [],
                                    'must': [],
                                    'filter': []
                                }
                            },
                            'score_mode': 'sum'
                        }
                    },
                    'size': 1000
                }
