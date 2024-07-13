RentManagement/
├── app/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py        # Define database setup
│   │   ├── db.py              # Define database session setup
│   │   └── models/            # Database models
│   │       ├── __init__.py
│   │       ├── payment.py     # PaymentModel definition
│   │       ├── room.py        # RoomModel definition
│   │       └── user.py        # UserModel definition
│   ├── internals/
│   │   ├── __init__.py
│   │   ├── crud/              # CRUD operations
│   │   │   ├── __init__.py
│   │   │   ├── payment.py     # Payment CRUD operations
│   │   │   ├── room.py        # Room CRUD operations
│   │   │   └── user.py        # User CRUD operations
│   │   └── payment.py         # Business logic specific to payments
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── payment.py         # Payment router
│   │   ├── room.py            # Room router
│   │   └── user.py            # User router
│   └── schemas/
│       ├── __init__.py
│       ├── CONSTANT.py        # Constants like ROOM_TYPES
│       ├── payment.py         # Payment schemas
│       ├── room.py            # Room schemas
│       └── user.py            # User schemas
├── app.py                      # FastAPI app instantiation
├── main.py                     # Entrypoint for running the application
└── test.db                     # SQLite database file
