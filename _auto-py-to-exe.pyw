from os import environ, path, remove, system
def command(p_cmd: str) -> None:
    import subprocess
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.check_call(p_cmd, startupinfo=startupinfo)

if __name__ == "__main__":
    t_temp_config_path = rf"{environ.get('TMP')}\auto-py-to-exe-config.json"
    t_path = path.split(__file__)[0]
    t_config = ""
    
    with open(rf"{t_path}\auto-py-to-exe.json", "r") as f:
        t_config = f.read()

    t_config = t_config.replace("%path%", t_path.replace("\\", "/"))

    with open(t_temp_config_path, "w") as f:
        f.write(t_config)
    
    system("pip install --upgrade --upgrade-strategy eager auto-py-to-exe && pip install --upgrade --upgrade-strategy eager -r requirements.txt") # executed with system instead of command to open a cmd window that shows the update process if executed in pythonw

    command(rf'auto-py-to-exe -c "{t_temp_config_path}" -o "{t_path}\output" -lang de')

    remove(t_temp_config_path)