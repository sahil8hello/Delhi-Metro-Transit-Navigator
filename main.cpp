#include<bits/stdc++.h>
#include "json.hpp"

using json = nlohmann::json;
using namespace std;

const double INF = numeric_limits<double>::infinity();

struct Edge {
    int to;
    double weight;
};

// Global structures
unordered_map<string, int> nameToIndex;
unordered_map<int, string> indexToName;
vector<vector<Edge>> adj;

int main() {
    // 1. Load JSON
    ifstream f("metro_graph.json");
    json data = json::parse(f);

    // 2. Map string IDs to Integers
    int idCounter = 0;
    for (auto& [node, edges] : data.items()) {
        if (nameToIndex.find(node) == nameToIndex.end()) {
            nameToIndex[node] = idCounter;
            indexToName[idCounter] = node;
            idCounter++;
        }
    }
    adj.resize(idCounter);

    // 3. Build Adjacency List
    for (auto& [node, edges] : data.items()) {
        int u = nameToIndex[node];
        for (auto& edge : edges) {
            string target = edge["to"];
            if (nameToIndex.find(target) == nameToIndex.end()) continue;
            int v = nameToIndex[target];
            adj[u].push_back({v, (double)edge["weight"]});
        }
    }

    // 4. Dijkstra's Algorithm
    string startNode = "109_23"; // Change as needed
    string endNode = "136_10";   // Change as needed

    int start = nameToIndex[startNode];
    int end = nameToIndex[endNode];

    vector<double> dist(idCounter, INF);
    vector<int> parent(idCounter, -1);
    priority_queue<pair<double, int>, vector<pair<double, int>>, greater<pair<double, int>>> pq;

    dist[start] = 0;
    pq.push({0, start});

    while (!pq.empty()) {
        double d = pq.top().first;
        int u = pq.top().second;
        pq.pop();

        if (d > dist[u]) continue;
        if (u == end) break;

        for (auto& edge : adj[u]) {
            if (dist[u] + edge.weight < dist[edge.to]) {
                dist[edge.to] = dist[u] + edge.weight;
                parent[edge.to] = u;
                pq.push({dist[edge.to], edge.to});
            }
        }
    }

    // 5. Output Results
    if (dist[end] == 0) {
        cout << "No path found." << endl;
    } else {
        cout << "Shortest time: " << dist[end]/60 << " minutes" << endl;
        vector<string> path;
        for (int at = end; at != -1; at = parent[at]) path.push_back(indexToName[at]);
        reverse(path.begin(), path.end());
        
        cout << "Path: ";
        for (const string& s : path) cout << s << " -> ";
        cout << "END" << endl;
    }

    return 0;
}