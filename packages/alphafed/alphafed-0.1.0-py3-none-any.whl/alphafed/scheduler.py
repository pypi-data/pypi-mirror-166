"""Algorithm scheduler."""


from abc import ABC, abstractmethod
from tempfile import TemporaryFile
from typing import Dict

import cloudpickle as pickle

from .bass import BassProxy
from .metrics_trace import MetricsTrace


class Scheduler(ABC):

    def launch_task(self, task_id: str):
        """Launch current task."""
        assert task_id and isinstance(task_id, str), f'invalid task ID: {task_id}'

        bass_proxy = BassProxy()
        with TemporaryFile() as tf:
            pickle.dump(self, tf)
            tf.seek(0)
            file_key = bass_proxy.upload_file(upload_name='model.pickle', fp=tf)
        bass_proxy.launch_task(task_id=task_id, pickle_file_key=file_key)

    def register_metrics(self, name: str, metrics: MetricsTrace):
        """Register a metrics trace tool to current task.

        The trace fo the metrics during training will be included in
        the task's running result and can be downloaded.
        """
        if not name or not isinstance(name, str):
            raise ValueError(f'invalid name of the metrics: {name}')
        if not metrics or not isinstance(metrics, MetricsTrace):
            raise ValueError(f'invalid type of metrics: {type(metrics)}')
        if not hasattr(self, '_metrics_bucket'):
            self._metrics_bucket: Dict[str, MetricsTrace] = {}
        if name in self._metrics_bucket:
            raise ValueError(f'cannot register on an existing name: {name}')
        self._metrics_bucket[name] = metrics

    def get_metrics(self, name: str) -> MetricsTrace:
        if not hasattr(self, '_metrics_bucket'):
            return None
        return self._metrics_bucket.get(name)

    @abstractmethod
    def _setup_context(self, id: str, task_id: str, is_initiator: bool = False):
        """Set up the local running context.

        This function is used by the context manager, DO NOT modify it, otherwize
        there would be strange errors raised.

        :args
            :id
                the node id of the running context
            :task_id
                the id of the task to be scheduled
            :is_initiator
                is this scheduler the initiator of the task
        """

    @abstractmethod
    def _run(self):
        """Run the scheduler.

        This function is used by the context manager, DO NOT modify it, otherwize
        there would be strange errors raised.
        """
