from rich.console import Console as RichConsole

DEFAULT_LOG_LEVEL = 'VERBOSE'
# TODO get log level from dotenv

LogLevel = {
    'NONE': 0,
    'ERROR': 1,
    'NORMAL': 2,
    'VERBOSE': 3,
}

class Console(RichConsole):
    def __init__(self, *args, log_level=DEFAULT_LOG_LEVEL, **kwargs):
        super().__init__(*args, **kwargs)

        self.log_level = log_level
        self.status_obj = None
        
        self._orig_log = self.log
        self.log = self._log_wrapper

        self._orig_status = self.status
        self.status = self._status_wrapper

    def _log_wrapper(self, *args, log_level = 'NORMAL', **kwargs):
        if (LogLevel[log_level] == LogLevel['NONE'] or LogLevel[log_level] > LogLevel[self.log_level]):
            return
        
        self._orig_log(*args, **kwargs)

    def verbose(self, *args, **kwargs):
        self.log(*args, log_level='VERBOSE', **kwargs)

    def error(self, error_msg, **kwargs):
        self.log(f"[red bold]{error_msg}[/]", log_level='ERROR', **kwargs)

    def _status_wrapper(self, *args, **kwargs):
        if self.status_obj is not None:
            self.status_obj.update(*args, **kwargs)
        else:
            self.status_obj = self._orig_status(*args, **kwargs)

        return self.status_obj

console = Console()
