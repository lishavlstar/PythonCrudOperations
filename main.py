try:
    from app import app
    import os
    from controller import *

except Exception as e:
    print('some of the modules are not imported.')

#Home route TODO: remove if not required
@app.route('/')
def home():
    return('home route please check API documentation')

#Function call for User registration
@app.route('/identity/registeruser', methods=['POST'])
def client():
    return (createClient())

@app.route('/identity/login', methods=['POST'])
def login_user():
    return (login())

@app.route('/identity/update', methods=['PUT'])
def user_update():
    return (update())

@app.route('/identity/changepasswd', methods=['PUT'])
def password_update():
    return (passwordUpdate())


@app.route('/identity/forgotpasswd', methods=['PUT'])
def forgot_password():
    return (forgotPassword())



if __name__ == "__main__":
    app.run(debug=True)


