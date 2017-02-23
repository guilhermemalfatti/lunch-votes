from unittest import TestCase
from app import main
from unittest.mock import patch, MagicMock, Mock
from app.votemanager.manager import VoteManager

class MockDB:

    def get_list(self, a):
        if a == 'mockkey.mockkey.rest01':
            return [1,1,1]
        return [3]

    def get(self, a):
        if a == 'restaurant.mockData02':
            return None
        if a == 'restaurant.mockData03':
            return []
        return 'mydate'

    def set(self, a, b):
        pass

    def push(self, a, b):
        pass

    def get_keys(self, a):
        return self.mock_list


def mockGet(self, a):
    return a

class TestManager(TestCase):

    @patch('app.votemanager.manager.DB')
    @patch('app.votemanager.manager.Config')
    def test_get_employee(self, mockConfig, mockDB):
        mockDB.side_effect = Mock(return_value=MagicMock())
        mockConfig.side_effect = Mock(return_value=MagicMock())

        vm = VoteManager()
        vm.employees = [1,2]
        result = vm.get_employees()

        self.assertEqual(result, [1,2], 'The result should be equal.')


    @patch('app.votemanager.manager.DB')
    @patch('app.votemanager.manager.Config')
    def test_get_restaurants(self, mockConfig, mockDB):
        mockDB.side_effect = Mock(return_value=MockDB())
        mockConfig.side_effect = Mock(return_value=MagicMock())

        vm = VoteManager()
        vm.restaurants = [3,4]
        result = vm.get_restaurants()

        self.assertEqual(result, [4], 'The result should be equal.')

    @patch('app.votemanager.manager.DB')
    @patch('app.votemanager.manager.Config')
    def test_user_vote(self, mockConfig, mockDB):
        mockDB.side_effect = Mock(return_value=MockDB())
        mockConfig.side_effect = Mock(return_value=MagicMock())

        vm = VoteManager()

        data = {'employee': 'fulano',
                'datetime': 'mydate',
                'restaurant': 'myRest'}
        result = vm.user_vote(data)

        self.assertEqual(result['message'], 'User allready voted!', 'The message should be equal.')
        self.assertEqual(result['status'], 'warning', 'The status should be equal.')

        data = {'employee': 'fulano',
                'datetime': 'mydate02',
                'restaurant': 'myRest'}
        result = vm.user_vote(data)

        self.assertEqual(result['message'], 'Your vote was stored', 'The message should be equal.')
        self.assertEqual(result['status'], 'success', 'The status should be equal.')


    @patch('app.votemanager.manager.DB')
    @patch('app.votemanager.manager.DB.get')
    @patch('app.votemanager.manager.Config')
    def test_get_result(self, mockConfig, mockdbGet, mockDB):
        mockdb = MockDB()
        mockDB.side_effect = Mock(return_value=mockdb)
        mockConfig.side_effect = Mock(return_value=MagicMock())
        mockdbGet.side_effect =  Mock(return_value=mockGet)

        vm = VoteManager()

        result = vm.get_result('mockData')
        self.assertEqual(result, 'mydate', 'The result should be equal.')

        mockdb.mock_list = []
        result = vm.get_result('mockData02')
        self.assertEqual(result, 'No one voted yet.', 'The result should be equal.')

        mockdb.mock_list = ['mockkey.mockkey.rest01', 'rest02']
        result = vm.get_result('mockData02')
        self.assertEqual(result, 'rest01', 'The result should be equal.')

