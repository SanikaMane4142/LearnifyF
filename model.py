import pandas as pd
import pickle

class CourseRecommender:
    def __init__(self):
        # Example course data (assuming you're working with a DataFrame)
        self.courses = pd.DataFrame([
            {'course_name': 'Python for Beginners', 'description': 'A beginner-level course for learning Python programming.', 'goal': 'learn python'},
            {'course_name': 'Data Science with Python', 'description': 'Learn data science concepts using Python.', 'goal': 'learn python'},
            {'course_name': 'Web Development Bootcamp', 'description': 'Master HTML, CSS, and JavaScript for full-stack development.', 'goal': 'web development'},
            {'course_name': 'Advanced Data Science', 'description': 'Learn advanced data science topics like machine learning and deep learning.', 'goal': 'data science'},
            {'course_name': 'Math for Data Science', 'description': 'Brush up on essential math skills for data science.', 'goal': 'improve math skills'}
        ])

    def recommend_courses(self, goal):
        # Normalize the goal to lowercase and filter the courses DataFrame
        goal = goal.lower()
        
        # Filter the courses based on the user's goal
        recommended_courses = self.courses[self.courses['goal'].str.contains(goal, case=False, na=False)]
        
        # Check if any courses match the goal
        if recommended_courses.empty:
            return []  # Return an empty list if no courses are found
        
        # If courses are found, return the filtered courses
        return recommended_courses.to_dict(orient='records')

# Create an instance of the CourseRecommender class
recommender = CourseRecommender()

# Create the model.pkl file if it doesn't already exist
with open('model.pkl', 'wb') as file:
    pickle.dump(recommender, file)

print("model.pkl has been successfully created.")

# Sample usage (you can test this once the model is created)
goal = 'learn python'
recommended_courses = recommender.recommend_courses(goal)

if recommended_courses:
    print("Recommended Courses:")
    for course in recommended_courses:
        print(course['course_name'])
else:
    print("No courses found for your goal.")
