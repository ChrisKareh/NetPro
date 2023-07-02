from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
import mysql.connector

app = Flask(__name__)
CORS(app)


db_host = "localhost"
db_user = "root"
db_password = "Test@1234"
db_database = "senior_db"


@app.route('/api/login', methods=['GET'])
@cross_origin()
def login():
    email = request.args.get('email')
    password = request.args.get('password')

 
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

  
    cursor = mydb.cursor()

  
    query = """
    SELECT * FROM users WHERE email = %s AND password = %s
    """
    cursor.execute(query, (email, password))
    result = cursor.fetchone()

    
    if result:
        user_id, email, _ = result  
        user_info = {
            'id': user_id,
            'email': email
            
        }
        response = {
            'status': 'success',
            'message': 'Login successful',
            'user': user_info
        }
    else:
        response = {
            'status': 'error',
            'message': 'Invalid credentials'
        }

    
    cursor.close()
    mydb.close()

    return jsonify(response)

if __name__ == '__main__':
    app.run(port= 5000)
