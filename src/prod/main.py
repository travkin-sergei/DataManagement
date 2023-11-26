import os
import sys
from src.prod.system.models import OrmCreateTable

sys.path.insert(1, os.path.join(sys.path[0], '..'))

OrmCreateTable()  # создать таблицы в базе данных

