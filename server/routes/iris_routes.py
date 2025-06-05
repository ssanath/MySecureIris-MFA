from flask import Blueprint, jsonify
import subprocess
import os

iris_bp = Blueprint('iris', __name__)

@iris_bp.route('/iris-register', methods=['POST'])
def iris_register_route():
    try:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'convert_iris.py'))
        python_path = os.path.join(os.environ['CONDA_PREFIX'], 'bin', 'python')  # Ensure correct python

        result = subprocess.run([python_path, script_path], capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Iris registered successfully'})
        else:
            return jsonify({'success': False, 'message': result.stderr or 'Iris registration failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@iris_bp.route('/iris-verify', methods=['POST'])
def iris_verify_route():
    try:
        # Run the OpenCV script to capture live iris image (like save_live.py)
        capture_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'save_live.py'))
        python_path = os.path.join(os.environ['CONDA_PREFIX'], 'bin', 'python')

        capture_result = subprocess.run([python_path, capture_script], capture_output=True, text=True)
        if capture_result.returncode != 0:
            return jsonify({'success': False, 'message': 'Failed to capture iris image'})

        # Then run match.py to compare
        match_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'match.py'))
        match_result = subprocess.run([python_path, match_script], capture_output=True, text=True)

        if match_result.returncode == 0:
            return jsonify({'success': True, 'message': 'Iris verified successfully'})
        else:
            return jsonify({'success': False, 'message': 'Iris does not match'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
