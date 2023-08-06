import argparse
import os
import sys

import cloudpickle as pickle

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)


_VANILLA = 'vanilla'
_DP = 'dp'
_SECURE = 'secure'

parser = argparse.ArgumentParser(description='Run aggregator demo.')
parser.add_argument('-m', '--mode',
                    type=str,
                    default=_VANILLA,
                    help=f'running mode: {_VANILLA}(default) | {_DP} | {_SECURE}')
args = parser.parse_args()
if args.mode == _VANILLA:
    from alphafed import logger
    from alphafed.fed_avg.demo_task import get_scheduler
elif args.mode == _DP:
    from alphafed import logger
    from alphafed.fed_avg.demo_task_dp import get_scheduler
elif args.mode == _SECURE:
    from alphafed import logger
    from alphafed.fed_avg.demo_task_secure import get_scheduler


scheduler = get_scheduler()
logger.debug(f'{type(scheduler)=}')
_pickle_file = os.path.join(CURRENT_DIR, 'model.pickle')
if os.path.exists(_pickle_file):
    os.remove(_pickle_file)
with open(_pickle_file, 'wb') as f:
    pickle.dump(scheduler, f)
