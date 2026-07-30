-- schema.sql
-- ----------------------------------------------------------------
-- Defines the full database structure for SkillSwap.
-- Run automatically once when the app starts (see models/db.py).
-- ----------------------------------------------------------------

-- Drop tables if they exist (only used during fresh setup/reset)
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS skills_offered;
DROP TABLE IF EXISTS skills_wanted;
DROP TABLE IF EXISTS swap_requests;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS ratings;

-- ----------------------------------------------------------------
-- USERS TABLE
-- Stores every registered member's profile information.
-- ----------------------------------------------------------------
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    bio TEXT DEFAULT '',
    location TEXT DEFAULT '',
    profile_image TEXT DEFAULT 'default-avatar.png',
    dark_mode INTEGER DEFAULT 0,             -- 0 = light, 1 = dark (user preference)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------
-- SKILLS OFFERED — skills a user can teach
-- One row per skill per user (many-to-many style relationship)
-- ----------------------------------------------------------------
CREATE TABLE skills_offered (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------
-- SKILLS WANTED — skills a user wants to learn
-- ----------------------------------------------------------------
CREATE TABLE skills_wanted (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    skill_name TEXT NOT NULL,
    category TEXT DEFAULT 'General',
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------
-- SWAP REQUESTS — a request from one user to another to exchange skills
-- status: 'pending', 'accepted', 'rejected'
-- ----------------------------------------------------------------
CREATE TABLE swap_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    offered_skill TEXT NOT NULL,
    wanted_skill TEXT NOT NULL,
    message TEXT DEFAULT '',
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------
-- MESSAGES — simple chat system between two users
-- ----------------------------------------------------------------
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER DEFAULT 0,
    FOREIGN KEY (sender_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------
-- RATINGS — feedback left after a completed swap
-- ----------------------------------------------------------------
CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rated_user_id INTEGER NOT NULL,
    rater_user_id INTEGER NOT NULL,
    stars INTEGER NOT NULL,
    comment TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rated_user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (rater_user_id) REFERENCES users (id) ON DELETE CASCADE
);
