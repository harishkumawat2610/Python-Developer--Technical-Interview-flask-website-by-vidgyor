from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

with open('config.json', 'r') as c:
    params = json.load(c)['params']

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = params['upload_location']
application.secret_key = os.urandom(24)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/python_task'
img_dir = "//home//kuma//Music//bootstrap//static//img"
vid_dir = "//home//kuma//Music//bootstrap//static//up_image"

# if(local_server):
#     application.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
# else:
#     application.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(application)






class User(db.Model):
    s_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180), nullable=False)
    description = db.Column(db.String(2100), nullable=False)
    tags = db.Column(db.String(120), nullable=False)
    categories = db.Column(db.String(120), nullable=False)
    ref = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(121), nullable=True)
    thumb = db.Column(db.String(121), nullable=True)
    video = db.Column(db.String(121), nullable=True)


@application.route("/register", methods=['POST', 'GET'])
def register():
    sign_error = None;
    cate = None;
    if request.method == 'POST':
        """Add entry"""
        user = request.form.get("register_name")
        email = request.form.get("register_email")
        password = request.form.get("register_password")
        test_name = User.query.filter_by(email=email).first()
        if test_name is None:
            entry = User(name=user, email=email, password=password)
            db.session.add(entry)
            db.session.commit()
            flash("Account Successfully Created", "alert-success")
            return render_template('index.html')
        elif test_name.email == email:
            flash("Email is Aready Exits", "alert-danger")
            return render_template('index.html')
    return render_template('/index.html')


@application.route("/", methods=['POST', 'GET'])
@application.route("/home", methods=['POST', 'GET'])
def login():
    if 'user' in session and session['user'] == "xxxccc":
        return redirect(url_for('video'))

    error = None
    if request.method == 'POST':
        uname = request.form.get('login_email')
        upass = request.form.get('login_pass')
        test_name = User.query.filter_by(email=uname).first()
        print(test_name)
        if test_name is None:
            error = "Invalid password and email"
            return render_template('index.html', error=error)
        elif test_name.email == uname and test_name.password == upass:
            session['user'] = "xxxccc"
            return redirect(url_for('video'))
        else:
            error = "Invalid password and email"
            return render_template('index.html', error=error)

    return render_template('index.html', error=error)

@application.route("/logout")
def logout():
    session.pop('user')
    flash("Log out Successfully", "alert-success")
    return render_template('index.html')

@application.route("/video")
@application.route("/video/<string:sno>")
def video():
    if 'user' in session and session['user'] == "xxxccc":
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.order_by(Posts.date.desc()).paginate(page=page, per_page=5)
        notif = "10"
        return render_template("page2.html", posts=posts, notif=notif)
    else:
        return render_template("error.html")

@application.route("/upload_data", methods=['POST', 'GET'])
def upload_data():
    if 'user' in session and session['user'] == "xxxccc":
        if request.method == 'POST':
            """Add entry"""
            sno = request.form.get("register_name")
            name = request.form.get("title")
            description = request.form.get("message")
            tags = request.form.get("tags")
            categories = request.form.get("cate")
            ref = request.form.get("rid")
            thumb = request.form.get("thumb")
            video = request.form.get("video")

            entry = Posts(sno=sno, name=name, description=description, tags=tags, categories=categories, ref=ref,
                          thumb=thumb, date=datetime.now(), video=video)
            db.session.add(entry)
            db.session.commit()
        return render_template('/page3.html')
    else:
        return render_template("error.html")


@application.route("/upload")
def upload():
    if 'user' in session and session['user'] == "xxxccc":
        return render_template("page3.html")
    else:
        return render_template("error.html")
 #--------------------------------------------------------------------
@application.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == "xxxccc":
        post = Posts.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/login_board')


@application.route("/login_board", methods=['GET', 'POST'])
@application.route("/login_board/<string:sno>", methods=['GET', 'POST'])
def login_board():
    if 'user' in session and session['user'] == "xxxccc":
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.order_by(Posts.date.desc()).paginate(page=page, per_page=5)
        return render_template('dashboard.html', posts=posts)

    # if request.method == 'POST':
    #     username = request.form.get('uname')
    #     userpass = request.form.get('pass')
    #     if username == params['admin_user'] and userpass == params['admin_password']:
    #         session['user'] = username
    #         posts = Posts.query.all()
    #         return render_template('dashboard.html', params=params, posts=posts)

    return render_template("index.html")


@application.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == "xxxccc":
        if request.method == 'POST':
            name = request.form.get('title')
            message = request.form.get('message')
            cate = request.form.get('cate')
            ref = request.form.get('rid')
            thumb = request.form.get('thumb')
            date = datetime.now()
            video = request.form.get('video')
            tags = request.form.get('tags')

            if sno == '0':
                post = Posts(name=name, description=message, tags=tags, categories=cate, ref=ref, date=date,video=video,thumb=thumb)
                db.session.add(post)
                db.session.commit()
                return render_template('page2.html')

            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.name = name
                post.description = message
                post.categories = cate
                post.ref = ref
                post.thumb = thumb
                post.video = video
                post.tags = tags
                db.session.commit()
                return redirect('/edit/' + sno)
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', post=post , sno=sno)



application.run(debug=True)












