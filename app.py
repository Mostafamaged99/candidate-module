from app import create_app
from app.models import db
from dotenv import load_dotenv


load_dotenv()
app = create_app()


@app.cli.command('db-init')
def init_db_commandd():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()


@app.route('/')
def index():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)
