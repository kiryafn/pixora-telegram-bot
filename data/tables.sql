CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR,
    full_name VARCHAR,
    language_code VARCHAR DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    registered_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE user_preferences (
    
)