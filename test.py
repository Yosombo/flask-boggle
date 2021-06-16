from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_render_board(self):
        with self.client as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<div class="toolbar">Score', res.data)
            self.assertIn(b'Score:', res.data)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<form method="POST" id="wordForm">', html)
            self.assertTrue(session["board"])

    def test_restart(self):
        with self.client as client:
            res = client.get('/restart')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    def test_redirection_followed(self):
        with self.client as client:
            res = client.get('/restart',  follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<form method="POST" id="wordForm">', html)
    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')
