from flask import render_template
from app import db
from app.errors import bp


@bp.errorhandler(404) # declare a custom error handler
def not_found_error(error):
	return render_template('errors/404.html'), 404 # both functions return a second value after the template, which is the error code number


@bp.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('errors/500.html'), 500