
DROP SCHEMA IF EXISTS catalog CASCADE;
DROP SCHEMA IF EXISTS sales CASCADE;
DROP SCHEMA IF EXISTS staff CASCADE;


CREATE SCHEMA catalog;
CREATE SCHEMA sales;
CREATE SCHEMA staff;


CREATE TABLE catalog.restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    phone VARCHAR(50)
);


CREATE TABLE catalog.menu_items (
    id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES catalog.restaurants(id),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    category VARCHAR(50)
);


CREATE TABLE catalog.allergens (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);


CREATE TABLE catalog.menu_item_allergens (
    menu_item_id INT NOT NULL REFERENCES catalog.menu_items(id),
    allergen_id INT NOT NULL REFERENCES catalog.allergens(id),
    PRIMARY KEY (menu_item_id, allergen_id)
);


CREATE TABLE sales.discounts (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    discount_percent NUMERIC(5,2),
    valid_from DATE,
    valid_to DATE
);


CREATE TABLE sales.orders (
    id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES catalog.restaurants(id),
    customer_name VARCHAR(100),
    order_time TIMESTAMP DEFAULT NOW(),
    delivery_fee NUMERIC(10,2),
    discount_id INT REFERENCES sales.discounts(id),
    subtotal_amount NUMERIC(10,2),
    total_amount NUMERIC(10,2)
);


CREATE TABLE sales.order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES sales.orders(id) ON DELETE CASCADE,
    menu_item_id INT NOT NULL REFERENCES catalog.menu_items(id),
    quantity INT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);


CREATE TABLE staff.employees (
    id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL REFERENCES catalog.restaurants(id),
    name VARCHAR(100),
    role VARCHAR(50),
    salary NUMERIC(10,2)
);


CREATE TABLE staff.shifts (
    id SERIAL PRIMARY KEY,
    employee_id INT NOT NULL REFERENCES staff.employees(id),
    shift_start TIMESTAMP,
    shift_end TIMESTAMP
);
