import subprocess
import getpass
import os
def cancel_current_job():
    hostname = os.uname().nodename
    username = getpass.getuser()
    bashCommand = f'squeue -u {username} | grep {hostname}'
    process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
    job_id = output.decode().split()[0]
    cancel_command = f'scancel {job_id}'
    print(f"Cancelling the job...")
    process = subprocess.Popen(cancel_command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
if __name__ == '__main__':
    slurm_cancel_current_job()