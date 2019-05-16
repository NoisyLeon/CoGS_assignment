import json
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        with open('data.json', 'r') as f:
            data= json.load(f)
        page                = int(request.args.get('page', 1)) # default page = 1
        per_page            = int(request.args.get('per_page', 20)) # default per_page = 20
        per_page            = 100 if per_page > 100 else per_page # max per_page = 100
        messages            = data['messages']
        pagination          = [messages[i:i+per_page] for i in range(0, len(messages), per_page)]
        results             = {}
        results['messages'] = pagination[page-1] if page <= len(pagination) else []
        if results['messages']:
            results['total_count'] = len(results['messages'])
        return jsonify(results)
    elif request.method == 'POST':
        data                = request.json
        data['source_ip']   = request.remote_addr
        data['timestamp']   = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        try:
            with open('data.json', 'r') as f:
                data_ext        = json.load(f)
        except FileNotFoundError:
            data_ext            = {}
            data_ext['messages']= []    
        data_ext['messages'].append(data)
        with open('data.json', 'w') as f:
            json.dump(data_ext, f)
        return 'success'


if __name__ == '__main__':
    app.run(debug=True)
