import os
import time

class RunningInspector:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, output_file='inspector.report'):
        self._output_file = os.path.abspath(output_file)
        # {'log': [10, 20, 30], 'quit': [300]}
        self._report = {}
        self._kw_start_time = {}

    def start_keyword(self, name, attrs):
        self._kw_start_time[name] = time.time()

    def end_keyword(self, name, attrs):
        duration = time.time() - self._kw_start_time[name]
        del(self._kw_start_time[name])
        if name in self._report:
            self._report[name].append(duration)
        else:
            self._report[name] = [duration]

    def close(self):
        ''' write report file '''
        with open(self._output_file, 'w+b') as f:
            for kw_name in self._report:
                f.write(kw_name)
                f.write('\n')
                f.write('\tcount: %d, duration: %d\n' % (len(self._report[kw_name]), sum(self._report[kw_name])))
