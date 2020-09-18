from peewee import MySQLDatabase, Model, CharField, BooleanField
mysql_db = MySQLDatabase('business_gazeta', user='root', password='1f53601c', host='localhost', port=3306)


class UserAgent(Model):
    user_agent = CharField(unique=True)

    class Meta:                                           
        database = mysql_db
        db_table = 'user_agents'     


class Proxy(Model):
    host_port = CharField(unique=True)
    login_pass = CharField(null=True)
    used = BooleanField(default=False)

    class Meta:
        database = mysql_db
        db_table = 'proxies'
