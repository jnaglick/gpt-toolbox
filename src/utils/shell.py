import subprocess

def run_shell_command(command, shell='/bin/zsh'):
    output = {
        "stdout": None,
        "stderr": None,
        "returncode": None
    }

    try:
        # Run the shell command using the specified shell and capture the output
        result = subprocess.run(command, capture_output=True, text=True, shell=True, executable=shell, check=True)
        
        output["stdout"] = result.stdout
        
        if result.stderr:
            output["stderr"] = result.stderr
        
        output["returncode"] = result.returncode
    except subprocess.CalledProcessError as e:
        # TODO log
        output["returncode"] = e.returncode

    return output
