DROP TABLE IF EXISTS recipe;

CREATE TABLE recipe (
  id serial PRIMARY KEY,
  name varchar(30) NOT NULL,
  date DATE NOT NULL,
  ingredients TEXT,
  instructions TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
