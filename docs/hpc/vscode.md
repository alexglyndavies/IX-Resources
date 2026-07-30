# Connecting to HPC via VSCode

1. Install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension in VSCode.
2. Click the "Open a Remote Window" button in the bottom left corner of VSCode and select "Connect to Host...", followed by "Configure SSH Host...".
3. This will open the SSH configuration file (`~/.ssh/config`) and add the following entry (replacing `<username>` with your actual username):
   ```
   Host ixhpc
       HostName login-node.ixhpc.ic.ac.uk
       User <username>
   ```
4. Again, click the "Open a Remote Window" button, "Connect to Host...", and select "ixhpc" to connect to your HPC account, entering in your password when prompted.
5. In the navigation bar, click the "Open Folder" button and select the folder you want to open - now you can use your local VSCode to edit files on the HPC.
