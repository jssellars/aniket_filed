import os

from werkzeug.datastructures import FileStorage

test_txt = "test_upload.txt"
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, test_txt)

test_file = FileStorage(
    stream=open(abs_file_path, "rb"),
    filename="test_upload.txt",
    content_type="application/json",
)
