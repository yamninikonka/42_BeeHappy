
import os
import logging
# import sys

# ----- Project root Path -----
# project_root=os.path.abspath("..")
pkg_path=os.path.abspath(os.path.dirname(__file__))
# # print(project_root)
# # print(pkg_path)
# # print(sys.path)

# ----- Add project root to system path ----- 
# if not project_root in sys.path:
#     sys.path.insert(0, project_root)
#     # print(sys.path)

# ----- logging configuration -----
# @TODO: import variable in src/__init__.py
# --- File exists
log_file=os.path.join(pkg_path, 'project/logging.log')
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        f.write('')

Logger = logging.getLogger(__name__)
# Logging configuration: filename, time, level, filename, message
logging.basicConfig(
                    filename=log_file, 
                    encoding='utf-8',
                    level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(filename)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
