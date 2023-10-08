import os

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
db = SQLAlchemy(app)


class Example(db.Model):
    __tablename__ = 'example'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


@app.route('/')
def index():
    examples = Example.query.order_by("id").all()
    return send_from_directory('templates', 'index.html')


from sqlalchemy import asc

ITEMS_PER_PAGE = 20

@app.route('/examples', methods=['GET'])
def get_examples():
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * ITEMS_PER_PAGE
    examples = db.session.query(Example).order_by(asc(Example.id)).limit(ITEMS_PER_PAGE).offset(offset).all()
    
    total_examples = db.session.query(Example).count()
    total_pages = (total_examples // ITEMS_PER_PAGE) + (1 if total_examples % ITEMS_PER_PAGE else 0)
    
    examples_list = [{"id": example.id, "name": example.name} for example in examples]

    return jsonify({
        'examples': examples_list,
        'total_pages': total_pages
    })



@app.route('/examples', methods=['POST'])
def create_example():
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400

    example = Example(name=data['name'])
    db.session.add(example)
    try:
        db.session.commit()
        return jsonify({'message': 'Example created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create example', 'error': str(e)}), 500

@app.route('/examples/<int:id>', methods=['DELETE'])
def delete_example(id):
    try:
        example = Example.query.filter_by(id=id).one()
        db.session.delete(example)
        db.session.commit()
        return '', 204  # Return 204 No Content on successful deletion
    except NoResultFound:
        return jsonify({'message': 'Example not found'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete example', 'error': str(e)}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
