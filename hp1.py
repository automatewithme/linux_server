from app import db, create_app
from app.models import User, Org

app = create_app()

@app.shell_context_processor # register the function as a shell context function
def make_shell_context():
	return {'db': db, 'User': User, 'Org': Org}