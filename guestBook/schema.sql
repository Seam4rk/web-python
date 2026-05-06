-- SELECT, INSERT, UPDATE, DELETE - +- универсальная для любой реляционной БД
-- CREATE TABLE, DROP TABLE, ALTER TABLE, CREATE INDEX 

-- PRIMARY KEY - первичный ключ
-- База данных - создает индекс (деревья, хэш-таблицы)

-- FOREIGN KEY - внешний ключ - ссылка на данные из другой таблицы
-- author_id может содержать только те значения, которые существуют 
-- в указанном столбце другой таблицы

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_name TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  approved BOOLEAN NOT NULL DEFAULT 0
);
