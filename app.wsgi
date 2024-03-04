# app.wsgi

import sys
import os

# Assuming your Flask app is located in the 'app' directory and 'app' is not a package
sys.path.insert(0, 'app')

from app import create_app  

# Set the environment variable to use the production configuration
os.environ['FLASK_ENV'] = 'production'
# TODO: SET_UP_PRODUCTIONs
# os.environ['APP_SETTINGS'] = 'config_production.ProductionConfig'

application = create_app()

if __name__ == "__main__":
    application.run()
