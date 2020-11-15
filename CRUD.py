from basic import db, Color

""" db.session.query(Color).delete()
db.session.commit() """

all_color = Color.query.all() # list of all puppies in table
print(all_color)
print('\n')
