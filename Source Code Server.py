{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, MediumMotor, OUTPUT_D\
from ev3dev2.sensor.lego import TouchSensor, ColorSensor\
from ev3dev2.sensor import INPUT_1,INPUT_4\
from math import log2, exp\
import threading\
import random as rand\
 \
\
from time import sleep\
\
import talk\
\
\
\
#Motors:\
motor1=LargeMotor(OUTPUT_A)\
motor2=LargeMotor(OUTPUT_B)\
motor3=MediumMotor(OUTPUT_D)\
\
#Sensors\
button=TouchSensor(INPUT_1)\
Col_Sensor=ColorSensor(INPUT_4)\
\
\
	\
def walk(speed=100, time=5):\
	motor1.on(speed)\
	sleep(time)\
\
	motor1.stop()\
\
\
\
\pard\pardeftab720\sa240\partightenfactor0
\cf0 \expnd0\expndtw0\kerning0
def head(speed=40, repetitions=3, factor=1):\
	if speed < 0:\
		speed = -speed\
	for i in range(repetitions):\
		if Col_Sensor.color == 5: #security (reset initial position if getting in the sensor range)\
			motor3.on_for_degree(100, 90, brake=True, block=True) \
	motor3.on_for_degrees(speed, -450, brake=True, block=True)\
	motor3.on_for_degrees(speed, 450, brake=True, block=True)\
	if Col_Sensor.color == 5: #security (reset initial position if getting in the sensor range)\
		motor3.on_for_degrees(100, 60, brake=True, block=True)
\f1 \
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0 \cf0 \kerning1\expnd0\expndtw0 \
\
\
def head_waiting(speed=20, repetitions=5):\
	for i in range(repetitions):\
		motor3.on(speed)\
		sleep(1.5)\
		motor3.stop()\
		sleep(0.6)\
		motor3.on(-speed*0.8)\
		sleep(1.3)\
		motor3.on(speed*1.2)\
		sleep(1)\
		motor3.on(-speed)\
		while Col_Sensor.color!=5:\
			sleep(0.1)\
	motor3.stop()\
\
\
def trunk_loop(speed=15, repetitions=5):\
\
    if speed <0:\
        speed = -speed\
    for i in range(repetitions):\
	if button.is_pressed == 1:  # Security purpose, reset initial position if button is touched\
        		motor2.on_for_degrees(speed, 60, brake=True, block=True)\
	motor2.on_for_degrees(speed, 600, brake=True, block=True)  # Move down the trunk until almost the end\
	motor2.on_for_degrees(speed, -600, brake=True, block=True)  # Move up again\
	if button.is_pressed == 1:  # Security purpose, reset initial position if button is touched\
		motor2.on_for_degrees(speed, 60, brake=True, block=True)\
\
\
def trunk_loop_half(speed=15, repetitions=5):\
	if speed <0:\
		speed = -speed\
	for i in range(repetitions):\
		if button.is_pressed == 1:  # Security purpose, reset initial position if button is touched\
        			motor2.on_for_degrees(speed, 60, brake=True, block=True)\
	motor2.on_for_degrees(speed, 350, brake=True, block=True)  # Move down the trunk until almost the end\
	motor2.on_for_degrees(speed, -350, brake=True, block=True)  # Move up again\
	if button.is_pressed == 1:  # Security purpose, reset initial position if button is touched\
		motor2.on_for_degrees(speed, 60, brake=True, block=True)\
\
def trunk(low_speed=30):\
	if low_speed > 50:\
		low_speed = 50\
	make_sound = threading.Thread(target=talk.elephant_sound)\
	mv_head = threading.Thread(target=head, args=(100, 1))\
\
	if low_speed < 0:\
		low_speed = -low_speed\
\
	if button.is_pressed == 1:  # Security purpose, reset initial position if button is touched\
        		motor2.on_for_degrees(speed, 60, brake=True, block=True)\
\
	motor2.on_for_degrees(low_speed, 400, brake=True, block=True)  # Move down the trunk until almost the end\
	sleep(1)\
	mv_head.start()\
	make_sound.start()\
	sleep(0.8)\
	motor2.on_for_degrees(low_speed * 2, 400, brake=True, block=True)\
	if button.is_pressed == 1:  # Security purpose, reset initial position if button is touched\
        		motor2.on_for_degrees(speed, 60, brake=True, block=True)\
	make_sound.join()\
	mv_head.join()\
\
\
def progressive_walk(speed=100, time=10):\
\
	for i in range(time*4):\
		motor1.on(i*4)\
		sleep(0.25)\
\
\
\
def is_waiting_trunk(low_speed, repetitions=3):\
	if low_speed>65:\
		low_speed=65\
\
	fast_speed=low_speed*1.2\
	for i in range(repetitions):\
		if waiting_status==False:\
			return\
		motor2.on(-low_speed) #1\
		motor2.stop()\
		sleep(0.3)\
		motor2.on(low_speed-10) #2\
		sleep(0.8)\
		motor2.on(-low_speed*1.2) #3\
		while button.is_pressed==0:\
			sleep(0.05)\
		motor2.on(low_speed) #4\
		sleep(1.5)\
\
		while button.is_pressed==0:\
			motor2.on(-fast_speed)\
			sleep(0.1)\
		motor2.stop()\
	motor2.stop()\
\
\
def is_waiting_legs(speed=15, repetitions=5):\
	for i in range (repetitions):\
		if waiting_status==False:\
			return\
		motor1.on(-speed)\
		sleep(0.7)\
		motor2.stop()\
		sleep(0.4)\
		motor1.on(speed-5)\
		sleep(0.5)\
		motor1.on(-speed+5)\
		sleep(0.5)\
		motor1.on(speed)\
		sleep(0.7)\
	motor1.stop()\
	\
\
def is_waiting(speed=8, repetitions=2):\
	waiting_status=True\
	if speed<4:\
		speed=4\
	walk_mov=threading.Thread(target=is_waiting_legs, args=(speed+3,repetitions))\
	head_mov=threading.Thread(target=head, args=(speed-3,repetitions,2))\
	trunk_move=threading.Thread(target=is_waiting_trunk, args=(speed, repetitions))\
	trunk_move.start()\
	head_mov.start()\
	walk_mov.start()\
	\
	trunk_move.join()\
	head_mov.join()\
	walk_mov.join()\
\
\
def is_angry_legs(time=5,intensity=100, trim=0.25):\
	for i in range (time*2):\
                motor1.on(intensity)\
                sleep(trim)\
                motor1.on(-intensity)\
                sleep(trim)\
	motor1.stop()\
\
def is_angry(time=5, intensity=100, trim=0.25, sound="0"):\
	thread2 = threading.Thread(target=head,args=(intensity, time))\
	thread1 = threading.Thread(target=trunk_loop_half, args=(intensity, 3))\
	thread3 = threading.Thread(target=is_angry_legs, args=(time, intensity,trim))\
	thread4 = threading.Thread(target=talk.elephant_sound, args=(sound))\
	thread1.start()\
	thread2.start()\
	thread3.start()\
	thread4.start()\
	thread1.join()\
	thread2.join()\
	thread3.join()\
	thread4.join()\
				\
\
\
\
#overide\
def perform_all(walk_sp=100, head_sp=50, trunk_sp=30, time=20, pause_head=0, pause_trunk=0, sequences=0, sq_pause=1):\
	remaining_seq = sequences +1\
	sq_time = (time / (sequences+1)) - sequences*sq_pause #calcute real time considering the pause and sequences\
\
	thread1 = threading.Thread(target=walk, args=(-walk_sp, sq_time))\
	thread2=threading.Thread(target=head,args=(head_sp, 5))\
	thread3 = threading.Thread(target=trunk_loop, args=(trunk_sp, 3))\
	thread4=threading.Thread(target=talk.elephant_sound)\
	thread1.start()\
\
	for i in range(sequences+1):\
		while remaining_seq>=1:\
\
			while thread1.is_alive():\
				if not thread2.is_alive():\
					sleep(pause_head)\
					thread2=threading.Thread(target=head,args=(head_sp, 1))\
					thread2.start() #restart head movement when it is finished, with an optional pause\
				if not thread3.is_alive():\
					sleep(pause_trunk)\
					thread3 = threading.Thread(target=trunk_loop_half, args=(trunk_sp, 3))\
					thread3.start()\
				if not thread4.is_alive():\
					thread4=threading.Thread(target=talk.elephant_sound)\
					thread4.start()\
\
		\
			sleep(sq_pause) #pause between each sequence\
			thread1 = threading.Thread(target=walk, args=(-walk_sp, sq_time))\
			thread1.start()\
			remaining_seq=remaining_seq-1\
		\
		\
	thread1.join()\
	thread2.join()\
	thread3.join()\
	thread4.join()\
	stop() #finish all movements when stopping walking\
\
def rand_speed():\
	return random.randint(14,100)\
\
\
\
def walk_all_random(walk_speed):\
	thread2=threading.Thread(target=head,args=(rand_speed(), 5))\
	thread1 = threading.Thread(target=trunk_loop, args=(rand_speed(), 3))\
	thread3 = threading.Thread(target=walk, args=(walk_speed, 5))\
	thread1.start()\
	thread2.start()\
	thread3.start()\
	thread1.join()\
	thread2.join()\
	thread3.join()\
\
#utilities:\
\
def stop(motors="all"):\
	if motors=="1" or motors=="all" :\
		motor1.stop()\
	if motors=="2" or motors=="all":\
		motor2.stop()\
	if motors=="3" or motors=="all":\
		motor3.stop()\
}