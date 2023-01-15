import os
#Well, we can actually write just one char, this is just for fun.

content = None

ONE_MB = 1000000
TARGET_SIZE = 10*ONE_MB
TEST_TXT_FILE = "TEST_{TARGET_SIZE}.txt"

PADDING_CHAR = 'A'

with open(TEST_TXT_FILE) as fd:
    content = content + PADDING_CHAR*needed_padding_size
    fd.write(content)

file_size = os.path.getsize(TEST_TXT_FILE)
print("New file:", TEST_TXT_FILE, "size is: ", file_size)

