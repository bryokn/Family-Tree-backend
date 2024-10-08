from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    death_date = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    photo = db.Column(db.String(255), nullable=True)
    biography = db.Column(db.Text, nullable=True)

    # Updated relationships
    parent_relationships = db.relationship('ParentChild', foreign_keys='ParentChild.child_id', backref='child')
    child_relationships = db.relationship('ParentChild', 
                                          primaryjoin="or_(People.id==ParentChild.parent1_id, People.id==ParentChild.parent2_id)",
                                          backref='parents')

    def __repr__(self):
        return f"<People(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': str(self.birth_date) if self.birth_date else None,
            'death_date': str(self.death_date) if self.death_date else None,
            'gender': self.gender,
            'photo': self.photo,
            'biography': self.biography
        }
        
class ParentChild(db.Model):
    __tablename__ = 'parent_child'
    id = db.Column(db.Integer, primary_key=True)
    parent1_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    parent2_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)  # Allow for single parent families
    child_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    parent1 = db.relationship('People', foreign_keys=[parent1_id])
    parent2 = db.relationship('People', foreign_keys=[parent2_id])

    def __repr__(self):
        return f"<ParentChild(parent1_id={self.parent1_id}, parent2_id={self.parent2_id}, child_id={self.child_id})>"

    def serialize(self):
        return {
            'id': self.id,
            'parent1_id': self.parent1_id,
            'parent2_id': self.parent2_id,
            'child_id': self.child_id
        }

class Relationship(db.Model):
    __tablename__ = 'relationships'
    id = db.Column(db.Integer, primary_key=True)
    person1_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    person2_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    relationship_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Relationship(person1_id={self.person1_id}, person2_id={self.person2_id}, type='{self.relationship_type}')>"

    def serialize(self):
        return {
            'id': self.id,
            'person1_id': self.person1_id,
            'person2_id': self.person2_id,
            'relationship_type': self.relationship_type
        }

class Marriage(db.Model):
    __tablename__ = 'marriages'
    id = db.Column(db.Integer, primary_key=True)
    husband_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    wife_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    marriage_date = db.Column(db.Date, nullable=True)
    divorce_date = db.Column(db.Date, nullable=True)

    husband = db.relationship('People', foreign_keys=[husband_id])
    wife = db.relationship('People', foreign_keys=[wife_id])

    def __repr__(self):
        return f"<Marriage(id={self.id}, husband_id={self.husband_id}, wife_id={self.wife_id}, marriage_date='{self.marriage_date}', divorce_date='{self.divorce_date}')>"

    def serialize(self):
        return {
            'id': self.id,
            'husband_id': self.husband_id,
            'wife_id': self.wife_id,
            'marriage_date': str(self.marriage_date) if self.marriage_date else None,
            'divorce_date': str(self.divorce_date) if self.divorce_date else None
        }
