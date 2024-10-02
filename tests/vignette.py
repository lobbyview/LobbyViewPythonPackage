# LobbyView Package Usage Vignette
# Investigating a Bill Using LobbyView

import os
from dotenv import load_dotenv

import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

# Load environment variables and set up LobbyView
env_paths = ["tests/.env", "../../tests/.env"]
for env_path in env_paths:
    load_dotenv(env_path)

LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")

lobbyview = LobbyView(LOBBYVIEW_TOKEN)

# Import necessary libraries
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.gridspec import GridSpec

# Let's investigate the Dodd-Frank Wall Street Reform and Consumer Protection Act
# This bill was introduced in the 111th Congress as H.R. 4173

# 1. Get information about the bill
bill_info = lobbyview.bills(congress_number=111, bill_chamber="H", bill_number=4173)
print("Bill Information:")
print(bill_info)

# 2. Get information about the bill's sponsor
sponsor_id = bill_info.data[0]['legislator_id']
sponsor_info = lobbyview.legislators(legislator_id=sponsor_id)
print("\nBill Sponsor Information:")
print(sponsor_info)

# 3. Find clients who lobbied on this bill
bill_client_networks = lobbyview.bill_client_networks(congress_number=111, bill_chamber="H", bill_number=4173)
client_names = {lobbyview.clients(client_uuid=network['client_uuid']).data[0]['client_name'] for network in bill_client_networks}
print("\nClients who lobbied on this bill:")
for client_name in client_names:
    print(f"- {client_name}")

# 4. Get detailed information about one of the clients (let's use the first one)
client_uuid = bill_client_networks.data[0]['client_uuid']
client_details = lobbyview.clients(client_uuid=client_uuid)
print("\nDetailed Client Information:")
print(client_details)

# 5. Get reports filed by this client
client_reports = lobbyview.reports(client_uuid=client_uuid, max_report_quarter_code=4)
print("\nReports filed by the client:")
print(client_reports)

# 6. Get issues mentioned in these reports
all_issues = []
for report in client_reports:
    report_issues = lobbyview.issues(report_uuid=report['report_uuid'])
    all_issues.extend(report_issues.data)

# 7. Get network information for this client
client_networks = lobbyview.networks(client_uuid=client_uuid)
print("\nNetwork information for the client:")
print(client_networks)

# 8. Get quarter-level network information
quarter_networks = lobbyview.quarter_level_networks(client_uuid=client_uuid, max_report_quarter_code=4)
print("\nQuarter-level network information:")
print(quarter_networks)

# Create a comprehensive visualization
plt.figure(figsize=(20, 15))
gs = GridSpec(3, 3, figure=plt.gcf())

# 1. Reports per year
ax1 = plt.subplot(gs[0, :2])
report_years = [report['report_year'] for report in client_reports]
year_counts = Counter(report_years)
ax1.bar(year_counts.keys(), year_counts.values())
ax1.set_title("Reports Filed per Year")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Reports")

# 2. Top 10 most frequent issues
ax2 = plt.subplot(gs[0, 2])
issue_codes = [issue['issue_code'] for issue in all_issues]
top_issues = Counter(issue_codes).most_common(10)
ax2.barh([code for code, _ in top_issues], [count for _, count in top_issues])
ax2.set_title("Top 10 Most Frequent Issues")
ax2.set_xlabel("Count")
ax2.set_ylabel("Issue Code")

# 3. Network activity over time
ax3 = plt.subplot(gs[1, :])
years = [network['report_year'] for network in client_networks]
bills_sponsored = [network['n_bills_sponsored'] for network in client_networks]
ax3.plot(years, bills_sponsored, marker='o')
ax3.set_title("Network Activity Over Time")
ax3.set_xlabel("Year")
ax3.set_ylabel("Number of Bills Sponsored")

# 4. Quarterly network activity heatmap
ax4 = plt.subplot(gs[2, :2])
quarter_data = {}
for network in quarter_networks:
    year = network['report_year']
    quarter = int(network['report_quarter_code'])
    bills = network['n_bills_sponsored']
    if year not in quarter_data:
        quarter_data[year] = [0, 0, 0, 0]
    if 1 <= quarter <= 4:  # Ensure quarter is within valid range
        quarter_data[year][quarter-1] = bills
    else:
        print(f"Warning: Unexpected quarter value {quarter} for year {year}")

years = sorted(quarter_data.keys())
data = [quarter_data[year] for year in years]
im = ax4.imshow(data, cmap='YlOrRd', aspect='auto')
ax4.set_title("Quarterly Network Activity")
ax4.set_xlabel("Quarter")
ax4.set_ylabel("Year")
ax4.set_yticks(range(len(years)))
ax4.set_yticklabels(years)
ax4.set_xticks(range(4))
ax4.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
plt.colorbar(im, ax=ax4, label="Bills Sponsored")

# 5. Pie chart of government entities lobbied
ax5 = plt.subplot(gs[2, 2])
gov_entities = [entity for issue in all_issues for entity in issue['gov_entity']]
entity_counts = Counter(gov_entities).most_common(5)
ax5.pie([count for _, count in entity_counts], labels=[entity for entity, _ in entity_counts], autopct='%1.1f%%')
ax5.set_title("Top 5 Government Entities Lobbied")

plt.tight_layout()
plt.savefig("lobbying_analysis.png")
plt.close()

print("\nA comprehensive analysis of lobbying activity has been saved as 'lobbying_analysis.png'")
