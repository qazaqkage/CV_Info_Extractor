from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os

# Initialize Flask app
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/job_matching_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = './uploaded_cvs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Welcome to the Job Matching API!"


# Registration endpoint
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        # Render a simple HTML form for registration
        return '''
        <form action="/register" method="post">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br><br>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br><br>
            <button type="submit">Register</button>
        </form>
        '''

    elif request.method == 'POST':
        # Handle JSON data or form data
        if request.is_json:
            data = request.json
        else:
            data = request.form

        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not email or not password or not name:
            return jsonify({'error': 'Missing required fields'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        new_user = User(
            email=email,
            password_hash=User.hash_password(password),
            name=name
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

# Login endpoint
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render an HTML form for testing login
        return '''
        <form action="/login" method="post">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
        '''

    elif request.method == 'POST':
        # Handle JSON or form data
        if request.is_json:
            data = request.json
        else:
            data = request.form

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid email or password'}), 401

        token = create_access_token(identity={'id': user.id, 'email': user.email})
        return jsonify({'access_token': token}), 200


# Secure endpoint
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({'user': current_user}), 200


@app.route('/upload_cv', methods=['POST'])
@jwt_required()
def upload_cv():
    try:
        if 'file' not in request.files:
            app.logger.error("No file part in the request")
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']
        if file.filename == '':
            app.logger.error("No file selected")
            return jsonify({'error': 'No file selected'}), 400

        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        app.logger.info(f"File saved successfully at {file_path}")

        return jsonify({'message': 'File uploaded successfully!', 'file_path': file_path}), 200

    except Exception as e:
        app.logger.error(f"Error during file upload: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500



class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())


@app.route('/add_job', methods=['POST'])
@jwt_required()
def add_job():
    data = request.json

    # Validate and parse input data
    title = data.get('title')
    description = data.get('description')
    company = data.get('company')
    location = data.get('location')

    if not all([title, description, company, location]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Save to database
    new_job = Job(
        title=title,
        description=description,
        company_name=company,
        location=location
    )
    db.session.add(new_job)
    db.session.commit()

    return jsonify({'message': 'Job added successfully'}), 201



# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
