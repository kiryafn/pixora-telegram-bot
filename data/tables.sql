CREATE TABLE users (
    id BIGINT PRIMARY KEY, -- Telegram ID

    username VARCHAR,       -- @username (nullable)
    full_name VARCHAR,      -- Имя и фамилия (nullable)
    language_code VARCHAR DEFAULT 'en', -- Язык интерфейса Telegram

    is_active BOOLEAN DEFAULT TRUE,     -- Пользователь активен или нет

    registered_at TIMESTAMP DEFAULT now(), -- Когда зарегистрировался
    updated_at TIMESTAMP DEFAULT now()     -- Последнее обновление
);