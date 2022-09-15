
from unittest import TestCase
from app import app
from flask import sessions

app.config['TESTING'] = True

class FlaskTests(TestCase):
    
    def test_main(self):
        with app.test_client() as client:
            users = {'first_name': 'John', 'last_name': 'Pearce', 'image_url': 'url'}
            result = client.get('/', data = {users})
            assert "John Pearce" in result


