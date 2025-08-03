from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from app.routes.auth_routes import auth_bp
from app.routes.task_routes import task_bp
from app.routes.page_routes import page_bp
from app.config import JWT_SECRET_KEY

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(task_bp, url_prefix="/task")
app.register_blueprint(page_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5010)



