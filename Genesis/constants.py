CREATE_TABLES = (
    """
    CREATE TABLE IF NOT EXISTS item_info(
        item_id SERIAL PRIMARY KEY UNIQUE,
        item_name TEXT,
        buy_price INTEGER DEFAULT NULL,
        sell_price INTEGER DEFAULT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY UNIQUE,
        discord_id BIGINT NOT NULL,
        balance INTEGER DEFAULT 0,
        multiplier INT NOT NULL DEFAULT 1,
        daily_claimed_at BIGINT NOT NULL DEFAULT 0,
        weekly_claimed_at BIGINT NOT NULL DEFAULT 0,
        monthly_claimed_at BIGINT NOT NULL DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS user_inventory(
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        count INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(item_id) REFERENCES item_info(item_id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
    )
    """,
)


JOBS = [
    "Someone paid you %amt% to do their homework!",
    "You took care of arc's turtle and he paid you %amt%!",
    "You sold sea shells on the sea shore for %amt%!",
    "You set up a lemonade stand and made %amt%!",
]
