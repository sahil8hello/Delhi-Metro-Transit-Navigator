An optimized pathfinding engine designed for the Delhi Metro rail network. This project provides a bridge between real-world transit data (GTFS) and a high-speed routing solver.

🚀 Overview: 	This project processes raw Delhi Metro transit schedules and constructs a weighted directed graph where nodes represent stations/platforms and edges represent travel times. The routing engine utilizes Dijkstra’s Algorithm implemented in C++ to calculate the shortest path between any two metro stations, accounting for interchange penalties between lines.

🛠 Tech StackData Processing: 	Python, Pandas (for cleaning and structuring GTFS data).Graph Modeling: JSON (for data serialization), Graph Theory (Adjacency List).Routing Engine: C++, STL (std::priority_queue), JSON (nlohmann/json).

🏗 System ArchitectureData Pipeline (Python): 	Parses raw GTFS stop_times.txt and trips.txt files, calculates average segment travel times, and generates a structured metro_graph.json map.Pathfinding Engine (C++): Loads the graph into memory using an efficient Adjacency List and executes Dijkstra's algorithm to provide sub-millisecond route calculation.Logic: Incorporates "Transfer Edges" to accurately model the time cost of switching lines at interchange stations.

⚙️ How to Run1

Data ProcessingEnsure you have the GTFS files in your root directory, then run the Python script:

	Bashpython process_metro.py.
	
Altough Json file is already given.

Compilation: Compile the C++ engine with optimizations: 

	Bashg++ -O3 main.cpp -o metro_app

Execution: 

	Bash./metro_app

📊 Project Highlights: 

	Algorithmic Efficiency: Achieves $O(E \log V)$ complexity by mapping string-based station IDs to integer indices for high-speed computation.
	Domain Modeling: Specifically handles interchange penalties (e.g., 5-minute walk time) by expanding station nodes based on route IDs.
	Extensibility: Easily updatable for future metro line expansions by simply refreshing the GTFS input data.
