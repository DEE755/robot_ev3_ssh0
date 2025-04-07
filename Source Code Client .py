{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import paramiko\
from time import sleep\
import speech_recognition as sr\
import keyz\
#UI\
import tkinter as tk\
from tkinter import Toplevel\
from UI import user_interface\
\
from openai import OpenAI\
\
import numpy as np\
\
class SpeakNowPopup(Toplevel):\
    def __init__(self, parent):\
        super().__init__(parent)\
        self.title("Speak Now")\
        self.label = tk.Label(self, text="Speak with Dumbot", font=("Helvetica", 16))\
        self.label.pack(pady=20, padx=20)\
        self.protocol("WM_DELETE_WINDOW", self.on_close)\
\
    def on_close(self):\
        self.destroy()\
\
def show_speak_now_popup(root):\
    popup = SpeakNowPopup(root)\
    popup.attributes('-topmost', True)  # Make the popup window stay on top\
    root.update()\
    return popup\
\
def close_popup_after(popup, delay):\
    def close():\
        popup.destroy()\
    popup.after(delay * 1000, close)  # Schedule the close function to run after the delay\
\
\
\
def speech_to_text():\
\
    root = tk.Tk()\
    root.withdraw()  # Hide the root window\
\
    popup = show_speak_now_popup(root)\
    close_popup_after(popup, 5)  # Close after 5 seconds\
\
    # Use the microphone as the source for input\
    with sr.Microphone() as source:\
        while True:\
            print("Please say something:")\
\
            audio = recognizer.listen(source)\
            #analysing a sample of one second for smart threesholding\
            #audio_test_sample = recognizer.listen(source, phrase_time_limit=0.5)  # Capture audio for 1 second\
            audio_frame_data= np.frombuffer(audio.frame_data, dtype=np.int16)\
            average_gain = np.mean(np.abs(audio_frame_data))\
            print(f"Average gain: \{average_gain\}")\
\
\
\
            if average_gain > 750:  # Check if the average gain is above the threshold\
                break\
\
            else:\
                print(f"Energy threshold is: 500 and average gain is: \{average_gain\}")\
                print("Audio energy below threshold, continue listening...")\
                natural_moves()\
\
    try:\
        # Recognize speech using Google Web Speech API\
        text = recognizer.recognize_google(audio)\
        print("You said: " + text)\
        return text\
    except sr.UnknownValueError:\
        print("Sorry, I could not understand.")\
        return "not_understand"\
    except sr.RequestError as e:\
        print("Could not request results; \{0\}".format(e))\
\
# Initialize recognizer\
recognizer = sr.Recognizer()\
\
# Initialize the GUI in a separate thread\
def start_gui():\
    root = user_interface.root  # Assuming user_interface.root is your Tkinter window\
    label = user_interface.label  # Assuming there's a label in the UI\
\
    # Use root.after to schedule the update on the main thread\
    root.after(0, update_label, label)  # Update label text using after() method\
\
    root.mainloop()\
\
def update_label(label):\
    # Update the label text on the main thread\
    label.config(text="Hello, World!")\
\
\
def open_ai(prompt):\
    context=("You are a robot elephant,Dumbot, programmed by your master, Dorian, "\
             "for a student project. You can go forward, backward, move your trunk or head, make elephant noise and speak if we ask you with the words 'go back' and 'go forward', 'go for a walk', 'move your trunk', 'move your head'. "\
             "You can answer to any question about anything. Be funny sometimes. Make a short and concise answer. "\
             "Dont use any punctuation except for dots or '!', dont use any smiley or any character that is not basic ascii. "\
             "Also don't use any ' for exemple instead of writing 'don't' write 'dont', etc"\
\
             #"Your favorite moto is 'I am Dumbot, but I am not so dumb! As you can see I love talking!'"\
             )\
    client = OpenAI(\
    api_key=keyz.keey\
    )\
\
    completion = client.chat.completions.create(\
    model="gpt-4o-mini",\
    store=True,\
    messages=[\
        \{"role": "user", "content": f" context: \{context\}, Prompt: \{prompt\}"\}\
    ]\
    )\
\
    return completion.choices[0].message.content\
\
\
def import_python(path_without_extension):\
    return txt_cmd("import " + path_without_extension)\
\
\
def create_ssh_client(host, port, username, password):\
    """Create and return an SSH client"""\
    ssh_client = paramiko.SSHClient()\
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add the server's host key\
    ssh_client.connect(hostname=host, port=port, username=username, password=password)\
    return ssh_client\
\
def create_interactive_shell(ssh_client):\
    """Create and return an interactive SSH shell"""\
    return ssh_client.invoke_shell()\
\
def send_command(cmd, interactive_shell):\
    """Send a command to the interactive shell"""\
    interactive_shell.send(cmd + '\\n')  # Send the command to the interactive shell\
    sleep(0.5)  # Wait for the command to execute\
    return interactive_shell.recv(1024).decode()\
\
def close_connection(ssh_client):\
    """Close the SSH connection"""\
    ssh_client.close()\
\
\
\
\
print("Connecting via SSH to the robot")\
host = 'ev3dev.local'\
username = 'robot'\
password = 'maker'\
port = 22  # Default SSH port\
\
# Create SSH client\
ssh_client0 = create_ssh_client(host, port, username, password)\
\
# Open interactive shell once\
shell = create_interactive_shell(ssh_client0)\
\
def txt_precmd(cmd, interactive_shell=shell):\
    """Run a bash command and print the result"""\
    result = send_command(cmd, interactive_shell)\
    print(result)\
\
def txt_cmd(cmd, interactive_shell=shell):\
    """Run a bash command and print the result"""\
    result = send_command("init." + cmd, interactive_shell)\
    print(result)\
\
def txt_cmd_answer(cmd, interactive_shell=shell):\
    """Run a bash command and print the result"""\
    result = send_command(cmd, interactive_shell)\
    print(result)\
    if "True" in result:\
        return True\
    else:\
        return False\
\
def take_action(m_action):\
    #txt_cmd("waiting_status=False")\
    if m_action == "forward":\
        txt_cmd("perform_all(100,25,25, 18, 1, 1, 4,2)")  # walk_speed, trunk_speed, head_speed, total_time, pause_head=0, pause_trunk=0, sequences=0, sq_pause=1\
    elif m_action == "backward":\
        txt_cmd("perform_all(-100,25,25, 25, 1, 1, 4,2)")\
    elif m_action == "stop":\
        txt_cmd("stop()")\
    elif m_action == "trunk":\
        txt_cmd("trunk()")\
    elif m_action == "head":\
        txt_cmd("head()")\
\
def request_routing(request):\
    if ("start" in request) or ("go for a walk" in request) or ("walk" in request) or ("go forward" in request):\
        txt_cmd('talk.sound.speak("im going forward")')\
        action = "forward"\
        take_action(action)\
    elif "go back" in request:\
        txt_cmd('talk.sound.speak("im going backward")')\
        action = "backward"\
        take_action(action)\
\
    elif "stop"in request:\
        action = "stop"\
        take_action(action)\
    elif "move your trunk"  in request or "move your trunk" in request or "mobile trunk" in request:\
        action = "trunk"\
        txt_cmd('talk.sound.speak("of course sir!")')\
        take_action(action)\
\
    elif "move your head" in request:\
        action = "head"\
        take_action(action)\
    else:\
        print("regular talk")\
        return 0\
    return 1\
\
def goodbye_dance():\
    txt_cmd("is_angry()")\
\
def natural_moves():\
    txt_precmd("thread=init.threading.Thread(target=init.is_waiting)")\
    txt_precmd("thread.start()")\
\
# Run commands using the same interactive shell\
txt_precmd("cd dee_project")\
txt_precmd("python3")\
txt_precmd("import init")\
txt_precmd("thread=init.threading.Thread(target=init.is_waiting)")\
txt_precmd("thread.start()")\
txt_cmd("talk.talk_ready()")\
\
\
sleep(15)\
request = ""\
\
\
\
\
\
while "stop talking" not in request:\
\
    natural_moves()\
    request = speech_to_text() # Use speech recognition\
\
\
    if request == "not_understand":\
        natural_moves()\
        txt_cmd('talk.talk_didnt_understand()')\
\
    elif request_routing(request) == 1:\
        sleep(5)\
        continue  # It was an action the function handled it\
    else:\
        print(f"trying to reach text-to-speech-API with request: \{request\}")\
        natural_moves()\
        try:\
            print("tryopenai")\
            answer = open_ai(request)\
            print(f"answer from the API: \{answer\}")\
            txt_cmd(f'talk.sound.speak("\{answer\}")')\
            sleep(7)\
        except Exception as e:\
            txt_cmd('talk.sound.speak("what a dumb question!")')\
            print(f"exceptopenai: \{e\}")\
\
txt_cmd('talk.sound.speak("Okay goodbye then !")')\
goodbye_dance()\
\
txt_cmd("stop()")\
\
sleep(20)\
\
# Close the connection after you're done\
close_connection(ssh_client0)\
}