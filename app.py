from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  

app = Flask(__name__)

client = MongoClient('mongodb+srv://sparta:jungle@cluster0.gsunejv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # MongoDB Altas 사이트의 링크를 가져옵니다
db = client.dbjungle 


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['GET'])
def read_memo():
    memo_list=list(db.memo.find({},{'_id':0}))
    return jsonify({"data":memo_list})

@app.route('/memo', methods=['POST'])
def create_memo():
    title=request.form['title']
    content=request.form['content']
    db.memo.insert_one({'title':title,'content':content})
    return jsonify({'result':'success','msg':'저장완료!'})

@app.route('/memo/delete', methods=['POST'])
def delete_memo():
    title = request.form['title']
    db.memo.delete_one({'title':title})
    return jsonify({'result':'success','msg':'삭제 완료!'})

@app.route('/memo/update', methods=['POST'])
def update_memo():
    old_title = request.form['old_title']
    new_title = request.form['new_title']
    content = request.form['comment']
    db.memo.update_one({'title':old_title},{'$set':{"title":new_title,"content":content}})
    return jsonify({'result':'success','msg':'수정 완료!'})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)