-- Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
);

-- Groups
CREATE TABLE groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contribution_amount INTEGER NOT NULL,
    cycle_duration TEXT
);

-- Group Membership
CREATE TABLE group_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Contributions
CREATE TABLE contributions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    group_id INTEGER,
    amount INTEGER,
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Transactions (Withdrawals/Loans)
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    group_id INTEGER,
    amount INTEGER,
    type TEXT, -- 'loan' or 'withdrawal'
    date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);
