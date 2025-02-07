-- Insert Users
INSERT INTO users (name, email)
VALUES
    ('Lisa', 'lisa@example.com'),
    ('Simon', 'simon@example.com')
ON CONFLICT (email) DO NOTHING;

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
    ('Bathroom'),
    ('Hall (Upstairs)'),
    ('Porch');

-- Insert Tasks

INSERT INTO tasks (title, priority, last_completed, repeat_interval, user_id)
VALUES
    ('Mop floor','LOW','2025-02-01',15,1),
('Change bed','LOW','2025-02-01',30,1),
('Clean sink','LOW','2025-02-01',20,1),
('Clean toilet','LOW','2025-02-01',20,1),
('Empty cardboard recycling','LOW','2025-02-01',5,1),
('Clean worktops','LOW','2025-02-01',5,1),
('Clean and tidy dining table','LOW','2025-02-01',10,1),
('Empty main bin','LOW','2025-02-01',5,1),
('Clean sink','LOW','2025-02-01',5,1),
('Clean sink','LOW','2025-02-01',15,1),
('Empty plastic/metal recycling','LOW','2025-02-01',10,1),
('Empty bin','LOW','2025-02-01',10,1),
('Clean toilet','LOW','2025-02-01',15,1),
('Tidy floor','LOW','2025-02-01',5,1),
('Clean bin lid','LOW','2025-02-01',30,1),
('Tidy','LOW','2025-02-01',90,1),
('Clean floor','LOW','2025-02-01',90,1),
('Tidy','LOW','2025-02-01',30,1),
('Empty compost bin','LOW','2025-02-01',5,1),
('Hoover','LOW','2025-02-01',7,1),
('Tidy','LOW','2025-02-01',15,1),
('Clean floor','LOW','2025-02-01',20,1),
('Hoover','LOW','2025-02-01',10,1),
('Hoover','LOW','2025-02-01',10,1),
('Change bed','LOW','2025-02-01',15,1),
('Clean shower door','LOW','2025-02-01',30,1),
('Empty recycling','LOW','2025-02-01',10,1),
('Tidy worktops','LOW','2025-02-01',10,1),
('Empty bin','LOW','2025-02-01',15,1),
('Tidy','LOW','2025-02-01',15,1),
('Clean microwave','LOW','2025-02-01',60,1),
('Clean coffee table','LOW','2025-02-01',30,1),
('Clean shower','LOW','2025-02-01',30,1),
('Hoover','LOW','2025-02-01',20,1),
('Hoover','LOW','2025-02-01',60,1),
('Hoover','LOW','2025-02-01',60,1),
('Hoover','LOW','2025-02-01',60,1),
('Clean fridge','LOW','2025-02-01',60,1);

-- Task tag relationships
INSERT INTO task_tags (task_id, tag_id)
VALUES
(1,(select id from tags where name='Kitchen')),
(2,(select id from tags where name='Our Room')),
(3,(select id from tags where name='Bathroom')),
(4,(select id from tags where name='Bathroom')),
(5,(select id from tags where name='Kitchen')),
(6,(select id from tags where name='Kitchen')),
(7,(select id from tags where name='Living Room')),
(8,(select id from tags where name='Kitchen')),
(9,(select id from tags where name='Kitchen')),
(10,(select id from tags where name='Shower')),
(11,(select id from tags where name='Kitchen')),
(12,(select id from tags where name='Shower')),
(13,(select id from tags where name='Shower')),
(14,(select id from tags where name='Living Room')),
(15,(select id from tags where name='Kitchen')),
(16,(select id from tags where name='Bathroom')),
(17,(select id from tags where name='Bathroom')),
(18,(select id from tags where name='Alec''s Room')),
(19,(select id from tags where name='Kitchen')),
(20,(select id from tags where name='Living Room')),
(21,(select id from tags where name='Office')),
(22,(select id from tags where name='Shower')),
(23,(select id from tags where name='Kitchen')),
(24,(select id from tags where name='Hall (Downstairs)')),
(25,(select id from tags where name='Alec''s Room')),
(26,(select id from tags where name='Shower')),
(27,(select id from tags where name='Porch')),
(28,(select id from tags where name='Kitchen')),
(29,(select id from tags where name='Bathroom')),
(30,(select id from tags where name='Hall (Downstairs)')),
(31,(select id from tags where name='Kitchen')),
(32,(select id from tags where name='Living Room')),
(33,(select id from tags where name='Shower')),
(34,(select id from tags where name='Office')),
(35,(select id from tags where name='Our Room')),
(36,(select id from tags where name='Hall (Upstairs)')),
(37,(select id from tags where name='Alec''s Room')),
(38,(select id from tags where name='Kitchen'));