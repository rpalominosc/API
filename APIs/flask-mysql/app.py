from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy 
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields
import pymysql, mariadb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:Polux9leo@127.0.0.1:3306/duoc'

#def create_app():
#    app= Flask(__name__)
#    with app.app_context():
#      init_db()
#
#    return app

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
    return '<Author %d>' % self.id

with app.app_context():db.create_all()

class AuthorsSchema(SQLAlchemySchema):
  class Meta(SQLAlchemySchema.Meta):
    model = Authors
    sqla_session = db.session
  
  id = fields.Number(dump_only=True)
  name = fields.String(required=True)
  specialisation = fields.String(required=True)

@app.route('/authors', methods = ['GET'])
def index():
  get_authors = Authors.query.all()
  author_schema = AuthorsSchema(many=True)
  authors, error = author_schema.dump(get_authors)
  return make_response(jsonify({"authors": authors}))

@app.route('/authors', methods = ['POST'])
def create_author():
  data = request.get_json()
  author_schema = AuthorsSchema()
  author, error = author_schema.load(data)
  result = author_schema.dump(author.create()).data
  return make_response(jsonify({"author": result}),200)

##
if __name__ == "__main__":
  app.run(debug=True)
