from database.DB_connect import DBConnect
from model.product import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_categories():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select category_name
                    from category """
        cursor.execute(query)
        for row in cursor:
            results.append(row["category_name"])

        cursor.close()
        conn.close()
        return list(results)

    @staticmethod
    def get_product(categoria):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select p.id, p.product_name, p.category_id
                    from product p, category c
                    where p.category_id = c.id and c.category_name = %s"""
        cursor.execute(query,(categoria,))
        for row in cursor:
            product = Product(
                id = row["id"],
                product_name = row["product_name"],
                category_id = row["category_id"],
                vendite = 0
            )
            results.append(product)

        cursor.close()
        conn.close()
        return list(results)

    @staticmethod
    def get_prodotti_venduti(inizio,fine,categoria):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select p.id,p.product_name, p.category_id, count(order_date) as vendite
                    from product p,  order_item oi, `order` o , category c
                    where p.id = oi.product_id and oi.order_id = o.id 
                                and order_date >=%s and order_date <=%s and p.category_id = c.id and c.category_name = %s
                    group by p.id,p.product_name, p.category_id
                    order by vendite DESC"""
        cursor.execute(query,(inizio,fine,categoria))
        for row in cursor:
            product = Product(
                id=row["id"],
                product_name=row["product_name"],
                category_id=row["category_id"],
                vendite=row["vendite"],
            )
            results.append(product)

        cursor.close()
        conn.close()
        return list(results)


