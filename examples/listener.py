import os
import time

class RunningInspector:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, output_file='inspector.report'):
        self._output_file = os.path.abspath(output_file)
        # {'log': [10, 20, 30], 'quit': [300]}
        self._report = {}
        self._duration_stack = []

    def start_keyword(self, name, attrs):
        self._duration_stack.append(time.time())

    def end_keyword(self, name, attrs):
        duration = time.time() - self._duration_stack.pop()
        self._report.setdefault(name, []).append(duration)

    def close(self):
        ''' write report file '''
        with open(self._output_file, 'w+b') as f:
            for kw_name, durations in self._report.iteritems():
                f.write(kw_name + '\n')
                f.write('\tcount: %d, duration: %d\n' % (len(durations), sum(durations)))
