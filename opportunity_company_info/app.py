from flask import Flask
from .urls import company_bp  # Import the blueprint

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(company_bp)

if __name__ == "__main__":
    app.run(debug=True)
