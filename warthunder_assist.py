# ==============================================================================================================================================================================
# USER CONFIGURATION

# ==============================================================================================================================================================================
# IMPORTANT

sound_path = "C:\\Users\\User\\Desktop\\Programs\\alert.wav"

# "sound_path" is telling the program where the sound file is on your computer. If you installed "alert.wav" file from github, "sound_path" should be 
# "C:\\Users\\User\\Downloads\\alert.wav". "User" SHOULD BE YOUR ACCOUNT NAME ON WINDOWS, if not, it won't work. If you want to use your own audio file,
# make sure you have the path correct. If you don't know how to check the path of a file, then open file explorer, navigate to your audio file, then double click the bar 
# at the top with a list of the files you have gone through. For example, it might look something like this: > This PC > Windows (C:) > Users > User > Downloads
# copy and paste it to "sound_path", add a backslash to the end, and type your file name. 
# Make sure to double the backslashes: (C:\Users\User\Downloads\file.mp3 -> C:\\Users\\User\\Downloads\\file.mp3)
# ==============================================================================================================================================================================

top_left = (1735, 125)
bottom_right = (1850, 190)
center_of_circle = (1785, 120)
radius_of_circle = 65

# "top_left" and "bottom_right" are the top left and bottom right corners of the box the program will search in x and y coordinates. The "radius_of_circle" and 
# "center_of_circle" are used to trim the edges of the box to fit the minimap. Changing these too much either make the circle too big or too small, so I don't 
# recommend changing them. These x and y coordinates are set for a 1080p monitor, i'm working on a fix so that it automatically fits to all monitors with 
# different pixel counts (1440p, 2160p, etc).

color_in_rgb = (180, 60, 50)

# Change "color_in_rgb" to set the rgb value you will be looking for.

color_range = 10

# Change "color_range" to change the accuracy. If it is set to "0", the program will only look for the exact value of "color_in_rgb". If it is set higher, it will look for 
# colors similar to "color_in_rgb". this is helpful when the color you are looking for is part of a gradient or if it slightly changes over time. The higher "color_range" 
# is set, the less accurate the program will be. For example, if "color_in_rgb" is (50, 50, 50), and "color_range" is 50, then any color from (0, 0, 0) to (99, 99, 99) 
# will be detected. If you do change this, I recommend setting "color_range" to 20 or less, as setting it too high will make the program innacurate.

timer = 1

# "timer" controls how long you want the program to run in minutes. "timer = 5" means that the program will run for 5 minutes.

debug = False

# To see debug info, change "debug" to "True"

mute = "rctrl + rshift"

# "mute" controls the hotkey that mutes the alert for 10 seconds. It is currently set to right control + right shift, but you can change it to whatever you want. Plain keys 
# ==============================================================================================================================================================================

import pyautogui as pag
from playsound import playsound
import keyboard
import time
import math

time.sleep(1)
matches = []
def get_colors(color: tuple[int, int, int], rgb_range: int, center: tuple[int, int], radius: int):
	screen = pag.screenshot()
	# Allowing modification of the top_left and bottom_right variables
	global top_left
	global bottom_right
	for pixelx in range(bottom_right[0] - top_left[0]):
		for pixely in range(bottom_right[1] - top_left[1]):
			# Setting x and y
			x = top_left[0] + pixelx
			y = top_left[1] + pixely
			# Calculating distance between pixel and center using the pythagorean thereom
			distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
			# Checking if pixel is within the radius
			if distance <= radius:
				# Checking if the pixel is in the color_range
				rgb = screen.getpixel((x, y))
				matches.append([[x, y], rgb])
				if rgb[0] >= color[0] - rgb_range and rgb[0] <= color[0] + rgb_range and rgb[1] >= color[1] - rgb_range and rgb[1] <= color[1] + rgb_range and rgb[2] >= color[2] - rgb_range and rgb[2] <= color[2] + rgb_range:
					playsound(sound_path)
					# Provide debug information if the user wants it
					if debug == True:
						print(f"The current bbox coords are {top_left}, {bottom_right}")
					# Only scan the area the color was found, both to speed up the program by reducing iterations and improve accuracy
					top_left = (x - 20, y - 20)
					bottom_right = (x + 20, y + 20)
					# provide debug information if the user wants it
					if debug == True:
						print(f"RGB value: {rgb} found at {x}, {y}. Moving bbox to {top_left}, {bottom_right}")
						print(f"The bbox coords are now {top_left}, {bottom_right}\n")
					return True
	# Reset bbox if nothing is found
	top_left = (1735, 125)
	bottom_right = (1850, 190)
	return False


# Main program loop
print("Program running...")

runtime = time.time() + 60 * timer
while time.time() <= runtime:
	get_colors(color_in_rgb, color_range, center_of_circle, radius_of_circle)
	# Detect if user has muted the alert
	if keyboard.is_pressed(mute):
		print("Muted for 10 seconds")
		time.sleep(10)
		print("Continuing program")

print("Program finished")
