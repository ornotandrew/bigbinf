from flask import Blueprint, render_template, request, jsonify, abort
from werkzeug import secure_filename

homeBP = Blueprint('home',__name__)

@homeBP.route('/', methods=['GET'])
def index():
	#print url_for('homeBP.static', filename='layout.html')
	#return render_template('index.html', title='Home')
	return render_template('layout.html')


@homeBP.route('/submitjob', methods=['POST'])
def submitJob():
	file = request.files['file']
	if file:
		filename = secure_filename(file.filename)
		print(filename)
	return jsonify({'file': filename}), 201