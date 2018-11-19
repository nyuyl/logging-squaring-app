import os
from flask import Flask, render_template, request, redirect,url_for, send_file, send_from_directory, make_response
from werkzeug import secure_filename
from flask import session
from models import db, User, Logging,Picture
from forms import SignupForm, LoginForm1, LoginForm
import cv2

# Get the absolute path of the current directory
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Size limit of uploads folder in KB
UPLOAD_FOLDER_LIMIT = 200 * 1024 # 200MB
DOWNLOAD_FOLDER_LIMIT = 200 * 1024 # 200MB
UPLOAD_FILE_LIMIT = 20 * 1024 # 20MB

# Cookies
session = {'filename': '', 'params': {}, 'filename_resized': ''}

#importing the Flask class and initialize
app = Flask(__name__)

#Configure Flask by providing the PostgreSQL URI so that the app is able to connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
#connect SQLAlchemy object to your application
db.init_app(app)

app.secret_key = "development-key"

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = os.path.join('THIS_FOLDER,uploads/')
app.config['DOWNLOAD_FOLDER'] = os.path.join('THIS_FOLDER,downloads/')
# Create upload_folder and download_folder if not exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

# These are the extension that are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

# Cache related to prevent cache problems
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300

# Limit the upload file size
app.config['MAX_CONTENT_LENGTH'] = UPLOAD_FILE_LIMIT*1024# Need to be in bytes

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return ('.' in filename) and ((filename.rsplit('.', 1)[1]).lower() in app.config['ALLOWED_EXTENSIONS'])

# Resize a image using user-defined parameters
def resizer_ratio(img, fx = 1, fy = 1):
    res = cv2.resize(src = img, dsize = None, fx = fx, fy = fx, interpolation = cv2.INTER_AREA)
    return res

def resizer_defined(img, width = None, height = None):
    res = cv2.resize(src = img, dsize = (width, width), fx = 0, fy = 0, interpolation = cv2.INTER_AREA)
    return res

# Calculate the total size of all files in a directory
def size_calculate(directory_path):
    size_total = 0
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        size_total += os.path.getsize(file_path)
    # Turn byte to KB
    size_total = size_total/1024
    return size_total

# Clean up all the files in a directory
def directory_cleanup(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)
    return

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation

#URL '/' to be handled by main() route handler
@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()
 
  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('home'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('login.html', form=form)
    else:
      newlogging = Logging(form.email.data, form.password.data)
      db.session.add(newlogging)
      db.session.commit()
   
      email = form.email.data 
      password = form.password.data 

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = form.email.data 
        return redirect(url_for('home'))
      else:
        return redirect(url_for('login'))

  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
 if 'email' not in session:
    return redirect(url_for('login'))
 elif request.method == 'GET':
    return render_template("home.html")

# Route that will process the file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Calculate the total size of upload folder and download folder
    # Cleanup the folders if the size exceeds the limits
    upload_folder_size = size_calculate(app.config['UPLOAD_FOLDER'])
    download_folder_size = size_calculate(app.config['DOWNLOAD_FOLDER'])
    if upload_folder_size > UPLOAD_FOLDER_LIMIT:
        directory_cleanup(app.config['UPLOAD_FOLDER'])
    if download_folder_size > DOWNLOAD_FOLDER_LIMIT:
        directory_cleanup(app.config['DOWNLOAD_FOLDER'])

    if request.method == 'POST':
        # Get the name of the uploaded file
        file = request.files['file']
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload folder we setup
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Get the resize_mode the user requested
            resize_mode = request.form['resize_mode']
            width = request.form['width']
            height = request.form['width']
            fx = request.form['fx']
            fy = request.form['fx']
            # User-defined parameter dictionary
            params = {'resize_mode':resize_mode, 'width': width, 'height': width, 'fx': fx, 'fy': fx}
            
            # Save parameters to cookies
            session['filename'] = filename
            session['params'] = params
            # Read image
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = cv2.imread(file_path)
            if params['resize_mode'] == 'ratio_mode':
                fx = float(params['fx'])
                fy = float(params['fx'])
                res = resizer_ratio(img, fx = fx, fy = fx)
            else: # defined_mode
                width = int(params['width'])
                height = int(params['width'])
                res = resizer_defined(img, width = width, height = width)

            # Save resized image
            filename_resized_prefix = filename.rsplit('.', 1)[0]
            filename_resized = filename_resized_prefix + '_resized.png'
            session['filename_resized'] = filename_resized

            dst_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename_resized)

            # Save resized image
            cv2.imwrite(filename = dst_path, img = res)

            # Original image file size in byte
            filesize_original = os.path.getsize(file_path)
            # Turn byte to KB
            filesize_original = int(filesize_original/1024)

            # Resized image file size in byte
            filesize_resized = os.path.getsize(dst_path)
            # Turn byte to KB
            filesize_resized = int(filesize_resized/1024)
            #add to db
            newpicture = Picture(imagename=filename,originalsize=filesize_original,newsize=filesize_resized)
            db.session.add(newpicture)
            db.session.commit()
            # Redirect the user to the resize_image route
            return redirect(url_for('resize_image'))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/resize')
def resize_image():
    filename = session['filename']
    params = session['params']

    # Read image
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = cv2.imread(file_path)
    if params['resize_mode'] == 'ratio_mode':
        fx = float(params['fx'])
        fy = float(params['fx'])
        res = resizer_ratio(img, fx = fx, fy = fx)
    else: # defined_mode
        width = int(params['width'])
        height = int(params['width'])
        res = resizer_defined(img, width = width, height = width)

    # Save resized image
    filename_resized_prefix = filename.rsplit('.', 1)[0]
    filename_resized = filename_resized_prefix + '_resized.png'
    session['filename_resized'] = filename_resized

    dst_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename_resized)

    # Save resized image
    cv2.imwrite(filename = dst_path, img = res)

    # Original image file size in byte
    filesize_original = os.path.getsize(file_path)
    # Turn byte to KB
    filesize_original = int(filesize_original/1024)

    # Resized image file size in byte
    filesize_resized = os.path.getsize(dst_path)
    # Turn byte to KB
    filesize_resized = int(filesize_resized/1024)

    return render_template('download.html', filesize_original = filesize_original, filesize_resized = filesize_resized)

@app.route('/download', methods=['GET', 'POST'])
def download():
    filename_resized = session['filename_resized']
    if request.method == 'GET':
        return send_from_directory(directory = app.config['DOWNLOAD_FOLDER'], filename = filename_resized)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Launch built-in web server and run this Flask webapp
if __name__ == "__main__":
  app.run(debug=False)
