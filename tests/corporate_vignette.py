# LobbyView Package Usage Vignette for Corporate Strategy
# Analyzing Lobbying Landscape for a Tech Company

import os
from dotenv import load_dotenv
import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView

import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.gridspec import GridSpec

# Load environment variables and set up LobbyView
env_paths = ["tests/.env", "../../tests/.env"]
for env_path in env_paths:
    load_dotenv(env_path)

LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")
lobbyview = LobbyView(LOBBYVIEW_TOKEN)

# 1. Start with a known client: Microsoft Corporation
client_name = "Microsoft Corporation"
client_info = lobbyview.clients(client_name=client_name)

if not client_info.data:
    print(f"No data found for {client_name}")
    sys.exit(1)

client_uuid = client_info.data[0]['client_uuid']
print(f"Analyzing lobbying activities for {client_name}")

# 2. Get reports for this client
client_reports = lobbyview.reports(client_uuid=client_uuid)
print(f"Number of reports found: {len(client_reports.data)}")

# 3. Analyze report years and quarters
report_years = Counter()
report_quarters = Counter()
for report in client_reports.data:
    report_years[report['report_year']] += 1
    report_quarters[report['report_quarter_code']] += 1

print("\nReports by year:")
for year, count in report_years.most_common():
    print(f"  {year}: {count}")

print("\nReports by quarter:")
for quarter, count in report_quarters.most_common():
    print(f"  Q{quarter}: {count}")

# 4. Analyze network data
network_data = lobbyview.networks(client_uuid=client_uuid)
print(f"\nNumber of network connections: {len(network_data.data)}")

legislator_counter = Counter()
for network in network_data.data:
    legislator_counter[network['legislator_id']] += network['n_bills_sponsored']

print("\nTop 5 legislators by bills sponsored:")
for legislator_id, count in legislator_counter.most_common(5):
    legislator_info = lobbyview.legislators(legislator_id=legislator_id)
    if legislator_info.data:
        legislator_name = legislator_info.data[0]['legislator_full_name']
        print(f"  {legislator_name}: {count}")

# 5. Analyze recent bills
recent_bills = lobbyview.bills(min_introduced_date="2020-01-01")
print(f"\nNumber of bills introduced since 2020: {len(recent_bills.data)}")

bill_sponsors = Counter()
for bill in recent_bills.data:
    bill_sponsors[bill['legislator_id']] += 1

print("\nTop 5 bill sponsors since 2020:")
for legislator_id, count in bill_sponsors.most_common(5):
    legislator_info = lobbyview.legislators(legislator_id=legislator_id)
    if legislator_info.data:
        legislator_name = legislator_info.data[0]['legislator_full_name']
        print(f"  {legislator_name}: {count}")

# Create visualization
plt.figure(figsize=(15, 15))
gs = GridSpec(2, 2, figure=plt.gcf())

# 1. Reports by Year
ax1 = plt.subplot(gs[0, 0])
years, counts = zip(*sorted(report_years.items()))
ax1.bar(years, counts)
ax1.set_title(f"Lobbying Reports by Year for {client_name}")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Reports")

# 2. Reports by Quarter
ax2 = plt.subplot(gs[0, 1])
quarters, counts = zip(*sorted(report_quarters.items()))
ax2.bar(quarters, counts)
ax2.set_title(f"Lobbying Reports by Quarter for {client_name}")
ax2.set_xlabel("Quarter")
ax2.set_ylabel("Number of Reports")

# 3. Top Legislators by Bills Sponsored
ax3 = plt.subplot(gs[1, 0])
top_legislators = dict(legislator_counter.most_common(10))
ax3.bar(top_legislators.keys(), top_legislators.values())
ax3.set_title(f"Top Legislators for {client_name} by Bills Sponsored")
ax3.set_xlabel("Legislator ID")
ax3.set_ylabel("Number of Bills Sponsored")
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha="right")

# 4. Top Bill Sponsors (Recent Bills)
ax4 = plt.subplot(gs[1, 1])
top_sponsors = dict(bill_sponsors.most_common(10))
ax4.bar(top_sponsors.keys(), top_sponsors.values())
ax4.set_title("Top Bill Sponsors (Since 2020)")
ax4.set_xlabel("Legislator ID")
ax4.set_ylabel("Number of Bills Sponsored")
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha="right")

plt.tight_layout()
plt.savefig("microsoft_lobbying_analysis.png")
plt.close()

print("\nA comprehensive analysis of Microsoft's lobbying activities has been saved as 'microsoft_lobbying_analysis.png'")

# Corporate Strategy Insights
print("\nKey Insights for Corporate Lobbying Strategy:")
print(f"1. {client_name} has been involved in {len(client_reports.data)} lobbying reports.")
print(f"2. The company has {len(network_data.data)} network connections with legislators.")
most_active_year = report_years.most_common(1)[0][0]
print(f"3. The most active year for lobbying was {most_active_year} with {report_years[most_active_year]} reports.")
most_active_quarter = report_quarters.most_common(1)[0][0]
print(f"4. The most active quarter for lobbying is Q{most_active_quarter} with {report_quarters[most_active_quarter]} reports.")
if legislator_counter:
    top_legislator = legislator_counter.most_common(1)[0][0]
    legislator_info = lobbyview.legislators(legislator_id=top_legislator)
    if legislator_info.data:
        legislator_name = legislator_info.data[0]['legislator_full_name']
        print(f"5. The legislator most frequently connected to {client_name}'s lobbying efforts is {legislator_name}, with {legislator_counter[top_legislator]} bills sponsored.")
print(f"6. Since 2020, {len(recent_bills.data)} bills have been introduced that may be relevant to the company's interests.")

# This vignette demonstrates how a corporation can use the LobbyView package to analyze their lobbying activities,
# identify key legislators, and understand the broader legislative landscape.