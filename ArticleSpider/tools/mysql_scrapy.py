
import pymysql
class JobboleConnectMysql:
    def __init__(self):
        db = pymysql.Connect(host="localhost",port=3306,user="root",passwd="07597321",charset="utf8mb4",use_unicode=True)

        cursor = db.cursor()
        cursor.execute("ALTER DATABASE ArticleSpider CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        cursor.execute("USE ArticleSpider")

        cursor.execute("DROP TABLE IF EXISTS Jobbole")

        sql = """CREATE TABLE Jobbole(   
                title varchar(200) not null,
                create_date date,
                url varchar(200),
                url_id varchar(200) primary KEY,
                image_url varchar(200),
                image_path varchar(200),
                vote_num int(11) default 0,
                comment_num int(11) default 0,
                book_num int(11) default 0,
                content longtext not null,
                tags varchar(200))"""

        cursor.execute(sql)

        cursor.execute("alter table Jobbole convert to character set utf8mb4 collate utf8mb4_bin")

        db.close()
