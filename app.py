from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class VisitorCount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

@app.before_first_request
def create_db():
    db.create_all()

def get_visitor_count():
    visitor = VisitorCount.query.first()
    if visitor is None:
        visitor = VisitorCount(count=0)
        db.session.add(visitor)
        db.session.commit()
    return visitor.count

def increment_visitor_count():
    visitor = VisitorCount.query.first()
    if visitor:
        visitor.count += 1
        db.session.commit()

@app.route('/')
def index():
    visitor_cookie = request.cookies.get('unique_visitor')
    if not visitor_cookie:
        increment_visitor_count()
        resp = make_response(render_template('index.html', visitors=get_visitor_count()))
        resp.set_cookie('unique_visitor', '1', max_age=60*60*24*365)
        return resp
    else:
        return render_template('index.html', visitors=get_visitor_count())

if __name__ == '__main__':
    app.run()
