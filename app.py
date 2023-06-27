from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import plotly.graph_objs as go
import json
import plotly
import logging
app = Flask(__name__, static_url_path='/static')
app.logger.setLevel(logging.DEBUG)

app.secret_key = '1101'  # Set a secret key for session management

app.config['MYSQL_HOST'] = 'localhost'  # Replace with your MySQL host
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'AmmuRitu@19a'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'student1'  # Replace with your MySQL database name

mysql = MySQL(app)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student1.user_info WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.execute("SELECT rollno FROM student1.user_info WHERE username = %s", (username,))
        rollno = cur.fetchone()
        session['rollno'] = rollno[0]
        cur.close()
        
        if user:
            session['username'] = user[0]
            return redirect('/dashboard')  # Redirect to the dashboard page after successful login
        else:
            error = 'Invalid username or password!!!'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

semester = None
@app.route('/grades', methods=['GET', 'POST'])
def grades():
    if request.method == "POST":
        semester = request.form.get('semester', '')  # Providing an empty string as the default value
        session['semester'] = semester
        if(semester != None):
            return redirect('/grades2')
        else:
            return render_template('grades.html')
    return render_template('grades.html')



@app.route('/home')
def home():
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    cur = mysql.connection.cursor()
    cur.execute('SELECT name, username, rollno, email FROM student1.user_info WHERE rollno = %s', (session['rollno'],))
    content = cur.fetchall()
    app.logger.debug(content)
    name = content[0][0]
    username = content[0][1]
    rollno = content[0][2]
    email = content[0][3]
    cur.execute('SELECT branch, year, sem FROM student1.info WHERE roll_no = %s', (session['rollno'],))
    t = cur.fetchall()
    branch = t[0][0]
    sem = t[0][2]
    year = t[0][1]
    cur.close()
    error = None
    if request.method == "POST":
        old = request.form['password1']
        new = request.form['password2']
        cur = mysql.connection.cursor()
        cur.execute("SELECT password from student1.user_info WHERE rollno = %s", (session['rollno'],))
        old1 = cur.fetchall()
        old3 = old1[0][0]
        app.logger.debug(session['rollno'])
        if old == old3:
            cur.execute('UPDATE student1.user_info SET password = %s WHERE rollno = %s;', (new, session['rollno']))
            mysql.connection.commit() 
            error = "Password changed successfully!!!"
        else:
            error = "old password is wrong!!!"
        cur.close()
    return render_template('profile.html', name=name, email=email, username=username, rollno=rollno, branch=branch, sem=sem, year=year, error=error)



grades = None
@app.route('/grades2')
def grades2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT subject_name, grade FROM student1.grades WHERE roll_no = %s AND semester = %s', (session['rollno'] ,session['semester']))
    grades = cur.fetchall()
    cur.close()
    # Get GPA for all semesters
    cur = mysql.connection.cursor()
    cur.execute('SELECT semester, avg_cgpa as gpa FROM student1.sem_graph WHERE roll_no = %s', (session['rollno'],))
    gpas = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('SELECT avg_cgpa FROM student1.sem_graph WHERE roll_no = %s AND semester = %s', (session['rollno'],session['semester']))
    gp = cur.fetchall()
    cur.close()
    for grade in grades:
        app.logger.debug(grade[0])
    
    # Create line chart data
    gpas = [{'semester': gpa[0], 'gpa': gpa[1]} for gpa in gpas]
    x = [gpa['semester'] for gpa in gpas]
    y = [gpa['gpa'] for gpa in gpas]
    data = go.Scatter(x=x, y=y, mode='lines', name='GPA')
    chart = json.dumps([data], cls=plotly.utils.PlotlyJSONEncoder)
    chart_data = json.loads(chart)[0]
    X_values = chart_data['x']
    # Parse the JSON string and extract the first item
    Y_values = chart_data['y']  # Extract the 'y' values from the chart data
    mode = chart_data['mode']
    name = chart_data['name']
    type = chart_data['type']
    gp = list(gp)
    X_values = [int(x) for x in X_values]
# Print the chart values
    app.logger.debug(gp)
    for value in X_values:
        app.logger.debug(value)
    return render_template('grades2.html', grades=grades, chart=chart, X_values = X_values, Y_values = Y_values, mode = mode, name = name, type = type, semester = semester, gp = gp[0][0])

error = None
@app.route('/', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        username = request.form["username"]
        rollno = request.form['rollno']
        email = request.form["email"]
        password = request.form["password"]
        re_password = request.form["re-password"]
        app.logger.debug(username)
        if password == re_password:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM student1.user_info')
            results = cur.fetchall()
            cur.execute('INSERT INTO user_info VALUES (%s, %s, %s, %s, %s)', (name, username, rollno, email, password))
            mysql.connection.commit()
            return render_template('login.html')
        else:
            error = "password and re-type doesnot match"
            return render_template('register.html', error=error)
    return render_template('register.html')

@app.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html'), getattr(error, 'code', 500)



app.run(debug=True)
