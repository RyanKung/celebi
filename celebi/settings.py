ENV = 'DEV'


POSTGRES_DEV = {
    'user': 'ryankung',
    'password': 'pi3.1415926',
    'database': 'celebi',
    'host': '127.0.0.1'
}


POSTGRES = {
    'DEV': POSTGRES_DEV
}.get('ENV', POSTGRES_DEV)
