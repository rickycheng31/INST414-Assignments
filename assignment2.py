import requests
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

drivers = []
for year in range(1950, 2022):
    response = requests.get(f'http://ergast.com/api/f1/{year}/driverStandings.json')
    standings = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    for driver in standings:
        if 'wins' in driver:
            drivers.append({
                'driverId': driver['Driver']['driverId'],
                'familyName': driver['Driver']['familyName'],
                'nationality': driver['Driver']['nationality'].strip(),
                'season': year,
                'wins': int(driver['wins']),
            })

drivers = pd.DataFrame(drivers)

G = nx.Graph()
win_to_drivers = {}
for _, row in drivers.iterrows():
    driver_id = row['driverId']
    wins = row['wins']
    
    if wins > 0:
        G.add_node(driver_id, label=row['familyName'], type='driver', wins=wins)
        
        if wins in win_to_drivers:
            # Connect this driver to all other drivers with the same number of wins
            for other_driver_id in win_to_drivers[wins]:
                G.add_edge(driver_id, other_driver_id)
            
            win_to_drivers[wins].append(driver_id)
        else:
            win_to_drivers[wins] = [driver_id]

plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, seed=42)  # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=500)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

plt.axis('off')
plt.show()
