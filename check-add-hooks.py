import os
import pathlib
from shutil import copyfile

def check_add_hook():
    proj_dir_list = os.listdir("..")
    proj_dir_list.remove("git_Hook_Scripts")

    for proj in proj_dir_list:
        search_path = "../" + proj + "/.git/hooks/"
        try:
            hooks_itens = os.listdir(search_path)
        except:
            continue
        flag = False
        for item in hooks_itens:
            if ".sample" not in item:
                flag = True
        if flag == False:
            print("({}) the following directory doesn't have git hook.".format(proj) + \
                " Do you want the git hook to be added to the directory? [y/n]")
            usr_iput = str(input())
            if usr_iput.lower() == "y":
                # add files needed for git hook in the project
                # print(search_path)
                copyfile("pre-commit.py", search_path + "pre-commit.py")
                copyfile("pre-commit", search_path + "pre-commit")
                copyfile("pre-push", search_path + "pre-push")
                os.chmod(search_path + "pre-commit", 0o711)
                os.chmod(search_path + "pre-push", 0o711)
                print("hook added.")
if __name__ == "__main__":
    check_add_hook()
