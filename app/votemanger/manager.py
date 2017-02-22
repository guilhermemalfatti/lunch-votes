from app.config import Config
from app.database.db import DB
class VoteManager:

    def __init__(self):

        # Get configurations
        config = Config().get_config()

        self.employees = config.get('general', 'employees').split(',')
        self.restaurants = config.get('general', 'restaurants').split(',')
        self.db = DB()
        self.restaurant_prefix = "restaurant."


    def get_employees(self):
        return self.employees

    def get_restaurants(self):
        return self.restaurants

    def user_vote(self, data):
        employee_data_vote = self.db.get(data['employee'])

        #se a chave do usuario existe e o valor e a mesma data do voto, quer dizer que ja votou nesta data
        if employee_data_vote is not None and employee_data_vote == data['datetime']:
            return {'message': 'User allready voted!', 'status': 'warning'}
        #caso contrario o voto sera validado
        else:
            self.db.set(data['employee'], data['datetime'])
            self.db.append(self.restaurant_prefix + data['datetime'] + "." + data['restaurant'], 1)
            return {'message': 'Your vote was stored', 'status': 'success'}

    def get_result(self, data):
        return
