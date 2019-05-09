import fileinput
import select
import sys
from queue import Queue
from queue import Empty
from threading import Thread


# "Learning artifact" to try out how to read from stdin in python, preferrably not blocking on empty input
#
# Example calls:
# cat ../tests/test_resources/test_ascii_art_small.txt | python3 streaming_from_stdin.py
# python3 streaming_from_stdin.py < ../tests/test_resources/test_ascii_art_small.txt
#
# This should not block indefinitely:
# python3 streaming_from_stdin.py

def main():
    # direct_read_from_stdin()
    # read_using_fileinput()
    # read_using_file_descriptor()
    read_using_select_probe()

    ## Had to abandon this approach for now, there seems no easy way to realize this except for the thread itself
    ## cooperating (no option here with the system call)
    # read_using_watchdog_thread_with_timeout()


def direct_read_from_stdin():
    # # This guard is not working:
    # if not sys.stdin.isatty():

    # input_lines = sys.stdin.readlines()
    input_lines = sys.stdin
    for line in input_lines:
        output_line(line)


def read_using_fileinput():
    fileinput_input = fileinput.input()
    for line in fileinput_input:
        output_line(line)


def read_using_file_descriptor():
    with open(0) as my_stdin:
        for line in my_stdin:
            output_line(line)


def read_using_select_probe():
    if sys.platform == 'Win32' or sys.platform == 'cygwin':
        # See
        # https://docs.python.org/3/library/sys.html#sys.platform
        # https://docs.python.org/3/library/select.html
        print("Not available for files on Windows")
        return

    ready_to_read = select.select([sys.stdin, ], [], [], 0.0)[0]
    if ready_to_read:
        for line in sys.stdin.readlines():
            output_line(line)
    else:
        print("No data")


class KillableThread(Thread):

    def __init__(self, queue_to_signal_success):
        Thread.__init__(self)
        self.queue_to_signal_success = queue_to_signal_success

    def run(self):
        self.run_internal_part_1()
        self.signal_watchdog_thread()
        self.run_internal_part_2()

    def run_internal_part_1(self):
        pass

    def signal_watchdog_thread(self):
        self.queue_to_signal_success.put("don't kill me!")

    def run_internal_part_2(self):
        pass

    def kill(self):
        # FIXME there seems to be no easy way to achieve this in python... :/
        pass


class ReadFromStdinThread(KillableThread):

    def __init__(self, queue_to_signal_success):
        KillableThread.__init__(self, queue_to_signal_success)

    def run_internal_part_1(self):
        self.lines = sys.stdin.readlines()

    def run_internal_part_2(self):
        for line in self.lines:
            output_line(line)


class WatchingThread(Thread):

    def __init__(self, guarded_thread, queue_as_waitable_object, timeout_seconds=0.5):
        Thread.__init__(self)
        self.guarded_thread = guarded_thread
        self.queue_as_waitable_object = queue_as_waitable_object
        self.timeout_seconds = timeout_seconds

    def run(self):
        try:
            self.queue_as_waitable_object.get(block=True, timeout=0.1)
        except Empty as exception:
            # wait timeout!
            print("Killing thread that took too long to respond.")
            self.guarded_thread.kill()


def read_using_watchdog_thread_with_timeout():
    q = Queue()

    worker = ReadFromStdinThread(q)
    watchdog = WatchingThread(worker, q)

    worker.start()
    watchdog.start()

    watchdog.join()
    worker.join()


def output_line(line):
    print("###" + line.replace('\n', ""))


if __name__ == "__main__":
    main()
