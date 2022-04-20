from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testi.db'
db = SQLAlchemy(app)

class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rsrq = db.Column(db.Numeric, nullable=False)
    rsrp = db.Column(db.Numeric, nullable=False)
    sinr = db.Column(db.Numeric, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Tuote %r' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        new_item = Lista(rsrq=request.form['rsrq'], rsrp=request.form['rsrp'], sinr=request.form['sinr'])
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect ('/')
        except:
            return 'Lisäys ei onnistunut'
    else:
        tuotteet = Lista.query.order_by(Lista.date).all()
        return render_template('index.html', tuotelista=tuotteet)

@app.route('/poista/<int:id>')
def poista(id):
    poistettava = Lista.query.get_or_404(id)
    try:
        db.session.delete(poistettava)
        db.session.commit()
        return redirect ('/')
    except:
        return 'Poisto ei onnistunut'


@app.route('/lisaadata', methods = ['POST'])
def lisaatuote():
    # luetaan json-data viestistä
    json_data = request.get_json(force=True)
    new_item = Lista(rsrq=json_data['rsrq'], rsrp=json_data['rsrp'], sinr=json_data['sinr'])

    try:
        db.session.add(new_item)
        db.session.commit()
        return redirect ('/')
    except:
        return 'Lisäys ei onnistunut'

if __name__=="__main__":
    app.run(debug=True)