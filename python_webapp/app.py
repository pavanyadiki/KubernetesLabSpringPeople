from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello_world"


@app.route('/environ')
def environment():
    import os
    response = "<h1>Environment Variables</h1><table><tbody>"
    for key, value in os.environ.items():
        if callable(value) or key == 'LS_COLORS':
            continue
        response += "<tr><td>%s</td><td>%s</td></tr>" % (key, value)
    response += "</tbody></table><br><h1>Installed Packages</h1>"
    packages = os.popen("pip freeze").read().split('\n')
    for package in packages:
        response += package + '<br>'
    return response


@app.route('/dns')
def dns():
    domain = request.args.get('search')
    if not domain:
        return '<h1>Please provide domain name in search in query params.</h1>'
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib2 import urlopen
    apiKey = 'at_NMNivTXiYDo33KkP9l0j5WGWbFXBi'

    url = 'https://www.whoisxmlapi.com/whoisserver/DNSService?apiKey=%s&domainName=%s&type=1&outputFormat=json' % ( # noqa
        apiKey, domain)
    response = urlopen(url)

    import json
    data = json.loads(response.read().decode('utf8'))

    response = "<h1>DNS Records for %s</h1><table><tr><th>Record Type</th><th>Record Data</th></tr>" % domain # noqa
    for record in data['DNSData']['dnsRecords']:
        if record['dnsType'] == 'A':
            record_data = record['address']
        else:
            if 'rawText' not in record:
                continue
            record_data = record['rawText']
        response += '<tr><td>%s</td><td>%s</td></tr>' % (
            record['dnsType'], record_data)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')