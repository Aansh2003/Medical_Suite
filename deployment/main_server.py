from flask import Flask,render_template,request,render_template_string,redirect,flash
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

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template('error.html',code = e.code),e.code


@app.route('/')
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

if __name__=="__main__":
    app.register_error_handler(HTTPException, handle_exception)
    app.run(host="0.0.0.0",port=5000)
