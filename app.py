from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pickle
from model import CourseRecommender

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key for session management

# Load the saved model from the model.pkl file
with open('model.pkl', 'rb') as file:
    recommender = pickle.load(file)  # This should load the CourseRecommender object

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('newcsv.sqlite')  # Path to your SQLite database file
    conn.row_factory = sqlite3.Row        # Enables accessing columns by name
    return conn

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Renders the home page

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM data WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
    
        if user:
            session['userid'] = user['userid']  # Store the user ID in the session
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

# Route for the profile page
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'userid' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM data WHERE userid = ?', (session['userid'],)).fetchone()
    conn.close()

    if request.method == 'POST':
        # Get the user's goal from the form
        goal = request.form.get('goal', '').lower()
        session['goal'] = goal  # Store the goal in the session
        return redirect(url_for('courses'))  # Redirect to the courses page

    if user:
        return render_template('profile.html', user=user)
    else:
        return "User not found."

# Route for the courses page
@app.route('/courses', methods=['POST', 'GET'])
def courses():
    goal = session.get('goal', None)
    
    if not goal:
        return redirect(url_for('profile'))  # If goal is not set, redirect to profile page
    
    # Use the recommender to get course recommendations
    recommended_courses = recommender.recommend_courses(goal)

    # Debugging output to check what courses are being returned
    print("Recommended Courses:", recommended_courses)

    # Pass the recommended courses or None to the template
    return render_template('courses.html', courses=recommended_courses)



if __name__ == '__main__':
    app.run(debug=True)
