import time

import paramiko
from time import sleep

import requests
import speech_recognition as sr
from sympy.codegen.ast import continue_

# Initialize recognizer
recognizer = sr.Recognizer()

#import openai


#openai.api_key = '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'

from openai import OpenAI

def open_ai(prompt):
    context="you are a robot elephant, programmed by your master, Dorian, for a student project. You can go forward, backward, if we ask you with the words 'go back' and 'go forward'. You can answer to any question about anything. Be funny sometimes. Make a short and concise answer. Dont use any punctuation except for dots or '!', dont use any smiley or any character that is not basic ascii. Also don't use any ' for exemple instead of writing 'don't' write 'dont', etc"
    client = OpenAI(
    api_key="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"
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
     {"role": "user", "content": f" context: {context}, Prompt: {prompt}"}
    ]
    )

    return completion.choices[0].message.content






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
        print("not connected to API")
        return "I don't know you're so annoying"






def import_python(path_without_extension):
    return txt_cmd("import " + path_without_extension)


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

def txt_cmd(cmd, interactive_shell=shell):
    """Run a bash command and print the result"""
    result = send_command(cmd, interactive_shell)
    print(result)

def speech_to_text():
        # Use the microphone as the source for input
    with sr.Microphone() as source:
        print("Please say something:")
        audio = recognizer.listen(source)

    try:
            # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return "not_understand"
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))


def take_action(m_action):
    j="init."
    if m_action == "forward":
        txt_cmd(j + "motor1.on(40)")
        txt_cmd(j + "motor2.on(40)")
    if m_action == "backward":
        txt_cmd(j + "motor1.on(-12)")
        txt_cmd(j + "motor2.on(-12)")
    if m_action == "stop":
        txt_cmd(j + "motor1.stop()")
        txt_cmd(j + "motor2.stop()")

def request_router(request):

    if ("start" in request) or ("go forward" in request and len(request)<20):
        #txt_command("init.talk.talk_okay()")
        txt_cmd('init.talk.sound.speak("im going forward")')
        action = "forward"
        take_action(action)

    elif("go back") in request:
        txt_cmd('init.talk.sound.speak("im going forward")')
        action = "backward"
        take_action(action)

    elif ("stop" or "Stop") in request:
        action="stop"
        take_action(action)
    else:
        #txt_command(f'init.talk.sound.speak("{request}")')
        print("regular talk")
        return 0


    return 1


def goodbye_dance():

    txt_cmd("init.motor1.on(70)")
    txt_cmd("init.motor2.on(50)")
    time.sleep(0.8)
    txt_cmd("init.motor1.on(-70)")
    txt_cmd("init.motor2.on(-50)")
    time.sleep(0.2)
    txt_cmd("init.motor1.stop()")
    txt_cmd("init.motor2.stop()")



# Run commands using the same interactive shell
txt_cmd("cd dee_project")
#bash("pwd")

# You can continue sending more commands in the same session
txt_cmd("python3")
#bash("import runpy")
#sleep(10)
txt_cmd("import init")

#bash('runpy.run_path("init.py")')



txt_cmd("init.talk.talk_ready()")

sleep(15)
request=""
while "stop talking" not in request:

    request = speech_to_text() #use speesh recognization
    if request=="not_understand":
        txt_cmd(f'init.talk.sound.speak("I did not get what your saying please articulate!")')
        sleep(4)

    elif request_router(request) == 1:
        sleep(5)
        continue# it was an action the function handled it

    else :
        print(f"trying to reach API with request:{request} ")

        try:
            answer = open_ai(request)
            print(f"answer from the API: {answer}")
            txt_cmd(f'init.talk.sound.speak("{answer}")')
            sleep(7)
        except:
            f'init.talk.sound.speak("what a dumb question!")'


txt_cmd(f'init.talk.sound.speak("Okay goodbye then !")')
goodbye_dance()




# Close the connection after you're done
close_connection(ssh_client0)
