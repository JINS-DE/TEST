from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  

app = Flask(__name__)

client = MongoClient('mongodb+srv://:@cluster0.gsunejv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # MongoDB Altas 사이트의 링크를 가져옵니다
db = client.dbjungle 

# index
@app.route('/')
def home():
    return render_template('index.html')

# todo리스트 둥록
@app.route('/todo', methods=['POST'])
def create_todo():
    todoName=request.form['todoName']
    db.todo.insert_one({'todoName':todoName,'done':False})
    return jsonify({'result':'success','msg':'등록 완료!'})

# DB 투두리스트 가져오기
@app.route('/todo', methods=['GET'])
def read_todo():
    todo_list=list(db.todo.find({},{'_id':0}))
    return jsonify({"data":todo_list})

#업데이트 done
@app.route("/todo/update/done", methods=['POST'])
def update_done():
    todoName=request.form['update_todo']
    done = request.form['done']

    # 완료 한 애들은 True, 아직 완료 못 한 애들은 False
    if done == 'true':
        done=True
    else:
        done=False

    db.todo.update_one({'todoName':todoName},{'$set':{"done":done}})
    return jsonify({'result':'success'})


@app.route("/todo/update/name", methods=['POST'])
def update_name():
    old_todo = request.form['old_todo']
    new_todo = request.form['new_todo']
    db.todo.update_one({'todoName': old_todo}, {'$set': {"todoName": new_todo}})
    return jsonify({'result':'success','msg':'할 일 업데이트 완료!'})

#삭제
@app.route("/todo/delete", methods=['POST'])
def delete_todo():
    todo = request.form['delete_todo']
    db.todo.delete_one({'todoName':todo})
    return jsonify({'result':'success','msg':'할 일 삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)