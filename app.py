from flask import Flask, render_template, request , redirect , Response
from pymongo import MongoClient
from datetime import datetime
from flask_wtf.csrf import CSRFProtect , CSRFError
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dar-k-aage-jeet-hai'

csrf = CSRFProtect(app)
# MongoDB configuration
client = MongoClient('localhost' , 27017)
db = client["dew"]
collection = db["form"]


@app.route('/')
def form():
    return render_template('index.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        name = request.form['name']
        contact = request.form['contact']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        city = request.form['city']
        activity = request.form.getlist('activity')
        feedback = request.form['feedback']
        timestamp = datetime.now()
        
    
        # Save the data to MongoDB
        data = {"name": name, "contact": contact, "age": age, "gender": gender, "email": email, "city": city, "activity": activity, "feedback": feedback,'timestamp': timestamp }
        collection.insert_one(data)

        return render_template('thanks.html' )
    
    except:
        return redirect('index.html')
    

@app.route('/dew/form')
def form_count():
    num_submissions = db.form.count_documents({})
    return render_template('counter.html', num_submissions=num_submissions)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400




@app.route('/download_csv')
def download_csv():
    # Retrieve data from MongoDB collection
    data = collection.find()
   
    # Create CSV file
    csv_data = []
    headers = ['Name', 'Contact', 'Age', 'Gender', 'Email', 'City', 'Activity', 'Feedback', 'Timestamp']
    for item in data:
        
        csv_data.append([
            item['name'],
            item['contact'],
            item['age'],
            item['gender'],
            item['email'],
            item['city'],
            item['activity'],
            item['feedback'],
           
        ])
    csv_bytes = '\n'.join([','.join(row) for row in csv_data]).encode()
   
    # Create response object with CSV data
    response = Response(
        csv_bytes,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=data.csv'}
    )

    return response



if __name__ == '__main__':
    app.run('0.0.0.0')
