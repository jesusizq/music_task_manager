import os
from app import create_app, db
from config import config
from flask_migrate import Migrate, upgrade

app = create_app(config[os.getenv("FLASK_CONFIG") or "default"])
migrate = Migrate(app, db, compare_type=True)

if __name__ == "__main__":
    app.run(debug=True)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()
