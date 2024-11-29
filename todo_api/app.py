import os
from chalice import Chalice
from chalicelib.todos import app as todos_blueprint

# Application name and environment
APP_NAME = os.getenv('APP_NAME')
ENV_NAME = os.getenv('ENV_NAME', 'dev')
app = Chalice(app_name=f'{APP_NAME}-{ENV_NAME}')

# Register the todos blueprint
app.register_blueprint(todos_blueprint)

