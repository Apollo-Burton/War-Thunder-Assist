import pyautogui as pag
from playsound import playsound
import time
import math

time.sleep(1)

# =========================================================================================================================================================================
# USER CONFIGURATION

# =========================================================================================================================================================================
# IMPORTANT

sound_path = "C:\\Users\\User\\Downloads\\mixkit-alarm-tone-996.wav"

# "sound_path" is telling the program where the sound file is on your computer. If you installed "mixkit-alarm-tone-996.wav" file from github, "sound_path" should be 
# "C:\\Users\\User\\Downloads\\mixkit-alarm-tone-996.wav". "User" SHOULD BE YOUR ACCOUNT NAME ON WINDOWS, if not, it won't work. If you want to use your own audio file,
# make sure you have the path correct. If you don't know how to check the path of a file, open file explorer, navigate to your audio file, then double click the bar at the top
# with a list of the files you have gonne through. For example, it might look something like this: > This PC > Windows (C:) > Users > User > Downloads
# copy and paste it to "sound_path", add a backslash to the end, and type your file name. 
# Make sure to double the backslashes: (C:\Users\User\Downloads\file.mp3 -> C:\\Users\\User\\Downloads\\file.mp3)
# =========================================================================================================================================================================

top_left = (1730, 125)
bottom_right = (1850, 190)
center_of_circle = (1785, 125)
radius_of_circle = 65

color_in_rgb = (190, 190, 30)
color_range = 20
timer = 1

# "top_left" and "bottom_right" are the top left and bottom right corners of the box the program will search in x and y coordinates. The "radius_of_circle" and "center_of_circle" 
# are used to trim the edges of the box to fit the minimap. Changing these too much either make the circle too big or too small, so I don't recommend changing them.
# These x and y coordinates are set for a 1080p monitor, i'm working on a fix so that it automatically fits to all monitors with different pixel counts (1440p, 2160p, etc)

# Change "color_in_rgb" to set the rgb value you will be looking for.

# Change "color_range" to change the accuracy. If it is set to "0", the program will only look for the exact value of "color_in_rgb". If it is set higher, it will look for colors
# similar to "color_in_rgb". this is helpful when the color you are looking for is part of a gradient or if it slightly changes over time. The higher "color_range" is set, the
# less accurate the program will be. For example, if "color_in_rgb" is (50, 50, 50), and "color_range" is 50, then any color from (0, 0, 0) to (99, 99, 99) will be detected.
# I recommend setting "color_range" to 20 or less, as setting it too high will make the program very innacurate.

# "timer" controls how long you want the program to run in minutes.
# =========================================================================================================================================================================


def get_colors(color: tuple[int, int, int], rgb_range: int, center: tuple[int, int], radius: int):
    screen = pag.screenshot()
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
                if rgb[0] >= color[0] - rgb_range and rgb[0] <= color[0] + rgb_range and rgb[1] >= color[1] - rgb_range and rgb[1] <= color[1] + rgb_range and rgb[2] >= color[2] - rgb_range and rgb[2] <= color[2] + rgb_range:
                    playsound(sound_path)
                    return True
    return False

print("Program running...")

runtime = time.time() + 60 * timer
while time.time() <= runtime:
	get_colors(color_in_rgb, color_range, center_of_circle, radius_of_circle)

print("Program finished")
