from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('cognigrasp_index.html')


@app.route('/process', methods=['POST'])
def process():
    study_material = request.form['study_material']
    # Simulate AI processing - in a real app, this would call NLP services
    summary = f"AI-generated summary for: {study_material}"
    flashcards = [f"Flashcard 1 about {study_material}", f"Flashcard 2 about {study_material}"]

    return render_template('cognigrasp_results.html',
                           summary=summary,
                           flashcards=flashcards,
                           original_input=study_material)


if __name__ == '__main__':
    app.run(debug=True, port=5000)