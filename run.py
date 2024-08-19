import os
from app import create_app
from config import DevelopmentConfig, ProductionConfig


config_name = (
    ProductionConfig
    if os.environ.get("FLASK_CONFIG") == "production"
    else DevelopmentConfig
)

app = create_app(config_name)

if __name__ == "__main__":
    app.run(debug=True)
