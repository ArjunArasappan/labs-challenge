# Penn Labs Backend Challenge

## Documentation


### **Overview**

The Penn Club Review API provides routes for users to interact with a database of clubs, including their details and associated files. Users can search for clubs, add new clubs, mark a club as favorite, update club information, upload and retriev club files, and more.


### **API Endpoints**

#### **1. Home Route**
- **Endpoint**: `/`
- **Method**: GET
- **Description**: A basic route returning a welcome message.

#### **3. Get All Clubs**
- **Endpoint**: `/api/clubs`
- **Method**: GET
- **Description**: Retrieves all the clubs from the database with their details including tags and favorite counts.

#### **4. Upload File for a Club**
- **Endpoint**: `/api/clubs/<club_code>/upload`
- **Method**: POST
- **Description**: Allows authenticated users to upload files associated with a club.


#### **5. Retrieve File for a Club**
- **Endpoint**: `/api/clubs/<club_code>/uploads/<file_name>`
- **Method**: GET
- **Description**: Allows authenticated users to download files associated with a club.


#### **6. Get User Profile**
- **Endpoint**: `/api/user/<username>`
- **Method**: GET
- **Description**: Retrieves the profile details of a specified user.


#### **7. Search for Clubs with Substring**
- **Endpoint**: `/api/clubs/search/<query>`
- **Method**: GET
- **Description**: Searches for clubs with names containing the provided substring.


#### **8. Add New Club**
- **Endpoint**: `/api/clubs`
- **Method**: POST
- **Description**: Allows authenticated users to add a new club to the database.


#### **9. Favorite a Club**
- **Endpoint**: `/api/clubs/<club_name>/favorite`
- **Method**: POST
- **Description**: Allows authenticated users to mark a club as their favorite.


#### **10. Modify Club Information**
- **Endpoint**: `/api/clubs/<club_name>`
- **Method**: PUT
- **Description**: Allows authenticated users to update a club's name and description.


#### **11. Show All Tags and Associated Club Counts**
- **Endpoint**: `/api/tags`
- **Method**: GET
- **Description**: Retrieves all tags from the database with the count of clubs associated with each tag.




### **Authentication and User Management**

#### **1. User Signup**
- **Endpoint**: `/api/signup`
- **Method**: POST
- **Description**: Allows new users to register.


#### **2. User Login**
- **Endpoint**: `/api/login`
- **Method**: POST
- **Description**: Authenticates and logs in a user.


#### **3. User Logout**
- **Endpoint**: `/api/logout`
- **Method**: POST
- **Description**: Logs out an authenticated user.


### **Helper Functions**

1. **allowed_file**: Checks if the uploaded file type is allowed.
2. **check_fields**: Ensures that all required fields are present in a data dictionary.



---

## Installation

1. Click the green "use this template" button to make your own copy of this repository, and clone it. Make sure to create a **private repository**.
2. Change directory into the cloned repository.
3. Install `pipenv`
   - `pip install --user --upgrade pipenv`
4. Install packages using `pipenv install`.

## File Structure

- `app.py`: Main file. Has configuration and setup at the top. Add your [URL routes](https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing) to this file!
- `models.py`: Model definitions for SQLAlchemy database models. Check out documentation on [declaring models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) as well as the [SQLAlchemy quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart) for guidance
- `bootstrap.py`: Code for creating and populating your local database. You will be adding code in this file to load the provided `clubs.json` file into a database.

## Developing

0. Determine how to model the data contained within `clubs.json` and then complete `bootstrap.py`
1. Run `pipenv run python bootstrap.py` to create the database and populate it.
2. Use `pipenv run flask run` to run the project.
3. Follow the instructions [here](https://www.notion.so/pennlabs/Backend-Challenge-862656cb8b7048db95aaa4e2935b77e5).
4. Document your work in this `README.md` file.

## Submitting

Follow the instructions on the Technical Challenge page for submission.

## Installing Additional Packages

Use any tools you think are relevant to the challenge! To install additional packages
run `pipenv install <package_name>` within the directory. Make sure to document your additions.
