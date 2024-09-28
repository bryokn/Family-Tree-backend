from flask import Flask, jsonify, request
from .models import db, People, Relationship, Marriage, ParentChild

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/people', methods=['GET', 'POST'])
def people():
    if request.method == 'GET':
        people = People.query.all()
        return jsonify([person.serialize() for person in people])
    elif request.method == 'POST':
        data = request.get_json()
        person = People(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            death_date=data['death_date'],
            gender=data['gender'],
            photo=data['photo'],
            biography=data['biography']
        )
        db.session.add(person)
        db.session.commit()
        return jsonify(person.serialize()), 201
    
@app.route('/relationships', methods=['GET', 'POST'])
def relationships():
    if request.method == 'GET':
        relationships = Relationship.query.all()
        return jsonify([relationship.serialize() for relationship in relationships])
    elif request.method == 'POST':
        data = request.get_json()
        relationship = Relationship(
            person1_id=data['person1_id'],
            person2_id=data['person2_id'],
            relationship_type=data['relationship_type']
        )
        db.session.add(relationship)
        db.session.commit()
        return jsonify(relationship.serialize()), 201
    
# @app.route('/relationships', methods=['GET', 'POST'])
# def relationships():
#     if request.method == 'GET':
#         relationships = Relationship.query.all()
#         return jsonify([relationship.serialize() for relationship in relationships])
#     elif request.method == 'POST':
#         data = request.get_json()
#         if data['relationship_type'] == 'Parent':
#             relationship = Relationship(
#                 parent_id=data['parent_id'],
#                 child_id=data['child_id'],
#                 relationship_type='Parent'
#             )
#         else:
#             relationship = Relationship(
#                 person1_id=data['person1_id'],
#                 person2_id=data['person2_id'],
#                 relationship_type=data['relationship_type']
#             )
#         db.session.add(relationship)
#         db.session.commit()
#         return jsonify(relationship.serialize()), 201

@app.route('/parent-child', methods=['POST'])
def add_parent_child():
    data = request.get_json()
    parent_child = ParentChild(
        parent1_id=data['parent1_id'],
        parent2_id=data.get('parent2_id'),  # This is optional
        child_id=data['child_id']
    )
    db.session.add(parent_child)
    db.session.commit()
    return jsonify(parent_child.serialize()), 201

@app.route('/people/<int:person_id>/parents', methods=['GET'])
def get_parents(person_id):
    person = People.query.get_or_404(person_id)
    parents = []
    for rel in person.parent_relationships:
        parents.append(rel.parent1.serialize())
        if rel.parent2:
            parents.append(rel.parent2.serialize())
    return jsonify(parents)

@app.route('/people/<int:person_id>/children', methods=['GET'])
def get_children(person_id):
    person = People.query.get_or_404(person_id)
    children = [rel.child.serialize() for rel in person.child_relationships]
    return jsonify(children)


# @app.route('/relationships', methods=['GET', 'POST'])
# def relationships():
#     if request.method == 'GET':
#         relationships = Relationship.query.all()
#         return jsonify([relationship.serialize() for relationship in relationships])
#     elif request.method == 'POST':
#         data = request.get_json()
#         relationship = Relationship(
#             person1_id=data['person1_id'],
#             person2_id=data['person2_id'],
#             relationship_type=data['relationship_type']
#         )
#         db.session.add(relationship)
#         db.session.commit()
#         return jsonify(relationship.serialize()), 201

#marriages routes
@app.route('/marriages', methods=['GET', 'POST'])
def marriages():
    if request.method == 'GET':
        marriages = Marriage.query.all()
        return jsonify([marriage.serialize() for marriage in marriages])
    elif request.method == 'POST':
        data = request.get_json()
        marriage = Marriage(
            husband_id=data['husband_id'],
            wife_id=data['wife_id'],
            marriage_date=data['marriage_date'],
            divorce_date=data['divorce_date']
        )
        db.session.add(marriage)
        db.session.commit()
        return jsonify(marriage.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)
