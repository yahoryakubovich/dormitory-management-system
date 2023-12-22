-- Создание таблиц one-to-many

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    sex CHAR(1) NOT NULL,
    room_id INT REFERENCES Rooms(id)
);

-- Список комнат и количество студентов в каждой из них

CREATE INDEX idx_students_room_id ON students(room_id);

SELECT rooms.id, rooms.name, COUNT(students.id) AS student_count
FROM rooms
LEFT JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
ORDER BY rooms.id;

-- 5 комнат, где самый маленький средний возраст студентов

CREATE INDEX idx_students_birthday ON students(birthday);

SELECT rooms.id, rooms.name, AVG(EXTRACT(YEAR FROM AGE(NOW(), students.birthday))) AS average_age
FROM rooms
LEFT JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
ORDER BY average_age ASC
LIMIT 5;

-- 5 комнат с самой большой разницей в возрасте студентов

CREATE INDEX idx_students_birthday ON students(birthday);

SELECT rooms.id, rooms.name, MAX(EXTRACT(YEAR FROM AGE(NOW(), students.birthday))) - MIN(EXTRACT(YEAR FROM AGE(NOW(), students.birthday))) AS age_difference
FROM rooms
LEFT JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
ORDER BY age_difference DESC
LIMIT 5;

-- Список комнат где живут разнополые студенты

CREATE INDEX idx_students_sex ON students(sex);

SELECT rooms.id, rooms.name
FROM rooms
INNER JOIN students ON rooms.id = students.room_id
GROUP BY rooms.id, rooms.name
HAVING COUNT(DISTINCT students.sex) > 1;
