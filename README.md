# MPycomm

Python Library with helper scripts for Yaskawa MPiec controllers and Compass G-Code Testing

Installation:
Clone the repo into your desired working folder with:

```
$ git clone https://github.com/plebied-yaskawa/MPycomm.git
```

Navigate to the working folder and create your own python script or edit the main.py

Basic usage ofthe Compass G-Code Creater is shown below:

First, import the correct scripts and create an ArcGen class with the basic constructors:

```
from scripts.generator.Generator import ArcGen

gen = ArcGen()
gen.segmentQueue.append('G0 X0 Y0')
gen.coordinateQueue.append([0, 0, 0])

gen.createPolygon(15, 100)
gen.segmentQueue.append(gen.reverseQueue(1,15))
gen.writeFile('basicexample')
```

This will create the G-Code file necesarry for a polygon of N=15 sides of length 100. The polygon will be drawn twice:
(1) - counter-clockwise 
(2) - clockwise
The reverseQueue method is used to take the pre-existing line segments and run them in reverse.

