from threading import Thread
import time
import pdb
from gpiozero import Button
from signal import pause


# Idee https://stackoverflow.com/questions/75178435/python-event-handler-for-background-task-complete


menu = 0

def say_16():
	global menu
	menu = 16
	#print("Btn 16")

def say_20():
	global menu
	menu = 20
	#print("Btn 20")

def say_21():
	global menu
	menu = 21
	#print("Btn 21")

def read_buttons():
	global menu
	btn16 = Button(16, pull_up=False)
	btn20 = Button(20, pull_up=False)
	btn21 = Button(21, pull_up=False)

	btn16.when_released = say_16
	btn20.when_released = say_20
	btn21.when_released = say_21

	while True:
		time.sleep(1)		
		pause() 

def main():
	global menu

	button_thread = Thread(target=read_buttons, daemon=True)
	button_thread.start()

	i=0
	print("start main")
	while True:
		#pdb.set_trace()
		if (menu > 0) :
			print("Menu: ", menu)
			menu = 0
		time.sleep(1)

if __name__ == "__main__":
	main()

