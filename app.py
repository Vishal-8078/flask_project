from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# ... (other routes)

@app.route('/', methods=['GET', 'POST'])
def quick_registration():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        district = request.form.get('district')

        # Validate the form fields as per your requirements
        # ...

        # Send data to the API for Quick Registration
        url = "https://dev.yip.kerala.gov.in/yipapp/index.php/Idea2021/add_pre_reg"
        data = {
            "prereg_name": name,
            "prereg_email": email,
            "prereg_mob": mobile,
            "districtd": district
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("Success") == "1":
                # Registration successful, store 'tempreg_id' and other data in session
                tempreg_id = json_response.get("tempregId")
                session['tempreg_id'] = tempreg_id
                session['prereg_name'] = name
                session['prereg_email'] = email
                session['prereg_mob'] = mobile
                session['districtd'] = district
                return redirect(url_for('verify_otp'))
            else:
                # Registration failed, display error message
                error_message = json_response.get("msg")
                return render_template('registration.html', error_message=error_message)
        else:
            # API request failed, display error message
            error_message = "Failed to register. Please try again later."
            return render_template('registration.html', error_message=error_message)
    else:
        return render_template('registration.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    tempreg_id = session.get('tempreg_id')

    if not tempreg_id:
        return redirect(url_for('quick_registration'))

    if request.method == 'POST':
        otp_received = request.form.get('otp')

        # Validate the OTP as per your requirements
        # ...

        # Retrieve data from the session
        name = session.get('prereg_name')
        email = session.get('prereg_email')
        mobile = session.get('prereg_mob')
        district = session.get('districtd')

        # Send data to the API for OTP verification
        url = "https://dev.yip.kerala.gov.in/yipapp/index.php/Com_mobile_otp/checkotp"
        data = {
            "otp_received": otp_received,
            "user_id": email,
            "prereg_name": name,
            "prereg_email": email,
            "prereg_mob": mobile,
            "districtd": district
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("Success") == "1":
                # OTP verification successful, send email and redirect to profile page
                # Implement email sending here
                # You can add your email sending logic here (e.g., using Flask-Mail or another email library)
                return redirect(url_for('login'))  # Redirect to the profile submission page
            else:
                # OTP verification failed, display error message
                error_message = json_response.get("msg")
                return render_template('verify_otp.html', error_message=error_message)
        else:
            # API request failed, display error message
            error_message = "Failed to verify OTP. Please try again later."
            return render_template('verify_otp.html', error_message=error_message)
    else:
        return render_template('verify_otp.html')
# ... (other routes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Perform login authentication here (you can use a database or any other authentication method)
        # For this example, let's assume a hardcoded user with email "admin@example.com" and password "password"
        if email == 'admin@example.com' and password == 'password':
            # If the login is successful, store user data in the session
            session['user_email'] = email
            return redirect(url_for('quick_registration'))
        else:
            error_message = "Invalid email or password. Please try again."
            return render_template('login.html', error_message=error_message)

    else:
        return render_template('login.html')


# ... (other routes)

if __name__ == '__main__':
    app.run(debug=True)



@app.route('/logout')
def logout():
    # Clear the user session and log out the user
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

    


