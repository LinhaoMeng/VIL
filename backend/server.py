## for production mode
## Running in Production
# If you want to use your .dotenv files in production, you have to make a small change because you won't be using the Flask CLI on a production server.

# If you want to see this work, you can install gunicorn so you don't have to use the development server for Flask.

# pipenv install gunicorn
# We need to create a file that gunicorn can find the app object in. For this, we'll create run.py. Let's start with the standard code that doesn't load the environment variables, which is only two lines.

# #run.py
# from demo import create_app

# app = create_app()
# gunicorn run:app
# This should run on port 8000 by default. If you navigate to the index, you'll see the value of API_KEY is None.


from flaskr import create_app
from dotenv import load_dotenv

load_dotenv('.env') #the path to your .env file (or any other file of environment variables you want to load)

app = create_app()