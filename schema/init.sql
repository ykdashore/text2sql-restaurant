-- create schemas
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS catalog;
CREATE SCHEMA IF NOT EXISTS staff;

-- catalog tables
CREATE TABLE IF NOT EXISTS catalog.restaurants (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT,
  rating NUMERIC(2,1)
);

CREATE TABLE IF NOT EXISTS catalog.menu_items (
  id SERIAL PRIMARY KEY,
  restaurant_id INT REFERENCES catalog.restaurants(id),
  name TEXT,
  category TEXT,
  price NUMERIC(8,2)
);

-- sales tables
CREATE TABLE IF NOT EXISTS sales.orders (
  id SERIAL PRIMARY KEY,
  restaurant_id INT REFERENCES catalog.restaurants(id),
  customer_name TEXT,
  order_time TIMESTAMP,
  total_amount NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS sales.order_items (
  id SERIAL PRIMARY KEY,
  order_id INT REFERENCES sales.orders(id),
  menu_item_id INT REFERENCES catalog.menu_items(id),
  quantity INT
);

-- staff
CREATE TABLE IF NOT EXISTS staff.employees (
  id SERIAL PRIMARY KEY,
  name TEXT,
  role TEXT,
  restaurant_id INT REFERENCES catalog.restaurants(id)
);
