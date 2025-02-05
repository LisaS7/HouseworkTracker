-- Insert Users
INSERT INTO users (name, email)
VALUES
    ('Lisa', 'lisa@example.com'),
    ('Simon', 'simon@example.com');

-- Insert Tags
INSERT INTO tags (name)
VALUES
    ('Living Room'),
    ('Kitchen'),
    ('Hall (Downstairs)'),
    ('Office'),
    ('Alec''s Room'),
    ('Our Room'),
    ('Shower'),
    ('Bathroom');

-- Insert Tasks

INSERT INTO tasks (title, priority, last_completed, user_id)
VALUES
    ('Mop floor', 'LOW', '2025-01-21', (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Change bed', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Clean toilet', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Clean sink', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Clean worktops', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Empty cardboard recycling', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Clean and tidy dining table', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Empty main bin', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Empty plastic/cans recycling', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com')),
    ('Clean sink', 'LOW', NULL, (SELECT id FROM users WHERE email = 'lisa@example.com'));

-- Example: Linking 'Mop floor' task with 'Kitchen' tag
INSERT INTO task_tags (task_id, tag_id)
VALUES
    ((SELECT id FROM tasks WHERE title = 'Mop floor'), (SELECT id FROM tags WHERE name = 'Kitchen')),
    ((SELECT id FROM tasks WHERE title = 'Change bed'), (SELECT id FROM tags WHERE name = 'Our Room')),
    ((SELECT id FROM tasks WHERE title = 'Clean toilet'), (SELECT id FROM tags WHERE name = 'Bathroom')),
    ((SELECT id FROM tasks WHERE title = 'Clean sink'), (SELECT id FROM tags WHERE name = 'Bathroom')),
    ((SELECT id FROM tasks WHERE title = 'Clean worktops'), (SELECT id FROM tags WHERE name = 'Kitchen')),
    ((SELECT id FROM tasks WHERE title = 'Empty cardboard recycling'), (SELECT id FROM tags WHERE name = 'Kitchen')),
    ((SELECT id FROM tasks WHERE title = 'Clean and tidy dining table'), (SELECT id FROM tags WHERE name = 'Living Room')),
    ((SELECT id FROM tasks WHERE title = 'Empty main bin'), (SELECT id FROM tags WHERE name = 'Kitchen')),
    ((SELECT id FROM tasks WHERE title = 'Empty plastic/cans recycling'), (SELECT id FROM tags WHERE name = 'Kitchen')),

