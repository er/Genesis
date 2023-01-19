CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    balance INT
);

CREATE TABLE Skills (
    user_id INT,
    farming INT,
    mining INT,
    fishing INT,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Inventory (
    user_id INT,
    item_id INT,
    quantity INT,
    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Items(item_id) ON DELETE CASCADE
);

CREATE TABLE Items (
    item_id INT PRIMARY KEY,
    description VARCHAR(255),
    price INT
);

CREATE TABLE Upgrades (
    user_id INT,
    upgrade_name VARCHAR(255),
    level INT,
    PRIMARY KEY (user_id, upgrade_name),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);



CREATE TRIGGER create_user
AFTER INSERT ON Users
FOR EACH ROW
BEGIN
    INSERT INTO Skills(user_id) VALUES (NEW.user_id);
    INSERT INTO Upgrades(user_id) VALUES (NEW.user_id);
END;

CREATE TRIGGER delete_user
AFTER DELETE ON Users
FOR EACH ROW
BEGIN
    DELETE FROM Skills WHERE user_id = OLD.user_id;
    DELETE FROM Inventory WHERE user_id = OLD.user_id;
    DELETE FROM Upgrades WHERE user_id = OLD.user_id;
END;
