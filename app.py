from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient  

app = Flask(__name__)

client = MongoClient('mongodb+srv://sparta:jungle@cluster0.gsunejv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # MongoDB Altas 사이트의 링크를 가져옵니다
db = client.dbjungle 

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['POST'])
def post_memo():
    title = request.form['input_title']
    content = request.form['input_text']
    db.memo.insert_one({'title':title,'content':content})
    return jsonify({'result':'success','msg':'저장완료!'})

@app.route('/memo', methods=['GET'])
def read_memo():
    memo_list=list(db.memo.find({},{'_id':0}))
    return jsonify({"memo_list":memo_list})

@app.route('/api/memo/delete', methods=['POST'])
def delete_memo():
    db.memo.delete_one({'title':request.form['delete_title']})
    return jsonify({'result':'success','msg':'삭제완료!'})

@app.route('/api/memo/update', methods=['POST'])
def update_momo():
    old_title = request.form['old_title']
    new_title = request.form['new_title']
    new_content = request.form['new_content']
    db.memo.update_one({'title':old_title},{'$set':{'title':new_title,'content':new_content}})
    return jsonify({'result':'success','msg':'수정 완료!'})

if __name__ == '__main__':  
   app.run('0.0.0.0',port='5000',debug=True)