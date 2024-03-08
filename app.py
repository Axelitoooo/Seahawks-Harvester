import json
import os

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/results', methods=['GET', 'POST'])
def show_results():
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
    selected_file = request.form.get('selected_file')

    if selected_file:
        file_path = os.path.join(data_folder, selected_file)
        with open(file_path, 'r') as file:
            results = json.load(file)
    else:
        results = None

    return render_template('results.html', files=files, results=results)


@app.route('/check-update', methods=['GET'])
def check_update():
    data_folder = os.path.join(os.path.dirname(__file__), 'data')
    most_recent_file = max([os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith('.json')],
                           default=None, key=os.path.getmtime)
    if most_recent_file:
        return jsonify({"update": True, "file": os.path.basename(most_recent_file),
                        "timestamp": os.path.getmtime(most_recent_file)})
    return jsonify({"update": False})


if __name__ == '__main__':
    app.run(debug=True)
