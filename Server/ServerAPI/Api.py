import os
import secrets
from ServerAPI import app, db, bcrypt, mail
from .DB_Model import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            print('missing')
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except:
            print('invalid')
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['username'], email=data['email'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/checkUser', methods=['GET'])
@token_required
def checkUser(current_user):
    if current_user:
        print(current_user)
        return jsonify({'Logged_in': True}), 200
    else:
        print(current_user)
        return jsonify({'Logged_in': False}), 401


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()

    output = []

    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['title'] = post.title
        post_data['date_posted'] = post.date_posted
        post_data['content'] = post.content
        post_data['user_id'] = User.query.get_or_404(post.user_id).public_id
        post_data['Author'] = User.query.get_or_404(post.user_id).username
        output.append(post_data)

    # countpost = 0
    # output = {}
    # for post in posts:
    #     output[countpost] = {
    #         "id": post.id,
    #         "title": post.title,
    #         "date_posted": post.date_posted,
    #         "content": post.content,
    #         'user_id': User.query.get_or_404(post.user_id).public_id,
    #         'Author': User.query.get_or_404(post.user_id).username

    #     }
    #     countpost += 1
    return jsonify(output)


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 406, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 406,  {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 406, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})

# ----------------------


@app.route("/register", methods=['GET', 'POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    username=data['username'], email=data['email'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route("/logout")
def logout():
    return jsonify({'Message': 'Logged out Successfully'})


def save_picture(form_picture):
    pass


@app.route("/account", methods=['GET'])
@token_required
def account(current_user):
    try:
        user_posts = Post.query.filter_by(user_id=current_user.id)
    except AttributeError:
        return jsonify({'Error': 'User Not Found'})
    countpost = 0
    userjson = {}
    for post in user_posts:
        userjson[countpost] = {
            "id": post.id,
            "title": post.title,
            "date_posted": post.date_posted,
            "content": post.content
        }
        countpost += 1
    user_data = {}
    user_data['public_id'] = current_user.public_id
    user_data['username'] = current_user.username
    user_data['email'] = current_user.email
    user_data['admin'] = current_user.admin
    return jsonify({'User_Posts': userjson, 'User_Data': user_data})


@app.route("/post/new", methods=['POST'])
@token_required
def new_post(current_user):
    data = request.get_json()
    new_post = Post(title=data.get('title'), content=data.get(
        'content'), user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'New post created!'})


@app.route("/post/<int:post_id>", methods=['GET'])
def postViewer(post_id):
    post = Post.query.get_or_404(post_id)
    user_P_id = User.query.get_or_404(post.user_id)
    postjson = {
        "id": post.id,
        "title": post.title,
        "date_posted": post.date_posted,
        "content": post.content,
        "user_id": user_P_id.public_id,
        "Author_Name": user_P_id.username
    }
    return jsonify({'Post': postjson})


@app.route("/post/<int:post_id>", methods=['PUT', 'DELETE'])
@token_required
def post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    user_P_id = User.query.get_or_404(post.user_id)

    if current_user.id == user_P_id.id or current_user.admin:
        if request.method == 'PUT':
            data = request.get_json()
            if data:
                if data.get('title'):
                    post.title = data['title']
                if data.get('content'):
                    post.content = data['content']
                if data.get('user_id'):
                    post.user_id = data['user_id']
                db.session.commit()
                return jsonify({'Message': 'Edited Post'})
        elif request.method == 'DELETE':
            db.session.delete(post)
            db.session.commit()

            return jsonify({'message': 'The post has been deleted!'})
        # return render_template('post.html', title=post.title, post=post)
    else:
        return jsonify({'message': 'Cannot perform that function!', 'user': current_user.id})


@app.route("/user/<public_id>/posts", methods=['GET'])
def user_posts(public_id):
    try:
        user = User.query.filter_by(public_id=public_id).first()
        user_posts = Post.query.filter_by(user_id=user.id)
    except AttributeError:
        return jsonify({'Error': 'User Not Found'})
    countpost = 0
    userjson = {}
    for post in user_posts:
        userjson[countpost] = {
            "id": post.id,
            "title": post.title,
            "date_posted": post.date_posted,
            "content": post.content,
            "user_id": user.public_id,
            "Author_Name": user.username
        }
        countpost += 1
    return jsonify(userjson)


def send_reset_email(user):
    pass


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    pass


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    pass


@app.route("/MyPosts", methods=['GET'])
@token_required
def MyPosts(current_user):
    try:
        user = User.query.filter_by(public_id=current_user.public_id).first()
        user_posts = Post.query.filter_by(user_id=user.id)
    except AttributeError:
        return jsonify({'Error': 'User Not Found'})
    countpost = 0
    userjson = {}
    for post in user_posts:
        userjson[countpost] = {
            "id": post.id,
            "title": post.title,
            "date_posted": post.date_posted,
            "content": post.content,
            "user_id": user.public_id,
            "Author_Name": user.username
        }
        countpost += 1
    return jsonify(userjson)
