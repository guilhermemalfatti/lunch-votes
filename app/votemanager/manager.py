from app.config import Config
from app.database.db import DB
import random
from app import logger
import datetime


class VoteManager:
    """

    This class provides a instance to the vote manager of project.
    """

    def __init__(self):
        """
        Starts a Config instance
        """

        # Get configurations
        config = Config().get_config()

        self.employees = config.get('general', 'employees').split(',')
        self.restaurants = config.get('general', 'restaurants').split(',')
        self.db = DB()
        self.restaurant_prefix = "restaurant."
        now = datetime.datetime.now()
        self.week_number = str(datetime.date(now.year, now.month, now.day).isocalendar()[1])

    def get_employees(self):
        """
        return the list of available employee
        """
        logger.info('start get employee. ')
        return self.employees

    def get_restaurants(self):
        """
        return a list of available restaurants
        """
        logger.info('start get available restaurant. ')

        try:
            result = self.db.get_list(self.restaurant_prefix + 'week.' + self.week_number)
            logger.debug('week number ' + str(self.week_number))

            # removing the duplicated values, avoid issue inside the loop
            result = list(set(result))
            logger.debug('restaurants already voted in the week: ' + str(result))

            # remove the restaurante already taken on this week
            for i in result:
                self.restaurants.remove(i)

            logger.debug('Available restaurants: ' + str(self.restaurants))
            return self.restaurants
        except Exception as err:
            logger.error('ERROR' + str(err))
            return None

    def user_vote(self, data):
        """
        Handle the vote by user
        """
        logger.info('start user vote.')
        try:
            logger.debug('employee: ' + str(data['employee']))
            employee_data_vote = self.db.get(data['employee'])

            # se a chave do usuario existe e o valor e a mesma data do voto, quer dizer que ja votou nesta data
            if employee_data_vote is not None and employee_data_vote == data['datetime']:
                logger.info('user already voted.')
                return {'message': 'User allready voted!', 'status': 'warning'}
            # caso contrario o voto sera validado
            else:
                logger.info('date of vote: ' + str(data['datetime']))
                logger.debug('restaurant of vote: ' + str(data['restaurant']))
                self.db.set(data['employee'], data['datetime'])
                self.db.push(self.restaurant_prefix + data['datetime'] + "." + data['restaurant'], 1)

                return {'message': 'Your vote was stored', 'status': 'success'}
        except Exception as err:
            logger.error('ERROR' + str(err))
            return None

    def get_result(self, date):
        """
        return the result of votes
        """
        logger.info('start get result')
        try:
            # get the votes by restaurant
            restaurant_list = dict()
            greater_votes = []

            # check if the restaurant already be chosen
            result = self.db.get(self.restaurant_prefix + date)

            if result is not None:
                logger.debug('restaurant already selected: ' + str(result))
                logger.info('restaurant selected:' + str(result))
                return result

            # getting all restaurant keys on redis
            result = self.db.get_keys(self.restaurant_prefix + date)
            logger.debug('all restaurant voted: ' + str(result))

            # that's mean, no one has voted yet
            if not result:
                logger.debug('No one voted yet.')
                return "No one voted yet."

            # getting the votes for each restaurant
            for i in result:
                restaurant_list[i] = len(self.db.get_list(i))
            logger.debug('votes to eache restaurant: ' + str(restaurant_list))

            # identify what is the greater value of votes
            max_vote = max(restaurant_list.values())
            logger.debug('max vote: ' + str(max_vote))

            # Identifying if there was a tie vote
            for i in restaurant_list:
                if restaurant_list[i] == max_vote:
                    greater_votes.append(i)

            # don't has tie votes, so return the greater
            if (len(greater_votes) == 1):
                selected_restaurant = greater_votes[0].split('.')[2]
                logger.debug('restaurant selected by majority: ' + str(selected_restaurant))
            else:
                # restaurant with greater votes selected randomically because has a tie
                selected_restaurant = random.choice(greater_votes).split('.')[2]
                logger.debug('restaurant selected randomically: ' + str(selected_restaurant))

            logger.info('restaurant selected:' + str(selected_restaurant))

            # setting the restaurant for the curretn week
            self.db.push(self.restaurant_prefix + 'week.' + self.week_number, selected_restaurant)
            # setting up the restaurant for the day
            self.db.set(self.restaurant_prefix + date, selected_restaurant)
            return selected_restaurant
        except Exception as err:
            logger.error('ERROR' + str(err))
            return None
