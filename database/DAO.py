from database.DB_connect import DBConnect
from model.names import Names


class DAO():
    @staticmethod
    def get_rates():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct r.avg_rating from ratings r order by avg_rating ASC"""

        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["avg_rating"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodi(minimo, massimo):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct n.* from ratings r , role_mapping rm , names n 
                    where r.movie_id = rm.movie_id 
                    and rm.name_id = n.id 
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    and n.date_of_birth is not null"""

        cursor.execute(query, (minimo, massimo))

        res = []
        for row in cursor:
            res.append(Names(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_archi(id_a, minimo, massimo):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select rm1.name_id as id1, rm2.name_id as id2, sum(REPLACE(m.worlwide_gross_income, "$ ", "")) as somma
                    from role_mapping rm1, role_mapping rm2, movie m, ratings r
                    where rm1.movie_id = rm2.movie_id 
                    and rm1.name_id < rm2.name_id 
                    and m.id = rm1.movie_id 
                    and m.worlwide_gross_income like "$%"
                    and r.movie_id = rm1.movie_id 
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                    group by rm1.name_id , rm2.name_id"""

        cursor.execute(query, (minimo, massimo))

        res = []
        for row in cursor:
            if row["id1"] in id_a and row["id2"] in id_a:
                res.append((id_a[row["id1"]], id_a[row["id2"]], row["somma"]))

        cursor.close()
        cnx.close()
        return res
