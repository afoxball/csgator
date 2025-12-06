from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Placeholder routes so your buttons work
@app.route('/register')
def register():
    return "Registration Page - Coming Soon!"

@app.route('/login')
def login():
    return "Login Page - Coming Soon!"

if __name__ == '__main__':
    # port 5000 is the default, but Render might set a PORT env var
    # This block is mainly for local testing
    app.run(debug=True)
