# Air_Route_Optimizer
An intelligent Air Route Optimizer that leverages Dijkstra's algorithm to find the most efficient flight paths based on time, price, or distance. Features an interactive Tkinter GUI and map visualization for clear results.

# Introduction :
The Air Route Optimizer is a desktop application designed to find the most efficient flight paths between given start and end points. It's a powerful tool for travelers and logistics planners, offering intelligent route suggestions based on user-defined priorities.

This project showcases a robust implementation of Dijkstra's algorithm to navigate a network of flight routes, providing three distinct optimization criteria: minimizing travel time, cost (price), or geographical distance. The application features an intuitive graphical user interface (GUI) built with Tkinter for seamless user interaction and integrates map visualization to graphically display the optimized routes.

# Features
# Three-Way Optimization: Users can choose their preferred optimization metric:
    Time: Calculates the fastest route, minimizing total travel duration.
    Price: Identifies the most economical path, minimizing total cost.
    Distance: Determines the geographically shortest route between points.
# Dijkstra's Algorithm Core:
    Implements Dijkstra's shortest path algorithm for efficient and accurate route computation.
# Interactive Map Visualization:
    Dynamically displays the optimized flight path on a map.
    Draws a clear line connecting the start and end points, using their geographical coordinates, providing an intuitive visual representation of the selected route.
# User-Friendly GUI (Tkinter):
    An clean and simple graphical interface built with Python's Tkinter library.
    Allows users to easily input origin/destination, select optimization criteria, and view detailed results.
    Modular Design: The project is structured with clear separation of concerns, making it easy to understand and extend.

# How it Works
# Data Representation: Flight routes and their attributes (time, price, distance) are internally structured as a graph data structure. Airports are represented as nodes (vertices), and flights between them are represented as edges with associated weights.

# User Input:
The Tkinter GUI captures the user's desired departure point, destination, and the chosen optimization type (Time, Price, or Distance).

# Graph Construction:
Based on the input data, a weighted graph is constructed where edge weights correspond to the selected optimization criterion (e.g., if "Time" is chosen, edge weights are flight durations).

# Dijkstra's Execution:
Dijkstra's algorithm is applied to the constructed graph to find the shortest path from the origin node to the destination node, according to the specified weights.

# Result Display: 
The optimal route, including intermediate stops, total optimized value (time, price, or distance), and path details, is presented to the user within the GUI.

# Visual Confirmation: 
The integrated mapping component takes the coordinates of the start and end points of the calculated path and draws a connecting line, providing a clear visual confirmation of the chosen route.

**Author** : Pranav Parsewar
**LinkedIn** : http://www.linkedin.com/in/pranav-parsewar-1a8178220 

<img width="594" height="699" alt="Screenshot 2025-07-30 001404" src="https://github.com/user-attachments/assets/4e1695d0-bceb-448e-af11-87187ed2efbf" />

