# Robot Routing

We're trying to build software to route a robot on a two-dimensional grid layout. The robot can move left, up, right,
or down on the grid. The robot cannot stay in place at any given time, it always needs to move. Each action takes the robot one second. Assume the grid itself is infinite in size
and indexed with larger x coordinates toward the right and larger y coordinates toward the top.

## First Version
We want to return a route that minimizes the number of steps taken by the robot.

#### Example Layout
In the example below, the O indicates the starting point for the robot, and the D indicates the destination.

```
 ____________
|            |
|  O         |
|            |
|        D   |
|____________|
 
```

Here is a route for the robot that minimizes the number of steps taken:

```
 ____________
|            |
|  O......   |
|        .   |
|        D   |
|____________|
 
```

## Obstacles

Now assume there are certain blocked spaces in the grid that the robot cannot traverse over.

### Example Layout
In the example below, the O indicates the starting point for the robot, the D indicates the destination, and
the X's mark barriers.

```
 ____________
|            |
|  O         |
|        X   |
|       XD   |
|____________|
 
```

Here is a route for the robot that minimizes the number of steps taken while avoiding the barriers:

```
 ____________
|            |
|  O.......  |
|        X.  |
|       XD.  |
|____________|
 
```

## Lasers

Assume we have lasers in the maze that point in a particular direction (indicated by a N, E, S, or W). A laser
shoots in its predetermined direction unless/until the laser's shooting path hits an obstacle.

In the example below we have two lasers, one that points east and one that points south.

```
 _____________
|         L   |
|     O   *   |
|        X*   |
|  L****XD*   |
|         *   |
|_________*___|
 
```

Here is a route that avoids the laser beams and obstacles while minimizing the number of steps taken.

```
 _____________
|         L   |
| ....O   *   |
| .      X*   |
| .L****XD*   |
| ........*   |
|_________*___|
 
```

## Rotating Lasers
Now assume the lasers all rotate clockwise every second. Recall that the robot's movements all take exactly one second.
For example, a laser initially pointing south, will point west on the next timestep, then north, then east, then south again.

## Wormholes
Now assume there are certain pairs of coordinates in the grid called "wormholes". They appear every 3 seconds, and they are all initially visible (at t=0).
If the robot walks onto a wormhole space as soon as it appears, it is instantly transported to the partner coordinate.

# I/O
Your program should read in a text file with the following structure:

```
(x_origin, y_origin) # origin coordinate
(x_destination, y_destination) # destination coordinate
[(x_0, y_0), (x_1, y_1), ...] # Barrier coordinates
[(x_0, y_0, d_0), (x_1, y_1, d_1), ...] # Laser coordinates and initial directions
[[(x_00, y_00), (x_01, y_01)],[(x_10, y_10), (x_11, y_11)], ... ] # Wormhole coordinate pairs

```

And you should write out your solution to a file with the following structure:
```
[(x_0, y_0), (x_1, y_1), ..., (x_N, y_N)]
```

If no solution is possible, you should output a file with an empty list.

# Visualization
You can use the visualizer.py script to visualize your robot in action:
```
python visualizer.py problem.txt solution.txt
```

As you build up your solution, you may want to test out the various extensions of the problem. You can pass in a flag to
visualize specific components while testing. For example, if you just want to make sure your solution is respecting barriers:
```
python visualizer.py problem.txt solution_barriers_only.txt --visualize barriers
```

Then later if you get non-rotating lasers as well:
```
python visualizer.py problem.txt solution_static_lasers.txt --visualize barriers static_lasers
```

You can try a sample visualization:
```
python visualizer.py sample/problem.txt sample/solution.txt --visualize rotating_lasers barriers
```

Press 'n' to advance forward in time and 'b' to go back. Press 'q' to quit.
