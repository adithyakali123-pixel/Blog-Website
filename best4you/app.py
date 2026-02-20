from flask import Flask
from database import init_db
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.main import main_bp

app = Flask(__name__)
app.secret_key = 'best4you_secret_key_2025'

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
