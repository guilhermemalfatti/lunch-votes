from flask import Flask, render_template, request, redirect, url_for, abort, session
import redis
from app.votemanger.manager import VoteManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

@app.route('/')
def home():
    vm = VoteManager()
    r = redis.StrictRedis(decode_responses=True)
    r.set("mykey", "anothervalue")
    employees_list = r.get("mykey")#vm.get_employees()
    restaurant_list = vm.get_restaurants()
    return render_template('index.html',
                           employees=employees_list,
                           restaurants = restaurant_list)

@app.route('/signup', methods=['POST'])
def signup():
    session['username'] = request.form['username']
    session['message'] = request.form['message']
    return redirect(url_for('message'))

@app.route('/message')
def message():
    if not 'username' in session:
        return abort(403)
    return render_template('message.html', username=session['username'],
                                           message=session['message'])

if __name__ == '__main__':
    app.run()