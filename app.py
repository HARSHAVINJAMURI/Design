from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)
# Load the dataset
dataset_path = 'dataset.xlsx'
dataset = pd.read_excel(dataset_path)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process_form', methods=['POST'])
def process_form():
    # Retrieve user inputs from the form
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    gender = request.form['gender']
    health_issues = request.form.getlist('health_issues')
    # Filter the dataset based on user inputs
    filtered_data = filter_dataset(age, gender, health_issues)
    # Extract diet plans based on age ranges
    Diet_Morning_Veg = filtered_data['Diet_Morning_Veg'].values[0] if not filtered_data.empty else "N/A"
    Diet_Morning_NonVeg = filtered_data['Diet_Morning_NonVeg'].values[0] if not filtered_data.empty else "N/A"
    Diet_Afternoon_Veg = filtered_data['Diet_Afternoon_Veg'].values[0] if not filtered_data.empty else "N/A"
    Diet_Afternoon_NonVeg = filtered_data['Diet_Afternoon_NonVeg'].values[0] if not filtered_data.empty else "N/A"
    Diet_Night_Veg = filtered_data['Diet_Night_Veg'].values[0] if not filtered_data.empty else "N/A"
    Diet_Night_NonVeg = filtered_data['Diet_Night_NonVeg'].values[0] if not filtered_data.empty else "N/A"
    # Render the result template with the filtered data
    return render_template('result.html', name=name, email=email, age=age, gender=gender, health_issues=health_issues,
                           Diet_Morning_Veg=Diet_Morning_Veg,Diet_Morning_NonVeg=Diet_Morning_NonVeg, Diet_Afternoon_Veg=Diet_Afternoon_Veg,Diet_Afternoon_NonVeg=Diet_Afternoon_NonVeg,
                           Diet_Night_Veg=Diet_Night_Veg,Diet_Night_NonVeg=Diet_Night_NonVeg)
def filter_dataset(age, gender, health_issues):
    # Convert the age string to a tuple of two integers representing the age range
    age_range = tuple(map(int, age.split('-')))
    # Filter the dataset based on user inputs
    filtered_data = dataset[
        (dataset['age'].apply(lambda x: age_range[0] <= int(x.split('-')[0]) <= age_range[1]))
        & (dataset['gender'] == gender)
        & (dataset['health_issue'].isin(health_issues))
    ]
    return filtered_data
if __name__ == '__main__':
    app.run(debug=True)
