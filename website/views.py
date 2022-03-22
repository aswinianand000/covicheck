from xmlrpc.client import boolean
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Patient
from . import db
import json
from  . import covid
import time
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        full_name = request.form.get('pFullName')
        p_id = request.form.get('pId')
        age = request.form.get('pAge')
        gender = request.form.get('pGender')
        
        if 'pChestXray' not in request.files:
            flash('No file part', category='error')
        else:
            file = request.files['pChestXray']
            if file.filename == '':
                flash('No selected file', category='error')
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    new_file_name = str(p_id) + "_"+ timestr + filename
                    file.save(os.path.join('website/static/test_images/', filename))
                    os.rename(os.path.join('website/static/test_images/', filename),
                                os.path.join('website/static/test_images/', new_file_name))
                    # flash('Image Uploaded!', category='success')

                if len(full_name) < 4:
                    flash('Full Name must be greater than 3 character.', category='error')
                elif len(p_id) < 4:
                    flash('Patient ID must be greater than 3 characters.', category='error')
                elif len(age)<1 or age.isnumeric()==False or int(age) <1 :
                    flash('Patient Age must be greater than 0.', category='error')
                elif len(gender) != 1:
                    flash('Please check Gender Field.', category='error')
                else:
                    pred_img = os.path.join('website/static/test_images/', new_file_name)
                    result =  covid.predict_covid(pred_img)
                    new_file = Patient(full_name=full_name, p_id=p_id, age=age, gender=gender,
                                    file_name=new_file_name,result=result,user_id=current_user.id)
                    db.session.add(new_file)
                    db.session.commit()
                    # covid.upload_file(file_name)
                    flash('Record inserted!', category='success')
                    patient = Patient.query.filter_by(file_name=new_file_name).first()
                    # return render_template("home.html", user=current_user, file_name=new_file_name)
                    return render_template("result.html", user=current_user, patient=patient)

    return render_template("home.html", user=current_user)


@views.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    if request.method == 'POST':
        patient = json.loads(request.data)
        # print(patient)
        id = patient['id']
        patient = Patient.query.get(id)
        if patient:
            if patient.user_id == current_user.id:
                return render_template("result.html", user=current_user, patient=patient)
    return render_template("result.html", user=current_user)