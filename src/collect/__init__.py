
# from db import AUTH_GROUPS
#from db.a98_db_beehives_update import db_table_update


import os
import sys

project_root=os.path.abspath(".")
pkg_path=os.path.abspath(os.path.dirname(__file__))
# print(project_root)
# print(pkg_path)
# print(sys.path)
if not project_root in sys.path:
    sys.path.insert(0, project_root)
    # print(sys.path)

