import fileinput
import multiprocessing
import os
import select
import sys
from multiprocessing import Process
from queue import Empty
from queue import Queue
from threading import Thread

# pip3 install psutil
import psutil


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
    # read_using_select_probe()

    ## Had to abandon this approach for now, there seems no easy way to realize this except for the thread itself
    ## cooperating (no option here with the system call)
    # read_using_watchdog_thread_with_timeout()

    # read_using_watchdog_process_with_timeout()
    read_using_separate_process_with_join_timeout()


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


# FIXME there seems to be no easy portable way to achieve this in python... :/
# (yet we need the killing feature and can't rely on cooperative threading as the sys calls for reading from
# stdin are blocking)
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
        raise Exception("It seems this can't be done in Python - read code comments")


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


def read_using_watchdog_process_with_timeout():
    queue_as_waitable_object = multiprocessing.Queue(maxsize=10)
    worker_process = Process(target=function_for_stdin_reading_process,
                             args=(queue_as_waitable_object, sys.stdin.fileno()))
    watchdog_process = Process(target=function_for_watchdog_process, args=(queue_as_waitable_object, worker_process,))

    worker_process.start()
    watchdog_process.start()

    watchdog_process.join()
    worker_process.join()


def function_for_stdin_reading_process(queue_to_signal_success, input_stream_fileno):
    # stdin is closed for new processes :/
    # https://docs.python.org/3.5/library/multiprocessing.html#all-start-methods
    # Note to self: portable :)
    # https://docs.python.org/3/library/os.html#os.fdopen
    input_stream = os.fdopen(input_stream_fileno)

    lines = input_stream.readlines()
    queue_to_signal_success.put("don't kill me!")
    for line in lines:
        output_line(line)


def function_for_watchdog_process(queue_as_waitable_object, guarded_process):
    try:
        queue_as_waitable_object.get(block=True, timeout=0.1)
    except Empty as exception:
        # wait timeout!

        print("Killing process that took too long to respond.")

        guarded_process.terminate()

        # for proc in psutil.process_iter():
        #     if "python" in proc.name():
        #         print("[DEBUG] There exists a python process with pid {} named '{}' with args '{}'".format(proc.pid,
        #                                                                                                    proc.name(),
        #                                                                                                    proc.cmdline()))
        #
        # # Using the psutil lib to be os-independent
        # # https://github.com/giampaolo/psutil
        # for proc in psutil.process_iter():
        #     if proc.pid == guarded_process.pid:
        #         print("[DEBUG] Killing process of name: {}".format(proc.name()))
        #         proc.kill()


def read_using_separate_process_with_join_timeout():
    queue_to_pass_lines_through = multiprocessing.Queue(maxsize=1)
    worker_process = Process(target=function_for_reading_lines_from_stdin_process,
                             args=(queue_to_pass_lines_through, sys.stdin.fileno()))
    worker_process.start()

    worker_process.join(timeout=0.1)
    has_exited = not worker_process.is_alive()
    if has_exited:
        try:
            lines = queue_to_pass_lines_through.get(block=False)
            for line in lines:
                output_line(line)
        except Empty as exception:
            raise Exception('unexpected exception')
    else:
        print("no output to generate")
        worker_process.terminate()


def function_for_reading_lines_from_stdin_process(queue_to_pass_lines_through, input_stream_fileno):
    input_stream = os.fdopen(input_stream_fileno)

    lines = input_stream.readlines()
    queue_to_pass_lines_through.put(lines)


def output_line(line):
    print("###" + line.replace('\n', ""))


if __name__ == "__main__":
    main()
