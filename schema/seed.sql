

INSERT INTO catalog.restaurants (name, location, phone) VALUES
('Pizza Palace', 'Downtown', '555-1234'),
('Burger Barn', 'Midtown', '555-5678'),
('Sushi Central', 'Uptown', '555-8765'),
('Taco Town', 'Suburbs', '555-4321'),
('Veggie Delight', 'Greenfield', '555-9090');


INSERT INTO catalog.menu_items (restaurant_id, name, description, price, category) VALUES
(1, 'Pepperoni Pizza', 'Classic pepperoni with mozzarella.', 12.99, 'Pizza'),
(1, 'Veggie Pizza', 'Loaded with fresh vegetables.', 11.99, 'Pizza'),
(2, 'Cheeseburger', 'Juicy beef patty with cheese.', 8.99, 'Burgers'),
(2, 'Veggie Burger', 'Plant-based patty with toppings.', 9.49, 'Burgers'),
(3, 'California Roll', 'Crab, avocado, cucumber.', 7.99, 'Sushi'),
(3, 'Spicy Tuna Roll', 'Tuna with spicy mayo.', 8.49, 'Sushi'),
(4, 'Chicken Taco', 'Grilled chicken with salsa.', 3.99, 'Tacos'),
(4, 'Beef Taco', 'Seasoned beef and cheese.', 4.49, 'Tacos'),
(5, 'Quinoa Salad', 'Healthy quinoa with veggies.', 6.99, 'Salads'),
(5, 'Veggie Wrap', 'Fresh vegetables in whole wheat wrap.', 5.99, 'Wraps'),
(1, 'Garlic Breadsticks', 'Freshly baked with garlic.', 4.50, 'Sides'),
(2, 'Fries', 'Crispy golden fries.', 3.50, 'Sides'),
(3, 'Miso Soup', 'Traditional Japanese soup.', 2.99, 'Soups'),
(4, 'Nachos', 'Loaded nachos with cheese.', 6.50, 'Appetizers'),
(5, 'Fruit Bowl', 'Mixed seasonal fruits.', 4.99, 'Snacks');


INSERT INTO catalog.allergens (name) VALUES
('Gluten'),
('Dairy'),
('Nuts'),
('Soy'),
('Shellfish'),
('Eggs');


INSERT INTO catalog.menu_item_allergens (menu_item_id, allergen_id) VALUES
(1, 1), (1, 2),
(2, 1),
(3, 2),
(4, 4),
(5, 5),
(6, 5),
(7, 6),
(8, 6),
(9, 4),
(10, 1),
(11, 1), (11, 2),
(12, 1),
(14, 1),
(15, 3);


INSERT INTO sales.discounts (code, description, discount_percent, valid_from, valid_to) VALUES
('DISC10', '10% off your order', 10, '2024-01-01', '2025-01-01'),
('DISC20', '20% off for orders above $50', 20, '2024-06-01', '2025-06-01'),
('FREESHIP', 'Free delivery on all orders', 0, '2024-02-01', '2025-02-01'),
('WELCOME5', '5% off for first-time customers', 5, '2024-01-01', '2025-12-31');


INSERT INTO sales.orders (restaurant_id, customer_name, delivery_fee, discount_id, subtotal_amount, total_amount)
VALUES
(1, 'John Doe', 3.00, NULL, 25.98, 28.98),
(2, 'Jane Smith', 2.50, 1, 18.48, 18.48 * 0.90 + 2.50),
(3, 'Mike Johnson', 4.00, NULL, 16.48, 20.48),
(4, 'Sarah Lee', 3.00, 3, 8.48, 8.48),
(5, 'David Kim', 2.00, 4, 12.98, 12.98 * 0.95 + 2.00),
(1, 'Emma Davis', 3.00, NULL, 4.50, 7.50),
(2, 'Olivia Brown', 2.50, NULL, 3.50, 6.00),
(3, 'Liam Wilson', 4.00, NULL, 10.98, 14.98),
(4, 'Noah Taylor', 3.00, NULL, 6.50, 9.50),
(5, 'Ava Martinez', 2.00, NULL, 4.99, 6.99),
(1, 'Lucas Anderson', 3.00, NULL, 11.99, 14.99);


INSERT INTO sales.order_items (order_id, menu_item_id, quantity, price) VALUES
(11, 2, 1, 11.99);


INSERT INTO staff.employees (restaurant_id, name, role, salary) VALUES
(1, 'Alice Manager', 'Manager', 50000),
(1, 'Bob Chef', 'Chef', 35000),
(2, 'Charlie Server', 'Server', 25000),
(2, 'Diana Cashier', 'Cashier', 22000),
(3, 'Ethan Sushi Chef', 'Chef', 40000),
(4, 'Fiona Taco Maker', 'Chef', 30000),
(5, 'George Salad Expert', 'Chef', 28000);


INSERT INTO staff.shifts (employee_id, shift_start, shift_end) VALUES
(1, '2024-10-01 09:00', '2024-10-01 17:00'),
(2, '2024-10-01 10:00', '2024-10-01 18:00'),
(3, '2024-10-01 08:00', '2024-10-01 16:00'),
(4, '2024-10-01 12:00', '2024-10-01 20:00'),
(5, '2024-10-01 11:00', '2024-10-01 19:00');