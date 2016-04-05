SHAREROBOT
==========

Run (Web Interface)
-------------------

1. Make sure Python v2.7 has installed. <small>On windows, make sure your directory containing `python.exe` in `PATH`.
</small>
2. Pull source to your machine and `cd` into the source folder.
3. Start the web server. Run `python server.py` (On Linux or Mac). Run `start.bat` (On Windows).
4. Click the following links from a web browser (Chrome is recommend) to see results.

### [Chapter 5](http://localhost:8000/c5.py)

Known skill mapping. This will print out a list of matching result between `sr_p`s in `states.json` and pre/post in `skills.json`.

Unknown skill generate. This will generate a new skill to a json file `skills_create.json`.

### [Chapter 6](http://localhost:8000/c6.py)

This will read a skill in `skills.json` (See Note 2) and use this skill to tell a real world Robot how to do. As a simulation, this program returns a Gantt Graph to show the schedule of the operations that the **"real"** robot done.

**Note 1** that press <kbd>F5</kbd> again and again can simulate the situations that same skill applies on
robots with different architecture in different environments.

**Note 2**
By default, the program using `skills_create.json` (generated from `Chapter 5`) instead of `skill.json`. So You need run `Chapter 5` first before run `Chapter 6` if you never run it before.
