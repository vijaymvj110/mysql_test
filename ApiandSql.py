from flask import Flask,request,json,jsonify

app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return jsonify({"Msg:Welcome to Python learning"})

if __name__=='__main__':
    app.run(debug=True)