import pytest
from cognigrasp_demo import app as flask_app, db
from models import StudyMaterial, UserInteraction, SubjectConfig
import json


@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with flask_app.app_context():
        db.create_all()

        # 添加测试数据
        test_material = StudyMaterial(
            input_text="Test input text",
            subject="math",
            summary="Test summary",
            flashcards=json.dumps(["Flashcard 1", "Flashcard 2"]),
            review_dates=json.dumps(["2023-01-01 10:00", "2023-01-02 10:00"])
        )
        db.session.add(test_material)

        # 添加学科配置测试数据
        math_config = SubjectConfig(
            subject_name="math",
            summary_template="Math summary template",
            flashcards=json.dumps(["Math flashcard 1", "Math flashcard 2"]),
            variations=json.dumps(["Math variation 1", "Math variation 2"])
        )
        db.session.add(math_config)

        db.session.commit()

        yield flask_app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()