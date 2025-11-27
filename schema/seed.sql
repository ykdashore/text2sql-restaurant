INSERT INTO catalog.restaurants (name, city, rating) VALUES
 ('Riverfront Diner','Indore',4.4),
 ('Spice Hub','Indore',4.0),
 ('Green Bowl','Pune',4.5);

INSERT INTO catalog.menu_items (restaurant_id, name, category, price) VALUES
 (1,'Margherita Pizza','Pizza', 8.99),
 (1,'Coke','Beverage', 1.50),
 (2,'Butter Chicken','Main',10.00),
 (3,'Quinoa Salad','Salad',7.50);

INSERT INTO sales.orders (restaurant_id, customer_name, order_time, total_amount) VALUES
 (1,'Amit','2025-11-01 12:10:00',10.49),
 (2,'Ria','2025-11-02 19:30:00',20.50);

INSERT INTO sales.order_items (order_id, menu_item_id, quantity) VALUES
 (1,1,1), (1,2,1), (2,3,2);
