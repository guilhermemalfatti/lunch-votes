from unittest import TestCase
from app import main
from unittest.mock import patch, MagicMock, Mock
from flask import Flask

app = Flask(__name__)

from app.main import app

def render_template(a, **context):
    return a, context

class MockVoteManager:

    def get_employees(self):
        return [1,2]

    def get_restaurants(self):
        return [1,2]

    def user_vote(self, data):
        return {'message': 'mock message', 'status': 'success'}

    def get_result(self, data):
        return 'selectedRestaurante'


class TestMain(TestCase):

    @patch('app.main.render_template')
    @patch('app.main.VoteManager')
    def test_home(self, mockVotemanager, mockRender_template):
        mockVotemanager.side_effect = Mock(return_value=MockVoteManager())
        mockRender_template.side_effect = render_template
        result = main.home()
        self.assertEqual(result[0], 'layout.html', 'The value should be equal.')
        self.assertIsNotNone(result[1]['employees'], 'The list should be not NONE')
        self.assertIsNotNone(result[1]['restaurants'], 'The list should be not NONE')


    @patch('app.main.VoteManager')
    def test_RecordVote_status_code(self, mockVotemanager):
        mockVotemanager.side_effect = Mock(return_value=MockVoteManager())

        with app.test_client() as c:
            response = c.post('/recordvote')
            self.assertEquals(response.status_code, 200, 'The status code should be 200')

    @patch('app.main.request')
    @patch('app.main.VoteManager')
    def test_ResultVote_status_code(self, mockVotemanager, mockRequest):
        mockVotemanager.side_effect = Mock(return_value=MockVoteManager())
        mockRequest.side_effect = Mock(return_value=MagicMock())

        app.testing = True
        with app.test_client() as c:
            response = c.get('/result')
            self.assertEquals(response.status_code, 200, 'The status code should be 200')



