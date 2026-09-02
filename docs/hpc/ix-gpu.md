# IX-GPU Documentation

- [Quickstart](#quickstart)
- [Fair Use Guide](#fair-use-guide)
- [VSCode Integration](#connecting-to-hpc-via-vscode)

# Quickstart

This documentation provides instructions on how to use the IX-GPU cluster. It covers how to use the web interface and how to use the terminal to login and submit jobs.

If you are not yet registered for the IX-GPU cluster, please email me at [a.glyndavies@imperial.ac.uk](mailto:a.glyndavies@imperial.ac.uk), give me your imperial details (short imperial name, full imperial email, full name). 
I will create your account and send back your username and temporary password which you can use to login for the first time.

Once logged in you should change your temporary password.

## Option 1: Using the web interface

### Login via web interface:
Follow the link [https://ix-gpu-cloud.ic.ac.uk/](https://ix-gpu-cloud.ic.ac.uk/#/). This brings you to the login-page


![alt-text='Login via web interface'](../../assets/images/lico.png)

Use your short imperial name as the username, and the temporary password to login. This will bring you to the homepage -- highlighted here in red is the terminal button -- click this to open a window at the bottom of the page.

![alt-text='Homepage'](../../assets/images/lico-homepage.png)

At the bottom of the page you will see on the left panel your home directory, and on the right panel the option to login to the login-node. Here you can run commands on the login-node (see [Option 2: Using the terminal](ix-gpu.md#option-2-using-the-terminal))

![alt-text='LiCO term'](../../assets/images/lico-term.png)

You can easily transfer and manage files using the left panel. You can start jupyter sessions using the "Cloud Tools" section.

![alt-text='LiCO interactive'](../../assets/images/lico-interactive.png)

Selecting the gear icon on the Jupyter session opens a configuration window where you can set the number of GPUs and other options -- include a simple password which you will use when connecting to the Jupyter session.

![alt-text='LiCO jupyter'](../../assets/images/lico-jupyter.png)

## Option 2: Using the terminal

### Login via SSH

From your terminal you can run the following command (swapping ```<username>``` for your username).

```bash
ssh <username>@login-node.ixhpc.ic.ac.uk
``` 

Once you have logged in using your password, you will be greeted with a message giving some simple instructions for running jobs, general information and maintenance notifications. You will see the following if you are logged in to the login-node: 
```bash
[<username>@login-node ~]$
``` 
> DO NOT run any heavy jobs from the login node. This is a shared resource and should only be used for simple tasks (submitting SLURM jobs or transferring small files). If you are downloading/transferring large files, installing large software, or running heavy computations, please use the compute nodes instead (see [Running interactive sessions](ix-gpu.md#running-interactive-sessions)).

From here you can submit SLURM jobs and run interactive sessions. The next few sections provide a guide for how to do this.

### Running interactive sessions
Interactive sesssions are shell sessions on the compute nodes - from here you can run intensive computations, download/transfer large files. To start an interactive session, run the following command from the terminal:
```bash
srun --pty bash
``` 
This will queue you up for an interactive session. When you are allocated the session you will join and you terminal will look something like this (here I'm logged into node ```ix-a17-3```).
```bash
[<username>@ix-a17-3 ~]$
``` 
By default, you will be allocated the following:
>  1 CPU core <br>
>  12 GB of RAM <br>
>  24 hours

Test this out yourself - start an interactive session as above, and use this to install the python package management software ```uv```:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Once this is complete, exit the interactive session. Try to avoid leaving interactive sessions running idle for long periods of time, and always exit when you are done.

Depending on your use case, you will need to request more resources (CPU cores, RAM, or time for your session). This is specified when starting the interactive session:
```bash
srun --pty \
--cpus-per-task=2 \
--gpus=1 \
--mem=16G \
--time=01:00:00 \
bash
``` 
This requests the following resources:
>  2 CPU cores <br>
>  1 GPU <br>
>  16 GB of RAM <br>
>  1 hour

It is best practice to request the minimum amount of resources needed for your job, and to request more resources only when necessary.

### Running SLURM jobs

If you want to queue up a job to run on the cluster, you can use the ```sbatch``` command to submit SLURM jobs. It is recommended to use this method of submitting larger jobs, as opposed to waiting to be allocated significant resources in an interactive session. 

Again, we must specify the resources needed, but this is done in the job script. Here we give a simple example of a job script running a python file.

#### Simple Python job

First, create a folder in your home directory to store your job script, python files and logs. These tasks can be carried out from the login-node, since they are inexpensive.
```bash
mkdir python-test
cd python-test
```

Create a new ```uv``` project and add in the required packages:
```bash
uv init
uv add numpy
```

Create a new python file called ```test.py``` and copy the below code into it:
```python
import os
import socket

import numpy as np

print(f"Running on node: {socket.gethostname()}")
print(f"SLURM job ID: {os.environ.get('SLURM_JOB_ID')}")
print(f"Allocated CPUs: {os.environ.get('SLURM_CPUS_PER_TASK')}")

values = np.arange(10)
print(f"Mean: {values.mean()}")
```

Now we have a script to run, we can generate a job script to specify the resources needed and run the job on the cluster. Create a new file called ```submit.slurm``` and copy the below code into it:
```bash
#!/bin/bash

#SBATCH --job-name=python-test
#SBATCH --output=python-test.out
#SBATCH --error=python-test.err

#SBATCH --time=00:10:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G

# Move to the directory from which sbatch was run.
cd "$SLURM_SUBMIT_DIR"

# Run Python from the uv-created virtual environment.
uv run test.py
```

The comments ```#SBATCH``` are used to specify the resources needed for the job, and the names of the output and error files. The file ```python-test.out``` will contain the standard output of the job (the print statements in the python script), and ```python-test.err``` will contain any error messages.

To submit the job to the cluster, run the following command:
```bash
sbatch submit.slurm
```
This will return a job ID that you can use to track the status of the job, and you are able to exit the terminal and the job will run once it reaches the end of the queue.

```bash
[<username>@login-node python-test]$ sbatch submit.slurm
Submitted batch job 64857
```

Once this has completed, you can view the output and error files in the directory from which you submitted the job. Try running the following command and observing the output:
```bash
cat python-test.out
```

#### Useful commands for tracking job status

Some useful commands for tracking the status of the job and the SLURM queue are shown here. To view the status of a job, run the following command:
```bash
squeue -j <job_id>
```
To view your own queued jobs, run the following command:
```bash
squeue -u <username>
```

# Fair Use Guide

<b>TODO</b>

# Connecting to HPC via VSCode

1. Install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension in VSCode.
2. Click the "Open a Remote Window" button in the bottom left corner of VSCode: 
![alt-text='open a remote window'](../../assets/images/ssh-1.png) <br>
Select "Connect to Host..." (bottom option)
![alt-text='connect to host'](../../assets/images/ssh-2.png) <br>
followed by "Configure SSH Host..."
![alt-text='configure ssh host'](../../assets/images/ssh-3.png) <br>
3. Select the config file highlighted below. 
![alt-text='configure ssh file'](../../assets/images/ssh-4.png) <br>
This will open the SSH configuration file (`~/.ssh/config`) and add the following entry (replacing `<username>` with your actual username):
   ```
   Host ixhpc
       HostName login-node.ixhpc.ic.ac.uk
       User <username>
   ```
<br>Which will look like this when complete:
![alt-text='ssh host file complete'](../../assets/images/ssh-host-full.png)
4. Again, click the "Open a Remote Window" button, "Connect to Host...", and select "ixhpc" to connect to your HPC account, entering in your password when prompted.
![alt-text='ssh password'](../../assets/images/ssh-password.png)
5. In the navigation bar, click the "Open Folder" button and select the folder you want to open - now you can use your local VSCode to edit files on the HPC.
