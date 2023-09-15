from flask import Flask,render_template,request,render_template_string,redirect,flash, session
from fileinput import filename
from werkzeug.utils import secure_filename
import os
from functionality.model_inference import binary_tumor_classifier
from functionality.model_inference import tumor_segmentation
from functionality.model_inference import retinal_classifier
from functionality.model_inference import vessel_extractor
import functionality.predictor as predictor
import functionality.email_generator as generator
import functionality.email_sender as sender
import math
from werkzeug.exceptions import HTTPException
from functionality.cloud_api import login
import pyrebase 

# Firebase Initialization

with open('functionality/cloud_api/firebase_credentials.txt', 'r') as f:
    creds = [line.strip() for line in f]
config = {
    "apiKey": creds[0],
    "authDomain": creds[1],
    "databaseURL": creds[2],
    "storageBucket": creds[3]
}
firebase = pyrebase.initialize_app(config)

# Global variable declarations
default = ('admin@admin.com','admin')

id = 0

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"


# App route definitions

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template('error.html',code = e.code),e.code

@app.route('/',methods=['POST','GET'])
def login_signup():
    global id
    if(request.method=='POST'):
        if(request.form.get('guest')):
            session['loggedin'] = False
            session['id'] = id
            id = id+1
            session['username'] = 'guest'
            return redirect('/home')
        
        if(request.form.get('login')):
            email = request.form['email']
            password = request.form['pass']
            if(email == default[0] and password == default[1]):
                session['loggedin'] = True
                session['id'] = id
                id = id+1
                session['username'] = email
                return redirect('/home')
            
            if(login.check_pass(email,password, firebase)):
                session['loggedin'] = True
                session['id'] = id
                id = id+1
                session['username'] = email
                return redirect('/home')
            else:
                return render_template('index.html',info='Incorrect username or password')

        elif(request.form.get('signup')):
                if request.form['pass_reg'] == request.form['conf_pass_reg']:
                    if len(request.form['pass_reg']) < 7:
                        return render_template('index.html',info='Password too short')
                    name = request.form['name_reg']
                    email = request.form['email_reg']
                    password = request.form['pass_reg']
                    if not login.signup(name,email,password, firebase):
                        return render_template('index.html',info='Registration failed')
                else:
                    return render_template('index.html',info='Passwords do not match')
    return render_template('index.html')

@app.route('/home')
def render_home_page():
    return render_template('home.html')


@app.route('/brain_tumor',methods=['POST','GET'])
def render_brain_tumor_detect():
    if(request.method=='POST'):

        name = request.form['fname']
        email = request.form['email']

        if 'scan' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['scan']
        val = len(os.listdir(str(os.getcwd())+'/'+UPLOAD_FOLDER))
        if file and allowed_file(file.filename):
            extension = file.filename[str(file.filename).rfind('.'):]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'file'+str(val+1)))
            filepath = str(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], 'file'+str(val+1)))
            prediction,prob = binary_tumor_classifier.classify(filepath)
            prob = int(prob*100)
            pred = predictor.predict('brain_tumor',prediction)
            segment = False

            if pred != 'No Tumor':
                segment = True
                segmented_path = tumor_segmentation.segment(filepath,extension)
                filepath = segmented_path

            html = generator.generator((pred,prob),'Brain tumor detector',name)
            sender.send_email(email,html,filepath,str(extension),segment)

    return render_template('brain_tumor_detect.html')

@app.route('/retinal_scan',methods=['POST','GET'])
def render_retinal_page():
    if(request.method=='POST'):

        name = request.form['fname']
        email = request.form['email']
        seg = "off"
        try:
            vessel = request.form['vessel']
            seg = "on"
        except:
            pass

        if 'scan' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['scan']
        val = len(os.listdir(str(os.getcwd())+'/'+UPLOAD_FOLDER))
        if file and allowed_file(file.filename):
            extension = file.filename[str(file.filename).rfind('.'):]
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'file'+str(val+1)))
            filepath = str(os.path.join(os.getcwd(),app.config['UPLOAD_FOLDER'], 'file'+str(val+1)))
            prediction,prob = retinal_classifier.classify(filepath)

            prob = int(prob*100)
            pred = predictor.predict('retinal',prediction)

            segment = False
            if(seg == "on"):
                vessel_path = vessel_extractor.extract(filepath,extension)
                segment = True
                filepath = vessel_path

            html = generator.generator((pred,prob),'Retinal disease detector',name)
            sender.send_email(email,html,filepath,str(extension),segment)
            
    return render_template('retinal_page.html')

@app.route('/model_details')
def render_model():
    return render_template('model_details.html')

@app.route('/support')
def support():
    return render_template('support.html')

if __name__=="__main__":
    app.register_error_handler(HTTPException, handle_exception)
    app.run(host="0.0.0.0",port=5000)
