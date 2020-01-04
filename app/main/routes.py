# the routes are the different URLs that the application implements.
# in flask, handlers for the application routes are written as python functions, called view functions.
# view functions are mapped to one or more route URLS so that FLASK knows what logic to execute when a client request a given URL.
from flask import render_template, flash, redirect, url_for, request, current_app, g
from app import db
from flask_login import current_user, login_required
from app.models import User, Org
from datetime import datetime
from app.main.forms import EditProfileForm, JobapplicationForm, SearchForm
from app.main import bp


@bp.before_request # register the decorated function to be executed right before the view function
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

	g.search_form = SearchForm()



@bp.route('/index')
#@login_required
def index():
    # user = {'username': 'Miguel'}
	# fake dictionary:
	# job listing:
    page = request.args.get('page', 1, type=int)
    posts = Org.query.order_by(Org.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Home Page', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)

@bp.route('/')
@bp.route('/home')
def home():
#	form = SearchForm()
#	if form.validate_on_submit():
#		redirect(url_for('search'))
	return render_template('homepage7.html', title='Home')

@bp.route('/who_we_are')
def who_we_are():
	return render_template('who_we_are.html', title='Who We Are')

@bp.route('/services')
def services():
	return render_template('services.html', title='Services')

@bp.route('/blog')
def blog():
	return render_template('blog.html', title='Blog')

@bp.route('/contact')
def contact():
	return render_template('contact.html', title='Contact Us')

#@bp.route('/home')
#def home():
#	return render_template('homepage.html', title='TalentDisha')


@bp.route('/jobseeker', methods=['GET', 'POST']) # if jobseeker go to /jobseeker
@login_required
def jobseeker():
	'''
	* go to your job seeker profile page
	* add resume
	* details about yourself
	'''
	return redirect(url_for('main.user', username=current_user.username)) # logged in go to profile page or home page to apply jobs
	'''
	form = StudentLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username of password')
			return redirect(url_for('studentlogin'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc!='':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)
	'''

@bp.route('/org', methods=['GET', 'POST']) # if jobseeker go to /jobseeker
def org():
	'''
	* go to your job application form page
	* add jobs
	* details about yourself
	'''
	form = JobapplicationForm()
	if form.validate_on_submit():
		post = Org(name = form.name.data, pos=form.position.data, loc=form.location.data, stipend=form.stipend.data, deadline=form.deadline.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('{} Job profile has been published, with deadline of {}'.format(
			form.position.data, form.deadline.data))
		return redirect(url_for('main.org'))
	return render_template('jobapplication.html', title='Job Profile', form=form)

#		return redirect(url_for('index'))
	'''
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = OrgLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('orglogin'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc!='':
			next_page = url_for('index')
		return redirect(next_page) # change this function to organization job profile or job application listing
		#return redirect(url_for('index')) # change this function to organization job profile or job application listing
	return render_template('login.html', title='Sign In', form=form)
	'''


@bp.route('/user/<username>') # dynamic component
@login_required # accessible to logged in users
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.orgs.order_by(Org.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile(): # use a resume format for jobseeker and their profile should be resume
	form=EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Your changes has been saved.')
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User {} not found.'.format(username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash('You cannot follow yourself!')
		return redirect(url_for('main.user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash('You are following {}!'.format(username))
	return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User {} not found.'.format(username))
		return redirect(url_for('main.index'))
	if user == current_user:
		flash('You cannot unfollow yourself!')
		return redirect(url_for('main.user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('You are not following {}'.format(username))
	return redirect(url_for('main.user', username=username))


@bp.route('/search')
def search():
	if not g.search_form.validate():
		return redirect(url_for('main.index'))
	page = request.args.get('page', 1, type=int)
	posts, total = Org.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
	next_url = url_for('main.search', q=g.search_form.q.data, page=page+1) \
		if total>page*current_app.config['POSTS_PER_PAGE'] else None
	prev_url = url_for('main.search', q=search_form.q.data, page=page-1) \
		if page>1 else None
	return render_template('search.html', title='Search', posts=posts, next_url=next_url, prev_url=prev_url)