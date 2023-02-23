import pyautogui as pag
from playsound import playsound
import time

time.sleep(1)

# =========================================================================================================================================================================
# USER CONFIGURATION

top_left = (1720, 125)
bottom_right = (1845, 175)

color_range = 20
color_in_rgb = (190, 190, 30)
timer = 1

# "top_left" and "bottom_right" are the top left and bottom right corners of the box the program will search. The two numbers in parentheses are x and y coordinates
# on your screen. These are already set to the lower half of the War Thunder air battles minimap, and if you are using this script for War Thunder, I don't recommend changing
# them.

# Change "color_in_rgb" to set the rgb value you will be looking for.

# Change "color_range" to change the accuracy. If it is set to "0", the program will only look for the exact value of "color_in_rgb". If it is set higher, it will look for colors
# similar to "color_in_rgb". this is helpful when the color you are looking for is part of a gradient or if it slightly changes over time. The higher "color_range" is set, the
# less accurate the program will be. For example, if "color_in_rgb" is (50, 50, 50), and "color_range" is 50, then any color from (0, 0, 0) to (99, 99, 99) will be detected.
# I recommend setting "color_range" to 20 or less, as setting it too high will make the program very innacurate.

# "timer" controls how long you want the program to run in minutes.

# To see debug info, go to line 37 and remove the hashtag. This will make the program slower
# =========================================================================================================================================================================


def get_colors(color: tuple[int, int, int], rgb_range: int):
	screen = pag.screenshot()
	for pixelx in range(bottom_right[0] - top_left[0]):
		for pixely in range(bottom_right[1] - top_left[1]):
			#print([top_left[0] + pixelx, top_left[1] + pixely], screen.getpixel((top_left[0] + pixelx, top_left[1] + pixely)))
			rgb = screen.getpixel((top_left[0] + pixelx, top_left[1] + pixely))
			if rgb[0] >= color[0] - rgb_range and rgb[0] <= color[0] + rgb_range and rgb[1] >= color[1] - rgb_range and rgb[1] <= color[1] + rgb_range and rgb[2] >= color[2] - rgb_range and rgb[2] <= color[2] + rgb_range:
				playsound("C:\\Users\\User\\Desktop\\Programs\\mixkit-alarm-tone-996.wav")
				print("Color found")
				return True
	return False

print("Starting...")

runtime = time.time() + 60 * timer
while time.time() <= runtime:
	get_colors(color_in_rgb, color_range)

print("Program finished")
