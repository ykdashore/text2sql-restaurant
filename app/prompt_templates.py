# few-shot template (baseline) - tune this heavily later
FEW_SHOT = """
You are a SQL generator for a Postgres database with schemas: catalog, sales, staff.
Only produce a single valid SQL SELECT statement. Use the schema names.
Examples:
### NL: "List restaurants in Indore with rating > 4"
SQL: SELECT id, name, city, rating FROM catalog.restaurants WHERE city = 'Indore' AND rating > 4;
###
### NL: "What are total sales per restaurant this month?"
SQL: SELECT r.id, r.name, SUM(o.total_amount) AS total_sales
FROM catalog.restaurants r
JOIN sales.orders o ON r.id = o.restaurant_id
WHERE o.order_time >= date_trunc('month', current_date)
GROUP BY r.id, r.name;
###
Now convert user query to SQL. Only return SQL.
USER: {user_query}
SQL:
"""
