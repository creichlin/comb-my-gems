comb my gems
============

this tool clicks like a maniac, combining gems for *GemCraft2: Chasing Shadows*

there is a tool for windows which does it in a much better and friendlier way: https://github.com/gemforce-team/wGemCombiner/

recipes for gems can be found here: https://github.com/gemforce-team/gemforce/tree/master/results

they have to be updated in the combmygems.py file on line 5

on line 6 the delay value can be decreased. i need a big delay because my computer is pretty slow

to do the actual clicking some tool called xdotool (sudo apt-get install xdotool) is used

there are probably plenty of bugs, it's not properly tested.

usage
-----
  
  * copy your preferred gem recipe to line 5
  * open a console, get the focus
  * move the mousecursor over the lowest, rightest slot of your gemventory
  * don't touch the mouse anymore and start the python script with your keyboard
