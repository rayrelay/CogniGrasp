# CogniGrasp

# CogniGrasp Development Setup

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Setting up the development environment

### Option 1: Using virtualenv (recommended)

1. Clone the repository
2. Run the setup script:
   - Linux/Mac: `./setup_venv.sh`
   - Windows: `.\setup_venv.ps1` or `setup_venv.bat`
3. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `.\venv\Scripts\Activate.ps1` or `venv\Scripts\activate.bat`
4. Copy environment variables:
   - `cp .env.example .env`
   - Edit `.env` with your configuration

### Option 2: Using Pipenv

1. Install Pipenv: `pip install pipenv`
2. Install dependencies: `pipenv install`
3. Activate environment: `pipenv shell`

## Running the application

1. Make sure the virtual environment is activated
2. Run: `python run.py` or `flask run`
3. Open http://localhost:5000 in your browser

## Running tests

1. Install test dependencies: `pip install pytest pytest-flask coverage`
2. Run tests: `pytest` or `python -m pytest`

## Project structure
