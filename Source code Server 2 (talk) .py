{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
from ev3dev2.sound import Sound\
import random as rnd\
from ev3dev2.display import Display\
\
\
sound=Sound()\
display=Display()\
\
def display_text(text):\
    display.text_pixels(text, True, 10, 10, 'black', None)\
\
\
vocal_list_okay = ["Of course,sir","All Right", "Lets do it", "At your service, sir", "As you wish", "Yes, sir, ", "Okay then","Lets go", "Anything you ask", "Il be glad to, sir", "Please", "Sir, yes Sir!"]\
\
def talk_okay(text=None):\
    if text is None:\
\
        to_say=vocal_list_okay[rnd.randint(0,len(vocal_list_okay)-1)]\
    else:\
        to_say=text\
\
    sound.speak(to_say)\
    display_text(to_say)\
\
\
vocal_list_ready=["Ready to take action at your commandment, sir", "Waiting for your call", "Its your call sir", "What shall i do now, sir ?", "I am waiting for your instructions,sir"]\
\
def talk_ready(text=None):\
    if text is None:\
        to_say=vocal_list_ready[rnd.randint(0,len(vocal_list_ready)-1)]\
    else:\
        to_say=text\
\
    display_text(to_say)\
    sound.speak(to_say)\
\
\
vocal_list_didnt_understand=["I did not get what your saying please articulate!", "Sorry,sir can you repeat?", "Well, i did not get what youre saying !", "Repeat please, I did not understand !"]\
\
def talk_didnt_understand(text=None):\
\
    if text is None:\
\
        to_say=vocal_list_didnt_understand[rnd.randint(0,len(vocal_list_didnt_understand)-1)]\
    else:\
        to_say=text\
\
    sound.speak(to_say)\
    display_text(to_say)\
\
\
\
\
\
\
def play_music():\
\
	sound.play_song((\
    	('D4', 'e3'),\
    	('D4', 'e3'),\
    	('D4', 'e3'),\
    	('G4', 'h'),\
    	('D5', 'h')\
	))\
\
\
\
\
def elephant_sound(sound_nb="0"):\
	rand_nb=rnd.randint(2,3)\
	print(rand_nb)\
	file_name="elephant" +str(rand_nb)+ ".wav"\
	sound.play_file(file_name)\
}