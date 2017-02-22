from app.config import Config

class VoteManager:

    def __init__(self):

        # Get configurations
        config = Config().get_config()

        self.employees = config.get('general', 'employees').split(',')
        self.restaurants = config.get('general', 'restaurants').split(',')


    def get_employees(self):
        return self.employees

    def get_restaurants(self):
        return self.restaurants