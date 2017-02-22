from app.config import Config
from app.database.db import DB
import random
import datetime
class VoteManager:

    def __init__(self):

        # Get configurations
        config = Config().get_config()

        self.employees = config.get('general', 'employees').split(',')
        self.restaurants = config.get('general', 'restaurants').split(',')
        self.db = DB()
        self.restaurant_prefix = "restaurant."
        now = datetime.datetime.now()
        self.week_number = str(datetime.date(now.year, now.month, now.day).isocalendar()[1])


    def get_employees(self):
        return self.employees

    def get_restaurants(self):
        result = self.db.get_list(self.restaurant_prefix + 'week.' + self.week_number)

        #removing the duplicated values, avoid issue inside the loop
        result = list(set(result))
        #remove the restaurante already taken on this week
        for i in result:
            self.restaurants.remove(i)
        return self.restaurants

    def user_vote(self, data):
        employee_data_vote = self.db.get(data['employee'])

        #se a chave do usuario existe e o valor e a mesma data do voto, quer dizer que ja votou nesta data
        if employee_data_vote is not None and employee_data_vote == data['datetime']:
            return {'message': 'User allready voted!', 'status': 'warning'}
        #caso contrario o voto sera validado
        else:
            self.db.set(data['employee'], data['datetime'])
            self.db.push(self.restaurant_prefix + data['datetime'] + "." + data['restaurant'], 1)
            return {'message': 'Your vote was stored', 'status': 'success'}

    def get_result(self, date):
        #get the votes by restaurant
        restaurant_list = dict()
        greater_votes = []

        # check if the restaurant already be chosen
        result = self.db.get(self.restaurant_prefix + date)
        if result is not None:
            return result

        #getting all restaurant keys on redis
        result = self.db.get_keys(self.restaurant_prefix + date)

        # that's mean, no one has voted yet
        if not result:
            return "No one voted yet."

        #getting the votes for each restaurant
        for i in result:
            restaurant_list[i] = len(self.db.get_list(i))

        #identify what is the greater value of votes
        max_vote = max(restaurant_list.values())

        #Identifying if there was a tie vote
        for i in restaurant_list:
            if restaurant_list[i] == max_vote:
                greater_votes.append(i)

        #don't has tie votes, so return the greater
        if (len(greater_votes) == 1):
            selected_restaurant = greater_votes[0].split('.')[2]
        else:
            selected_restaurant = random.choice(greater_votes).split('.')[2]

        #setting the restaurant for the curretn week
        self.db.push(self.restaurant_prefix + 'week.' + self.week_number, selected_restaurant)
        # setting up the restaurant for the day
        self.db.set(self.restaurant_prefix + date, selected_restaurant)
        return selected_restaurant
