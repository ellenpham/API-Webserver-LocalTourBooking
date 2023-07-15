# Documentation of API endpoints

## User Routes

### Get all users (full info access) - Admin only

**/users**

- Path example: `localhost:8080/users`
- Method: GET
- Argument: None
- Authentication: Bearer Token upon login
- Authorization: `authorise_as_admin`
- Request body: None
- Response body:

```
[
	{
		"date_created": "2023-07-14",
		"description": null,
		"dob": null,
		"email": "admin@email.com",
		"f_name": null,
		"gender": null,
		"id": 1,
		"identity_doc_ID": null,
		"identity_doc_type": null,
		"is_active": true,
		"l_name": null,
		"phone": null,
		"role": {
			"name": "Admin"
		},
		"role_id": 1,
		"spoken_language": null,
		"tour_bookings": [],
		"tours": [],
		"username": "AdminUser"
	},
	{
		"date_created": "2023-07-14",
		"description": null,
		"dob": null,
		"email": "daniel_n@email.com",
		"f_name": null,
		"gender": null,
		"id": 2,
		"identity_doc_ID": null,
		"identity_doc_type": null,
		"is_active": true,
		"l_name": null,
		"phone": null,
		"role": {
			"name": "Tourist"
		},
		"role_id": 2,
		"spoken_language": null,
		"tour_bookings": [],
		"tours": [],
		"username": "daniel.neal"
	},
	{
		"date_created": "2023-07-14",
		"description": null,
		"dob": null,
		"email": "evelyn_z@email.com",
		"f_name": null,
		"gender": null,
		"id": 3,
		"identity_doc_ID": null,
		"identity_doc_type": null,
		"is_active": true,
		"l_name": null,
		"phone": null,
		"role": {
			"name": "Tourist"
		},
		"role_id": 2,
		"spoken_language": null,
		"tour_bookings": [],
		"tours": [],
		"username": "evelyn.zamora"
	},
	{
		"date_created": "2023-07-14",
		"description": null,
		"dob": null,
		"email": "jiro_h@email.com",
		"f_name": null,
		"gender": null,
		"id": 4,
		"identity_doc_ID": null,
		"identity_doc_type": null,
		"is_active": true,
		"l_name": null,
		"phone": null,
		"role": {
			"name": "Tour Guide"
		},
		"role_id": 3,
		"spoken_language": null,
		"tour_bookings": [],
		"tours": [
			{
				"country": "Japan",
				"description": "Tokyo, Osaka, Kyoto",
				"from_date": "05-01-2024",
				"id": 1,
				"is_available": true,
				"is_private": true,
				"price": 600.0,
				"reviews": [],
				"to_date": "05-07-2024",
				"tour_bookings": [],
				"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
				"tourist_capacity": "Up to 5 people"
			}
		],
		"username": "jiro.hayashi"
	},
	{
		"date_created": "2023-07-14",
		"description": null,
		"dob": null,
		"email": "leslie_w@email.com",
		"f_name": null,
		"gender": null,
		"id": 5,
		"identity_doc_ID": null,
		"identity_doc_type": null,
		"is_active": true,
		"l_name": null,
		"phone": null,
		"role": {
			"name": "Tour Guide"
		},
		"role_id": 3,
		"spoken_language": null,
		"tour_bookings": [],
		"tours": [
			{
				"country": "China",
				"description": "Beijing, Nanjing, Hangzhou",
				"from_date": "08-01-2024",
				"id": 2,
				"is_available": true,
				"is_private": false,
				"price": 1800.0,
				"reviews": [],
				"to_date": "08-10-2024",
				"tour_bookings": [],
				"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
				"tourist_capacity": "Up to 8 people"
			}
		],
		"username": "leslie.wu"
	}
]
```

### Get one user (full info access) - Admin only

**/users/<user_id>**

- Path example: `localhost:8080/users/2`
- Method: GET
- Argument: `user_id` as Integer 
- Authentication: Bearer Token upon login
- Authorization: `authorise_as_admin`
- Request body: None
- Response body:

```
{
	"date_created": "2023-07-14",
	"description": null,
	"dob": null,
	"email": "daniel_n@email.com",
	"f_name": null,
	"gender": null,
	"id": 2,
	"identity_doc_ID": null,
	"identity_doc_type": null,
	"is_active": true,
	"l_name": null,
	"phone": null,
	"role": {
		"name": "Tourist"
	},
	"role_id": 2,
	"spoken_language": null,
	"tour_bookings": [],
	"tours": [],
	"username": "daniel.neal"
}
```
### Delete one user - Admin only

**/users/<user_id>**

- Path example: `localhost:8080/users/6`
- Method: DELETE
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `authorise_as_admin`

**Note**: Only can delete an user without a current booking. If the user is currently having a booking, the booking needs to be deleted first before the user being deleted.

- Request body: None
- Response body:

```
{
	"error": "The user can not be deleted due to an existing related booking. Please cancel the related booking before deleting the user."
}
```
Once the related tour booking is deleted, the result is returned as below:

```
{
	"message": "User milena.jones has been deleted successfully."
}
```

### Get all tours with tour bookings info - Admin only

**/users/tours**

- Path example: `localhost:8080/users/tours`
- Method: GET
- Argument: None
- Authentication: Bearer Token upon login
- Authorization: `authorise_as_admin`
- Request body: None
- Response body:

```
[
	{
		"country": "Japan",
		"description": "Tokyo, Osaka, Kyoto",
		"from_date": "05-01-2024",
		"id": 1,
		"is_available": true,
		"is_private": true,
		"price": 600.0,
		"reviews": [],
		"to_date": "05-07-2024",
		"tour_bookings": [
			{
				"extra_request": "Lorem ipsum",
				"id": 2,
				"preferred_language": "English, Japanese",
				"tourist_number": 4,
				"user": {
					"email": "daniel_n@email.com",
					"role": {
						"name": "Tourist"
					},
					"username": "daniel.neal"
				}
			}
		],
		"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
		"tourist_capacity": "Up to 5 people",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	{
		"country": "China",
		"description": "Beijing, Nanjing, Hangzhou",
		"from_date": "08-01-2024",
		"id": 2,
		"is_available": true,
		"is_private": false,
		"price": 1800.0,
		"reviews": [],
		"to_date": "08-10-2024",
		"tour_bookings": [
			{
				"extra_request": "Lorem ipsum dolor sit amet",
				"id": 5,
				"preferred_language": "English",
				"tourist_number": 2,
				"user": {
					"email": "evelyn_z@email.com",
					"role": {
						"name": "Tourist"
					},
					"username": "evelyn.zamora"
				}
			}
		],
		"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
		"tourist_capacity": "Up to 8 people",
		"user": {
			"email": "leslie_w@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "leslie.wu"
		}
	},
	{
		"country": "Japan",
		"description": "Yokohama",
		"from_date": "01-10-2024",
		"id": 5,
		"is_available": true,
		"is_private": true,
		"price": 250.0,
		"reviews": [],
		"to_date": "01-10-2024",
		"tour_bookings": [
			{
				"extra_request": "Lorem ipsum dolor sit amet",
				"id": 4,
				"preferred_language": "Japanese",
				"tourist_number": 2,
				"user": {
					"email": "evelyn_z@email.com",
					"role": {
						"name": "Tourist"
					},
					"username": "evelyn.zamora"
				}
			}
		],
		"tour_name": "1-day walking tour in Yokohama",
		"tourist_capacity": "2",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	}
]
```

<br>

## Authentication routes

### User register 

**/auth/register**

- Path example: `localhost:8080/auth/register`
- Method: POST
- Argument: None
- Authentication: None
- Authorization: None
- Request body: required fields `username`, `email`, `password`, `role_id`
- Data validation:
    - `username` has to have a least 5 character and only special character dot `.`, underscore `_` and dash `-` are allowed.
    - `email` must be a valid email.
    - `password` must have at least 5 characters and must contain at least one uppercase, one lowercase and on special character.
    - `role_id` must be one of the following integer value: `1` for Admin, `2` for Tourist and `3` for Tour Guide.
```
{
	"username": "milena.jones",
	"email" : "milena_j@email.com",
	"password" : "Milena123!",
	"role_id" : 2
}
```
- Response body:

```
{
	"date_created": "2023-07-14",
	"description": null,
	"dob": null,
	"email": "milena_j@email.com",
	"f_name": null,
	"gender": null,
	"id": 6,
	"identity_doc_ID": null,
	"identity_doc_type": null,
	"is_active": true,
	"l_name": null,
	"phone": null,
	"role": {
		"name": "Tourist"
	},
	"role_id": 2,
	"spoken_language": null,
	"tour_bookings": [],
	"username": "milena.jones"
}
```

### User login 

**/auth/login**

- Path example: `localhost:8080/auth/login`
- Method: POST
- Argument: None
- Authentication: None
- Authorization: None
- Request body:
```
{
	"username": "daniel.neal",
	"password": "Daniel123!"
}
```
- Response body:
```
{
	"role_id": 2,
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4OTMwMDg5OCwianRpIjoiMmQ3ZTMxOTEtOTQyYy00MWZhLTg3NzYtZTJmOGY3NDEyNTdjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjIiLCJuYmYiOjE2ODkzMDA4OTgsImV4cCI6MTY4OTM4NzI5OH0.qpiZY9yGukJPksNucEN0Wzxa7O01n4qfELLfxJQ5hVo",
	"username": "daniel.neal"
}
```

<br>

## Tourist Routes

### Get a tourist account (full info access) - Account owner only

**/tourists/<user_id>**

- Path example: `localhost:8080/tourists/2`
- Method: GET
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response body:
```
{
	"date_created": "2023-07-14",
	"dob": null,
	"email": "daniel_n@email.com",
	"f_name": null,
	"gender": null,
	"id": 2,
	"identity_doc_ID": null,
	"identity_doc_type": null,
	"is_active": true,
	"l_name": null,
	"phone": null,
	"role": {
		"name": "Tourist"
	},
	"role_id": 2,
	"spoken_language": null,
	"tour_bookings": [],
	"username": "daniel.neal"
}
```
<br>

### Update a tourist account - Account owner only

**/tourists/<user_id>**

- Path example: `localhost:8080/tourists/2`
- Method: PUT, PATCH
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Data validation:
    - `f_name` and `l_name` must have at least 2 characters and must only contain letters and space
    - `dob` must be in date format of `dd-mm-yy`
    - `spoken_language` must have at least 2 characters, multiple languages are separated by commas
    - `gender` must be one of `male`, `female` or `others`
    - `phone` must be unique and contain numbers only
    - `identity_doc_type` must be one of `passport`, `driver license` or `identity card`
    - `identity_doc_ID` must be unique and contain numbers and letters only
    - `is_active` must be a valid boolean value (`true`, `false`, `1`, `0`)
- Request body:

```
{
	"f_name" : "Daniel",
	"l_name" : "Neal",
	"dob" : "23-08-1992",
	"gender" : "male",
	"spoken_language" : "English",
	"phone" : "0123456789",
	"identity_doc_type" : "passport",
	"identity_doc_ID" : "A12345678",
	"is_active" : true
}
```
- Response body:

```
{
	"date_created": "2023-07-14",
	"dob": "23-08-1992",
	"email": "daniel_n@email.com",
	"f_name": "Daniel",
	"gender": "male",
	"id": 2,
	"identity_doc_ID": "A12345678",
	"identity_doc_type": "passport",
	"is_active": true,
	"l_name": "Neal",
	"phone": "0123456789",
	"role": {
		"name": "Tourist"
	},
	"role_id": 2,
	"spoken_language": "English",
	"tour_bookings": [],
	"username": "daniel.neal"
}
```

### Get a tourist's all bookings - Tour booking owner only 

**/tourists/<user_id>/tourbookings**

- Path example: `localhost:8080/tourists/3/tourbookings`
- Method: GET
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response body:
```
[
	{
		"extra_request": "Lorem ipsum dolor sit amet",
		"id": 4,
		"preferred_language": "Japanese",
		"tour": {
			"tour_name": "1-day walking tour in Yokohama",
			"user": {
				"email": "jiro_h@email.com",
				"role": {
					"name": "Tour Guide"
				},
				"username": "jiro.hayashi"
			}
		},
		"tourist_number": 2,
		"user": {
			"email": "evelyn_z@email.com",
			"role": {
				"name": "Tourist"
			},
			"username": "evelyn.zamora"
		}
	},
	{
		"extra_request": "Lorem ipsum dolor sit amet",
		"id": 5,
		"preferred_language": "English",
		"tour": {
			"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
			"user": {
				"email": "leslie_w@email.com",
				"role": {
					"name": "Tour Guide"
				},
				"username": "leslie.wu"
			}
		},
		"tourist_number": 2,
		"user": {
			"email": "evelyn_z@email.com",
			"role": {
				"name": "Tourist"
			},
			"username": "evelyn.zamora"
		}
	}
]
```
<br>

## Tour Guide Routes 

### Get all tour guides (limited info access)

**/tourguides**

- Path example: `localhost:8080/tourguides`
- Method: GET
- Argument: None
- Authentication: Bearer Token upon login
- Authorization: None

**Note**: can only view active tour guide accounts

- Response body:
```
[
	{
		"date_created": "2023-07-14",
		"description": null,
		"dob": null,
		"email": "jiro_h@email.com",
		"f_name": null,
		"gender": null,
		"is_active": true,
		"l_name": null,
		"phone": null,
		"role": {
			"name": "Tour Guide"
		},
		"spoken_language": null,
		"tours": [
			{
				"country": "Japan",
				"description": "Tokyo, Osaka, Kyoto",
				"from_date": "05-01-2024",
				"id": 1,
				"is_available": true,
				"is_private": true,
				"price": 600.0,
				"reviews": [],
				"to_date": "05-07-2024",
				"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
				"tourist_capacity": "Up to 5 people"
			}
		],
		"username": "jiro.hayashi"
	},
	{
		"date_created": "2023-07-14",
		"description": null,
		"dob": null,
		"email": "leslie_w@email.com",
		"f_name": null,
		"gender": null,
		"is_active": true,
		"l_name": null,
		"phone": null,
		"role": {
			"name": "Tour Guide"
		},
		"spoken_language": null,
		"tours": [
			{
				"country": "China",
				"description": "Beijing, Nanjing, Hangzhou",
				"from_date": "08-01-2024",
				"id": 2,
				"is_available": true,
				"is_private": false,
				"price": 1800.0,
				"reviews": [],
				"to_date": "08-10-2024",
				"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
				"tourist_capacity": "Up to 8 people"
			}
		],
		"username": "leslie.wu"
	}
]
```

### Get one tour guide (limited info access) - DONE

**/tourguides/<user_id>**

- Path example: `localhost:8080/tourguides/4`
- Method: GET
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: None

**Note**: can only view active tour guide account

- Request body: None
- Response body:
```
{
	"date_created": "2023-07-14",
	"description": null,
	"dob": null,
	"email": "jiro_h@email.com",
	"f_name": null,
	"gender": null,
	"is_active": true,
	"l_name": null,
	"phone": null,
	"role": {
		"name": "Tour Guide"
	},
	"spoken_language": null,
	"tours": [
		{
			"country": "Japan",
			"description": "Tokyo, Osaka, Kyoto",
			"from_date": "05-01-2024",
			"id": 1,
			"is_available": true,
			"is_private": true,
			"price": 600.0,
			"reviews": [],
			"to_date": "05-07-2024",
			"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
			"tourist_capacity": "Up to 5 people"
		}
	],
	"username": "jiro.hayashi"
}
```

### Get one tour guide (full info access) - Account owner only - DONE

**/tourguides/<user_id>**

- Path example: `localhost:8080/tourguides/5`
- Method: GET
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response body:
```
{
	"date_created": "2023-07-14",
	"description": null,
	"dob": null,
	"email": "leslie_w@email.com",
	"f_name": null,
	"gender": null,
	"id": 5,
	"identity_doc_ID": null,
	"identity_doc_type": null,
	"is_active": true,
	"l_name": null,
	"phone": null,
	"role": {
		"name": "Tour Guide"
	},
	"role_id": 3,
	"spoken_language": null,
	"tours": [
		{
			"country": "China",
			"description": "Beijing, Nanjing, Hangzhou",
			"from_date": "08-01-2024",
			"id": 2,
			"is_available": true,
			"is_private": false,
			"price": 1800.0,
			"reviews": [],
			"to_date": "08-10-2024",
			"tour_bookings": [],
			"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
			"tourist_capacity": "Up to 8 people"
		}
	],
	"username": "leslie.wu"
}
```

### Update a tour guide account - Account owner only

**/tourguides/<user_id>**

- Path example: `localhost:8080/tourguides/5`
- Method: PUT, PATCH
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body:

```
{
	"date_created": "2023-07-14",
	"description": "Lorem ipsum",
	"dob": "15-02-1995",
	"email": "leslie_w@email.com",
	"f_name": "Leslie",
	"gender": "male",
	"id": 5,
	"identity_doc_ID": "12345678",
	"identity_doc_type": "driver license",
	"is_active": true,
	"l_name": "Wu",
	"phone": "01234567890",
	"role": {
		"name": "Tour Guide"
	},
	"role_id": 3,
	"spoken_language": "english, mandarin",
	"tours": [
		{
			"country": "China",
			"description": "Beijing, Nanjing, Hangzhou",
			"from_date": "08-01-2024",
			"id": 2,
			"is_available": true,
			"is_private": false,
			"price": 1800.0,
			"reviews": [],
			"to_date": "08-10-2024",
			"tour_bookings": [],
			"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
			"tourist_capacity": "Up to 8 people"
		}
	],
	"username": "leslie.wu"
}
```

### Get a tourist account (limited info access) - Tour guide used only and only can retrieve a tourist who has booked their tour

**/tourguides/<tourguide_id>/<tourist_id>**

- Path example: `localhost:8080/tourguides/4/2`
- Method: GET
- Argument: `tourguide_id` and `tourist_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identuty`
- Request body: None
- Response body:
```
{
	"date_created": "2023-07-14",
	"description": null,
	"dob": "1992-08-23",
	"email": "daniel_n@email.com",
	"f_name": "Daniel",
	"gender": "male",
	"is_active": true,
	"l_name": "Neal",
	"phone": "0123456789",
	"role": {
		"name": "Tourist"
	},
	"spoken_language": "English",
	"username": "daniel.neal"
}
```
If the tour guide who requests is not authorized, the result is returned as below:

```
{
	"error": "Unauthorized to view tourist account with id 2."
}
```
### Get a tour guide's all tours with full booking info - Tour owner only

**/tourguides/<user_id>/tours**

- Path example: `localhost:8080/tourguides/4/tours`
- Method: GET
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response body:

```
[
	{
		"country": "Japan",
		"description": "Tokyo, Osaka, Kyoto",
		"from_date": "05-01-2024",
		"id": 1,
		"is_available": true,
		"is_private": true,
		"price": 600.0,
		"reviews": [],
		"to_date": "05-07-2024",
		"tour_bookings": [
			{
				"extra_request": "Lorem ipsum",
				"id": 2,
				"preferred_language": "English, Japanese",
				"tourist_number": 4,
				"user": {
					"email": "daniel_n@email.com",
					"role": {
						"name": "Tourist"
					},
					"username": "daniel.neal"
				}
			}
		],
		"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
		"tourist_capacity": "Up to 5 people",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	{
		"country": "Japan",
		"description": "Yokohama",
		"from_date": "01-10-2024",
		"id": 5,
		"is_available": true,
		"is_private": true,
		"price": 250.0,
		"reviews": [],
		"to_date": "01-10-2024",
		"tour_bookings": [
			{
				"extra_request": "Lorem ipsum dolor sit amet",
				"id": 4,
				"preferred_language": "Japanese",
				"tourist_number": 2,
				"user": {
					"email": "evelyn_z@email.com",
					"role": {
						"name": "Tourist"
					},
					"username": "evelyn.zamora"
				}
			}
		],
		"tour_name": "1-day walking tour in Yokohama",
		"tourist_capacity": "2",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	}
]
```


### Get a tour guide's all bookings - Related tour guide only

**/tourguides/<user_id>/tourbookings**

- Path example: `localhost:8080/tourguides/2/tourbookings`
- Method: GET
- Argument: `user_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response body:

```
[
	{
		"extra_request": "Lorem ipsum",
		"id": 2,
		"preferred_language": "English, Japanese",
		"tour": {
			"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
			"user": {
				"email": "jiro_h@email.com",
				"role": {
					"name": "Tour Guide"
				},
				"username": "jiro.hayashi"
			}
		},
		"tourist_number": 4,
		"user": {
			"email": "daniel_n@email.com",
			"role": {
				"name": "Tourist"
			},
			"username": "daniel.neal"
		}
	},
	{
		"extra_request": "Lorem ipsum dolor sit amet",
		"id": 4,
		"preferred_language": "Japanese",
		"tour": {
			"tour_name": "1-day walking tour in Yokohama",
			"user": {
				"email": "jiro_h@email.com",
				"role": {
					"name": "Tour Guide"
				},
				"username": "jiro.hayashi"
			}
		},
		"tourist_number": 2,
		"user": {
			"email": "evelyn_z@email.com",
			"role": {
				"name": "Tourist"
			},
			"username": "evelyn.zamora"
		}
	}
]
```

<br>

## Tour Routes

### Create a tour - Tour guide only

**/tours/**

- Path example: `localhost:8080/tours/`
- Method: POST
- Argument: None
- Authentication: Bearer Token upon login
- Authorization: `authorise_as_tourguide`
- Data validation:
    - `country` is required, must have at least 2 characters and only contain letters
    - `tour_name` is required and must be between 10-200 characters
    - `description` is required and must be longer than 5 characters
    - `from_date` and `to_date` are required, must be in valid date format of `dd-mm-yy`
    - `tourist_capacity` must have at least 1 character
    - `is_private` and `is_available` must be a valid boolean value
    - `price` is required and must be a valid decimal number
- Request body:
```
{
	"country" : "Japan",
	"tour_name" : "1-day walking tour in Yokohama",
	"description" : "Lorem ipsum",
	"from_date" : "01-10-2024",
	"to_date" : "01-10-2024",
	"tourist_capacity" : "2",
	"is_private" : true,
	"price" : "250.00"
}
```
- Response body:

```
{
	"country": "Japan",
	"description": "Lorem ipsum",
	"from_date": "01-10-2024",
	"id": 4,
	"is_available": true,
	"is_private": true,
	"price": 250.0,
	"reviews": [],
	"to_date": "01-10-2024",
	"tour_bookings": [],
	"tour_name": "1-day walking tour in Yokohama",
	"tourist_capacity": "2",
	"user": {
		"email": "jiro_h@email.com",
		"role": {
			"name": "Tour Guide"
		},
		"username": "jiro.hayashi"
	}
}
```

### Get one tour without private bookings info - All visitors and users

**/tours/<id>**

- Path example: `localhost:8080/tours/1`
- Method: GET
- Argument: `id` as Integer
- Authentication: None
- Authorization: None
- Request body: None
- Response body:
```
{
	"country": "China",
	"description": "Beijing, Nanjing, Hangzhou",
	"from_date": "08-01-2024",
	"id": 2,
	"is_available": true,
	"is_private": false,
	"price": 1800.0,
	"reviews": [
		{
			"date_created": "2023-07-14",
			"id": 1,
			"message": "The tour was great! Leslie is dedicated and attentive. Highly recommended.",
			"rating": 5,
			"user": {
				"role": {
					"name": "Tourist"
				},
				"username": "evelyn.zamora"
			}
		}
	],
	"to_date": "08-10-2024",
	"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
	"tourist_capacity": "Up to 8 people",
	"user": {
		"email": "leslie_w@email.com",
		"role": {
			"name": "Tour Guide"
		},
		"username": "leslie.wu"
	}
}
```

### Get all tours without private bookings info - All visitors and users

**/tours**

- Path example: `localhost:8080/tours`
- Method: GET
- Argument: None
- Authentication: None
- Authorization: None
- Request body: None
- Response body:
```
[
	{
		"country": "Japan",
		"description": "Tokyo, Osaka, Kyoto",
		"from_date": "05-01-2024",
		"id": 1,
		"is_available": true,
		"is_private": true,
		"price": 600.0,
		"reviews": [],
		"to_date": "05-07-2024",
		"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
		"tourist_capacity": "Up to 5 people",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	{
		"country": "China",
		"description": "Beijing, Nanjing, Hangzhou",
		"from_date": "08-01-2024",
		"id": 2,
		"is_available": true,
		"is_private": false,
		"price": 1800.0,
		"reviews": [
			{
				"date_created": "2023-07-14",
				"id": 1,
				"message": "The tour was great! Leslie is dedicated and attentive. Highly recommended.",
				"rating": 5,
				"user": {
					"role": {
						"name": "Tourist"
					},
					"username": "evelyn.zamora"
				}
			}
		],
		"to_date": "08-10-2024",
		"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
		"tourist_capacity": "Up to 8 people",
		"user": {
			"email": "leslie_w@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "leslie.wu"
		}
	},
	{
		"country": "Japan",
		"description": "Yokohama",
		"from_date": "01-10-2024",
		"id": 5,
		"is_available": true,
		"is_private": true,
		"price": 250.0,
		"reviews": [],
		"to_date": "01-10-2024",
		"tour_name": "1-day walking tour in Yokohama",
		"tourist_capacity": "2",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	{
		"country": "Taiwan",
		"description": "Lorem ipsum",
		"from_date": "01-11-2024",
		"id": 6,
		"is_available": false,
		"is_private": false,
		"price": 500.0,
		"reviews": [],
		"to_date": "05-11-2024",
		"tour_name": "Discover Taipei in a 5-day tour",
		"tourist_capacity": "6",
		"user": {
			"email": "leslie_w@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "leslie.wu"
		}
	}
]
```
### Search a tour by country - All visitors and users

**/tours/search**

- Path example: `localhost:8080/tours/search?country=Japan`
- Method: GET
- Argument: `search?country=`
- Authentication: None
- Authorization: None
- Request body: None
- Response body:

```
[
	{
		"country": "Japan",
		"description": "Tokyo, Osaka, Kyoto",
		"from_date": "05-01-2024",
		"id": 1,
		"is_available": true,
		"is_private": true,
		"price": 600.0,
		"reviews": [],
		"to_date": "05-07-2024",
		"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
		"tourist_capacity": "Up to 5 people",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	{
		"country": "Japan",
		"description": "Yokohama",
		"from_date": "01-10-2024",
		"id": 5,
		"is_available": true,
		"is_private": true,
		"price": 250.0,
		"reviews": [],
		"to_date": "01-10-2024",
		"tour_name": "1-day walking tour in Yokohama",
		"tourist_capacity": "2",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	}
]
```

### Update a tour - Tour owner only 

**/tours/<id>**

- Path example: `localhost:8080/tours/3`
- Method: PUT, PATCH
- Argument: `id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body:
```
{
	"country" : "Japan",
	"tour_name" : "1-day walking tour in Yokohama",
	"description" : "Lorem ipsum lorem ipsum",
	"from_date" : "01-10-2024",
	"to_date" : "01-10-2024",
	"tourist_capacity" : "2",
	"is_private" : true,
	"is_available" : false,
	"price" : "250.00"
}
```
- Response body:
```
{
	"country": "Japan",
	"description": "Lorem ipsum lorem ipsum",
	"from_date": "01-10-2024",
	"id": 3,
	"is_available": false,
	"is_private": true,
	"price": 250.0,
	"reviews": [],
	"to_date": "01-10-2024",
	"tour_name": "1-day walking tour in Yokohama",
	"tourist_capacity": "2",
	"user": {
		"email": "jiro_h@email.com",
		"role": {
			"name": "Tour Guide"
		},
		"username": "jiro.hayashi"
	}
}
```

### Delete a tour - Tour owner only

**/tours/<id>**

- Path example: `localhost:8080/tours/3`
- Method: DELETE
- Argument: `id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`

**Note**: can not delete if tour is booked with an existing booking ID. Only can delete if related booking has been deleted.

- Request body: None
- Response body:
```
{
	"error": "The tour can not be deleted as it has been booked. Please cancel the related booking before deleting the tour."
}
```
Once the related booking is deleted, the result is returned as below:

```
{
	"message": "Tour 3 deleted successfully."
}
```
<br>

## Tour Booking Routes

### Create a tour booking - Tourist only

**/tours/<tour_id>/tourbookings/**

- Path example: `localhost:8080/tours/1/tourbookings/`
- Method: POST
- Argument: `tour_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `authorise_as_tourist`

**Note**: can only book an available tour 

- Data validation:
    - `tourist_number` must be a valid integer
    - `preferred_language` must be longer than 2 characters, multiple languages are separated by commas
    - `extra_request` must be longer than 5 characters
- Request body:
```
{
	"tourist_number" : "4",
	"preferred_language" : "English", 
	"extra_request" : "Lorem ipsum"
}
```
- Response body:
```
{
	"extra_request": "Lorem ipsum",
	"id": 1,
	"preferred_language": "English",
	"tour": {
		"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	"tourist_number": 4,
	"user": {
		"email": "daniel_n@email.com",
		"role": {
			"name": "Tourist"
		},
		"username": "daniel.neal"
	}
}
```
If a tour is unavailable, when creating a booking using this path `localhost:8080/tours/6/tourbookings`, the below result is returned:

```
{
	"country": "Taiwan",
	"description": "Lorem ipsum",
	"from_date": "01-11-2024",
	"id": 6,
	"is_available": false,
	"is_private": false,
	"price": 500.0,
	"reviews": [],
	"to_date": "05-11-2024",
	"tour_name": "Discover Taipei in a 5-day tour",
	"tourist_capacity": "6",
	"user": {
		"email": "leslie_w@email.com",
		"role": {
			"name": "Tour Guide"
		},
		"username": "leslie.wu"
	}
}
```
```
{
	"error": "Tour not found with id 6."
}
```

### Get a tour booking - Booking owner and related tour guide only

**tours/<tour_id>/tourbookings/<booking_id>**

- Path example: `localhost:8080/tours/1/tourbookings/1`
- Method: GET
- Argument: `tour_id` and `booking_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response body:

```
{
	"extra_request": "Lorem ipsum",
	"id": 1,
	"preferred_language": "English",
	"tour": {
		"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	"tourist_number": 4,
	"user": {
		"email": "daniel_n@email.com",
		"role": {
			"name": "Tourist"
		},
		"username": "daniel.neal"
	}
}
```

### Update a tour booking - Booking owner only 

**tours/<tour_id>/tourbookings/<booking_id>**

- Path example: `localhost:8080/tours/2/tourbookings/1`
- Method: PUT, PATCH
- Argument: `tour_id` and `booking_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body:
```
{
	"tourist_number" : "5",
	"preferred_language" : "English, Japanese", 
	"extra_request" : "Lorem ipsum lorem ipsum"
}
```
- Response result:
```
{
	"extra_request": "Lorem ipsum lorem ipsum",
	"id": 1,
	"preferred_language": "English, Japanese",
	"tour": {
		"tour_name": "7-day cultural-cuisine tour: Tokyo-Osaka-Kyoto",
		"user": {
			"email": "jiro_h@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "jiro.hayashi"
		}
	},
	"tourist_number": 5,
	"user": {
		"email": "daniel_n@email.com",
		"role": {
			"name": "Tourist"
		},
		"username": "daniel.neal"
	}
}
```

### Delete a tour booking - Tour booking owner only

**tours/<tour_id>/tourbookings/<booking_id>**

- Path example: `localhost:8080/tours/1/tourbookings/1`
- Method: DELETE
- Argument: `tour_id` and `booking_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response body:
```
{
	"message": "Tour booking 1 deleted successfully."
}
```
<br>

## Review Routes

### Create a review - Tourist used only and only applied for tourist who has booked the tour

**/tours/<tour_id>/reviews/**

- Path example: `localhost:8080/tours/2/reviews/`
- Method: POST
- Argument: `tour_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Data validation:
	- `rating` : must be a valid integer from 1 to 5
	- `message` : must be longer than 5 characters
- Request body:
```
{
	"rating" : 5,
	"message" : "The tour was great!, Leslie is dedicated and attentive!"
}
```
- Response body:
```
{
	"date_created": "2023-07-14",
	"id": 1,
	"message": "The tour was great!, Leslie is dedicated and attentive!",
	"rating": 5,
	"tour": {
		"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
		"user": {
			"email": "leslie_w@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "leslie.wu"
		}
	},
	"user": {
		"role": {
			"name": "Tourist"
		},
		"username": "evelyn.zamora"
	}
}
```
If the user who is currently logged in has never booked the tour, when sending the request, the below result is returned:

```
{
	"error": "Unauthorized to review tour with id 2."
}
```


### Update a review - Review owner only

**tours/<tour_id>/reviews/<review_id>**

- Path example: `localhost:8080/tours/2/reviews/1`
- Method: PUT, PATCH
- Argument: `tour_id` and `review_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body:
```
{
	"rating" : 5,
	"message" : "The tour was great! Leslie is dedicated and attentive. Highly recommended."
}
```
- Response body:
```
{
	"date_created": "2023-07-14",
	"id": 1,
	"message": "The tour was great! Leslie is dedicated and attentive. Highly recommended.",
	"rating": 5,
	"tour": {
		"tour_name": "10-day historical tour: Beijing-Nanjing-Hangzhou",
		"user": {
			"email": "leslie_w@email.com",
			"role": {
				"name": "Tour Guide"
			},
			"username": "leslie.wu"
		}
	},
	"user": {
		"role": {
			"name": "Tourist"
		},
		"username": "evelyn.zamora"
	}
}
```

### Delete a review - Review owner and Admin only

**/reviews/<review_id>**

- Path example: `localhost:8080/tours/2/reviews/1`
- Method: DELETE
- Argument: `tour_id` and `review_id` as Integer
- Authentication: Bearer Token upon login
- Authorization: `get_jwt_identity`
- Request body: None
- Response result:
```
{
	"message": "Review 1 deleted successfully."
}
```
