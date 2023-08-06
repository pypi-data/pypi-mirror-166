import argparse
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHONPATH = os.path.join(CURRENT_DIR, os.pardir, os.pardir)
sys.path.insert(0, PYTHONPATH)


_VANILLA = 'vanilla'
_DP = 'dp'
_SECURE = 'secure'
_FED_IRM = 'fedirm'

parser = argparse.ArgumentParser(description='Run aggregator demo.')
parser.add_argument('-m', '--mode',
                    type=str,
                    default=_VANILLA,
                    help=f'running mode: {_VANILLA}(default) | {_DP} | {_SECURE}')
args = parser.parse_args()
if args.mode == _VANILLA:
    from alphafed import logger
    from alphafed.fed_avg.demo_task import (AGGREGATOR_ID, get_scheduler,
                                            get_task_id)
elif args.mode == _DP:
    from alphafed import logger
    from alphafed.fed_avg.demo_task_dp import (AGGREGATOR_ID, get_scheduler,
                                               get_task_id)
elif args.mode == _SECURE:
    from alphafed import logger
    from alphafed.fed_avg.demo_task_secure import (AGGREGATOR_ID,
                                                   get_scheduler, get_task_id)
elif args.mode == _FED_IRM:
    from alphafed import logger
    from alphafed.fed_avg.demo_FedIRM import (AGGREGATOR_ID, get_scheduler,
                                              get_task_id)


task_id = get_task_id()
scheduler = get_scheduler()
logger.debug(f'{type(scheduler)=}')
scheduler._setup_context(id=AGGREGATOR_ID, task_id=task_id, is_initiator=True)
scheduler.data_channel._ports = [i for i in range(21000, 21010)]
logger.info(f'run aggregator in {args.mode} mode: task_id = {task_id}')
scheduler._run()
