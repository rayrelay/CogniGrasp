import pytest
import json
from unittest.mock import patch
from models import StudyMaterial, UserInteraction
from dotenv import load_dotenv

load_dotenv()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'CogniGrasp' in response.data


def test_process_empty_input(client):
    response = client.post('/process', data={'study_material': ''})
    assert response.status_code == 200
    assert b'Please enter some study material' in response.data


@patch('cognigrasp_demo.generate_ai_response')
def test_process_valid_input(mock_ai_response, client):
    mock_ai_response.return_value = {
        "summary": "Test summary",
        "flashcards": ["Flashcard 1", "Flashcard 2"],
        "subject": "math",
        "review_dates": ["2023-01-01 10:00", "2023-01-02 10:00"]
    }

    response = client.post('/process', data={'study_material': 'Test input'})
    assert response.status_code == 200
    assert b'Test summary' in response.data

    # 检查数据是否保存到数据库
    material = StudyMaterial.query.first()
    assert material is not None
    assert material.input_text == 'Test input'


def test_api_get_materials(client):
    response = client.get('/api/materials')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['subject'] == 'math'


def test_api_get_material(client):
    material = StudyMaterial.query.first()
    response = client.get(f'/api/materials/{material.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['subject'] == 'math'


def test_api_get_nonexistent_material(client):
    response = client.get('/api/materials/999')
    assert response.status_code == 404


def test_view_material(client):
    material = StudyMaterial.query.first()
    response = client.get(f'/material/{material.id}')
    assert response.status_code == 200
    assert b'Test summary' in response.data


def test_view_nonexistent_material(client):
    response = client.get('/material/999')
    assert response.status_code == 200
    assert b'Material not found' in response.data


def test_api_get_stats(client):
    # 添加一个交互记录
    material = StudyMaterial.query.first()
    interaction = UserInteraction(
        material_id=material.id,
        interaction_type="view"
    )
    from cognigrasp_demo import db
    db.session.add(interaction)
    db.session.commit()

    response = client.get('/api/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['total_materials'] == 1
    assert data['total_interactions'] == 1


def test_api_log_interaction(client):
    material = StudyMaterial.query.first()

    response = client.post('/api/interaction',
                           json={
                               'material_id': material.id,
                               'interaction_type': 'test_interaction'
                           }
                           )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'

    # 检查交互是否被记录
    interaction = UserInteraction.query.first()
    assert interaction is not None
    assert interaction.interaction_type == 'test_interaction'


def test_api_log_interaction_missing_fields(client):
    response = client.post('/api/interaction',
                           json={'material_id': 1}  # 缺少 interaction_type
                           )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_api_log_interaction_invalid_json(client):
    response = client.post('/api/interaction',
                           data='invalid json',
                           content_type='application/json'
                           )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_api_get_subject_configs(client):
    response = client.get('/api/subject-configs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0  # 应该至少有一个配置


def test_api_get_subject_config(client):
    response = client.get('/api/subject-configs/math')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['subject_name'] == 'math'


def test_api_get_nonexistent_subject_config(client):
    # 测试获取不存在的学科配置
    response = client.get('/api/subject-configs/nonexistent')
    assert response.status_code == 404  # 应该返回 404
    data = json.loads(response.data)
    assert 'error' in data  # 响应中应该包含错误信息


def test_generate_ai_response():
    from cognigrasp_demo import generate_ai_response
    # 测试 generate_ai_response 使用数据库配置
    response = generate_ai_response("quadratic equation")
    assert response is not None
    assert response['subject'] == 'math'
    assert 'Mathematical Concept Analysis' in response['summary']