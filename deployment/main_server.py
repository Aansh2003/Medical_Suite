from flask import Flask,render_template,request,render_template_string,redirect,flash
from fileinput import filename
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'),404

@app.route('/')
def render_home_page():
    return render_template('home_page.html')

@app.route('/brain_tumor',methods=['POST','GET'])
def render_brain_tumor_detect():
    if(request.method=='POST'):

        name = request.form['fname']
        email = request.form['email']

        if 'scan' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['scan']
        if file and allowed_file(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('brain_tumor_detect.html')

if __name__=="__main__":
    app.register_error_handler(404, page_not_found)
    app.run(host="0.0.0.0",port=5000)
