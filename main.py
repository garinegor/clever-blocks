from flask import Flask, request, render_template
from clever import run_code

app = Flask(__name__)

@app.route('/')
@app.route('/blockly')
def hello():
    return render_template("index.html")

@app.route('/run', methods=['POST'])
def login():
    run_code(request.form['code'])
    return "oke"
        
if __name__=="__main__":
    app.run()
