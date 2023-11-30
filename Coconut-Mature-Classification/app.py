from flask import Flask, request, render_template, redirect, url_for, session

import os
import base64
import io
from PIL import Image
from utils import *
from configs import *

app = Flask(__name__)
app.secret_key = "your_secret_key"
 
@app.route("/")
def index():

    """
    View function for the root route ("/"), rendering the "index.html" template.

    This route serves as the main entry point of the web application, displaying the home or landing page.

    Returns:
    - Renders the "index.html" template.
    """

    return render_template("index.html")

@app.route("/products", methods=["GET", "POST"])
def products():

    """
    View function for the "/products" route, handling both GET and POST requests.

    This route allows users with an active session (logged in) to upload images or provide captured image data
    for coconut type prediction. The predicted results, including the coconut type and confidence score,
    are displayed on the "products.html" template.

    Methods:
    - GET: Renders the "products.html" template with the option to upload images or provide captured image data.
    - POST: Processes the uploaded image or captured image data, performs coconut type prediction,
            saves the image and prediction results, and updates the current_id for the next upload.

    Returns:
    - If the user is not logged in, redirects to the login page.
    - If the request is a GET, renders the "products.html" template.
    - If the request is a POST, renders the "products.html" template with the prediction results.

    Variables:
    - current_id: A global variable representing the current identifier for uploaded images.
    - class_name: The predicted coconut type.
    - class_score: The confidence score associated with the prediction.
    - captured_image_data: The base64-encoded image data if provided through the captured-image-data field.
    """

    if "email" in session:
        global current_id

        class_name = None
        class_score = 0
        captured_image_data = None

        if request.method == "POST":
            file = request.files.get("file")
            captured_image_data = request.form.get("captured-image-data")

            if file:
                # Xử lý ảnh đã tải lên
                image = Image.open(file)
                class_name, class_score = predict(image)

                # Tạo tên tệp ảnh dựa trên ID và lưu ảnh vào thư mục predict
                image_filename = os.path.join(SAMPLE_FOLDER, "image", f"{current_id}.jpg")
                image.save(image_filename)

                # Tạo tên tệp txt chung để lưu kết quả dự đoán
                result_filename = os.path.join(SAMPLE_FOLDER, "results.txt")
                with open(result_filename, "a", encoding="utf-8") as result_file:
                    result_file.write(f"ID: {current_id}, Coconut Type: {class_name}, Confidence: {class_score*100:.2f}%\n")

                # Tăng ID lên để sử dụng cho lần tải lên tiếp theo
                current_id += 1

                # Cập nhật giá trị mới của current_id vào tệp
                update_current_id(current_id)
            elif captured_image_data:
                # Lấy dữ liệu ảnh từ trường captured-image-data
                image_data_uri = captured_image_data

                # Chuyển đổi dữ liệu ảnh dưới dạng URI thành đối tượng hình ảnh
                image_data = base64.b64decode(image_data_uri.split(",")[1])
                file = io.BytesIO(image_data)
                image = Image.open(file)

                # Thực hiện dự đoán
                class_name, class_score = predict(image)

                # Tạo tên tệp ảnh dựa trên ID và lưu ảnh vào thư mục predict
                image_filename = os.path.join(SAMPLE_FOLDER, "image", f"{current_id}.jpg")
                image.save(image_filename)

                # Tạo tên tệp txt chung để lưu kết quả dự đoán
                result_filename = os.path.join(SAMPLE_FOLDER, "results.txt")
                with open(result_filename, "a", encoding="utf-8") as result_file:
                    result_file.write(f"ID: {current_id}, Coconut Type: {class_name}, Confidence: {class_score*100:.2f}%\n")

                # Tăng ID lên để sử dụng cho lần tải lên tiếp theo
                current_id += 1

                # Cập nhật giá trị mới của current_id vào tệp
                update_current_id(current_id)

            if class_name is None:
                class_name = "Không xác định"
        return render_template("products.html", captured_image_data=captured_image_data, class_name=class_name, class_score=class_score)
    else:
        return redirect(url_for("login"))
    

@app.route("/aboutus")
def aboutus():

    """
    View function for the "/aboutus" route, rendering the "aboutus.html" template.

    This route provides information about the web application, team, or any relevant content on the "aboutus.html" page.

    Returns:
    - Renders the "aboutus.html" template.
    """

    return render_template("aboutus.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    """
    View function for the "/login" route, handling both GET and POST requests.

    This route allows users to log in by providing their email and password. If the login is successful,
    the user's email and username are stored in the session, and they are redirected to the "products" page.
    If the user chooses to register, they are redirected to the registration page.

    Methods:
    - GET: Renders the "login.html" template with an optional login error message.
    - POST: Processes the login form, validates the user's credentials, and logs in the user if successful.
            If the user chooses to register, redirects to the registration page.

    Returns:
    - If the login is successful, redirects to the "products" page.
    - If the user chooses to register, redirects to the registration page.
    - If the login is unsuccessful, renders the "login.html" template with an error message.

    Variables:
    - mess: A message variable used to display login error messages.
    """

    mess = ""

    if request.method == "POST":
        if "register" in request.form:
            # Nếu người dùng chọn đăng ký, chuyển hướng đến trang đăng ký
            return redirect(url_for("register"))

        email = request.form["email"]  # Lấy email từ form
        password = request.form["password"]
        authenticated, username = is_authenticated(email, password)

        if authenticated:
            session["email"] = email
            session["username"] = username  # Set the username in the session
            return redirect(url_for("products"))
        else:
            mess = "Đăng nhập không thành công. Thử lại."

    return render_template("login.html", mess=mess)


@app.route("/register", methods=["GET", "POST"])
def register():

    """
    View function for the "/register" route, handling both GET and POST requests.

    This route allows users to register by providing a username, email, and password.
    If the registration is successful, the user information is added to the users file,
    and a success message is displayed on the "login.html" template.

    Methods:
    - GET: Renders the "login.html" template with an optional registration success message.
    - POST: Processes the registration form, validates the email uniqueness,
            adds the new user to the users file if successful, and displays a success message.

    Returns:
    - If the registration is successful, renders the "login.html" template with a success message.
    - If the email is already registered, renders the "login.html" template with an error message.

    Variables:
    - message: A message variable used to display registration success or error messages.
    - success: A boolean variable indicating whether the registration was successful or not.
               Used to conditionally display the success message.
    - isRegisterShown: A boolean variable indicating whether the registration form is shown or not.
                      Used to conditionally display the registration form on the "login.html" template.
    """

    message = ""
    success = False

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        users_df = pd.read_csv(USERS_FILE, dtype={"password": str})

        if email in users_df["email"].values:
            message = "Email đã tồn tại. Thử lại."
        else:
            new_user = pd.DataFrame({"username": [username], "email": [email], "password": [password]})
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            users_df.to_csv(USERS_FILE, index=False)
            message = "Đăng ký thành công!"
            success = True

    return render_template("login.html", message=message, success=success,isRegisterShown=True)

@app.route("/logout")
def logout():

    """
    View function for the "/logout" route.

    This route logs the user out by clearing the session and redirects them to the home page.

    Returns:
    - Redirects to the "index" page after clearing the session.
    """

    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)