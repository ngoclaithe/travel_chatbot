import sqlalchemy
from datetime import datetime
from app.database import metadata

destinations = sqlalchemy.Table(
    "destinations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("province", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("region", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("category", sqlalchemy.String(100)),
    sqlalchemy.Column("rating", sqlalchemy.Numeric(2, 1), default=0),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("best_time_to_visit", sqlalchemy.String(255)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

activities = sqlalchemy.Table(
    "activities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("destination_id", sqlalchemy.Integer),
    sqlalchemy.Column("type", sqlalchemy.String(100)),
    sqlalchemy.Column("price", sqlalchemy.Numeric(10, 2)),
    sqlalchemy.Column("duration", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

hotels = sqlalchemy.Table(
    "hotels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("address", sqlalchemy.Text),
    sqlalchemy.Column("destination_id", sqlalchemy.Integer),
    sqlalchemy.Column("star_rating", sqlalchemy.Integer),
    sqlalchemy.Column("price_range", sqlalchemy.String(50)),
    sqlalchemy.Column("rating", sqlalchemy.Numeric(2, 1), default=0),
    sqlalchemy.Column("amenities", sqlalchemy.ARRAY(sqlalchemy.Text)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

restaurants = sqlalchemy.Table(
    "restaurants",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("address", sqlalchemy.Text),
    sqlalchemy.Column("destination_id", sqlalchemy.Integer),
    sqlalchemy.Column("cuisine_type", sqlalchemy.String(100)),
    sqlalchemy.Column("price_range", sqlalchemy.String(50)),
    sqlalchemy.Column("rating", sqlalchemy.Numeric(2, 1), default=0),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

tours = sqlalchemy.Table(
    "tours",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("destinations", sqlalchemy.Text),
    sqlalchemy.Column("duration_days", sqlalchemy.Integer),
    sqlalchemy.Column("price", sqlalchemy.Numeric(10, 2)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

transportation = sqlalchemy.Table(
    "transportation",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("from_destination_id", sqlalchemy.Integer),
    sqlalchemy.Column("to_destination_id", sqlalchemy.Integer),
    sqlalchemy.Column("type", sqlalchemy.String(50)),
    sqlalchemy.Column("duration", sqlalchemy.String(100)),
    sqlalchemy.Column("price_range", sqlalchemy.String(100)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

weather = sqlalchemy.Table(
    "weather",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("destination_id", sqlalchemy.Integer),
    sqlalchemy.Column("month", sqlalchemy.Integer),
    sqlalchemy.Column("avg_temp", sqlalchemy.Numeric(4, 1)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("is_best_time", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

reviews = sqlalchemy.Table(
    "reviews",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("entity_type", sqlalchemy.String(50)),
    sqlalchemy.Column("entity_id", sqlalchemy.Integer),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
    sqlalchemy.Column("comment", sqlalchemy.Text),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.utcnow),
)

events = sqlalchemy.Table(
    "events",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("sender_id", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("type_name", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("timestamp", sqlalchemy.Float),
    sqlalchemy.Column("intent_name", sqlalchemy.String(255)),
    sqlalchemy.Column("action_name", sqlalchemy.String(255)),
    sqlalchemy.Column("data", sqlalchemy.Text),
)