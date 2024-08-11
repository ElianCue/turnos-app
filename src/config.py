class Config:
        SECRET_KEY = '(594h8^h@*e-e*zgy^hs1g1)$q5ekt77ip!)z1!3!=i74a+s&6'

class DevelopmentConfig(Config):
        DEBUG=True
        MYSQL_HOST = 'localhost'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = '!testingcosas123'
        MYSQL_DB = 'flask_login'

config = {
        'development' : DevelopmentConfig
}