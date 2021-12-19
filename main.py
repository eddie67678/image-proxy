import datetime
import requests
from flask import request, send_file
import flask
import os
import json

app = flask.Flask(__name__)


@app.route('/api/images', methods=["GET"])
def proxy():
    try:
        url = request.args.get('url')

        img = hash(url)
        if os.path.exists(f'images/{str(img)}'):
            print("[" + str(datetime.datetime.now()) + "] URL Used Before - Returning Cached Image.")
            return send_file(f"images/{str(img)}.png",download_name= f"{str(img)}.png")

        else:
            print("[" + str(datetime.datetime.now()) + "] New URL - Downloading and Returning Image.")

            response = requests.get(url, headers={"user-agent" : "Mozzila/5.0"})

            file = open(f"images/{str(img)}.png", "wb")
            file.write(response.content)
            file.close()

            return send_file(f"images/{str(img)}.png",download_name= f"{str(img)}.png")

    except Exception as e:
        print("[" + str(datetime.datetime.now()) + "] ERR - " + str(e))
        data = {"Error" : str(e)}
        response = app.response_class(
            response=json.dumps(data),
            status=500,
            mimetype='application/json'
        )
        return response


@app.route('/api/status')
def status():
    data = {"Yes" : "I Am Online M8"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    app.run(debug=False)