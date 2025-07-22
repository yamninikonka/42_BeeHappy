
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

