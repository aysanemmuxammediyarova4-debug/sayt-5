from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'furniture_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Furniture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # Mehmonxona, Yotoqxona, Oshxona
    dimensions = db.Column(db.String(50), nullable=False) # Masalan: 200x150x90 cm
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    room = request.args.get('room')
    if room:
        items = Furniture.query.filter_by(room_type=room).all()
    else:
        items = Furniture.query.all()
    return render_template('index.html', items=items, selected_room=room)

@app.route('/add', methods=['GET', 'POST'])
def add_furniture():
    if request.method == 'POST':
        title = request.form['title']
        room_type = request.form['room_type']
        dimensions = request.form['dimensions']
        price = float(request.form['price'])
        image_url = request.form['image_url']

        new_item = Furniture(
            title=title, room_type=room_type, dimensions=dimensions, price=price, image_url=image_url
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_furniture.html')

if __name__ == '__main__':
    app.run(debug=True)