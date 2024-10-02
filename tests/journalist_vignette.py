# Advanced LobbyView Package Usage Vignette for Investigative Journalism

import os
from dotenv import load_dotenv
import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from matplotlib.gridspec import GridSpec

# Load environment variables and set up LobbyView
env_paths = ["tests/.env", "../../tests/.env"]
for env_path in env_paths:
    load_dotenv(env_path)

LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")
lobbyview = LobbyView(LOBBYVIEW_TOKEN)

# Investigate the Dodd-Frank Wall Street Reform and Consumer Protection Act
# This bill was introduced in the 111th Congress as H.R. 4173

# 1. Get bill information
bill_info = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
bill_data = bill_info.data[0]
print(f"Bill Information: {bill_data['bill_number']} - {bill_data['bill_state']}")

# 2. Get sponsor information
sponsor_info = lobbyview.legislators(legislator_id=bill_data['legislator_id'])
sponsor_data = sponsor_info.data[0]
print(f"\nBill Sponsor: {sponsor_data['legislator_full_name']}")

# 3. Get lobbying data
bill_client_networks = lobbyview.bill_client_networks(congress_number=111, bill_chamber="H", bill_number=4173)

# 4. Analyze top lobbying clients
client_lobby_count = Counter(network['client_uuid'] for network in bill_client_networks)
top_clients = client_lobby_count.most_common(10)

client_names = {}
for client_uuid, _ in top_clients:
    client_info = lobbyview.clients(client_uuid=client_uuid)
    client_names[client_uuid] = client_info.data[0]['client_name']

# 5. Analyze lobbying intensity over time
lobbying_timeline = defaultdict(int)
for network in bill_client_networks:
    report = lobbyview.reports(report_uuid=network['report_uuid']).data[0]
    year = report['report_year']
    quarter = report['report_quarter_code']
    lobbying_timeline[f"{year} Q{quarter}"] += 1

# 6. Analyze issues and government entities
all_issues = []
for network in bill_client_networks:
    issues = lobbyview.issues(report_uuid=network['report_uuid'])
    all_issues.extend(issues.data)

issue_codes = Counter(issue['issue_code'] for issue in all_issues)
gov_entities = []
for issue in all_issues:
    if issue['gov_entity']:
        for entity in issue['gov_entity']:
            if entity:
                gov_entities.append(entity)

gov_entities = Counter(gov_entities)

# 7. Analyze network connections
legislator_connections = defaultdict(int)
for network in lobbyview.networks(client_uuid=top_clients[0][0]):
    legislator_connections[network['legislator_id']] += network['n_bills_sponsored']

top_legislators = sorted(legislator_connections.items(), key=lambda x: x[1], reverse=True)[:5]
legislator_names = {}
for leg_id, _ in top_legislators:
    leg_info = lobbyview.legislators(legislator_id=leg_id)
    legislator_names[leg_id] = leg_info.data[0]['legislator_full_name']

# Create comprehensive visualization
plt.figure(figsize=(20, 20))
gs = GridSpec(3, 2, figure=plt.gcf())

# 1. Lobbying Intensity Over Time
ax1 = plt.subplot(gs[0, :])
sorted_timeline = dict(sorted(lobbying_timeline.items()))
ax1.bar(sorted_timeline.keys(), sorted_timeline.values())
ax1.set_title("Lobbying Intensity Over Time")
ax1.set_xlabel("Year and Quarter")
ax1.set_ylabel("Number of Lobbying Activities")
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha="right")

# 2. Top Lobbying Clients
ax2 = plt.subplot(gs[1, 0])
client_names_list = [client_names[uuid] for uuid, _ in top_clients]
client_counts = [count for _, count in top_clients]
ax2.barh(client_names_list, client_counts)
ax2.set_title("Top 10 Lobbying Clients")
ax2.set_xlabel("Number of Lobbying Activities")
ax2.set_ylabel("Client Name")

# 3. Top Issues Lobbied
ax3 = plt.subplot(gs[1, 1])
top_issues = issue_codes.most_common(10)
ax3.pie([count for _, count in top_issues], labels=[issue for issue, _ in top_issues], autopct='%1.1f%%')
ax3.set_title("Top 10 Issues Lobbied")

# 4. Top Government Entities Lobbied
ax4 = plt.subplot(gs[2, 0])
top_entities = gov_entities.most_common(5)
ax4.bar([entity for entity, _ in top_entities], [count for _, count in top_entities])
ax4.set_title("Top 5 Government Entities Lobbied")
ax4.set_ylabel("Number of Lobbying Activities")
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha="right")

# 5. Top Legislator Connections for Main Lobbying Client
ax5 = plt.subplot(gs[2, 1])
ax5.bar([legislator_names[leg_id] for leg_id, _ in top_legislators], 
        [count for _, count in top_legislators])
ax5.set_title(f"Top 5 Legislator Connections for {client_names[top_clients[0][0]]}")
ax5.set_ylabel("Number of Bills Sponsored")
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha="right")

plt.tight_layout()
plt.savefig("dodd_frank_lobbying_analysis.png")
plt.close()

print("\nA comprehensive analysis of lobbying activity has been saved as 'dodd_frank_lobbying_analysis.png'")

# Journalist's Key Findings
print("\nKey Findings for Investigative Piece:")
print(f"1. The Dodd-Frank Act (H.R. 4173) was sponsored by {sponsor_data['legislator_full_name']}.")
print(f"2. The bill's current state is: {bill_data['bill_state']}")
print(f"3. The most active lobbying client was {client_names[top_clients[0][0]]}, with {top_clients[0][1]} lobbying activities.")
print(f"4. Lobbying activity peaked in {max(lobbying_timeline, key=lobbying_timeline.get)}, with {max(lobbying_timeline.values())} activities.")
print(f"5. The most lobbied issue was '{top_issues[0][0]}', accounting for {top_issues[0][1]} activities.")
print(f"6. The government entity most frequently lobbied was {top_entities[0][0]}, targeted {top_entities[0][1]} times.")
print(f"7. For the top lobbying client, the legislator most frequently connected to sponsored bills was {legislator_names[top_legislators[0][0]]}, with {top_legislators[0][1]} bills.")
