# bgp_interface_test.py
# Author: Thomas MINIER - MIT License 2017-2018
import pytest
from http_server.server import sage_app
from tests.http.utils import jsonPost

app = sage_app('tests/data/test_config.yaml')

bgp_queries = [
    ({
        'query': {
            'type': 'bgp',
            'bgp': [
                {
                    'subject': 'http://db.uwaterloo.ca/~galuc/wsdbm/Offer1000',
                    'predicate': 'http://purl.org/goodrelations/price',
                    'object': '?price'
                }
            ],
            "filters": [
                "?price = \"232\""
            ]
        }
    }, 1),
    ({
        'query': {
            'type': 'bgp',
            'bgp': [
                {
                    'subject': 'http://db.uwaterloo.ca/~galuc/wsdbm/Offer1000',
                    'predicate': 'http://purl.org/goodrelations/price',
                    'object': '?price'
                },
                {
                    'subject': 'http://db.uwaterloo.ca/~galuc/wsdbm/Offer1000',
                    'predicate': 'http://schema.org/eligibleQuantity',
                    'object': '?quantity'
                }
            ],
            "filters": [
                "isLiteral(?price) && ?price = \"232\"",
                "?quantity = \"4\""
            ]
        }
    }, 1)
]


class TestFilterInterface(object):
    @classmethod
    def setup_class(self):
        app.testing = True
        self.app = app.test_client()

    @classmethod
    def teardown_class(self):
        pass

    @pytest.mark.parametrize('body,cardinality', bgp_queries)
    def test_filter_interface(self, body, cardinality):
        query = body
        nbResults = 0
        nbCalls = 0
        hasNext = True
        while hasNext:
            response = jsonPost(self.app, '/sparql/watdiv100', query)
            nbResults += len(response['bindings'])
            hasNext = response['hasNext']
            query['next'] = response['next']
            nbCalls += 1
        assert nbResults == cardinality
        assert nbCalls > 0
