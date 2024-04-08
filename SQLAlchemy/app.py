from flask import Flask, request, redirect, render_template
from random import sample
from models import db, connect_db, User

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

# Connect to the database
connect_db(app)
db.create_all()

@app.route('/')
def base():
    return redirect('/users')

# List User home page
@app.route('/users')
def show_users():
    users = User.query.all()
    random_users = sample(users, min(len(users), 5))
    return render_template('users/base.html', users=random_users)

# New User
@app.route('/users/newuser', methods=["POST"])
def new_user():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

# User Detail
@app.route('/users/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/userDetail.html', user=user)

# Edit User
@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect(f'/users/{user_id}')
    return render_template('users/editUser.html', user=user)

# Delete User
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)
