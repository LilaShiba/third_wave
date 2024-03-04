# app.py

from app import create_app
from app.configs.logging_config import setup_logging

# Configure logging as early as possible
setup_logging()


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Corrected call to app.run()
