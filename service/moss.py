"""checker python lint"""
import subprocess
import os
from .utils import InitSubmissionEnv

PWD = "/tmp"

def file_check(hw_id: str, language: str, files: list):
    """
    check files
    """
    with InitSubmissionEnv(PWD, hw_id=str(hw_id)) as tmp_dir:
        hw_dir = tmp_dir
        extension = ""
        file_list = []

        if language == "python3":
            extension = ".py"
        elif language == "java":
            extension = ".java"
        elif language == "clang":
            extension = ".c"
        elif language == "cpp":
            extension = ".cpp"

        for file in files:
            src_path = os.path.join(hw_dir, file["name"] + extension)
            with open(src_path, "w", encoding="utf-8") as target:
                target.write(file["content"])
            file_list.append(file["name"] + extension)
            os.chmod(src_path, 0o400)

        return _moss(hw_dir, language, file_list)

def _moss(hw_dir, language, files): # call moss
    # 判斷是哪種程式語言
    if language == "python3":
        command = ["perl", "/src/moss", "-l", "python", *files]
    elif language == "java":
        command = ["perl", "/src/moss", "-l", "java", *files]
    elif language == "clang":
        command = ["perl", "/src/moss", "-l", "c", *files]
    elif language == "cpp":
        command = ["perl", "/src/moss", "-l", "cc", *files]

    result = subprocess.run(command, cwd=hw_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = result.stdout.decode("utf-8")
    result = result.splitlines()

    # 紀錄 moss 噴出來的 url , 會在 result 的最後一個
    url = result[len(result)-1]
    # 先 return url
    return url
