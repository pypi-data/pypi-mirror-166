import subprocess
import getpass
import os
def cancel_current_job():
    hostname = os.uname().nodename
    username = getpass.getuser()
    job_id = os.environ('SLURM_JOBID')
    cancel_command = f'scancel {job_id}'
    print(f"Cancelling the job {job_id} from {username} at host {hostname}....")
    process = subprocess.Popen(cancel_command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate()
if __name__ == '__main__':
    cancel_current_job()