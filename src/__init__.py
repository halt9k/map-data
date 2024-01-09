import os
import sys
from pathlib import Path

app_root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(app_root_path)

if Path(os.curdir).absolute().name == 'src':
    os.chdir(app_root_path)
    print(f'Root path is set to {app_root_path}')

# TODO stable way to set path?