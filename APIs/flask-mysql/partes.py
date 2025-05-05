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

@app.route('/authors/<id>', methods = ['GET'])
def get_author_by_id(id):
  get_author = Authors.query.get(id)
  author_schema = AuthorsSchema()
  author, error = author_schema.dump(get_author)
  return make_response(jsonify({"author": author}))

@app.route('/authors/<id>', methods = ['PUT'])
def update_author_by_id(id):
  data = request.get_json()
  get_author = Authors.query.get(id)
  if data.get('specialisation'):
    get_author.specialisation = data['specialisation']
  if data.get('name'):
    get_author.name = data['name']

  db.session.add(get_author)
  db.session.commit()
  author_schema = AuthorsSchema(only=['id', 'name', 'specialisation'])
  author, error = author_schema.dump(get_author)
  return make_response(jsonify({"author": author}))

@app.route('/authors/<id>', methods = ['DELETE'])
def delete_author_by_id(id):
  get_author = Authors.query.get(id)
  db.session.delete(get_author)
  db.session.commit()
  return make_response("",204)

@app.route('/authors', methods = ['POST'])
def create_author():
  data = request.get_json()
  author_schema = AuthorsSchema()
  author, error = author_schema.load(data)
  result = author_schema.dump(author.create()).data
  return make_response(jsonify({"author": result}),200)


if __name__ == "__main__":
  app.run(debug=True)
