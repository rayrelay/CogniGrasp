import os
from cognigrasp_demo import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    app.run(host=host, port=port, debug=debug)