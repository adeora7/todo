from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from app import app, db, lm, oid
from .forms import LoginForm, TaskForm
from .models import User, Task


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = TaskForm()
    if form.validate_on_submit():
        t = Task(body=form.task.data, status='1', username=g.user.nickname)
        db.session.add(t)
        db.session.commit()
        flash('Task added to active tasks !')
        return redirect(url_for('index'))
    
    newtask = Task.query.all()
    return render_template('index.html',
                           title='All',
                           user=g.user,
                           form=form,
                           tasks=newtask)



@app.route('/active')
@login_required
def active():
    user = g.user
    newtask = Task.query.all()
    return render_template('active.html',
                           title='Active',
                           user=user,
                           tasks=newtask)

@app.route('/completed')
@login_required
def completed():
    user = g.user
    newtask = Task.query.all()
    return render_template('completed.html',
                           title='Completed',
                           user=user,
                           tasks=newtask)


@app.route('/changestatus/<id>')
@login_required
def changestatus(id):
    t = Task.query.filter_by(id=id).first()
    t.status = '0'
    db.session.commit()
    return redirect(url_for('active'))


@app.route('/delete/<id>')
@login_required
def delete(id):
    t = Task.query.filter_by(id=id).first()
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for('index'))




@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
