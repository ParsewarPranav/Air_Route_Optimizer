import tkinter as tk
from tkinter import messagebox, ttk
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from gmplot import gmplot
import webbrowser

# Dijkstra's algorithm
def dijkstra(graph, start, end, metric):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    shortest_path = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight_dict in graph[current_node].items():
            weight = weight_dict[metric]
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_path[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, shortest_path

# Function to reconstruct the shortest path
def reconstruct_path(shortest_path, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = shortest_path[end]
    path.reverse()
    return path

# Function to visualize the graph
def visualize_graph(graph, path, start, end, metric):
    G = nx.DiGraph()

    for node, neighbors in graph.items():
        for neighbor, weight_dict in neighbors.items():
            G.add_edge(node, neighbor, weight=weight_dict[metric])

    pos = nx.spring_layout(G)

    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, alpha=0.5, edge_color='black')  # Default edge color

    # Highlight the shortest path
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='green')  # Highlighted path edges

    nx.draw_networkx_labels(G, pos, font_size=16, font_family="sans-serif")

    edge_labels = {(u, v): f"{G[u][v]['weight']} {metric}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(f"Shortest path from {start} to {end} based on {metric}")
    plt.show()

# Function to dynamically adjust the zoom level based on distance
def adjust_zoom(distance):
    if distance < 500:
        return 10  # Zoom level for shorter distances
    elif distance < 1000:
        return 7   # Mid-level zoom
    else:
        return 5   # Lower zoom for longer distances

# Function to visualize the path on Google Maps
def visualize_on_google_maps(path, distances, start, end, metric):
    # Coordinates for the cities (you can replace these with the actual coordinates)
    coordinates = {
        'Mumbai': (19.0902, 72.8628),
        'Delhi': (28.5561, 77.1000),
        'Bangalore': (13.1989, 77.7069),
        'Kolkata': (22.6536, 88.4451),
        'Chennai': (12.9822, 80.1642),
        'Hyderabad': (17.2403, 78.4294),
        'Pune': (18.5793, 73.9089),
    }

    # Extract the latitude and longitude for the path
    lats, lons = zip(*[coordinates[city] for city in path])

    # Your API key
    api_key = '***********************'  # Replace with your actual API key

    # Adjust zoom level dynamically based on distance
    zoom_level = adjust_zoom(distances[end])

    # Create the map plotter
    gmap = gmplot.GoogleMapPlotter(lats[0], lons[0], zoom_level, apikey=api_key)

    # Plot the path with a distinct color and line thickness
    gmap.plot(lats, lons, color='darkred', edge_width=5, alpha=0.8)

    # Mark the start and end points with green and red markers
    gmap.marker(lats[0], lons[0], 'green', title=f'Start: {path[0]}')  # Starting point
    gmap.marker(lats[-1], lons[-1], 'red', title=f'End: {path[-1]}')    # Ending point

    # Add markers for waypoints along the route
    for lat, lon in zip(lats[1:-1], lons[1:-1]):
        gmap.marker(lat, lon, 'blue', title="Waypoint")

    # Draw the map and save it to an HTML file
    filename = "shortest_path_map.html"
    gmap.draw(filename)

    # Automatically open the HTML file in the default web browser
    webbrowser.open(filename)

    messagebox.showinfo("Result", f"Google Maps visualization saved as '{filename}' and opened in your browser.")

# Function to handle the submit button
def submit():
    loading_label.pack(pady=10)  # Show loading indicator
    window.update()  # Update the window to show loading message

    start_airport = start_airport_combobox.get()
    end_airport = end_airport_combobox.get()
    metric_choice = metric_var.get()

    if start_airport not in graph or end_airport not in graph:
        loading_label.pack_forget()  # Hide loading label
        messagebox.showerror("Error", "Invalid airport code entered. Please try again.")
        return

    metric_map = {'1': 'distance', '2': 'time', '3': 'cost'}
    metric = metric_map.get(metric_choice)

    if not metric:
        loading_label.pack_forget()  # Hide loading label
        messagebox.showerror("Error", "Invalid metric choice. Please try again.")
        return

    distances, shortest_path = dijkstra(graph, start_airport, end_airport, metric)
    path = reconstruct_path(shortest_path, start_airport, end_airport)

    loading_label.pack_forget()  # Hide loading label

    if distances[end_airport] == float('infinity'):
        messagebox.showinfo("Result", f"No available route from {start_airport} to {end_airport}.")
    else:
        result = (f"Shortest path from {start_airport} to {end_airport} based on {metric}: {path}\n"
                  f"Total {metric}: {distances[end_airport]} {metric}")
        messagebox.showinfo("Result", result)
        visualize_graph(graph, path, start_airport, end_airport, metric)
        visualize_on_google_maps(path, distances, start_airport, end_airport, metric)

# Graph data (Updated to include all airports)
graph = {
    'Mumbai': {'Delhi': {'distance': 1148, 'time': 145, 'cost': 4352},
               'Bangalore': {'distance': 842, 'time': 110, 'cost': 3188},
               'Kolkata': {'distance': 1652, 'time': 170, 'cost': 4450},
               'Chennai': {'distance': 1029, 'time': 115, 'cost': 5130},
               'Hyderabad': {'distance': 623, 'time': 75, 'cost': 3300},
               'Pune': {'distance': 118, 'time': 60, 'cost': 1050}},
    'Delhi': {'Mumbai': {'distance': 1148, 'time': 150, 'cost': 4200},
              'Bangalore': {'distance': 1740, 'time': 165, 'cost': 5000},
              'Kolkata': {'distance': 1305, 'time': 130, 'cost': 5015},
              'Chennai': {'distance': 1756, 'time': 170, 'cost': 6500},
              'Hyderabad': {'distance': 1253, 'time': 130, 'cost': 4050},
              'Pune': {'distance': 1173, 'time': 125, 'cost': 6291}},
    'Bangalore': {'Mumbai': {'distance': 842, 'time': 100, 'cost': 3200},
                  'Delhi': {'distance': 1740, 'time': 170, 'cost': 5200},
                  'Kolkata': {'distance': 1561, 'time': 155, 'cost': 4300},
                  'Chennai': {'distance': 284, 'time': 70, 'cost': 1200},
                  'Hyderabad': {'distance': 560, 'time': 90, 'cost': 2200},
                  'Pune': {'distance': 731, 'time': 95, 'cost': 2800}},
    'Kolkata': {'Mumbai': {'distance': 1652, 'time': 180, 'cost': 4700},
                'Delhi': {'distance': 1305, 'time': 140, 'cost': 5200},
                'Bangalore': {'distance': 1561, 'time': 175, 'cost': 4500},
                'Chennai': {'distance': 1694, 'time': 165, 'cost': 6700},
                'Hyderabad': {'distance': 792, 'time': 100, 'cost': 3200},
                'Pune': {'distance': 1694, 'time': 165, 'cost': 6700}},
    'Chennai': {'Mumbai': {'distance': 1029, 'time': 115, 'cost': 5130},
                'Delhi': {'distance': 1756, 'time': 170, 'cost': 6500},
                'Bangalore': {'distance': 284, 'time': 70, 'cost': 1200},
                'Kolkata': {'distance': 1694, 'time': 165, 'cost': 6700},
                'Hyderabad': {'distance': 630, 'time': 90, 'cost': 3100},
                'Pune': {'distance': 1000, 'time': 120, 'cost': 5000}},
    'Hyderabad': {'Mumbai': {'distance': 623, 'time': 75, 'cost': 3300},
                  'Delhi': {'distance': 1253, 'time': 130, 'cost': 4050},
                  'Bangalore': {'distance': 560, 'time': 90, 'cost': 2200},
                  'Kolkata': {'distance': 792, 'time': 100, 'cost': 3200},
                  'Chennai': {'distance': 630, 'time': 90, 'cost': 3100},
                  'Pune': {'distance': 711, 'time': 100, 'cost': 3400}},
    'Pune': {'Mumbai': {'distance': 118, 'time': 60, 'cost': 1050},
             'Delhi': {'distance': 1173, 'time': 125, 'cost': 6291},
             'Bangalore': {'distance': 731, 'time': 95, 'cost': 2800},
             'Kolkata': {'distance': 1694, 'time': 165, 'cost': 6700},
             'Chennai': {'distance': 1000, 'time': 120, 'cost': 5000},
             'Hyderabad': {'distance': 711, 'time': 100, 'cost': 3400}},
}

# Create the main window
window = tk.Tk()
window.title("Airport Route Finder")
window.geometry("400x500")

# Create and place the labels and comboboxes
tk.Label(window, text="Select Start Airport:").pack(pady=10)
start_airport_combobox = ttk.Combobox(window, values=list(graph.keys()), state="readonly")
start_airport_combobox.pack(pady=10)

tk.Label(window, text="Select End Airport:").pack(pady=10)
end_airport_combobox = ttk.Combobox(window, values=list(graph.keys()), state="readonly")
end_airport_combobox.pack(pady=10)

tk.Label(window, text="Select Metric:").pack(pady=10)
metric_var = tk.StringVar(value='1')  # Default value
tk.Radiobutton(window, text="Distance", variable=metric_var, value='1').pack(pady=5)
tk.Radiobutton(window, text="Time", variable=metric_var, value='2').pack(pady=5)
tk.Radiobutton(window, text="Cost", variable=metric_var, value='3').pack(pady=5)

# Create the submit button
submit_button = tk.Button(window, text="Submit", command=submit)
submit_button.pack(pady=20)

# Loading indicator
loading_label = tk.Label(window, text="Processing...", fg="blue")

# Start the GUI loop
window.mainloop()
