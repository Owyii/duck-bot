from flask import Flask
from dotenv import load_dotenv
import utils.helper as helper

app = Flask(__name__)
load_dotenv()

@app.route('/test')
def testing():
    result = helper.test()
    return result

@app.route('/')
def hello():
    return "Hi from Card app"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)