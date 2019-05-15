import json
import datetime

from flask import Flask, request, jsonify


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        data = request.json
        data['source_ip'] = request.remote_addr
        data['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        with open('data.json', 'r') as f:
            data_ext = json.load(f)
        data_ext['messages'].append(data)
        with open('data.json', 'w') as f:
            json.dump(data_ext, f)
        return 'success'
    else:
        with open('data.json', 'r') as f:
            data = json.load(f)
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per-page', 20))
        per_page = 100 if per_page > 100 else per_page
        messages = data['messages']
        pagination = [messages[i:i+per_page] for i in range(0, len(messages), per_page)]
        results = {}
        results['messages'] = pagination[page-1] if page <= len(pagination) else []
        if results['messages']:
            results['total_count'] = len(results['messages'])
        return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
