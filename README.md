# Python_Portfolio
**Python Portfolio Assessment**

The program simulates agents/'Nibblers' which exist atop a DTM converted into a two-dimensional environment. The nibblers execute a number of tasks based on random chance such as: eating/grazing the environment beneath them, sharing stored food with one another, excreting back to the environment, moving randomly, independently aging and slowing down with age, and even reproducing when certain requirements are met.

While currently simple the framework exists within this model to build into real-world simulations such as bacteria cultures or floral growth.

The model is displayed using MatPlotLib on a graph with iterations played rapidly as the TKInter animation. The .py files are fully commented for developers to further understand and alter the code.

**File and their Contents**

  **A4GUIModel.py**
Contained within this model is:
  - imports for matplotlib animation and pyplot, tkinter, beautifulsoup, and requests.
  - An error catcher for troubleshooting.
  - Web scrapping code and parser.
  - Defines the models variables i.e. number of agents, iterations, etc...
  - User changeable variables controlling the agents interactions.
  - Functions controlling the model i.e. run, stop, etc...
  - Animation system which updates frames/iterations using tkinter.
  - Nested if/else statements which calls functions from the A4Agentframework
  - Plotting code which displays the agents and the environment in a graph format.
  - Code which determines the GUI.

  **A4agentframework**
  - Defines the agents class and assigns attributes when the program is initialised.
  - Defines a full set of functions passed to A4GUImodel when called which control the agents behavior i.e. move, eat, age,  die, etc...

  **A4environments_reader**
  - A function which reads in and appends the environments1.csv to the model when called in A4GUImodel.

  **environments1.csv**
  - This file contains a altitude data/a dtm for an area used in the model as the environment for the agents to iteract with.

  **Running the Software**
The software can be run in Python which will open a simple GUI with the options to run or stop the model. Beginning the model will place the agents randomly and then track the community as they execute activities with one another. As generations are born, age, and die eventually there will not be enough food to sustain the group or they will simply due out naturally. The software can be stopped at any point using "Stop Model" in the GUI.

  **Further Development**
While this model is simple the framework exists to improve upon the agents behaviour to model other real-world things such as bacteria. Depending on the scope a developer could add additional behaviours, change the environment to other locations, layer the environments to have the agents interact with multiple properties of the environment (altitude and slope for example). A potential idea would be using this model as the groundwork to model small floral ecosystems. 
