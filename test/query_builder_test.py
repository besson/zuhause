from unittest import TestCase
from zuhause.search.query_builder import QueryBuilder

class QueryBuilderTest(TestCase):

    def test_keep_default_query_with_no_params(self):
        params = {}
        expected = str({
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
                })

        self.assertEquals(expected, str(QueryBuilder(params).build()))

    def test_should_add_query_params(self):
        params = {'q': 'Modern building'}
        self.assertTrue(str({'match': {'all': 'Modern building'}}) in str(QueryBuilder(params).build()))

    def test_should_add_pets_allowed_param(self):
        params = {'pets_allowed': True}

        expected =  "'must': [{'match': {'allows_pets': 'yes'}}]"
        self.assertTrue(expected in str(QueryBuilder(params).build()))

    def test_should_add_not_pets_allowed_param(self):
        params = {'pets_allowed': False}

        expected =  "'must': [{'match': {'allows_pets': 'no'}}]"
        self.assertTrue(expected in str(QueryBuilder(params).build()))

    def test_should_add_price_filter(self):
        params = {'max_price': 1200}
        self.assertTrue(str({'range': {'rent_price': {'to': 1200}}}) in str(QueryBuilder(params).build()))

    def test_should_filter_available_at(self):
        params = {'available_at': '2017-01-01'}
        self.assertTrue(str({'range': {'available_at': {'to': '2017-01-01'}}}) in str(QueryBuilder(params).build()))

    def test_should_boost_by_distance(self):
        params = {'base_location': {'lat': 52.5219184, 'long': 13.411026, 'radius': '42km'}}

        expected = "'gauss': {'geolocation': {'origin': '52.5219184,13.411026', 'scale': '42km'}"
        self.assertTrue(expected in str(QueryBuilder(params).build()))

    def test_should_boost_by_rooms(self):
        params = {'rooms': 2}
        query = str({ 'multi_match':
                        {'query': '%d room' % params['rooms'],
                         'type': 'phrase_prefix',
                         'fields': [
                            'description.english',
                            'dimensions.english'
                          ]
                        }
                    })

        self.assertTrue(query in str(QueryBuilder(params).build()))
