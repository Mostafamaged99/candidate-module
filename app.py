import click
import models
import routes
import config
from extensions import app
import routes.auth

app.config.from_object(config.DevelopmentConfig)
models.db.init_app(app)


@app.cli.command('db-init')
def init_db_command():
    """Clear the existing data and create new tables."""
    models.db.drop_all()
    models.db.create_all()
    click.echo('Initializing the database: Done')


app.register_blueprint(routes.candidate_blp)
app.register_blueprint(routes.auth_blp)

if __name__ == '__main__':
    app.run()
