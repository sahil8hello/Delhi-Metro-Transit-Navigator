import pandas as pd
import json

def time_to_seconds(t_str):
    h, m, s = map(int, t_str.split(':'))
    return h * 3600 + m * 60 + s

# 1. Load Data
stop_times = pd.read_csv('stop_times.txt')
trips = pd.read_csv('trips.txt')
stop_times = stop_times.merge(trips[['trip_id', 'route_id']], on='trip_id')

# stop_times.to_csv('debug_stop_times.csv', index=False)

# 2. Create unique node identifiers (StationID_RouteID)
stop_times['node_id'] = stop_times['stop_id'].astype(str) + "_" + stop_times['route_id'].astype(str)


# stop_times.to_csv('debug_stop_times.csv', index=False)


# trips_subset = trips[['trip_id', 'route_id']]
# trips_subset = trips_subset.sort_values(['trip_id', 'route_id'])
# # 2. Export that specific subset to a new CSV file
# trips_subset.to_csv('trips_subset.csv', index=False)

# 3. Calculate travel times
stop_times['arrival_s'] = stop_times['arrival_time'].apply(time_to_seconds)
stop_times['departure_s'] = stop_times['departure_time'].apply(time_to_seconds)
stop_times = stop_times.sort_values(['trip_id', 'stop_sequence'])

# stop_times.to_csv('debug_stop_times.csv', index=False)

# 4. Movement on the same line
stop_times['next_node'] = stop_times.groupby('trip_id')['node_id'].shift(-1)
stop_times['next_arr'] = stop_times.groupby('trip_id')['arrival_s'].shift(-1)
stop_times['travel'] = (stop_times['next_arr'] - stop_times['departure_s'])

# stop_times.to_csv('debug_stop_times.csv', index=False)

# 5. Build Graph
graph = {}

# A. Add Travel Edges (Average time between stations on same line)
travel_edges = stop_times.groupby(['node_id', 'next_node'])['travel'].mean().reset_index()
travel_edges.to_csv('debug_.csv', index=False)

for _, row in travel_edges.iterrows():
    u, v, weight = row['node_id'], row['next_node'], round(row['travel'], 2)
    if u not in graph: graph[u] = []
    graph[u].append({"to": v, "weight": weight})

# B. Add Transfer Edges (Switching lines at the same station)
# We find all route_ids present at each stop_id
station_mapping = stop_times.groupby('stop_id')['route_id'].unique()
TRANSFER_PENALTY = 300.0 # sec

for stop_id, routes in station_mapping.items():
    if len(routes) > 1:
        # Create bidirectional transfer edges between all routes at this station
        for i in range(len(routes)):
            for j in range(i + 1, len(routes)):
                node1 = f"{stop_id}_{routes[i]}"
                node2 = f"{stop_id}_{routes[j]}"
                
                if node1 not in graph: graph[node1] = []
                if node2 not in graph: graph[node2] = []
                
                graph[node1].append({"to": node2, "weight": TRANSFER_PENALTY})
                graph[node2].append({"to": node1, "weight": TRANSFER_PENALTY})

# 6. Save to JSON
with open('metro_graph.json', 'w') as f:
    json.dump(graph, f, indent=4)

print("metro_graph.json created with unique route nodes and transfer edges!")