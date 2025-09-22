from flask import Flask, render_template, request
import random
import re
from datetime import datetime, timedelta

app = Flask(__name__)


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

    # 根据学科生成不同的摘要和闪卡
    if subject == "math":
        summary = f"Mathematical Concept Analysis:\n- Identified core mathematical principles in the text\n- Extracted key formulas and equations\n- Highlighted problem-solving approaches\n- Recommended practice exercises on related topics"
        flashcards = [
            "Key Formula: Quadratic Equation - x = [-b ± √(b² - 4ac)] / 2a",
            "Concept: Derivatives measure the rate of change of a function",
            "Technique: Factorize polynomials to simplify equations"
        ]
    elif subject == "history":
        summary = f"Historical Context Analysis:\n- Identified key historical events and figures\n- Established chronological timeline\n- Highlighted cause-and-effect relationships\n- Connected to broader historical themes"
        flashcards = [
            "Event: World War II (1939-1945) - Global conflict involving most nations",
            "Concept: The Renaissance - Cultural and intellectual revival in Europe",
            "Figure: Napoleon Bonaparte - French military leader and emperor"
        ]
    elif subject == "science":
        summary = f"Scientific Principles Analysis:\n- Identified core scientific concepts and laws\n- Explained natural phenomena described\n- Connected to fundamental scientific principles\n- Suggested related experiments or observations"
        flashcards = [
            "Law: Newton's First Law - Objects at rest stay at rest, objects in motion stay in motion",
            "Concept: Photosynthesis - Process by which plants convert light to energy",
            "Term: Atom - Basic unit of matter consisting of nucleus and electrons"
        ]
    elif subject == "programming":
        summary = f"Programming Concepts Analysis:\n- Identified key programming paradigms and patterns\n- Extracted algorithms and data structures\n- Highlighted best practices and potential pitfalls\n- Suggested related coding exercises"
        flashcards = [
            "Concept: Object-Oriented Programming - Organizing code around objects rather than functions",
            "Algorithm: Binary Search - Efficient search algorithm for sorted arrays",
            "Term: API - Application Programming Interface for software communication"
        ]
    else:
        summary = f"General Knowledge Analysis:\n- Identified key concepts and relationships\n- Extracted main ideas and supporting details\n- Created structured knowledge representation\n- Generated study aids for improved retention"
        flashcards = [
            "Study Tip: Use spaced repetition for better long-term memory",
            "Technique: Create mind maps to visualize connections between ideas",
            "Concept: The forgetting curve shows how information is lost over time"
        ]

    # 添加一些随机性使结果看起来更自然
    variations = [
        "Based on cognitive science principles, I've organized this information for optimal learning.",
        "Using natural language processing, I've extracted the most important concepts for study.",
        "Leveraging educational psychology research, I've created study materials that enhance retention.",
        "Applying machine learning algorithms, I've identified patterns and relationships in the content."
    ]

    summary += f"\n\n{random.choice(variations)}"

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
    return render_template('cognigrasp_index_demo.html')


@app.route('/process', methods=['POST'])
def process():
    study_material = request.form['study_material']

    # 如果输入为空，返回错误
    if not study_material.strip():
        return render_template('cognigrasp_index_demo.html', error="Please enter some study material.")

    # 生成AI响应
    ai_response = generate_ai_response(study_material)

    return render_template('cognigrasp_results_demo.html',
                           summary=ai_response["summary"],
                           flashcards=ai_response["flashcards"],
                           subject=ai_response["subject"],
                           review_dates=ai_response["review_dates"],
                           original_input=study_material)


if __name__ == '__main__':
    app.run(debug=True)