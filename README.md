# CS Gator

A basic Flask web application with Bootstrap styling and SQLAlchemy database integration.

## Features

- Welcome page with "Welcome to CS Gator!" message
- User account sign-up page
- SQLAlchemy ORM with SQLite database
- Bootstrap 5 responsive design
- Form validation with flash messages
- Duplicate username/email checking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/afoxball/csgator.git
cd csgator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application in debug mode (development only):
```bash
FLASK_DEBUG=true python app.py
```

To run the application in production mode:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`

## Environment Variables

- `SECRET_KEY`: Secret key for Flask sessions (defaults to development key)
- `FLASK_DEBUG`: Set to 'true' to enable debug mode (should be disabled in production)

## Database

The application uses SQLite database stored in `instance/csgator.db`. The database is automatically created when the application starts.

## Pages

- `/` - Home page with welcome message
- `/signup` - Account sign-up page with username and email fields