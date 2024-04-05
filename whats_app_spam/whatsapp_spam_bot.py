# whatas app spam bot

import os
import time
import pyautogui
import keyboard

# This function Wait for pressing enter from the user

def wait_for_enter():

    while True:
        end_loop = 0
        if keyboard.is_pressed('enter'):
            end_loop = 1
        if end_loop == 1:
            break
    return

# To send limited number of messages 

def limited_number_messages(target_no_of_message):
	no_of_messages = 0
	print("press enter to start")
	wait_for_enter()
	for i in range(10):
		os.system("cls")
		print(f"open whatsapp window with in {10-i} sec")
		time.sleep(1)
	while True:
		pyautogui.hotkey('ctrl','v')
		time.sleep(0)
		pyautogui.hotkey('enter')
		no_of_messages += 1
		os.system("cls")
		print(f"number of messages sent - {no_of_messages}")
		print("───▄▄▄\n─▄▀░▄░▀▄\n─█░█▄▀░█\n─█░▀▄▄▀█▄█▄▀\n▄▄█▄▄▄▄███▀")
		target_no_of_message -= 1
		if keyboard.is_pressed('esc'):
			os.system("cls")
			print("\n\n───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───\n───█▒▒░░░░░░░░░▒▒█───\n────█░░█░░░░░█░░█────\n─▄▄──█░░░▀█▀░░░█──▄▄─\n█░░█─▀▄░░░░░░░▄▀─█░░█")
			print(f"number of messages sent - {no_of_messages}")
			print('LOOP IS BREAKED PRESS ENTER TO CLOSE')
			wait_for_enter()
			break
		if target_no_of_message == 0:
			os.system("cls")
			print("\n\n───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───\n───█▒▒░░░░░░░░░▒▒█───\n────█░░█░░░░░█░░█────\n─▄▄──█░░░▀█▀░░░█──▄▄─\n█░░█─▀▄░░░░░░░▄▀─█░░█")
			print(f"number of messages sent - {no_of_messages}")
			print("PRESS ENTER TO CONTINUE :")
			wait_for_enter()
			break
	pass

# This function to send unlimited messages 

def unlimided_messages():
	no_of_messages = 0
	print("messages will be sent till you press 'esc'")
	print("press enter to start")
	wait_for_enter()
	for i in range(10):
		os.system("cls")
		print(f"open whatsapp window with in {10-i} sec")
		time.sleep(1)
	while True:
		pyautogui.hotkey('ctrl','v')
		time.sleep(0)
		pyautogui.hotkey('enter')
		no_of_messages += 1
		os.system("cls")
		print("───▄▄▄\n─▄▀░▄░▀▄\n─█░█▄▀░█\n─█░▀▄▄▀█▄█▄▀\n▄▄█▄▄▄▄███▀")
		print(f"number of messages sent - {no_of_messages}")
		if keyboard.is_pressed('esc'):
			os.system("cls")
			print("───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───\n───█▒▒░░░░░░░░░▒▒█───\n────█░░█░░░░░█░░█────\n─▄▄──█░░░▀█▀░░░█──▄▄─\n█░░█─▀▄░░░░░░░▄▀─█░░█")
			print(f"number of messages sent - {no_of_messages}")
			print('LOOP IS BREAKED')
			input("PRESS ENTER TO CONTINUE :")
			wait_for_enter()
			break

	pass
# this function to get target from the user to send how many number of messages to be send

def get_target():
	time.sleep(1)
	target = input("if you have any target for number of messages to be sent entet 'Y' or 'N' :")
	target = target.lower()
	return target

def ask_for_rerun():
	while True:
		os.system("cls")
		request = input("do you want to run again? entet 'y' or 'n' :")
		request.lower()
		if request == 'y' or request == 'n':
			return request
		else:
			print("please enter the correct values")


# just for decorations

os.system("cls")
print("\n█░░░█ █░░█ █▀▀█ ▀▀█▀▀ █▀▀ █▀▀█ █▀▀█ █▀▀█ 　 █▀▀ █▀▀█ █▀▀█ █▀▄▀█ 　 █▀▀▄ █▀▀█ ▀▀█▀▀ \n█▄█▄█ █▀▀█ █▄▄█ ░░█░░ ▀▀█ █▄▄█ █░░█ █░░█ 　 ▀▀█ █░░█ █▄▄█ █░▀░█ 　 █▀▀▄ █░░█ ░░█░░ \n░▀░▀░ ▀░░▀ ▀░░▀ ░░▀░░ ▀▀▀ ▀░░▀ █▀▀▀ █▀▀▀ 　 ▀▀▀ █▀▀▀ ▀░░▀ ▀░░░▀ 　 ▀▀▀░ ▀▀▀▀ ░░▀░░")
time.sleep(1)
print("\n\n█▀▀ █▀▀█ █▀▀ █▀▀█ ▀▀█▀▀ █▀▀ █▀▀▄ 　 █▀▀▄ █──█ \n█── █▄▄▀ █▀▀ █▄▄█ ──█── █▀▀ █──█ 　 █▀▀▄ █▄▄█ \n▀▀▀ ▀─▀▀ ▀▀▀ ▀──▀ ──▀── ▀▀▀ ▀▀▀─ 　 ▀▀▀─ ▄▄▄█")
print("\n░█████╗░██████╗░░█████╗░██╗░░░██╗██╗███╗░░██╗██████╗░\n██╔══██╗██╔══██╗██╔══██╗██║░░░██║██║████╗░██║██╔══██╗\n███████║██████╔╝███████║╚██╗░██╔╝██║██╔██╗██║██║░░██║\n██╔══██║██╔══██╗██╔══██║░╚████╔╝░██║██║╚████║██║░░██║\n██║░░██║██║░░██║██║░░██║░░╚██╔╝░░██║██║░╚███║██████╔╝\n╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝╚═╝░░╚══╝╚═════╝░\n")

# working logic

while True:
	target = get_target()
	if target == "y":
		targer_to_send = int(input("enter the how many messages to be send: "))
		limited_number_messages(targer_to_send)
		rerun = ask_for_rerun()
	elif target == "n":
		unlimided_messages()
		rerun = ask_for_rerun()
	else:
		os.system("cls")
		print("Please enter 'y' or 'n' :")
		target = get_target()
	if rerun != 'y':
		os.system('cls')
		print("\n\n▀▀█▀▀ █░░█ █▀▀█ █▀▀▄ █░█ █░░█ █▀▀█ █░░█ \n░░█░░ █▀▀█ █▄▄█ █░░█ █▀▄ █▄▄█ █░░█ █░░█ \n░░▀░░ ▀░░▀ ▀░░▀ ▀░░▀ ▀░▀ ▄▄▄█ ▀▀▀▀ ░▀▀▀")
		break