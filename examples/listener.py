import os
import time
from robot.output import XmlLogger
from robot.running import EXECUTION_CONTEXTS
from robot.reporting.resultwriter import ResultWriter

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


class SuiteLogger:
    ROBOT_LISTENER_API_VERSION = 2

    def start_suite(self, name, attributes):
        attributes['name'] = name
        self._get_logger().start_suite(_DictObj(attributes))

    def end_suite(self, name, attributes):
        attributes['name'] = name
        self._get_logger().end_suite(_DictObj(attributes))
        self._get_logger().close()

    def start_test(self, name, attributes):
        attributes['name'] = name
        self._get_logger().start_test(_DictObj(attributes))

    def end_test(self, name, attributes):
        attributes['name'] = name
        self._get_logger().end_test(_DictObj(attributes))

    def start_keyword(self, name, attributes):
        attributes['name'] = name
        attributes['type'] = 'kw'
        self._get_logger().start_keyword(_DictObj(attributes))

    def end_keyword(self, name, attributes):
        attributes['name'] = name
        attributes['type'] = 'kw'
        self._get_logger().end_keyword(_DictObj(attributes))

    def log_message(self, message):
        if self._get_logger():
            self._get_logger().log_message(_DictObj(message))

    def message(self, message):
        if self._get_logger():
            self._get_logger().message(_DictObj(message))

    def set_log_level(self, level):
        self._get_logger().set_log_level(level)

    def _get_logger(self):
        current = EXECUTION_CONTEXTS.current
        if not current:
            return None
        if hasattr(current, 'suite_logger'):
            return current.suite_logger
        log_path = os.path.join(current.variables['${OUTPUT DIR}'], current.suite.name + '.output.xml')
        current.suite_logger = XmlLogger(log_path)
        return current.suite_logger

class _DictObj(object):
    def __init__(self, attributes):
        self._attrs = attributes

    def __getattr__(self, attr):
        return self._attrs.get(attr, None)
