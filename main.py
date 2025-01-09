import paramiko
from time import sleep

#initial connection
def create_ssh_client(host, port, username, password):
    """Create and return an SSH client"""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the server's host key
    ssh_client.connect(hostname=host, port=port, username=username, password=password)
    return ssh_client




host = 'ev3dev.local'
username = 'robot'
password = 'maker'
port = 22  # Default SSH port

# Create a persistent SSH connection
ssh_client = create_ssh_client(host, port, username, password)
#internal function for message sending
def send_message(cmd,ssh_client=ssh_client):
    """Send a message (command) over the open SSH connection"""
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    return stdout.read().decode()
#shorcut for command-like transparency

def bash(cmd):
    print(send_message(cmd))

def close_connection(ssh_client):
    """Close the SSH connection"""
    ssh_client.close()

# Send multiple messages using the same connection
#response1 = send_message(ssh_client, "ls")

#print(initial_message())
#response2 = send_message(ssh_client, initial_message())
bash("cd dee_project\npwd")
sleep(1)
bash("pwd")
bash("python3 dee_project/init.py")
#bash("python3")
#bash('print("python")')

# Print the responses from the remote server
#print("Response 1:", response1)
#print("Response 2:", response2)

# Close the connection after you're done
close_connection(ssh_client)
