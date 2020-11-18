from app import db, Post

db.session.query(Post).delete()
db.session.commit()

