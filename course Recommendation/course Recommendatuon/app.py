from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'psychometric-secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course_recommendation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/profiles'  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

questions = {
    "aptitude": [
        {"q": "What is 12 * 8?", "options": ["96", "88", "108", "86"], "answer": "96"},
        {"q": "What comes next: 2, 4, 8, 16, ...?", "options": ["32", "24", "20", "30"], "answer": "32"},
        {"q": "What is the square root of 144?", "options": ["12", "11", "13", "14"], "answer": "12"},
        {"q": "Which number is a prime?", "options": ["15", "17", "20", "21"], "answer": "17"},
        {"q": "Solve: 45 / 5", "options": ["9", "10", "8", "11"], "answer": "9"},
        {"q": "Find the next: 3, 6, 9, ?", "options": ["12", "10", "15", "11"], "answer": "12"},
        {"q": "What is 7 * 9?", "options": ["63", "72", "56", "69"], "answer": "63"},
        {"q": "Which is an even number?", "options": ["21", "23", "20", "19"], "answer": "20"},
        {"q": "Find the missing: 1, 1, 2, 3, 5, ?", "options": ["7", "8", "9", "6"], "answer": "8"},
        {"q": "What is 100 - 45?", "options": ["55", "60", "65", "70"], "answer": "55"}
    ],
    "personality": [
        {"q": "You enjoy being in social situations.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You prefer detailed plans over spontaneous ideas.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You keep emotions under control.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You often help others without being asked.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You are detail-oriented.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You enjoy teamwork.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You like to lead group projects.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You adapt easily to change.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You are a good listener.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]},
        {"q": "You enjoy challenges.", "options": ["Strongly Agree", "Agree", "Disagree", "Strongly Disagree"], "weight": [4,3,2,1]}
    ],
    "stress": [
        {"q": "You feel overwhelmed easily.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [4,3,2,1]},
        {"q": "You remain calm under pressure.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [1,2,3,4]},
        {"q": "You struggle with deadlines.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [4,3,2,1]},
        {"q": "You lose sleep due to stress.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [4,3,2,1]},
        {"q": "You take regular breaks to relax.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [1,2,3,4]},
        {"q": "You talk to others when stressed.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [1,2,3,4]},
        {"q": "You procrastinate tasks often.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [4,3,2,1]},
        {"q": "You manage multiple tasks well.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [1,2,3,4]},
        {"q": "You feel anxious before tests.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [4,3,2,1]},
        {"q": "You feel calm in unfamiliar situations.", "options": ["Always", "Often", "Sometimes", "Never"], "weight": [1,2,3,4]}
    ],
    "softskills": [
        {"q": "You often take leadership roles.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You communicate clearly.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You are empathetic to others.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You are good at resolving conflict.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You are confident in interviews.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You give and receive feedback well.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You work well under deadlines.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You collaborate effectively.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You are open to learning new things.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]},
        {"q": "You express ideas confidently.", "options": ["Always", "Often", "Sometimes", "Rarely"], "weight": [4,3,2,1]}
    ]
}

app.config['UPLOAD_FOLDER'] = 'static/uploads'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    location = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    mobile = db.Column(db.String(20))
    password = db.Column(db.String(100))  # Added password field
    profile_img = db.Column(db.String(200))
    results = db.relationship('Result', backref='user', lazy=True)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aptitude = db.Column(db.Integer)
    personality = db.Column(db.Integer)
    stress = db.Column(db.Integer)
    softskills = db.Column(db.Integer)
    recommendations = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        location = request.form['location']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        profile = request.files['profile']

        if not all([name, age, location, email, mobile, password, profile]):
            flash('Please fill in all fields.')
            return redirect(url_for('register'))

        filename = secure_filename(profile.filename)
        profile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.')
            return redirect(url_for('register'))

        user = User(
            name=name,
            age=int(age),
            location=location,
            email=email,
            mobile=mobile,
            password=password,  # Optionally hash this
            profile_img=filename
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_id'] = user.id
            session['name'] = user.name
            session['profile'] = user.profile_img
            return redirect(url_for('start'))
        else:
            flash('Invalid credentials.')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first!')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    
@app.route('/start')
def start():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    session.pop('aptitude', None)
    session.pop('personality', None)
    session.pop('stress', None)
    session.pop('softskills', None)
    return redirect(url_for('aptitude'))


@app.route('/aptitude', methods=['GET', 'POST'])
def aptitude():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        score = 0
        for i, q in enumerate(questions["aptitude"]):
            if request.form.get(f"q{i}") == q["answer"]:
                score += 1
        session["aptitude"] = score
        return redirect(url_for('personality'))

    user = User.query.get(session['user_id'])
    return render_template("quiz_page.html", category="aptitude", questions=questions["aptitude"], name=user.name)


@app.route('/personality', methods=['GET', 'POST'])
def personality():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        score = 0
        for i, q in enumerate(questions["personality"]):
            ans = request.form.get(f"q{i}")
            if ans:
                idx = q["options"].index(ans)
                score += q["weight"][idx]
        session["personality"] = score
        return redirect(url_for('stress'))

    user = User.query.get(session['user_id'])
    return render_template("quiz_page.html", category="personality", questions=questions["personality"], name=user.name)


@app.route('/stress', methods=['GET', 'POST'])
def stress():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        score = 0
        for i, q in enumerate(questions["stress"]):
            ans = request.form.get(f"q{i}")
            if ans:
                idx = q["options"].index(ans)
                score += q["weight"][idx]
        session["stress"] = score
        return redirect(url_for('softskills'))

    user = User.query.get(session['user_id'])
    return render_template("quiz_page.html", category="stress", questions=questions["stress"], name=user.name)


@app.route('/softskills', methods=['GET', 'POST'])
def softskills():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        score = 0
        for i, q in enumerate(questions["softskills"]):
            ans = request.form.get(f"q{i}")
            if ans:
                idx = q["options"].index(ans)
                score += q["weight"][idx]
        session["softskills"] = score
        return redirect(url_for('result'))

    user = User.query.get(session['user_id'])
    return render_template("quiz_page.html", category="softskills", questions=questions["softskills"], name=user.name)


from flask import session, render_template, redirect


@app.route('/result')
def result():
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login page if not logged in

    score = {
        "aptitude": session.get("aptitude", 0),
        "personality": session.get("personality", 0),
        "stress": session.get("stress", 0),
        "softskills": session.get("softskills", 0),
    }

    recommendations = []

    # Aptitude
    if score["aptitude"] >= 16:
        recommendations.append("High aptitude: Engineering, Analytics, AI, or Competitive Exams.")
    elif score["aptitude"] >= 10:
        recommendations.append("Good problem-solving skills. Explore Data Science, Finance, or IT.")
    else:
        recommendations.append("Consider basic quantitative training and aptitude improvement courses.")

    # Personality
    if score["personality"] >= 35:
        recommendations.append("Strong personality fit. Consider Psychology, Leadership, or HR roles.")
    elif score["personality"] >= 25:
        recommendations.append("Balanced personality. Can explore Management, Social Work, or Consulting.")
    else:
        recommendations.append("You may benefit from personality development workshops.")

    # Stress
    if score["stress"] <= 15:
        recommendations.append("High stress levels. Try Meditation, Time Management, or Mental Wellness programs.")
    elif score["stress"] <= 25:
        recommendations.append("Mild stress. Practice mindfulness and improve emotional regulation.")
    else:
        recommendations.append("Well-balanced under pressure. Fit for emergency or high-responsibility jobs.")

    # Softskills
    if score["softskills"] >= 35:
        recommendations.append("Excellent soft skills. Ideal for Teaching, Public Speaking, or Marketing.")
    elif score["softskills"] >= 25:
        recommendations.append("Strong communication and leadership potential. Explore Management or Team Roles.")
    else:
        recommendations.append("Consider soft skill improvement programs, group activities, or workshops.")

    user_id = session.get("user_id")  # Must be set at login

    # Save result in DB if user is logged in
    if user_id:
        result_entry = Result(
            aptitude=score["aptitude"],
            personality=score["personality"],
            stress=score["stress"],
            softskills=score["softskills"],
            recommendations=" | ".join(recommendations),
            user_id=user_id
        )
        db.session.add(result_entry)
        db.session.commit()

    return render_template("result.html", score=score, recommendations=recommendations)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@app.route('/admin/user/<int:user_id>/result')
def view_user_result(user_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    user = User.query.get_or_404(user_id)
    result = Result.query.filter_by(user_id=user_id).first()
    if not result:
        return "No result found for this user"

    # Suggested courses based on scores
    suggestions = []
    if result.aptitude >= 16:
        suggestions.append("Engineering, Analytics, AI, Competitive Exams")
    elif result.aptitude >= 10:
        suggestions.append("Data Science, Finance, IT")
    else:
        suggestions.append("Aptitude training courses")

    if result.personality >= 35:
        suggestions.append("Psychology, Leadership, HR")
    elif result.personality >= 25:
        suggestions.append("Management, Social Work, Consulting")
    else:
        suggestions.append("Personality development programs")

    if result.stress <= 15:
        suggestions.append("Meditation, Time Management, Mental Wellness")
    elif result.stress <= 25:
        suggestions.append("Mindfulness programs")
    else:
        suggestions.append("Emergency jobs, High-pressure roles")

    if result.softskills >= 35:
        suggestions.append("Teaching, Public Speaking, Marketing")
    elif result.softskills >= 25:
        suggestions.append("Team Management, Sales")
    else:
        suggestions.append("Soft skills workshops")

    return render_template("admin_user_result.html", user=user, result=result, suggestions=suggestions)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
