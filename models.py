from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class SubjectConfig(db.Model):
    """存储不同学科的配置数据"""
    __tablename__ = 'subject_configs'

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(50), unique=True, nullable=False)
    summary_template = db.Column(db.Text, nullable=False)
    flashcards = db.Column(db.Text, nullable=False)  # JSON string
    variations = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SubjectConfig {self.subject_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'subject_name': self.subject_name,
            'summary_template': self.summary_template,
            'flashcards': json.loads(self.flashcards),
            'variations': json.loads(self.variations),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class StudyMaterial(db.Model):
    __tablename__ = 'study_materials'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    flashcards = db.Column(db.Text, nullable=False)  # JSON string
    review_dates = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<StudyMaterial {self.id} - {self.subject}>'

    def to_dict(self):
        return {
            'id': self.id,
            'input_text': self.input_text,
            'subject': self.subject,
            'summary': self.summary,
            'flashcards': json.loads(self.flashcards),
            'review_dates': json.loads(self.review_dates),
            'created_at': self.created_at.isoformat(),
            'processed_at': self.processed_at.isoformat()
        }


class UserInteraction(db.Model):
    __tablename__ = 'user_interactions'

    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('study_materials.id'))
    interaction_type = db.Column(db.String(50), nullable=False)  # e.g., 'view', 'export', 'share'
    interaction_data = db.Column(db.Text)  # Additional data as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserInteraction {self.id} - {self.interaction_type}>'