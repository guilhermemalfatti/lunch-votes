from flask import Flask, render_template, request
from app.votemanager.manager import VoteManager
from app import logger
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    logger.info('start render')
    try:
        vm = VoteManager()

        employees_list = vm.get_employees()
        restaurant_list = vm.get_restaurants()

        logger.debug('employee list: ' + str(employees_list))
        logger.debug('restaurant list: ' + str(restaurant_list))

        return render_template('layout.html',
                               employees=employees_list,
                               restaurants=restaurant_list)
    except Exception as err:
        logger.error('ERROR' + str(err))
        return {'message': err}, 500


class Recordvote(Resource):
    def post(self):
        logger.info('start record vote.')
        try:
            logger.debug('parameters of vote: ' + str(request.form))
            vm = VoteManager()
            result = vm.user_vote(request.form)

            logger.debug('result of vote: ' + str(result))
            return result, 200
        except Exception as err:
            logger.error('ERROR' + str(err))
            return {'message': err}, 500


class Resultvote(Resource):
    def get(self):
        logger.info('start result vote.')
        try:
            vm = VoteManager()

            logger.debug('result vote args: ' + str(request.args['datetime']))

            date = request.args['datetime']
            result = vm.get_result(date)

            logger.debug('result Vote: ' + str(result))
            return result, 200
        except Exception as err:
            logger.error('ERROR' + str(err))
            return {'message': err}, 500


class AvailableRestaurant(Resource):
    def get(self):
        logger.info('start available restaurant.')
        try:
            vm = VoteManager()

            restaurant_list = vm.get_restaurants()
            logger.debug('Available restaurant: ' + str(restaurant_list))
            return restaurant_list, 200
        except Exception as err:
            logger.error('ERROR' + str(err))
            return {'message': err}, 500


api.add_resource(Recordvote, '/recordvote')
api.add_resource(Resultvote, '/result')
api.add_resource(AvailableRestaurant, '/availablerest')

if __name__ == '__main__':
    logger.info("Application started.")
    app.run()
