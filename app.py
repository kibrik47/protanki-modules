from flask import Flask, render_template, jsonify
import modules

app = Flask(__name__)


@app.route('/')
def index():
    # Pass the turret mapping (numbers -> names) into the template
    return render_template('index.html', turrets=modules.turret_map)


@app.route('/get_missing_turrets/<int:turret_num>')
def get_missing_turrets(turret_num):
    turret_name = modules.turret_map.get(turret_num)
    if not turret_name:
        return jsonify({'error': 'Invalid turret number'}), 400
    try:
        missing = modules.find_missing_turrets(turret_name)
        # Convert to a sorted list for predictable client-side output
        return jsonify(sorted(list(missing)))
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the app on all interfaces so it's reachable from outside the container
    # (Inside Docker you must bind to 0.0.0.0 to accept external connections.)
    app.run(host='0.0.0.0', port=5000, debug=True)
