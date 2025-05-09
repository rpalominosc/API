from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy 
from marshmallow_sqlalchemy import SQLAlchemySchema,SQLAlchemyAutoSchema
from marshmallow import fields, Schema
import pymysql, mariadb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:secret@127.0.0.1:3306/duoc'

db = SQLAlchemy(app)


class Authors(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20)) 
  specialisation = db.Column(db.String(50))

  def create(self):
    db.session.add(self)
    db.session.commit()
    return self

  def __init__(self, name, specialisation):
    self.name = name
    self.specialisation = specialisation
  
  def __repr__(self):
    #return '<Author %d>' % self.id
    return f'<Author {self.name}>'

with app.app_context():db.create_all()

class AuthorsSchema(SQLAlchemyAutoSchema):
  class Meta(Schema.Meta):
    model = Authors
    sqla_session = db.session
    include_fk = True
    load_instance = True
  
  id = fields.Integer(dump_only=True)
  name = fields.String(required=True)
  specialisation = fields.String(required=True)

@app.route('/')
def test():
    from sqlalchemy import text
    try:
        db.session.execute(text('SELECT 1'))
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection failed: {str(e)}', 500


@app.route('/authors', methods = ['GET'])
def index():
  get_authors = Authors.query.all()
  author_schema = AuthorsSchema(many=True)
  authors = author_schema.dump(get_authors)
  
  return make_response(jsonify({"authors": authors}))

@app.route('/authors', methods = ['POST'])
def create_author():
  data = request.get_json()
  author_schema = AuthorsSchema()
  new_author =author_schema.load(data)
  db.session.add(new_author)
  db.session.commit()
  result = author_schema.dump(new_author)
#  result = author_schema.dump(author.create()).data
  return make_response(jsonify({"author": result}),200)

@app.route('/authors/<id>', methods = ['GET'])
def get_author_by_id(id):
  get_author = Authors.query.get(id)
  author_schema = AuthorsSchema()
  author = author_schema.dump(get_author)
  return make_response(jsonify({"author": author}))

@app.route('/authors/<id>', methods = ['DELETE'])
def delete_author_by_id(id):
  get_author = Authors.query.get(id)
  db.session.delete(get_author)
  db.session.commit()
  return make_response("",204)

##
if __name__ == "__main__":
  app.run(debug=True)
