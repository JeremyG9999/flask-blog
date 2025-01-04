from app import app, db
with app.app_context():
    db.create_all()
# migrations
"""
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
"""