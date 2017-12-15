from celebi.schema.utils import init_db
from celebi.settings import ENV

if ENV in ['TEST', 'DEV']:
    init_db()
else:
    for i in range(0, 100):
        print('YOU ARE TRING TO DROP DATABASE ON NONETEST ENVIREMENT !!')
