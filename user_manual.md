The program is designed to have a saved CSV file with the program where relative paths are used. Best used with Visual Studio Code; open as a folder, as it has Relative Paths in the Integrated Terminal for Python

The ToDo app is designed to help students organise their tasks and focus on them.

It is split into 3 main tabs

1. The Dashboard
2. The Task Manager
3. The timer

##### Dashboard:

The dashboard is to keep track of the overall progress; it displays the percentage of overall completed tasks with a progress bar

##### The task manager:

* The task manager is the largest and most important component of the program
* In here, the user can either add a new task or interact with existing tasks
* The user can input a title to describe the task, choose a colour-coded priority(choosing from low, medium or high) to indicate urgency and choose a due date. Once done, click “Add”, and the task will be saved in the table and the CSV file
* \*Note that the chosen due date cannot be in the past or more than 360 days in the future.
* Once their is a few tasks saved up, they are able to mark one done just by double-clicking on it. 
* To delete the task, click the task to highlight it and click Delete (user can delete multiple tasks at once by Ctrl+left click)
* The tasks can be sorted; the selected category will be put on top. The sorting categories are “Name” (alphabetical), “Due Date”, “Highest Priority”, “Lowest Priority”, “Completed” and “Incomplete.” 
* The user can import a previously saved CSV file by clicking Import and choosing a file from their directory; note that it must be in the same format as the CSV file provided
* If the user wants to use the program on a different device without losing the saved tasks, they click Export and create a copy of the file to a location on their disk, if they choose.

##### Timer:

* The timer is created so that the user can focus on doing their tasks
* The user can input their desired time in the format HH:mm:ss; hours, minutes, then seconds. The program will run input longer than 60 seconds; for example, 00:00:70 will be converted to 00:01:10, 1 minute and 10 seconds.
* Once the time is input, the user can run the program by clicking Start. The timer will count down from the inputted time.
* The user cannot change the time while the timer is running, only when it’s finished or Skip is clicked. If the user wants to go back to the same countdown, they can click Restart, then the Start button. Note that Restart goes to the last run countdown time
* 

