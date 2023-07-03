from flask import Flask,render_template,request,render_template_string

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'),404

@app.route('/')
def render_home_page():
    return render_template('home_page.html')

@app.route('/brain_tumor',methods=['POST','GET'])
def render_brain_tumor_detect():
    if(request.method=='POST'):
        pass
    return render_template('brain_tumor_detect.html')

app.register_error_handler(404, page_not_found)
app.run(host="0.0.0.0",port=5000)
