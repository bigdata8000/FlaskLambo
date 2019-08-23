from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dimsum99@localhost/lambo'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ljcellzrpcjhxy:6daf359427ec33c0a7d82ebfea5070c07050a6d91fec749085dd778021e288bb@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/de2ckt70ss46g9'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class LamFeedBack(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']  
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(LamFeedBack).filter(LamFeedBack.customer == customer).count() == 0:
            data = LamFeedBack(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()    

