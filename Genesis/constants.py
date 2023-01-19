CREATE_TABLES = (
    """
    CREATE TABLE IF NOT EXISTS users(
        user_id BIGINT PRIMARY KEY,
        balance INT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS user_farms(
        user_id BIGINT,
        farm_id SERIAL PRIMARY KEY,
        farm_size INT DEFAULT 9,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE        
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS farms(
        farm_id INT,
        planted_seed_id INT,
        planted_at BIGINT,
        finished_at BIGINT,
        FOREIGN KEY (farm_id) REFERENCES user_farms(farm_id) ON DELETE CASCADE
    )
    """
)

RUN_ONCE = (
    """
    CREATE OR REPLACE FUNCTION insert_user_farms()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO user_farms(user_id, farm_id) VALUES (NEW.user_id, Default);
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE TRIGGER create_user
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION insert_user_farms();
    """
)


JOBS = [
    "Someone paid you %amt% to do their homework!",
    "You took care of arc's turtle and he paid you %amt%!",
    "You sold sea shells on the sea shore for %amt%!",
    "You set up a lemonade stand and made %amt%!",
]
