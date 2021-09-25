from . import create_app, db


app = create_app()
db.create_all(app=app)

