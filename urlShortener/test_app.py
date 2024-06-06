import unittest
from flask import json
from app import create_app

class UrlShortenerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_shorten_url_success(self):
        response = self.client.get('/shorten', query_string={'url': 'http://example.com'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('short_url', data)

    def test_shorten_url_missing_url(self):
        response = self.client.get('/shorten')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'URL is required')

    def test_expand_url_success(self):
        # First, shorten a URL to have something to expand
        shorten_response = self.client.get('/shorten', query_string={'url': 'http://example.com'})
        shorten_data = json.loads(shorten_response.data)
        short_url = shorten_data['short_url']

        # Now, expand the shortened URL
        expand_response = self.client.get('/expand', query_string={'short_url': short_url})
        expand_data = json.loads(expand_response.data)
        self.assertEqual(expand_response.status_code, 200)
        self.assertEqual(expand_data['original_url'], 'http://example.com')

    def test_expand_url_missing_short_url(self):
        response = self.client.get('/expand')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Short URL is required')

    def test_expand_url_not_found(self):
        response = self.client.get('/expand', query_string={'short_url': 'n.abl/nonexistent'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'URL not found')

    def test_maximum_capacity_reached(self):
        # Simulate reaching maximum capacity by adding MAX_URL entries
        for i in range(self.app.config['MAX_URL']):
            self.client.get('/shorten', query_string={'url': f'http://example.com/{i}'})

        # Now try to shorten another URL
        response = self.client.get('/shorten', query_string={'url': 'http://overflow.com'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 507)
        self.assertEqual(data['message'], 'Insufficient Storage')

if __name__ == '__main__':
    unittest.main()
