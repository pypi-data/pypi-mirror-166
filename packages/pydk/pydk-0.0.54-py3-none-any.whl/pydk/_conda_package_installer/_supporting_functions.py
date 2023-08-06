

# import packages -------------------------------------------------------------
import licorice_font
import os
import pandas as pd
import subprocess


# conda list ------------------------------------------------------------------
def _conda_list_subprocess():
    return subprocess.run(
        ["conda", "list"], stdout=subprocess.PIPE, stderr=False
    ).stdout.decode()


def _write_conda_list_to_table(conda_list, path):

    f = open(path, "w")
    for line in conda_list.split("\n"):
        if not line.startswith("#"):
            newline = []
            for word in line.split(" "):
                if len(word) > 1:
                    newline.append(word)
            if len(newline) == 3:
                newline.append("conda/ubuntu")
            f.write("\t".join(newline) + "\n")
    f.close()


def _read_conda_list_tmp_file(path):
    return pd.read_table(
        path, sep="\t", header=None, names=["library", "version", "info", "channel"]
    )


def _conda_list_to_pandas_df(tmp_path):

    conda_list = _conda_list_subprocess()
    _write_conda_list_to_table(conda_list, tmp_path)
    df = _read_conda_list_tmp_file(tmp_path)
    os.remove(tmp_path)  # clean-up

    return df
    

# installation ----------------------------------------------------------------
def _check_installation(conda_list_df, pkg_name):
    return pkg_name in conda_list_df["library"].to_list()


def _do_install_conda_pkg(channel, package_name):

    package_name_ = licorice_font.font_format(package_name, ["BOLD", "GREEN"])
    download_message = "Installing {} via conda... this may take a few seconds...".format(
        package_name_
    )
    print(download_message, end=" ")
    command = ["conda", "install", "-c", channel, package_name, "-y"]
    log = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("done.")
    return log


# check download --------------------------------------------------------------
def _check_download_log(download_log):

    msg = download_log.stdout.decode("utf-8")

    flex_solve = "Retrying with flexible solve.\n"
    done = "done\n"
    trouble_shoot_msg = None

    if msg.endswith(done):
        return True, trouble_shoot_msg
    elif msg.endswith(flex_solve):
        trouble_shoot_msg = "Ended on flexible solve..."
        return False, trouble_shoot_msg
    else:
        return False, trouble_shoot_msg
    

# rm package ------------------------------------------------------------------
def _remove_package(package_name):

    command = ["conda", "remove", package_name, "-y"]
    rm_log = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if rm_log.stdout.decode("utf-8").endswith("done\n"):
        return rm_log, "removed"
    else:
        return rm_log, "there was a problem during removal..."
    try:
        rm_log = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if rm_log.stdout.decode("utf-8").endswith("done\n"):
            return rm_log, "removed"
    except:
        package_name = licorice_font.font_format(package_name, ["BOLD", "GREEN"])
        print("Could not remove: {}. Maybe it is not installed.".format(package_name))
        return None, "not_removed"