from pprint import pprint 
import sys
import traceback


def print_pretty(obj):
    pprint(obj)

def print_block(string, end="\n"):
    hash_num = 45
    print("\n\n")
    print("#" * hash_num)

    mid_hash_num = min((hash_num - len(string) - 2) // 2, 3)
    mid_hash = "#" * mid_hash_num
    mid_space = " " * ((hash_num - 2 * mid_hash_num - len(string))//2)
    print("{}{}{}{}{}".format(
        mid_hash, mid_space, " "*len(string), mid_space, mid_hash
    ))
    print("{}{}{}{}{}".format(
        mid_hash, mid_space, string, mid_space, mid_hash
    ))
    print("{}{}{}{}{}".format(
        mid_hash, mid_space, " "*len(string), mid_space, mid_hash
    ))
    print("#" * hash_num)
    print()


# Both `DuplicateWriter` and `Tee` are contributed to the following repo:
#       https://github.com/netsharecmu/NetShare/blob/0ade9916d27307e63a31d17afcbcb9785c14b9f0/netshare/utils/tee.py
class DuplicateWriter(object):
    def __init__(self, file_objects):
        self._file_objects = file_objects

    def write(self, data):
        for file_object in self._file_objects:
            file_object.write(data)
            file_object.flush()

    def writelines(self, data):
        for file_object in self._file_objects:
            file_object.write(data)
            file_object.flush()

    def flush(self):
        for file_object in self._file_objects:
            file_object.flush()


class Tee(object):
    def __init__(self, stdout_path, stderr_path):
        self.stdout_file = open(stdout_path, 'w')
        self.stderr_file = open(stderr_path, 'w')
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.stdout_writer = DuplicateWriter([sys.stdout, self.stdout_file])
        self.stderr_writer = DuplicateWriter([sys.stderr, self.stderr_file])

    def __enter__(self):
        sys.stdout = self.stdout_writer
        sys.stderr = self.stderr_writer

    def __exit__(self, exc_type, exc, exc_tb):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        if exc_type is not None:
            self.stderr_writer.write(traceback.format_exc())
        self.stderr_writer.flush()
        self.stdout_writer.flush()
        self.stderr_file.close()
        self.stdout_file.close()