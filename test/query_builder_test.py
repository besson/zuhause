from unittest import TestCase
from zuhause.search.query_builder import QueryBuilder

class QueryBuilderTest(TestCase):

    def test_keep_default_query_with_no_params(self):
        params = {}
        expected = str({
                    'query': {
                        'bool': {
                            'should': [
                               {'match_all': {}
                               }
                            ],
                            'must_not': [],
                            'filter': []
                          }
                        },
                        'size': 1000
                })

        self.assertEquals(expected, str(QueryBuilder(params).build()))

    def test_should_add_query_params(self):
        params = {'q': 'Modern building'}
        self.assertTrue(str({'match': {'all': 'Modern building'}}) in str(QueryBuilder(params).build()))

    def test_should_add_pets_allowed_param(self):
        params = {'pets_allowed': 'yes'}

        expected =  "'must_not': [{'match_phrase': {'description.english': 'pet not allowed'}}]"
        self.assertTrue(expected in str(QueryBuilder(params).build()))

    def test_should_add_not_pets_allowed_param(self):
        params = {'pets_allowed': 'not'}

        expected =  "'must_not': [{'match_phrase': {'description.english': 'pet not allowed'}}"
        self.assertTrue(expected not in str(QueryBuilder(params).build()))

    def test_should_add_price_filter(self):
        params = {'max_price': 1200}
        self.assertTrue(str({'range': {'rent_price': {'lte': 1200}}}) in str(QueryBuilder(params).build()))

    def test_should_available_from_filter(self):
        params = {'available_from': '2017-01-01'}
        self.assertTrue(str({'range': {'available_at': {'gte': '2017-01-01'}}}) in str(QueryBuilder(params).build()))

    def test_should_filter_by_radius(self):
        params = {'base_location': {'lat': 52.5219184, 'long': 13.411026, 'radius': '42km'}}

        expected = "'geo_distance': {'distance': '42km', 'geolocation': {'lat': 52.5219184, 'lon': 13.411026}}"
        self.assertTrue(expected in str(QueryBuilder(params).build()))
