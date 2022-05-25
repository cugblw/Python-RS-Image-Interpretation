from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_restful import Api
from starlette import status


app = Flask(__name__)
api = Api(app)

@app.route('/')
@app.route('/homepage', methods=['GET'])
def homepage():
    return {"message": "This is the Image Tiler Homepage!"}




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001, debug=True)
