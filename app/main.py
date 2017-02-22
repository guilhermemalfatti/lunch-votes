from flask import Flask, render_template, request, redirect, url_for, abort, session
from app.votemanger.manager import VoteManager

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/')
def home():
    try:
        vm = VoteManager()

        employees_list = vm.get_employees()
        restaurant_list = vm.get_restaurants()
        return render_template('layout.html',
                               employees=employees_list,
                               restaurants=restaurant_list)
    except Exception as err:
        return {'message': err}, 500


class Recordvote(Resource):
    def post(self):
        try:
            vm = VoteManager()
            result = vm.user_vote(request.form)

            return result, 200
        except Exception as err:
            return {'message': err}, 500

class Resultvote(Resource):
    def get(self):
        try:
            vm = VoteManager()

            date = request.args['datetime']
            result = vm.get_result(date)
            return result, 200
        except Exception as err:
            return {'message': err}, 500

class AvailableRestaurant(Resource):
    def get(self):
        try:
            vm = VoteManager()

            restaurant_list = vm.get_restaurants()
            return restaurant_list, 200
        except Exception as err:
            return {'message': err}, 500

@app.route('/message')
def message():
    if not 'username' in session:
        return abort(403)
    return render_template('message.html', username=session['username'],
                                           message=session['message'])

api.add_resource(Recordvote, '/recordvote')
api.add_resource(Resultvote, '/result')
api.add_resource(AvailableRestaurant, '/availablerest')

if __name__ == '__main__':
    app.run()