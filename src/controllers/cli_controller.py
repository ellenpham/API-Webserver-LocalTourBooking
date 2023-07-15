from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.role import UserRole
from models.tour import Tour
from models.tour_booking import TourBooking
from models.review import Review
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print('Table created')

@db_commands.cli.command('drop')
def drop_all():
    db.drop_all()
    print('Table dropped')

@db_commands.cli.command('seed')
def seed_db():
    roles = [
        UserRole(
            name = 'Admin'
        ),
        UserRole(
            name = 'Tourist'
        ),
        UserRole(
            name = 'Tour Guide'
        ),
    ]

    db.session.add_all(roles)

    users = [
        User(
            username='AdminUser',
            email='admin@email.com',
            password=bcrypt.generate_password_hash('Admin123!').decode('utf-8'),
            role=roles[0],
            date_created=date.today(),
        ),
        User(
            username='daniel.neal',
            email='daniel_n@email.com',
            password=bcrypt.generate_password_hash('Daniel123!').decode('utf-8'),
            role=roles[1],
            date_created=date.today(),
        ),
        User(
            username='evelyn.zamora',
            email='evelyn_z@email.com',
            password=bcrypt.generate_password_hash('Evelyn123!').decode('utf-8'),
            role_id=2,
            role=roles[1],
            date_created=date.today(),
        ),
        User(
            username='jiro.hayashi',
            email='jiro_h@email.com',
            password=bcrypt.generate_password_hash('Jiro123!').decode('utf-8'),
            role=roles[2],
            date_created=date.today(),
        ),
        User(
            username='leslie.wu',
            email='leslie_w@email.com',
            password=bcrypt.generate_password_hash('Leslie123!').decode('utf-8'),
            role=roles[2],
            date_created=date.today(),
        ),
    ]

    db.session.add_all(users)

    tours = [
        Tour(
            country = 'Japan',
            tour_name = '7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto',
            description = 'Tokyo, Osaka, Kyoto', 
            from_date = '01-05-2024',
            to_date = '07-05-2024',
            tourist_capacity = 'Up to 5 people',
            is_private = True, 
            price = 600.00,
            user=users[3]
        ),
        Tour(
            country = 'China',
            tour_name = '10-day historical tour: Beijing-Nanjing-Hangzhou',
            description = 'Beijing, Nanjing, Hangzhou', 
            from_date = '01-08-2024',
            to_date = '10-08-2024',
            tourist_capacity = 'Up to 8 people',
            is_private = False, 
            price = 1800.00,
            user=users[4]
        ),
    ]

    db.session.add_all(tours)

    # The below tour bookings and reviews data are seeded for testing purpose
    # not being seeded when documenting API endpoints to keep a concise documentation
    tour_bookings = [
        TourBooking(
            tourist_number= 3,
            preferred_language = 'English, Japanese', 
            extra_request = 'Lorem ipsum dolor sit amet',
            user=users[1],
            tour=tours[0]
        ),
        TourBooking(
            tourist_number= 8,
            preferred_language = 'English, Mandarin', 
            extra_request = 'Lorem ipsum dolor sit amet',
            user=users[2],
            tour=tours[1]
        ),
    ]

    db.session.add_all(tour_bookings)

    reviews = [
        Review(
            rating = 4,
            message = 'The tour was well organised, Jiro is enthusiatic and switched on!',
            user=users[1],
            tour=tours[0]
        ),
        Review(
            rating = 5,
            message = 'We have had a memorable trip, Leslie is dedicated and attentive!',
            user=users[2],
            tour=tours[1]
        ),
    ]

    db.session.add_all(reviews)

    # commit to db
    db.session.commit()

    print('Table seeded')
                    

