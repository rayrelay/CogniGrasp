from flask import current_app
from models import db, StudyMaterial, UserInteraction, SubjectConfig
import json
from datetime import datetime, timedelta
import random


class DatabaseManager:
    @staticmethod
    def init_app(app):
        db.init_app(app)
        with app.app_context():
            db.create_all()
            # Initialize with sample data if needed
            DatabaseManager._init_subject_configs()
            if not StudyMaterial.query.first():
                DatabaseManager._add_sample_data()

    @staticmethod
    def _init_subject_configs():
        """Initialize subject configurations"""
        if SubjectConfig.query.first():
            return  # Already initialized

        subject_configs = [
            {
                'subject_name': 'math',
                'summary_template': "Mathematical Concept Analysis:\n- Identified core mathematical principles in the text\n- Extracted key formulas and equations\n- Highlighted problem-solving approaches\n- Recommended practice exercises on related topics",
                'flashcards': [
                    "Key Formula: Quadratic Equation - x = [-b ± √(b² - 4ac)] / 2a",
                    "Concept: Derivatives measure the rate of change of a function",
                    "Technique: Factorize polynomials to simplify equations"
                ],
                'variations': [
                    "Based on cognitive science principles, I've organized this information for optimal learning.",
                    "Using mathematical modeling techniques, I've extracted the most important formulas for study.",
                    "Leveraging educational research, I've created study materials that enhance mathematical understanding."
                ]
            },
            {
                'subject_name': 'history',
                'summary_template': "Historical Context Analysis:\n- Identified key historical events and figures\n- Established chronological timeline\n- Highlighted cause-and-effect relationships\n- Connected to broader historical themes",
                'flashcards': [
                    "Event: World War II (1939-1945) - Global conflict involving most nations",
                    "Concept: The Renaissance - Cultural and intellectual revival in Europe",
                    "Figure: Napoleon Bonaparte - French military leader and emperor"
                ],
                'variations': [
                    "Based on historical analysis methods, I've organized this information chronologically.",
                    "Using historical research techniques, I've identified the most significant events.",
                    "Leveraging historical context, I've created study materials that enhance understanding of timelines."
                ]
            },
            {
                'subject_name': 'science',
                'summary_template': "Scientific Principles Analysis:\n- Identified core scientific concepts and laws\n- Explained natural phenomena described\n- Connected to fundamental scientific principles\n- Suggested related experiments or observations",
                'flashcards': [
                    "Law: Newton's First Law - Objects at rest stay at rest, objects in motion stay in motion",
                    "Concept: Photosynthesis - Process by which plants convert light to energy",
                    "Term: Atom - Basic unit of matter consisting of nucleus and electrons"
                ],
                'variations': [
                    "Based on scientific methodology, I've organized this information systematically.",
                    "Using scientific analysis techniques, I've identified the fundamental principles.",
                    "Leveraging experimental data, I've created study materials that enhance scientific understanding."
                ]
            },
            {
                'subject_name': 'programming',
                'summary_template': "Programming Concepts Analysis:\n- Identified key programming paradigms and patterns\n- Extracted algorithms and data structures\n- Highlighted best practices and potential pitfalls\n- Suggested related coding exercises",
                'flashcards': [
                    "Concept: Object-Oriented Programming - Organizing code around objects rather than functions",
                    "Algorithm: Binary Search - Efficient search algorithm for sorted arrays",
                    "Term: API - Application Programming Interface for software communication"
                ],
                'variations': [
                    "Based on software engineering principles, I've organized this information for optimal learning.",
                    "Using code analysis techniques, I've identified the most important programming concepts.",
                    "Leveraging development best practices, I've created study materials that enhance coding skills."
                ]
            },
            {
                'subject_name': 'general',
                'summary_template': "General Knowledge Analysis:\n- Identified key concepts and relationships\n- Extracted main ideas and supporting details\n- Created structured knowledge representation\n- Generated study aids for improved retention",
                'flashcards': [
                    "Study Tip: Use spaced repetition for better long-term memory",
                    "Technique: Create mind maps to visualize connections between ideas",
                    "Concept: The forgetting curve shows how information is lost over time"
                ],
                'variations': [
                    "Based on cognitive science principles, I've organized this information for optimal learning.",
                    "Using natural language processing, I've extracted the most important concepts for study.",
                    "Leveraging educational psychology research, I've created study materials that enhance retention.",
                    "Applying machine learning algorithms, I've identified patterns and relationships in the content."
                ]
            }
        ]

        for config in subject_configs:
            subject_config = SubjectConfig(
                subject_name=config['subject_name'],
                summary_template=config['summary_template'],
                flashcards=json.dumps(config['flashcards']),
                variations=json.dumps(config['variations'])
            )
            db.session.add(subject_config)

        db.session.commit()

    @staticmethod
    def _add_sample_data():
        """Add sample data for testing and demonstration"""
        sample_data = [
            {
                'input_text': 'The quadratic formula is x = [-b ± √(b² - 4ac)] / 2a. It is used to find the roots of quadratic equations.',
                'subject': 'math',
                'summary': 'Mathematical Concept Analysis:\n- Identified core mathematical principles in the text\n- Extracted key formulas and equations\n- Highlighted problem-solving approaches\n- Recommended practice exercises on related topics\n\nBased on cognitive science principles, I\'ve organized this information for optimal learning.',
                'flashcards': [
                    "Key Formula: Quadratic Equation - x = [-b ± √(b² - 4ac)] / 2a",
                    "Concept: Derivatives measure the rate of change of a function",
                    "Technique: Factorize polynomials to simplify equations"
                ],
                'review_dates': [
                    (datetime.utcnow() + timedelta(hours=6)).strftime("%Y-%m-%d %H:00"),
                    (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:00"),
                    (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d %H:00"),
                    (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:00")
                ]
            },
            {
                'input_text': 'World War II was a global war that lasted from 1939 to 1945. It involved the vast majority of the world\'s countries forming two opposing military alliances: the Allies and the Axis.',
                'subject': 'history',
                'summary': 'Historical Context Analysis:\n- Identified key historical events and figures\n- Established chronological timeline\n- Highlighted cause-and-effect relationships\n- Connected to broader historical themes\n\nUsing natural language processing, I\'ve extracted the most important concepts for study.',
                'flashcards': [
                    "Event: World War II (1939-1945) - Global conflict involving most nations",
                    "Concept: The Renaissance - Cultural and intellectual revival in Europe",
                    "Figure: Napoleon Bonaparte - French military leader and emperor"
                ],
                'review_dates': [
                    (datetime.utcnow() + timedelta(hours=6)).strftime("%Y-%m-%d %H:00"),
                    (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d %H:00"),
                    (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d %H:00"),
                    (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d %H:00")
                ]
            }
        ]

        for data in sample_data:
            material = StudyMaterial(
                input_text=data['input_text'],
                subject=data['subject'],
                summary=data['summary'],
                flashcards=json.dumps(data['flashcards']),
                review_dates=json.dumps(data['review_dates'])
            )
            db.session.add(material)

        db.session.commit()

    @staticmethod
    def get_subject_config(subject_name):
        """Get configuration for a specific subject"""
        config = SubjectConfig.query.filter_by(subject_name=subject_name).first()
        if config:
            return {
                'summary_template': config.summary_template,
                'flashcards': json.loads(config.flashcards),
                'variations': json.loads(config.variations)
            }
        # Fallback to general if subject not found
        general_config = SubjectConfig.query.filter_by(subject_name='general').first()
        if general_config:
            return {
                'summary_template': general_config.summary_template,
                'flashcards': json.loads(general_config.flashcards),
                'variations': json.loads(general_config.variations)
            }
        return None

    @staticmethod
    def save_material(input_text, subject, summary, flashcards, review_dates):
        """Save processed study material to database"""
        material = StudyMaterial(
            input_text=input_text,
            subject=subject,
            summary=summary,
            flashcards=json.dumps(flashcards),
            review_dates=json.dumps(review_dates)
        )
        db.session.add(material)
        db.session.commit()
        return material.id

    @staticmethod
    def log_interaction(material_id, interaction_type, interaction_data=None):
        """Log user interaction with study materials"""
        interaction = UserInteraction(
            material_id=material_id,
            interaction_type=interaction_type,
            interaction_data=json.dumps(interaction_data) if interaction_data else None
        )
        db.session.add(interaction)
        db.session.commit()

    @staticmethod
    def get_recent_materials(limit=10):
        """Get recently processed materials"""
        return StudyMaterial.query.order_by(StudyMaterial.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_material_by_id(material_id):
        """Get material by ID"""
        return StudyMaterial.query.get(material_id)

    @staticmethod
    def get_materials_by_subject(subject, limit=10):
        """Get materials by subject"""
        return StudyMaterial.query.filter_by(subject=subject).order_by(
            StudyMaterial.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_interaction_stats():
        """Get statistics about user interactions"""
        stats = {
            'total_materials': StudyMaterial.query.count(),
            'total_interactions': UserInteraction.query.count(),
            'interactions_by_type': {},
            'materials_by_subject': {}
        }

        # Count interactions by type
        interaction_types = db.session.query(
            UserInteraction.interaction_type,
            db.func.count(UserInteraction.id)
        ).group_by(UserInteraction.interaction_type).all()

        for type_name, count in interaction_types:
            stats['interactions_by_type'][type_name] = count

        # Count materials by subject
        subject_counts = db.session.query(
            StudyMaterial.subject,
            db.func.count(StudyMaterial.id)
        ).group_by(StudyMaterial.subject).all()

        for subject, count in subject_counts:
            stats['materials_by_subject'][subject] = count

        return stats