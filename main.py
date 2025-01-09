import paramiko
from time import sleep

import requests
i=0

def ask_wolfram_alpha(query, i=0):
    api_key = '3HHHT3-QAVL535XW6'  # Replace with your actual API key
    url = f'http://api.wolframalpha.com/v1/conversation.jsp?appid={api_key}&i={query}'

    # Send the request to Wolfram Alpha API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Retrieve the result from the JSON response
        if 'result' in data:
            return data['result']
        else:
            if i<=0:
                return "What a dumb question!"
                i+=1
            else:
                return "Now shut your mouth!"
    else:
        return "I don't know you're so annoying"






def import_python(path_without_extension):
    return bash("import "+path_without_extension)


def create_ssh_client(host, port, username, password):
    """Create and return an SSH client"""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the server's host key
    ssh_client.connect(hostname=host, port=port, username=username, password=password)
    return ssh_client

def create_interactive_shell(ssh_client):
    """Create and return an interactive SSH shell"""
    return ssh_client.invoke_shell()

def send_command(cmd, interactive_shell):
    """Send a command to the interactive shell"""
    interactive_shell.send(cmd + '\n')  # Send the command to the interactive shell
    sleep(0.5)  # Wait for the command to execute
    return interactive_shell.recv(1024).decode()



def close_connection(ssh_client):
    """Close the SSH connection"""
    ssh_client.close()

# Usage example:
host = 'ev3dev.local'
username = 'robot'
password = 'maker'
port = 22  # Default SSH port

# Create SSH client
ssh_client0 = create_ssh_client(host, port, username, password)

# Open interactive shell once
shell = create_interactive_shell(ssh_client0)

def bash(cmd, interactive_shell=shell):
    """Run a bash command and print the result"""
    result = send_command(cmd, interactive_shell)
    print(result)

# Run commands using the same interactive shell
bash("cd dee_project")
#bash("pwd")

# You can continue sending more commands in the same session
bash("python3")
#bash("import runpy")
#sleep(10)
bash("import init")

#bash('runpy.run_path("init.py")')



bash("init.talk.talk_ready()")

#sleep(5)

question = "Go left"#use speesh recognization
answer = ask_wolfram_alpha(question)

bash(f'init.talk.sound.speak("{answer}")')

bash("init.talk.talk_okay()")

#sleep(5)

# Use the imported file's functionality

# Test the AI robot speaking


# Close the connection after you're done
sleep(35)
close_connection(ssh_client0)
