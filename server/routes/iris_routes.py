# server/routes/iris_routes.py
from flask import Blueprint, jsonify
import subprocess
import os

iris_bp = Blueprint('iris', __name__)

@iris_bp.route('/register', methods=['POST'])
def iris_register_route():
    try:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'convert_iris.py'))
        conda_prefix = os.environ.get('CONDA_PREFIX')
        if conda_prefix:
            python_path = os.path.join(conda_prefix, 'bin', 'python')
        else:
            # fallback to system python
            python_path = 'python'  # or 'python3' depending on your OS

        result = subprocess.run([python_path, script_path], capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Iris registered successfully'})
        else:
            return jsonify({'success': False, 'message': result.stderr or 'Iris registration failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@iris_bp.route('/verify', methods=['POST'])
def iris_verify_route():
    import subprocess
    import os

    try:
        # Step 1: Capture iris live
        capture_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'save_live.py'))
        match_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'match.py'))
        conda_prefix = os.environ.get('CONDA_PREFIX')
        if conda_prefix:
            python_path = os.path.join(conda_prefix, 'bin', 'python')
        else:
            # fallback to system python
            python_path = 'python'  # or 'python3' depending on your OS

        # Run webcam capture
        capture_result = subprocess.run([python_path, capture_script], capture_output=True, text=True)
        if capture_result.returncode != 0:
            return jsonify({'success': False, 'message': 'Failed to capture iris image'})

        # Run match.py
        match_result = subprocess.run([python_path, match_script], capture_output=True, text=True)
        if match_result.returncode == 0:
            return jsonify({'success': True, 'message': 'Iris matched'})
        else:
            return jsonify({'success': False, 'message': 'Iris does not match'})

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
