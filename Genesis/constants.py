CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        discord_id BIGINT NOT NULL,
        balance INT NOT NULL DEFAULT 0,
        multiplier INT NOT NULL DEFAULT 1,
        daily_claimed_at BIGINT NOT NULL DEFAULT 0,
        weekly_claimed_at BIGINT NOT NULL DEFAULT 0,
        monthly_claimed_at BIGINT NOT NULL DEFAULT 0
    )
"""

JOBS = [
    "Someone paid you %amt% to do their homework!",
    "You took care of arc's turtle and he paid you %amt%!",
    "You sold sea shells on the sea shore for %amt%!",
    "You set up a lemonade stand and made %amt%!",
]
