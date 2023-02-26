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

mute = "right_ctrl + right_shift"

# "mute" controls the hotkey that mutes the alert for 10 seconds. It is currently set to right control + right shift, but you can change it to whatever you want. Plain keys 
# are just reprented by their letter. So if you wanted your keybind to be "m", you would make mute: mute = "m". and if you wanted it to be 5 you would make mute: mute = "5".
# If you wanted to make mute m and 5 you would make mute: mute = "m + 5"

timer = 1

# "timer" controls how long you want the program to run in minutes. "timer = 5" means that the program will run for 5 minutes.
# ==============================================================================================================================================================================

top_left = (1735, 125)
bottom_right = (1850, 190)
center_of_circle = (1785, 120)
radius_of_circle = 65

# "top_left" and "bottom_right" are the top left and bottom right corners of the box the program will search in x and y coordinates. The "radius_of_circle" and 
# "center_of_circle" are used to trim the edges of the box to fit the minimap. Changing these too much either make the circle too big or too small, so I don't 
# recommend changing them. These x and y coordinates are set for a 1080p monitor, I wrote some code between line 60 and line 80 that should scale the coordinates with
# resolution, but I have literally no way of testing it, so just pray that it works.

debug = True

# To see debug info, change "debug" to "True"
# ==============================================================================================================================================================================

import pyautogui as pag
from playsound import playsound
import keyboard
import tkinter
import time
import math

# Scaling coordinates with monitor resolution
root = tkinter.Tk()
root.withdraw()
xpixels, ypixels = root.winfo_screenwidth(), root.winfo_screenheight()

new_top_leftx = top_left[0] / 1080 * ypixels
new_top_lefty = top_left[1] / 1080 * ypixels
new_top_left = (int(new_top_leftx), int(new_top_lefty))

new_bottom_rightx = bottom_right[0] / 1080 * ypixels
new_bottom_righty = bottom_right[1] / 1080 * ypixels
new_bottom_right = (int(new_bottom_rightx), int(new_bottom_righty))

new_center_of_circlex = center_of_circle[0] / 1080 * ypixels
new_center_of_circley = center_of_circle[1] / 1080 * ypixels
new_center_of_circle = (int(new_center_of_circlex), int(new_center_of_circley))

new_radius_of_circle = int(radius_of_circle / 1080 * ypixels)

time.sleep(1)

# get_colors() function; the main function for this program
def get_colors(center: tuple[int, int], radius: int, debug: bool = False):
	screen = pag.screenshot()
	matches = [0]
	continue_range = range(0)
	# Looping through the bbox
	for pixelx in range(int((new_bottom_right[0] - new_top_left[0]) / 1080 * ypixels)):
		# Skipping 10 iterations if a match is found, this is to prevent multiple matches on the same enemy
		if pixelx in continue_range:
			continue
		for pixely in range(int((new_bottom_right[1] - new_top_left[1]) / 1080 * ypixels)):
			# Setting x and y
			x = new_top_left[0] + pixelx
			y = new_top_left[1] + pixely
			# Calculating distance between pixel and center using the pythagorean thereom
			distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
			# Checking if pixel is within the radius of the minimap
			if distance <= radius:
				# Checking if the pixel is in the color_range
				rgb = screen.getpixel((x, y))
				rgb_in_range = rgb[0] >= 170 and rgb[2] <= 60
				if rgb_in_range:
					# Checking if the program is picking up ground clutter or not. If the program detects more than 3 enemies in one call, it is most likely detecting ground clutter
					matches.append((x, y))
					matches[0] += 1
					if debug:
						print(f"Match found: matches = {matches[0]}")
						print(f"The current iteration is: {pixely}\n")
					continue_range = range(pixelx + int(10 / 1080 * ypixels))
					if matches[0] >= 4:
						return False
					break
	# If the program didn't detect any ground clutter, and an enemy was found:
	if matches[0] >= 1:
		skip_condition = False
		# If the program detected only one enemy, don't check if points are spread apart
		if matches[0] == 1:
			skip_condition = True
		# Running checks to see if the points are spread apart. If they are clumped together, it is probably ground clutter
		if skip_condition or (abs(matches[-1][0] - matches[-2][0]) > 50 and abs(matches[-1][1] - matches[-2][1]) > 50):
			playsound(sound_path)
			# Provide debug information if the user wants it
			if debug:
				print(f"Matches = {matches}")
				print(f"Enemy found at {matches[1:]}, setting off alarm\n")
			return True
	return False


# Main program loop
def start_program():
	print("Program running...")

	runtime = time.time() + 60 * timer
	while time.time() <= runtime:
		get_colors(new_center_of_circle, new_radius_of_circle, debug)
		# Detect if user has muted the alert
		if keyboard.is_pressed(mute):
			print("Muted for 10 seconds")
			time.sleep(10)
			print("Continuing program")

	print("Program finished")

start_program()
