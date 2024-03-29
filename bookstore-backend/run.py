import datetime

from flask import Flask, jsonify, request
from flask_cors import cross_origin
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.json_util import dumps
import requests
import json
import time
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 禁止中文转义
app.config['MONGO_URI'] = 'mongodb://booker:123456@127.0.0.1:27017/bookstore?authMechanism=DEFAULT'
mongo = PyMongo(app)
APP_KEY = 'e3ef05d3a2ea405c906c7d67b0ff9386'


@app.route("/query/<isbn>", methods=["GET"])
@cross_origin()
def query_by_isbn(isbn):
    """根据ISBN查询图书信息"""
    result = requests.get(
        'http://47.99.80.202:6066/openApi/getInfoByIsbn?isbn=' + isbn + '&appKey=' + APP_KEY)
    result.encoding = 'utf-8'
    return result.json()


@app.route("/types", methods=["GET"])
@cross_origin()
def clc_query():
    """查询所有分类"""
    cursor = mongo.db.books.aggregate([
        {'$unwind': '$clcName'},
        {'$group': {'_id': '$clcName'}},
        {'$project': {'_id': 0, 'clcName': "$_id"}}
    ])
    result = []
    for document in cursor:
        result.append(document['clcName'])
    return jsonify({
        "code": 0,
        "success": True,
        "msg": "",
        "data": json.loads(dumps(result))
    })


@app.route("/tags", methods=["GET"])
@cross_origin()
def tag_query():
    """查询标签"""
    cursor = mongo.db.books.aggregate([
        {'$unwind': '$tags'},
        {'$group': {'_id': '$tags'}},
        {'$project': {'_id': 0, 'tags': "$_id"}}
    ])
    result = []
    for document in cursor:
        result.append(document['tags'])
    return jsonify({
        "code": 0,
        "success": True,
        "msg": "",
        "data": json.loads(dumps(result))
    })


@app.route("/books", methods=["GET"])
@cross_origin()
def query():
    """根据条件查询图书"""
    request_args = request.args.to_dict()
    params = {}
    if request_args['bookName'] != '':
        params['bookName'] = re.compile(request_args['bookName'])
    if request_args['clcName'] != '':
        params['clcName'] = {'$in': request_args['clcName'].split(',')}
    if request_args['tags'] != '':
        params['tags'] = {'$in': request_args['tags'].split(',')}
    if request_args['author'] != '':
        params['author'] = re.compile(request_args['author'])
    total = mongo.db.books.count_documents({})
    page = int(request_args['page'])
    print(request_args)
    print(params)
    cursor = mongo.db.books.find(params).skip(10 * (page - 1)).limit(10).sort('createTime', -1)
    books = []
    for document in cursor:
        document['_id'] = str(document['_id'])
        books.append(document)

    result = {
        "total": total,
        "data": json.loads(dumps(books))
    }
    return jsonify({
        "code": 0,
        "success": True,
        "msg": "",
        "data": result
    })


@app.route("/books/<book_id>", methods=["GET"])
@cross_origin()
def query_by_id(book_id):
    """根据主键查询图书"""
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    book['_id'] = str(book['_id'])
    return jsonify({
        "code": 0,
        "success": True,
        "msg": "",
        "data": json.loads(dumps(book))
    })


@app.route("/books", methods=["POST"])
@cross_origin()
def create_book():
    """创建图书"""
    book = json.loads(request.get_data())
    book['createTime'] = time.time()
    mongo.db.books.insert_one(book)
    return jsonify({
        "code": 0,
        "success": True,
        "msg": "",
        "data": ""
    })


@app.route("/books/<book_id>", methods=["PUT"])
@cross_origin()
def update_book(book_id):
    """更新图书"""
    book = request.get_data()
    mongo.db.books.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": json.loads(book)}
    )
    return jsonify({
        "code": 0,
        "success": True,
        "msg": "",
        "data": ""
    })


@app.route("/books/<book_id>", methods=["DELETE"])
@cross_origin()
def delete_book(book_id):
    """删除图书"""
    mongo.db.books.delete_one({"_id": ObjectId(book_id)})
    return jsonify({
        "code": 0,
        "success": True,
        "msg": "",
        "data": ""
    })


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
