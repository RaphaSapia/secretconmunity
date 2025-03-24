from PIL.EpsImagePlugin import field
from flask import render_template, url_for, request, flash, redirect, abort
from secretcommunity import app, database, Bcrypt, bcrypt
from secretcommunity.forms import FormLogin, FormCreate, Form_editprofile, Form_createpost
from secretcommunity.models import User, Post
from flask_login import login_user
from flask_login import logout_user, current_user, login_required
import secrets
from PIL import Image
from datetime import datetime
import os
import pytz


@app.route("/secretconmunity")
def secretconmunity():
    return render_template('secretconmunity.html')

@app.route("/")
@login_required
def home():
    posts = Post.query.order_by(Post.post_id.desc()).all()
    for post in posts:
        post.body = post.body.strip()
    return render_template('home.html', posts=posts)



@app.route("/contacts")
def contacts():
    return render_template('contacts.html')


@app.route("/users")
@login_required
def users():
    users_list = User.query.all()
    return render_template('users.html', users_list=users_list)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()

    if form_login.validate_on_submit() and 'submit_login' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.key.data):
            login_user(user, remember=form_login.reminds_me.data)
            flash(f'Login Success for {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccess', 'alert-danger')

    return render_template('login.html', form_login=form_login)

@app.route("/create", methods=['GET', 'POST'])
def create():
    form_create = FormCreate()
    if form_create.validate_on_submit():
        key_cript = bcrypt.generate_password_hash(form_create.key.data).decode('utf-8')
        user = User(user=form_create.user.data, email=form_create.email.data, password=key_cript)
        database.session.add(user)
        database.session.commit()
        flash(f'Successfully created for email {form_create.email.data}', 'alert-success')
        login_user(user, remember=False)
        return redirect(url_for('home'))
    return render_template('create.html', form_create=form_create)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout Success', 'alert-success')
    return redirect(url_for('secretconmunity'))


@app.route("/profile")
@login_required
def profile():
    photo = url_for('static', filename='photo_profile/{}' .format(current_user.photo_profile))
    return render_template('profile.html', user=current_user.user, email=current_user.email, photo_profile=photo)


@app.route("/createpost/create", methods=['GET', 'POST'])
@login_required
def createpost():
    form = Form_createpost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.content.data, user_id=current_user.id)
        database.session.add(post)
        database.session.commit()
        flash('Create Post Success', 'alert-success')
        return redirect(url_for('home'))
    return render_template('createpost.html', form=form)

def save_photo(form_photo):
    random_hex = secrets.token_hex(8)
    name, extention = os.path.splitext(form_photo.filename)
    photo_name = name + random_hex + extention
    photo_path = os.path.join(app.root_path, 'static', 'photo_profile', photo_name)
    form_photo.save(photo_path)
    size = (200, 200)
    img = Image.open(photo_path)
    img.thumbnail(size)
    img.save(photo_path)
    return photo_name

def update_especialities(form):
    especialities_list = []
    for field in form:
        if 'esp_' in field.name:
            if field.data == True:
                especialities_list.append(field.label.text)
    return ';'.join(especialities_list)

@app.route("/editprofile", methods=['GET', 'POST'])
@login_required
def editprofile():
    form = Form_editprofile()
    if form.validate_on_submit():
        current_user.user = form.user.data
        current_user.email = form.email.data
        if form.photo_profile.data:
            photo_profile_name = save_photo(form.photo_profile.data)
            current_user.photo_profile = photo_profile_name
        current_user.subjects = update_especialities(form)
        database.session.commit()
        flash('Edit Profile Success', 'alert-success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.user.data = current_user.user
        form.email.data = current_user.email
    photo_profile = url_for('static', filename='photo_profile/{}' .format(current_user.photo_profile))
    return render_template('editprofile.html', user=current_user.user, email=current_user.email, photo_profile=photo_profile, form=form)


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = Form_createpost() if current_user.id == post.user_id else None

    if form and form.validate_on_submit():
        post.title = form.title.data
        post.body = form.content.data
        post.date_created = datetime.now(pytz.timezone('America/Sao_Paulo'))
        database.session.commit()
        flash('Edit Post Success', 'alert-success')
        return redirect(url_for('home', post_id=post.post_id))

    elif form and request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.body

    return render_template('post.html', post=post, form=form)

@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        database.session.delete(post)
        database.session.commit()
        flash('Delete Post Success', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)