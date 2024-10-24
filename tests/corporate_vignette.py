# LobbyView Package Usage Vignette for Corporate Strategy
# Analyzing Lobbying Landscape for Microsoft

import os
from dotenv import load_dotenv
import sys
sys.path.append('./src/lobbyview/')
sys.path.append('../src/lobbyview/')
from LobbyView import LobbyView
from exceptions import InvalidPageNumberError

import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.gridspec import GridSpec

# Load environment variables and set up LobbyView
env_paths = ["tests/.env", "../../tests/.env"]
for env_path in env_paths:
    load_dotenv(env_path)

LOBBYVIEW_TOKEN = os.environ.get('LOBBYVIEW_TOKEN', "NO TOKEN FOUND")
lobbyview = LobbyView(LOBBYVIEW_TOKEN)

def get_legislator_name(legislator_id):
    legislator_info = lobbyview.legislators(legislator_id=legislator_id)
    if legislator_info.data:
        return legislator_info.data[0]['legislator_full_name']
    return legislator_id  # Return ID if name not found

# 1. Start with a known client: Microsoft Corporation
client_name = "Microsoft Corporation"
client_info = lobbyview.clients(client_name=client_name)

if not client_info.data:
    print(f"No data found for {client_name}")
    sys.exit(1)

# The LobbyView API uses UUIDs to uniquely identify entities.
# We need to convert from the human-readable company name to its UUID for subsequent queries.
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

print("\nAnalyzing Microsoft's lobbying issues...")

# Get all issues from Microsoft's reports
all_issues = []
for report in client_reports.data:
    try:
        issues = lobbyview.issues(report_uuid=report['report_uuid'])
        all_issues.extend(issues.data)
    except InvalidPageNumberError:
        # Skip reports with no issues
        continue

if not all_issues:
    print("No lobbying issues found for Microsoft")
else:
    # Count frequency of issue codes
    issue_codes = Counter()
    for issue in all_issues:
        issue_codes[issue['issue_code']] += 1
        
    # Create a cache for issue text descriptions
    issue_text_cache = {}

    print("\nTop issues by frequency:")
    for code, count in issue_codes.most_common(10):
        if code not in issue_text_cache:
            try:
                # Try multiple report UUIDs until we find one with text
                for issue in all_issues:
                    if issue['issue_code'] == code:
                        sample_text = lobbyview.texts(issue_code=code, report_uuid=issue['report_uuid'])
                        if sample_text.data:
                            issue_text_cache[code] = sample_text.data[0]['issue_text']
                            break
                if code not in issue_text_cache:
                    issue_text_cache[code] = "No description available"
            except (InvalidPageNumberError, IndexError):
                issue_text_cache[code] = "No description available"
        
        print(f"  {code}: {count} occurrences")
        print(f"    Sample issue text: {issue_text_cache[code][:100]}...")  # Show first 100 chars

# 4. Analyze network data
network_data = lobbyview.networks(client_uuid=client_uuid)
print(f"\nNumber of network connections: {len(network_data.data)}")

legislator_counter = Counter()
for network in network_data.data:
    legislator_counter[network['legislator_id']] += network['n_bills_sponsored']

print("\nTop 5 legislators by bills sponsored:")
for legislator_id, count in legislator_counter.most_common(5):
    legislator_name = get_legislator_name(legislator_id)
    print(f"  {legislator_name}: {count}")

# 5. Analyze recent Microsoft-connected bills
recent_ms_bills = []
for network in network_data.data:
    try:
        # Get bills sponsored by legislators connected to Microsoft since 2020
        legislator_bills = lobbyview.bills(
            legislator_id=network['legislator_id'],
            min_introduced_date="2020-01-01"
        )
        recent_ms_bills.extend(legislator_bills.data)
    except InvalidPageNumberError:
        # Skip legislators with no recent bills
        continue

print(f"\nNumber of Microsoft-connected bills introduced since 2020: {len(recent_ms_bills)}")

bill_sponsors = Counter()
for bill in recent_ms_bills:
    bill_sponsors[bill['legislator_id']] += 1

print("\nTop 5 Microsoft-connected bill sponsors since 2020:")
for legislator_id, count in bill_sponsors.most_common(5):
    legislator_name = get_legislator_name(legislator_id)
    print(f"  {legislator_name}: {count}")

# Create visualization
plt.figure(figsize=(20, 20))
gs = GridSpec(3, 2, figure=plt.gcf())

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
legislator_names = []
legislator_values = []
for leg_id, value in top_legislators.items():
    name = get_legislator_name(leg_id)
    if name:
        legislator_names.append(name)
        legislator_values.append(value)
    else:
        print(f"Warning: No name found for legislator ID {leg_id}")

ax3.bar(legislator_names, legislator_values)
ax3.set_title(f"Top Legislators for {client_name} by Bills Sponsored")
ax3.set_xlabel("Legislator Name")
ax3.set_ylabel("Number of Bills Sponsored")
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha="right")

# 4. Top Bill Sponsors (Recent Bills)
if recent_ms_bills:  # Only create this plot if we have data
    ax4 = plt.subplot(gs[1, 1])
    top_sponsors = dict(bill_sponsors.most_common(10))
    sponsor_names = []
    sponsor_values = []
    for leg_id, value in top_sponsors.items():
        name = get_legislator_name(leg_id)
        if name:
            sponsor_names.append(name)
            sponsor_values.append(value)
        else:
            print(f"Warning: No name found for legislator ID {leg_id}")

    if sponsor_names:  # Only plot if we have names
        ax4.bar(sponsor_names, sponsor_values)
        ax4.set_title("Top Microsoft-Connected Bill Sponsors (Since 2020)")
        ax4.set_xlabel("Legislator Name")
        ax4.set_ylabel("Number of Bills Sponsored")
        plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha="right")

# Add issues plot
ax5 = plt.subplot(gs[2, :])  # Use entire bottom row
top_issues = dict(issue_codes.most_common(10))
ax5.bar(top_issues.keys(), top_issues.values())
ax5.set_title(f"Top 10 Issues in {client_name}'s Lobbying Reports")
ax5.set_xlabel("Issue Code")
ax5.set_ylabel("Number of Occurrences")
plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha="right")

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
    top_legislator_id = legislator_counter.most_common(1)[0][0]
    top_legislator_name = get_legislator_name(top_legislator_id)
    print(f"5. The legislator most frequently connected to {client_name}'s lobbying efforts is {top_legislator_name}, with {legislator_counter[top_legislator_id]} bills sponsored.")
if recent_ms_bills:
    print(f"6. Since 2020, {len(recent_ms_bills)} bills have been introduced by legislators connected to {client_name}'s lobbying network.")
else:
    print(f"6. No recent bills found for legislators connected to {client_name}'s lobbying network.")
if issue_codes:
    print(f"7. The company's most frequent lobbying issues are:")
    for code, count in issue_codes.most_common(3):
        description = issue_text_cache.get(code, "No description available")
        print(f"   - {code} ({count} occurrences): {description[:100]}...")
else:
    print("7. No lobbying issues found in the available data.")