from basic import db, Color

# create table
""" db.create_all() """

green = Color('ruru','green')
blue = Color("evans", 'red')

print(green.id)
print(blue.id)

db.session.add(blue)
db.session.commit()

print(green)
print(blue)
