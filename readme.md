# Identification of the problem and why it needs solving

API Webserver Project: backend development using Python-Flask as web framework and PostgresSQL as database management system.

[GitHub repository](https://github.com/ellenpham/API_Webserver_LocalTourBookingWebApp)

The purpose of this application is to to provide an alternative to the traditional method of travel guide, which is usually provided through the service of travel agencies. This application creates a platform where tourists can find a local tour guide for their upcoming overseas trips and for self-employed tour guides to offer their tours to tourists all around the world without the need of a travel agency. All interactions and transactions between tourists and tour guides are 100% self-operating, the application only acts as a facilitating tool or a networking system. 

The problem to which this application is the solution, is based on the increasing trend for cultural immersion experience in travelling. Nowadays, travelling is not just a getaway trip, to many people, travelling is to explore different horizons, to gain insights and connect with people from different backgrounds, make the trip a memorable experience. The best way is to have a local tour guide who has the most authentic experience, who can offer a unique and personalized experience. Even self-guided tourists might find it helpful to have a local tour guide, who can give tips that save them from costly and timely experience. 

On the other hand, self-employed tour guides can also benefit from the platform, as they can offer the tours designed based on their own capabilities, flexibly schedule the timeframe, especially if this serves as side job. Most importantly, there is no need for an intermediary agent, it means all communications and transactions between tourists and tour guides are direct and open, this helps establish a mateship between them prior to the trips and even after. 

## Problems to be solved

Now we know the purposes for building the application, we further break down the problems that need solving to achieve those purpose. First, a list of user stories was created to be the foundation for developing the application features. Based on the user stories, an outline of CRUD functionalities is created as part of functionality requirements. These functionality requirements are the problems needed to be solved within the scope of this application.

## User stories

View user stories [here](docs/user_stories.md)

## Functionality requirements

#### CRUD functionalities for tourists
- Tourist account owner:
    - Register/Log in
    - Create/View/Update their own account with full privileges
    - Deactivate their own account
    - View an active tour guide account with limited access to information 
    - View tours
    - Create a booking to an available tour
    - Create/View/Update/Delete a tour booking with full privileges (assuming that the privilege to Delete complies with a cancellation policy based on mutual agreement)
    - Create/View/Update/Delete their own reviews with full privileges (can only review the tours they have booked)
    - View other tourists' reviews

#### CRUD functionalities for tour guides
- Tour guide account owner:
    - Register/Log in 
    - Create/View/Update their own account with full privileges
    - Deactivate their own account
    - View a tourist account with limited access to information (only applied for tourists who have booked their tours)
    - Create/View/Update/Delete their own tours with full privileges (only can Delete a tour if it has not been booked)
    - View tour bookings (only apply to the tour bookings of their own tours)
    - View tourists' reviews

#### CRUD functionalities for admins
- Admin account owner:
    - View all information with full info: user accounts, tours, tour bookings, reviews
    - Delete all information: user accounts, tours, tour bookings, reviews

Other functionality requirements include:

- Data security: by using authentication mechanism upon login requests and authorization mechanism for granting privileges to relevant users.

- Data integrity and accuracy: by validating and sanitizing incoming data and handling exceptions for graceful response to errors.

<br>

# Database Management System

PostgresSQL is the database management system used in this application. 

*Advantages*

- The database used in the application is relational database, where different entities in the database are mostly related to each other. PostgresSQL is one of the most popular relational database management system (RDBMS), which help manage data in a secure, rules-based and consistent way. 
- It is known for its reliability, extensibility, availability, scalability as well as performance and data security. All these factors are important as this application will be operated based on the exchanging interactions of users and there will be sensitive data involved. 
- Cross-platform and extensive language support it is compatible with Python programming language, which is the language used for this application's web framework. Cross-platform support is also required as this application will be used from worldwide users and most likely by mobile devices.
- Open source and strong community support: it is free, well maintained and supported by strong community of developers, its documentation is comprehensive and informative.
- Full ACID compliance which helps ensure data validity and integrity.
- Advanced data types and processing with a rich set of built-in data types.

*Disadvantages*

- PostgresSQL as a RDBMS is more complex compared to other NoSQL database system like MongoDB. In the early phase of development, data modelling with reasonable normalisation level is required before getting built with PostgresSQL to avoid further modifications which can be complicated. 

- PostgresSQL is lightly slower than MySQL for read-only commands but it is faster for handling massive data sets, complicated queries, and read-write operations. Ultimately, speed will depend on the way you’re using the database ([Integrate.io](https://www.integrate.io/blog/postgresql-vs-mysql-which-one-is-better-for-your-use-case/)).

- Installation and configuration is more complex than MySQL. MySQL has more user-friendly interface, it is simpler to set up and manage.

<br>

# ORM - Key functionalities and benefits

ORM stands for Object Relational Mapping, it is used for interaction between an application and a database. Instead of plain SQL, it is written in the programming language used to code the application, hence, make it easier to develop the database without switching back and forth with SQL queries to interact with database. In another word, ORM allows developers to write queries using the object-oriented paradigm of preferred programming language, this facilitates the integration of database entities as classes in object-oriented programming applications, or as models in MVC applications. In this application, SQLAlchemy is used as Object Relational Mapper and Flask-SQLAlchemy is the Flask extension that adds support for SQLAlchemy to the Flask application ([pythonbasics.org](https://pythonbasics.org/flask-sqlalchemy/)).

### Key functionalities of ORM

As mentioned earlier, SQLAlchemy is the ORM used to connect Flask and PostgresSQL. Therefore, in the scope in this project, we will use examples of SQLAlchemy and PostgresSQL in discussing ORM and the corresponding SQL.

**Create a model**

ORM helps create a model as a class, from which we can create objects/entities and establish the tabular structure of entities in the database. Similar to a table in SQL, where rows are records and columns are attributes/fields. With ORM, we can also define them using variables within a class. 

Models and routes are modularized by using different `.py` files for different models. This makes it easier to import the models as modules when needed. 

```
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created= db.Column(db.Date, default=date.today())
```

The above example illustrates how a table is created using ORM. Review is the database model which is created as a Review class. `__tablename__` is used to refer the model to `reviews` table in the database. In the `reviews` table, there are following columns `id`, `rating`, `message` and `date_created` and these variables within the Review class are defined as columns using `db.Column`. Similar to SQL, data types and constraints of an attribute can also be defined using ORM.

Also, foreign keys are defined as below when using ORM:

```
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```

To create the associations between tables, the below ORM syntax is used. In this case, the relationship between `user` and `reviews` is one-to-many relationship, and it is established using `db.relationship`.

In `review..py`
```
user = db.relationship('User', back_populates='reviews')
```
In `user.py`

```
reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
```

With PostgresSQL, this could be written as below:

```
CREATE TABLE REVIEWS (
    id integer PRIMARY KEY,
    rating integer NOT NULL,
    message text NOT NULL, 
    date_created date DEFAULT CURRENT_DATE,
    user_id integer NOT NULL,
    FOREIGN KEY(user_id) REFERENCES USERS(id) ON DELETE CASCADE
);
```

**CLI commands**

The data seeding is done using the ORM functionality of CLI commands. The syntax to create a CLI command is `@db_commands.cli.command('create')` and it will invoke the `create_db` function. It acts similarly as `CREATE TABLE` in SQL. The `DROP TABLE` operation is done the same way using `@db_commands.cli.command('drop')`. 

```
db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Table created')
```

The seeding operation is similar to `INSERT`. A record in the table is an instance of the class and it is seeded to the database as below: 

```
@db_commands.cli.command('seed')
def seed_db():
    review = Review(
        id = '1',
        rating = '5',
        message = 'Lorem ipsum dolor sit amet',
        date_created = date.today(),
        user_id = '1',
    )
    db.session.add(review)
    db.session.commit()
```

With PostgresSQL, this could be written as below:

```
INSERT INTO reviews(id, rating, message, date_created, user_id) VALUES (2, 5, 'Lorem ipsum dolor sit amet', DEFAULT, 1);
```

To execute these operations, we run the following commands in the terminal: `flask create`, `flask drop` and `flask seed`. In this case, because a Blueprint is used for the purpose of organizing routes, therefore, the CLI commands are run in the terminal as `flask db create`, `flask db drop` and `flask db seed`.

**Data manipulation**

ORM also supports other SQL commands for data manipulation such as `SELECT`, `DELETE`, `UPDATE`, SQL queries clauses such as `WHERE`, `GROUP BY`, `ORDER BY`, etc and multi-table queries (subqueries and join tables). Below are some examples:

- Code written using ORM to get all reviews from `reviews` table in an ascending date order:

```
def get_all_reviews():
    stmt = db.select(Review).order_by(Review.date_created.asc())
    reviews = db.session.scalars(stmt)
    return reviews
```

With PostgresSQL, this could be written as below:

```
SELECT * FROM reviews ORDER BY date_created ASC;
```

- Code written using ORM to get the review message from the first review in the `reviews` table:

```
def get_one_review():
    stmt = db.select(Review).filter_by(id=1)
    review = db.session.scalar(stmt)
    return review.message
```

In SQL, this could be written as below:

```
SELECT message FROM reviews where id = 1;
```

- Code written using ORM to delete a review:

```
def delete_review():
    stmt = db.select(Review).join(Tour).filter(and_(Tour.id==1, Review.id==2))
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
```

With PostgresSQL, this could be written as below using subqueries:

```
DELETE FROM reviews
WHERE reviews.id=2 AND tour_id = (SELECT id FROM tours WHERE id='1');
```

There are many available ORM tools for OOP languages, such as Django, SQLAlchemy, web2py for Python app, Hibernate, Apache OpenJPA, jOOQ for Java app; Microsoft Entity Framework or Dapper for .NET framework; Laravel, CakePHP or Qcodo for PHP app, etc. They all have the below key features (source: [DEV community](https://dev.to/dak425/what-are-orms-and-why-should-you-use-them-2ng4), [EDUCBA](https://www.educba.com/what-is-orm/) and [freeCodeCamp](https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/)):

- The application is made independent of the DBMS used in the backend. Therefore, generic queries can be written, which makes it easier for when migrating to another database.
- Developers are not required to learn SQL syntaxes separately for whichever database being used to support the application.
- All small or big changes can be implemented using ORM, no such restrictions in data handling and manipulation.
- The connection are robust and more secure due to less intervention in code.
- ORM also has its shortcoming, it is only recommended for small to mid-sized projects. When very complex queries are involved, ORM is likely not going to perform better. Also, ORM is mainly used for SQL databases, it is not common in NOSQL databases. 


### Key benefits of ORM

- ORM helps simplify the interaction between relational databases and different OOP languages. CRUD operations can be performed with the ORM API without writing raw SQL statements ([pythonbasics.org](https://pythonbasics.org/flask-sqlalchemy/)).
- It supports tasks like transactions, connection pooling, migrations, seeds, etc.
- The implementation is simple and easy to maintain, which helps speed up development time. 
- Less and neater code is written when using ORM than with SQL
- If there are changes in database, the code is not likely to change or just needs minor changes.
- Security is improved as ORM tools are built with the idea of data abstraction, which helps prevent the risk of SQL injection attacks ([freeCodeCamp](https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/)).
- Queries via ORM can be written irrespective of whatever database one is using in the backend, which provides flexibility to developers. ([EDUCBA](https://www.educba.com/what-is-orm/)).

<br>

# API endpoints documentation

## App installation

### System prerequisites

- Python Version 3x is required to run the application. If Python has not been installed in your computer, please download by following [this link](https://www.python.org/downloads/).

- Git Setup is required to be able to clone the repo to your computer, follow [this link](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) to set up Git. Alternatively, you can download zip file to your computer by going to my [GitHub repo](https://github.com/ellenpham/API_Webserver_LocalTourBookingWebApp), click into **Code**, then **Download ZIP**.

- PostgresSQL is required for this applcation as database management system. If PostgresSQL has not been installed in your computer, please download and install by following [this link](https://www.postgresql.org/download/).

### Installation steps

In your computer, open terminal or command prompt:

- Change the directory to a folder where you want to download the app using `cd <directory>`

- Clone this repository using `git clone https://github.com/ellenpham/API_Webserver_LocalTourBookingWebApp`

- Change the directory to the `src` folder using `cd ./API_Webserver_LocalTourBookingWebApp/src`

- Create virtual environment an activate it using the following commands:

    ```    
    python3 -m venv .venv
    source .venv/bin/activate
    ```

- Install the dependencies, using `pip3 install -r requirements.txt`

- In another terminal window, start your PostgresSQL service and run `psql` to access the database management system. Set up environment variables and create database in your PostgresSQL by following the configuration in the `.env` folder or provided `config.md` folder to set up the database URL and JWT key. 

- To create the initial database for API testing run the following CLI commands in order: `flask db drop`, `flask db create`, `flask db seed`

- Once the database is all set up, run the following SQL commands to check if the data has been seeded successfully:

    ```
        \c <db_name>
        \dt
        SELECT * FROM <table_name>
    ```

- Run the app using `flask run`

- Open an API client, follow the API endpoints documentation to implement the test. 


## API client

As this project is developed as an API Webserver, the front-end has not been built for a proper APIs testing. We will need a different tool for sending requests to an API and inspecting the generated response. An API client is the tool to do such query testing, two popular choices are [Postman](https://www.postman.com/downloads/) and [Insomnia](https://insomnia.rest/download), you can choose your preferred one.

## API endpoints

Once Postman or Insomnia is installed, you can create HTTP requests and use the routes, methods and data provided in the below documentation to test the application. 

View the documentation of API endpoints [here](docs/API_endpoints.md)

<br>

# Entity Relationship Diagram (ERD)

![ERD](docs/T2A2_ERD.png)

<br>

# Third party services used in the app

**Flask** (version 2.3.2)

Flask is a lightweight WSGI web framework, it is a Python library used to make web applications in Python programming language. Here, Flask is used for the controller and model part in the backend when applied in an MVC architecture. Flask provides useful tools and features foe easily develop web apps, it is easy to extend and has a built-in debugger, which shows tracebacks in the browser when an unhandled error happen during a request ([Flask documentation](https://flask-docs.readthedocs.io/en/latest/debugging/#the-built-in-debugger)).

**Psycopg2** (version 2.9.6)

Psycopg2 is used to create the database connection in a Flask app, it is the most common PostgresSQL database adapter for Python programming language. With Psycopg2, Python data types are supported and adapted to match data types in PostgreSQL. Its key features are the complete implementation of the Python DB API 2.0 specifications, especially thread safety. Psycopg2 is both efficient and secure because it was built around libpq, a PostgreSQL client library, which performs the majority of network communications and returns query results in C structures. ([PyPI](https://pypi.org/project/psycopg2/)).

**Python-dotenv** (version 1.0.0)

Python-dotenv is a library that helps read key-value pairs from encrypted `.env` files and set them as environment variables. Normally, your application might need some sensitive or environment specific information to perform certain tasks that you might want to keep in the local machine instead of publicly disclosed on source control system like GitHub. A `.env` file is used to store those information. To read the `.env` files, every programming language has a different package or library and `Python-dotenv` is the option for Python applications ([DEV Community](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1)).


**SQLAlchemy** (version 2.0.18)

SQLAlchemy is a Python SQL toolkit and an Object Relational Mapper (ORM). It provides developers the full power and flexibility to access database access in relational databases. SQLAlchemy as an ORM is used to make queries and handle data using simple Python objects and methods. In this application, Flask-SQLAlchemy (version 3.0.5) is also installed. It is an extension for Flask, which provides methods and tools to interact with database in Flask apps through SQLAlchemy. It simplifies the use of SQLAlchemy with Flask by setting up objects and patterns to use those objects such as sessions tied to web requests, models and engines ([DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application), [Flask-SQLAlchemy documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)).

**Marshmallow** (version 3.19.0)

Marshmallow is an ORM framework-agnostic library. It is used for converting complex datatypes like objects, to and from primitive Python datatypes. When we get data from database and pass it to API using HTTP requests, our data needs to be serialized for it to be rendered to standard JSON format, and vice versa, when data is loaded from the request, it needs to be parsed or deserialized into Python datatypes to be processed at the backend. Marshmallow is the tool that do such tasks. Marshmallow schemas are used to validate input data, deserialize input data to app-level objects and serialize app-level objects to native Python datatypes ([Marshmallow documentation](https://marshmallow.readthedocs.io/en/stable/)).

In this application, Flask-Marshmallow (version 0.15.0) and Marshmallow-SQLAlchemy (version 0.29.0) are also installed. They are integrated with each other to add additional features to Marshmallow and make the whole API work with Flask and SQLAlchemy ([Flask-Marshmallow documentaion](https://flask-marshmallow.readthedocs.io/en/latest/)).

**bcrypt** (version 4.0.1)

Bcrypt is a password hashing function, it is used for encrypting sensitive data and files in the database storage. In this application, Flask-Bcrypt (version 1.0.1) is also installed, it is the Flask extension for Bcrypt hashing utilities. Flask-Bcrypt uses the slow hashing technique, it is designed to be "de-optimized", which helps prevent brute force attacks, it is recommended for protecting sensitive data, such as passwords ([Flask-Bcrypt documentation](https://flask-bcrypt.readthedocs.io/en/1.0.1/)).

**Flask-JWT-extended** (version 4.5.2)

JSON Web Tokens (JWT) is the chosen authentication/authorization standard in this application. Once a user is registered with the app, every time they log in, they will be grant a token (can be expired or non-expired), it is used to verify the user's identity. The token is stored by the user and it is used for whenever the user needs to access their personal information or perform certain tasks within the app that only them being authorised to perform, unauthorised users will not be permitted. To use this token in API testing, simply copy and paste the generated token to the Bearer Token section in Postman and Insomnia following the API endpoints documentation.

In this application Flask-JWT-extended is the library used to add support for using JWT in Flask. It helps protecting routes and has many useful built-in features to make it easier for the Flask app to work with JWT. You will need the JWT secret key to use JWT in this application. 

<br>

# Project models

In this application, models are created using SQLAlchemy, they reflect the entities in the database and are treated like Python classes. There are five models: `UserRole`, `User`, `Tour`, `TourBooking` and `Review`.

### UserRole model

The `UserRole` model is associated with the `roles` table in the database. The relationship with `User` model is one-to-many relationship. One role can be assigned to zero or many users, but one user can only have one and only one role. 

The association is established using the below code:

In `role.py`, the `users` variable in `role.py` has `cascade='all,delete'` constraint, because a user must have a role, if a role is deleted, no associated users should exist. 

The `relationship.back_populates` parameter is used to establish a bidirectional relationship in one-to-many relationship, where the "reverse" side is a many-to-one.

```
users = db.relationship('User', back_populates = 'role', cascade ='all, delete')
```

In `user.py`:

```
role = db.relationship('UserRole', back_populates='users')
```

Schemas are nested to represent the relationship between objects. The reason to nest `UserRoleSchema` in `UserSchema` because a user can either be admin, tourist or tour guide, therefore, we want to see the user role when a user is returned in the response. Nesting schemas are defined to represent this relationship as below:


In `role.py`, `role` is excluded to prevent circular references.

```
users = fields.List(fields.Nested('UserSchema', exclude=['role']))
```

In `user.py`(under `UserSchema`), we only need the `name` attribute of roles when nested in a user object.

```
role = fields.Nested('UserRoleSchema', only=['name'])
```

### User model

This application encourages the self-operated interaction between users. Hence, `users` is the main entity and `User` model is the centre model, all other models are associated to `User` model by some means. 

**Relationship with UserRole model**

This relationship is one-to-many as discussed above, `role_id` in `User` model is the foreign key, referencing the `id` of the `UserRole` model and it is not nullable, because a user must be associated with a role for applying authorisation based on the user role later on. 

In `user.py`:

```
role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
```


**Relationship with Tour model**

This relationship is one-to-many relationship. One user can have zero or many tours but one tour only belong to one and only one user. `user_id` in `Tour` model is the foreign key, referencing the `id` of the `User` model and it is not nullable, because a tour must belong to a user (a user with the role of tour guide, to be more specific).

In `tour.py`:

```
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```

The association is established using the below code:

In `user.py`, `cascade='all,delete` is the constraint of `tours` in `user.py` because once a user is deleted, all associated tours belong to that user will also be deleted. 

```
tours = db.relationship('Tour', back_populates='user', cascade='all, delete')
```

In `tour.py`:

```
user = db.relationship('User', back_populates='tours')
```

`TourSchema` is nested in `UserSchema` for when a user (a tour guide in particular) is returned in the response, their tours are stored in a list that nested in the user object. `UserSchema` is also nested in `TourSchema` but not in a list because one tour should only belong to one user. Nesting schemas are defined to represent this relationship as below:

In `user.py` (under `UserSchema`), `user` is excluded to prevent circular references.

```
tours = fields.List(fields.Nested('TourSchema', exclude=['user']))
```

In `tour.py` (under `TourSchema`), we only need `username`, `email` and `role` attributes of the tour guide user to show up in the nested user of a tour object.

```
user = fields.Nested('UserSchema', only=['username', 'email', 'role'])
```

**Relationship with TourBooking model**

This relationship is one-to-many relationship. One user can have zero or many tour bookings but one tour booking only belong to one and only one user. `user_id` in `TourBooking` model is the foreign key, referencing the `id` of the `User` model and it is not nullable, because a tour booking must belong to a user (a user with the role of tourist, to be more specific).

In `tour_booking.py`:

```
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```

The association is established using the below code:

In `user.py`, there is no `cascade='all,delete` constraint of `tour_bookings` in `user.py` because it is assumed as a feature of the application that a user cannot be deleted if there is still a existing tour booking linked to them. This associated tour booking needs to be deleted (or cancelled) for the user to be removed. 

```
tour_bookings = db.relationship('TourBooking', back_populates='user')
```

In `tour_booking.py`:

```
user = db.relationship('User', back_populates='tour_bookings')
```

`TourBookingSchema` is nested in `UserSchema` for when a user (a tourist in particular) is returned in the response, their tour bookings are stored in a list that nested in the user object. `UserSchema` is also nested in `TourBookingSchema` but not in a list because one tour booking should only belong to one user. Nesting schemas are defined to represent this relationship as below:

In `user.py` (under `UserSchema`), `user` is excluded to prevent circular references.

```
tour_bookings = fields.List(fields.Nested('TourBookingSchema', exclude=['user']))
```

In `tour_booking.py` (under `TourBookingSchema`), we only need `username`, `email` and `role` attributes of the tourist user to show up in the nested list of tour bookings.

```
user = fields.Nested('UserSchema', only=['username', 'email', 'role'])
```

**Relationship with Review model**

This relationship is one-to-many relationship. One user can have many reviews but one review can only belong to one and only one user. `user_id` in `Review` model is the foreign key, referencing the `id` of the `User` model and it is not nullable, because a review must belong to a user (this application assumes that only tourist can write reviews).

In `review.py`:

```
user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```
The association is established using the below code:

In `user.py`, `cascade='all,delete` is the constraint of `reviews` in `user.py` because once a user is deleted, all associated reviews belong to that user will also be deleted. 

```
reviews = db.relationship('Review', back_populates='user', cascade='all, delete')
```

In `review.py`:

```
user = db.relationship('User', back_populates='reviews')
```

`UserSchema` is nested in `ReviewSchema` for when a review (a tourist in particular) is returned in the response, the info of user who wrote the review is nested in the review object. There is unnecessary for `ReviewSchema` to be nested in `UserSchema`.

In `review.py` (under `ReviewSchema`), the `user` variable defines the nesting `UserSchema` within `ReviewSchema`. Only two attributes of users `username` and `role` needed to show up in the review object to tell who is the review owner. 

```
user = fields.Nested('UserSchema', only=['username', 'role'])
```

### Tour model and TourBooking model

The one-to-many relationship between `User` and `Tour` has been discussed above. From a different perspective, we can essentially say that the relationship between `Tour` and `User` can be a many-to-many relationship. In that case, the `TourBooking` is the model that joins `Tour` and `User`.

The relationship between `Tour` and `TourBooking` model is one-to-many relationship. One tour can have many or zero booking but one booking must belong to one and only one tour. `tour_id` in `TourBooking` model is the foreign key, referencing the `id` of the `Tour` model and it is not nullable, because a booking must belong to a tour.

In `tour_booking.py`:

```
tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
```

The association is established using the below code:

In `tour.py`, there is no `cascade='all,delete` constraint of `tour_bookings` in `tour.py` because it is assumed as a feature of the application that a tour cannot be deleted if there is still a existing tour booking linked to it. This associated tour booking needs to be deleted (or cancelled) for the tour to be deleted.

```
tour_bookings = db.relationship('TourBooking', back_populates='tour')
```

In `tour_booking.py`:

```
tour = db.relationship('Tour', back_populates='tour_bookings')
```

`TourBookingSchema` is nested in `TourSchema` for when a tour is returned in the response, the associated tour bookings are stored in a list that nested in the tour object. This nesting schema is only returned in a limited scenarios where an admin retrieves tours or a tour guide retrieves their own tours with full information. Generally, when unauthorized users like website visitors or general tourists want to view all tours or one tour, `tour_bookings` will be excluded in `TourSchema` because a tour booking is not supposed to be explicitly viewed. 

`TourSchema` is also nested in `TourBookingSchema` but not in a list because one tour booking should only belong to one tour. 

Nesting schemas are defined to represent this relationship as below:

In `tour.py`, `tour` is excluded to prevent circular references.

```
tour_bookings = fields.List(fields.Nested("TourBookingSchema", exclude=["tour"]))
```

In `tour_booking.py`, we only need two attributes of tours to show up in the nested tour in a tour booking object: `tour_name` and `user`. Here, `user` is the tour guide who owns the tour, and the info of user will be nested in one more layer with only three attributes belong to the user, namely `name`, `role`, `email`. 

```
tour = fields.Nested('TourSchema', only=['user', 'tour_name'])
```

### Review Model

The one-to-many relationship between `User` and `Review` has been discussed above. We will now discuss the relationship between `Review` and `Tour`. In this application, it is assumed that tourists are the reviewers and tours are the object to be reviewed. This relationship is one-to-many, a tour can have many reviews but one review can only belong to one tour. `tour_id` in `Review` model is the foreign key, referencing the `id` of the `Tour` model and it is not nullable, because a review must belong to a tour. 

In `review.py`:

```
tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
```

The association is established using the below code:

In `tour.py`, there is `cascade='all,delete` constraint of `reviews` in `tour.py` because a review must associated to a tour, it means that once a tour is deleted, all associated reviews will also be deleted.

```
reviews = db.relationship('Review', back_populates='tour', cascade='all, delete')
```

In `review.py`:

```
tour = db.relationship('Tour', back_populates='reviews')
```

`ReviewSchema` is nested in `TourSchema` for when a tour is returned in the response, the associated reviews are stored in a list that nested in the tour object. That is because when a tour is retrieved, it is reasonable to show all of reviews about that tour. `TourSchema` is also nested in `ReviewSchema` but not in a list because one review should only belong to one tour. 

Nesting schemas are defined to represent this relationship as below:

In `tour.py` (under `TourSchema`), `tour` is excluded to prevent circular references.

```
reviews = fields.List(fields.Nested('ReviewSchema', exclude=['tour']))
```

In `review.py` (under `ReviewSchema`), we only need two attributes of tours to show up in the nested tour in the review object: `tour_name` and `user`. Here, `user` is the tour guide who owns the tour that being reviewed.

```
tour = fields.Nested('TourSchema', only=['tour_name', 'user'])
```

<br>

# Database relations

There are five entities/tables involved in this application, namely `roles`, `users`, `tours`, `tour_bookings` and `reviews`.

### `roles` 

This entity has 2 attributes `id` and `name`. The datatype and constraints are listed as below:
- `id`: serial, not null, primary key
- `name`: string, not null

Relationships with other entities:

- `roles` and `users`: one-to-many relationship. One role can have zero to many users and one user can only have one and only one role. When a role is deleted, all the associated users will also be deleted.

### `users` 

This entity has 16 attributes. The datatype and constraints are listed as below:

- `id`: serial, not null, primary key

- `role_id`: integer, not null, foreign key (referencing `id` from the entity `roles` on `DELETE CASCADE`). 

- `username`: string, not null, unique

- `password`: string, not null

- `email`: string, not null, unique

- `date_created`: date, default is set as current date

- `f_name`: string

- `l_name`: string

- `dob`: date

- `gender`: string, must be one of the following values: male, female or others

- `spoken_language`: string

- `description`: text

- `phone`: string, unique

- `identity_doc_type`: string, must be one of the following values: passport, driver license or identity card

- `identity_doc_ID`: string, unique

- `is_active`: boolean

Relationships with other entities:

- `users` and `roles`: one-to-many relationship (as discussed above)

- `users` and `tours`: one-to-many relationship. One user (tour guide) can have zero or many tours but one tour can only belong to one and only one user. Once an user is deleted, all associated tours will also be deleted.

- `users` and `tour_bookings`: one-to-many relationship. One user (tourist) can have zero or many bookings but one booking can only belong to one and only one user. 

- `users` and `reviews`: one-to-many relationship. One user (tourist) can have zero or many reviews but one review can only belong to one and only one user. Once a user is deleted, all associated reviews will also be deleted. 

### `tours` 

This entity has 11 attributes. The datatype and constraints are listed as below:

- `id`: serial, not null, primary key

- `user_id`: integer, not null, foreign key (referencing `id` from the entity `users` on `DELETE CASCADE`). 

- `country`: string, not null

- `tour_name`: string, not null

- `description`: string, not null

- `from_date`: date, not null

- `to_date`: date, not null

- `tourist_capacity`: string

- `is_private`: boolean

- `is_available`: boolean

- `price`: float

Relationships with other entities:

- `tours` and `users`: one-to-many relationship (as discussed above). The relationship can also be many-to-many, many tours are created by many users. In this case, the joint table is `tour_bookings` or `reviews`.

- `tours` and `tour_bookings`: one-to-many relationship. One tour can have zero to many bookings (if a tour is a public tour it can have many bookings). However, it is assumed that a tour cannot be deleted if there is still an existing booking that links to the tour. 

- `tours` and `reviews`: one-to-many relationship. One tour can have zero to many reviews but a review must only belong to one and only one tour. Once a tour is deleted, all associated reviews will also be deleted. 

### `tour_bookings`

This entity has 6 attributes. The datatype and constraints are listed as below:

- `id`: serial, not null, primary key

- `user_id`: integer, not null, foreign key (referencing `id` from the entity `users`).

- `tour_id`: integer, not null, foreign key (referencing `id` from the entity `tours`).

- `tourist_number`: integer, not null

- `preferred_language`: integer, not null

- `extra_request`: text

Relationships with other entities:

- `tour_bookings` and `users`: one-to-many relationship (as discussed above). 

- `tour_bookings` and `tours`: one-to-many relationship (as discussed above). `tour_bookings` is a join table between `users` and `tours` in their many-to-many relationship, therefore, it has two foreign keys `user_id` and `tour_id`. However, it is assumed that a tour booking must be cancelled/deleted for a tour or a user who owns the tour to be deleted. Hence, no `DELETE CASCADE` constraint is set on these foreign keys.

### `reviews`

This entity has 6 attributes. The datatype and constraints are listed as below:

- `id`: serial, not null, primary key

- `user_id`: integer, not null, foreign key (referencing `id` from the entity `users` on `DELETE CASCADE`).

- `tour_id`: integer, not null, foreign key (referencing `id` from the entity `tours` on `DELETE CASCADE`).

- `rating`: integer, not null

- `message`: text, not null

- `date_created`: date, default is set as current date

Relationships with other entities:

- `reviews` and `users`: one-to-many relationship (as discussed above). 

- `reviews` and `tours`: one-to-many relationship (as discussed above). `reviews` is also another join table between `users` and `tours` in their many-to-many relationship, therefore, it also has two foreign keys `user_id` and `tour_id`. 

<br>

# Tasks planning and tracking

View the description of the way tasks are allocated and tracked in the project [here](docs/tasks_tracking.md).

Link to project management tool [Trello](https://trello.com/b/CRoqP48W/t2a2-api-webserver).