from flask import Flask, render_template, request, jsonify
import random
import re
import os
import json
from datetime import datetime, timedelta
from models import db
from database import DatabaseManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 从环境变量获取配置，否则使用默认值
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///cognigrasp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Initialize database
DatabaseManager.init_app(app)


# 模拟不同学科的知识处理
def generate_ai_response(text):
    text_lower = text.lower()

    # 检测学科类型
    subject = "general"
    if any(word in text_lower for word in ["math", "calculate", "equation", "algebra", "calculus"]):
        subject = "math"
    elif any(word in text_lower for word in ["history", "war", "king", "century", "ancient"]):
        subject = "history"
    elif any(word in text_lower for word in ["science", "physics", "chemistry", "biology", "atom"]):
        subject = "science"
    elif any(word in text_lower for word in ["programming", "code", "python", "java", "algorithm"]):
        subject = "programming"

    # 从数据库获取学科配置
    subject_config = DatabaseManager.get_subject_config(subject)
    if not subject_config:
        # 如果找不到配置，使用默认值
        subject_config = {
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

    # 使用数据库中的配置生成响应
    summary = subject_config['summary_template']
    flashcards = subject_config['flashcards']

    # 添加随机变体
    summary += f"\n\n{random.choice(subject_config['variations'])}"

    # 生成复习计划
    now = datetime.now()
    review_dates = [
        (now + timedelta(hours=6)).strftime("%Y-%m-%d %H:00"),
        (now + timedelta(days=1)).strftime("%Y-%m-%d %H:00"),
        (now + timedelta(days=3)).strftime("%Y-%m-%d %H:00"),
        (now + timedelta(days=7)).strftime("%Y-%m-%d %H:00")
    ]

    return {
        "summary": summary,
        "flashcards": flashcards,
        "subject": subject,
        "review_dates": review_dates
    }


@app.route('/')
def index():
    return render_template('cognigrasp_index.html')


@app.route('/process', methods=['POST'])
def process():
    study_material = request.form['study_material']

    # 如果输入为空，返回错误
    if not study_material.strip():
        return render_template('cognigrasp_index.html', error="Please enter some study material.")

    # 生成AI响应
    ai_response = generate_ai_response(study_material)

    # Save to database
    material_id = DatabaseManager.save_material(
        study_material,
        ai_response["subject"],
        ai_response["summary"],
        ai_response["flashcards"],
        ai_response["review_dates"]
    )

    # Log the processing interaction
    DatabaseManager.log_interaction(material_id, "process")

    return render_template('cognigrasp_results.html',
                           summary=ai_response["summary"],
                           flashcards=ai_response["flashcards"],
                           subject=ai_response["subject"],
                           review_dates=ai_response["review_dates"],
                           original_input=study_material,
                           material_id=material_id)


@app.route('/api/materials', methods=['GET'])
def api_get_materials():
    """API endpoint to get processed materials"""
    limit = request.args.get('limit', 10, type=int)
    subject = request.args.get('subject', None)

    if subject:
        materials = DatabaseManager.get_materials_by_subject(subject, limit)
    else:
        materials = DatabaseManager.get_recent_materials(limit)

    return jsonify([material.to_dict() for material in materials])


@app.route('/api/materials/<int:material_id>', methods=['GET'])
def api_get_material(material_id):
    """API endpoint to get a specific material"""
    material = DatabaseManager.get_material_by_id(material_id)
    if not material:
        return jsonify({'error': 'Material not found'}), 404

    # Log the view interaction
    DatabaseManager.log_interaction(material_id, "api_view")

    return jsonify(material.to_dict())


@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    """API endpoint to get usage statistics"""
    stats = DatabaseManager.get_interaction_stats()
    return jsonify(stats)


@app.route('/api/interaction', methods=['POST'])
def api_log_interaction():
    """API endpoint to log user interactions"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        material_id = data.get('material_id')
        interaction_type = data.get('interaction_type')

        if not material_id or not interaction_type:
            return jsonify({'error': 'Missing required fields'}), 400

        # Log the interaction
        DatabaseManager.log_interaction(material_id, interaction_type, data)

        return jsonify({'status': 'success', 'message': 'Interaction logged'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/material/<int:material_id>', methods=['GET'])
def view_material(material_id):
    """View a previously processed material"""
    material = DatabaseManager.get_material_by_id(material_id)
    if not material:
        return render_template('cognigrasp_index.html', error="Material not found.")

    # Log the view interaction
    DatabaseManager.log_interaction(material_id, "view")

    return render_template('cognigrasp_results.html',
                           summary=material.summary,
                           flashcards=json.loads(material.flashcards),
                           subject=material.subject,
                           review_dates=json.loads(material.review_dates),
                           original_input=material.input_text,
                           material_id=material_id)


@app.route('/api/subject-configs', methods=['GET'])
def api_get_subject_configs():
    """API endpoint to get all subject configurations"""
    configs = SubjectConfig.query.all()
    return jsonify([config.to_dict() for config in configs])


@app.route('/api/subject-configs/<string:subject_name>', methods=['GET'])
def api_get_subject_config(subject_name):
    """API endpoint to get a specific subject configuration"""
    config = SubjectConfig.query.filter_by(subject_name=subject_name).first()
    if not config:
        return jsonify({'error': 'Subject configuration not found'}), 404

    return jsonify(config.to_dict())


@app.route('/api/subject-configs/<string:subject_name>', methods=['PUT'])
def api_update_subject_config(subject_name):
    """API endpoint to update a subject configuration"""
    try:
        config = SubjectConfig.query.filter_by(subject_name=subject_name).first()
        if not config:
            return jsonify({'error': 'Subject configuration not found'}), 404

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if 'summary_template' in data:
            config.summary_template = data['summary_template']
        if 'flashcards' in data:
            config.flashcards = json.dumps(data['flashcards'])
        if 'variations' in data:
            config.variations = json.dumps(data['variations'])

        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Subject configuration updated'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)