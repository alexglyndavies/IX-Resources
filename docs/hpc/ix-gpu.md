# IX-GPU Documentation

## Registration

If you are not registered, please email me at a.glyndavies@imperial.ac.uk, give me your imperial details (short imperial name, full imperial email, full name). 
I will then create your account and send you a temporary password which you can use to login for the first time.

## Using the web interface

### Login via web interface:
Follow the link [https://ix-gpu-cloud.ic.ac.uk/](https://ix-gpu-cloud.ic.ac.uk/#/) and use your short imperial name as the username, and the temporary password to login.

Username: aglyndav

Password: ****

Once logged in you should change your temporary password.

### Running jobs:

*TODO*

## Using the terminal.

### Login via SSH:

From your terminal you can run the following command (swapping ```aglyndav``` for your username).

```bash
ssh aglyndav@login-node.ixhpc.ic.ac.uk
``` 

This will show the following message showing that you have accessed the login-node. DO NOT run sessions from here.
```bash
Last login: Tue Jun 23 16:51:00 2026 from XXX.XXX.XXX.XX
[aglyndav@login-node ~]$
``` 

From here you can start interactive GPU sessions, or run slurm jobs.

### Starting an interactive session:
Start an interactive session from the terminal:
```bash
srun --gpus=1 --pty bash
``` 
Which will now queue you up for an interactive session, which when you join will look like this (here I'm logged into node ix-a17-3).
```bash
[aglyndav@ix-a17-3 ~]$
``` 


### Running slurm jobs:

*TODO*
