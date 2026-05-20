# =============================================================================
# Digital Application Portfolio Governance Dashboard
# Author: Muhammad Umar Siddiqui
# Description: Enterprise application portfolio analysis covering lifecycle
#              management, owner alignment, audit compliance, and Jira-style
#              action item tracking for digital governance teams.
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150
})

# LeanIX-inspired color palette
BLUE       = '#0066CC'
TEAL       = '#00A8A8'
GREEN      = '#2ECC71'
AMBER      = '#F39C12'
RED        = '#E74C3C'
GRAY       = '#7F8C8D'
DARK       = '#2C3E50'
LIGHT_BLUE = '#EBF5FB'

# =============================================================================
# 1. LOAD DATA
# =============================================================================
df_apps   = pd.read_csv('data/application_portfolio.csv')
df_issues = pd.read_csv('data/action_items.csv')
df_audits = pd.read_csv('data/audit_trail.csv')

print("=" * 60)
print("PORTFOLIO OVERVIEW")
print("=" * 60)
print(f"Total Applications    : {len(df_apps)}")
print(f"Total Action Items    : {len(df_issues)}")
print(f"Total Audit Records   : {len(df_audits)}")
print(f"Total Annual Cost     : €{df_apps['Annual_Cost_EUR'].sum():,.0f}")
print(f"Non-Compliant Apps    : {(df_apps['Audit_Status'] == 'Non-Compliant').sum()}")
print(f"Open Issues           : {(df_issues['Status'].isin(['Open', 'In Progress'])).sum()}")

# =============================================================================
# 2. CHART 1 — LeanIX-Style Application Lifecycle Heatmap
# =============================================================================
lifecycle_bu = df_apps.groupby(['Business_Unit', 'Lifecycle_Stage']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(lifecycle_bu, annot=True, fmt='d', cmap='Blues',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Application Count'})
ax.set_title('Application Lifecycle Distribution by Business Unit (LeanIX View)')
ax.set_xlabel('')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('outputs/01_lifecycle_heatmap.png', bbox_inches='tight')
plt.close()
print("Chart saved: 01_lifecycle_heatmap.png")

# =============================================================================
# 3. CHART 2 — Technical Fit vs Business Fit Matrix
# =============================================================================
fit_map = {'Excellent': 4, 'Good': 3, 'Adequate': 2, 'Poor': 1}
biz_map = {'Mission Critical': 4, 'Important': 3, 'Useful': 2, 'Low Value': 1}
df_apps['tech_score'] = df_apps['Technical_Fit'].map(fit_map)
df_apps['biz_score']  = df_apps['Business_Fit'].map(biz_map)

color_map = {'Active': BLUE, 'Under Review': AMBER, 'Phase-Out': RED, 'Planned': TEAL, 'Pilot': GREEN}
colors = df_apps['Lifecycle_Stage'].map(lambda x: color_map.get(x, GRAY))

fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(df_apps['tech_score'], df_apps['biz_score'],
                     c=colors, s=df_apps['Active_Users'] / 20 + 50,
                     alpha=0.75, edgecolors='white', linewidth=0.8)

ax.axvline(2.5, color=GRAY, linestyle='--', alpha=0.5)
ax.axhline(2.5, color=GRAY, linestyle='--', alpha=0.5)
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['Poor', 'Adequate', 'Good', 'Excellent'])
ax.set_yticks([1, 2, 3, 4])
ax.set_yticklabels(['Low Value', 'Useful', 'Important', 'Mission Critical'])
ax.set_xlabel('Technical Fit')
ax.set_ylabel('Business Fit')
ax.set_title('Application Portfolio Matrix: Technical Fit vs Business Fit')

legend_elements = [mpatches.Patch(color=v, label=k) for k, v in color_map.items()]
ax.legend(handles=legend_elements, loc='lower right', title='Lifecycle Stage')

ax.text(1.25, 3.75, 'Invest / Migrate', fontsize=9, color=DARK, alpha=0.6)
ax.text(3.25, 3.75, 'Maintain & Grow', fontsize=9, color=DARK, alpha=0.6)
ax.text(1.25, 1.1, 'Eliminate', fontsize=9, color=DARK, alpha=0.6)
ax.text(3.25, 1.1, 'Phase Out / Review', fontsize=9, color=DARK, alpha=0.6)

plt.tight_layout()
plt.savefig('outputs/02_portfolio_matrix.png', bbox_inches='tight')
plt.close()
print("Chart saved: 02_portfolio_matrix.png")

# =============================================================================
# 4. CHART 3 — Jira-Style Action Items by Status and Priority
# =============================================================================
issue_summary = df_issues.groupby(['Status', 'Priority']).size().unstack(fill_value=0)
priority_order = ['Critical', 'High', 'Medium', 'Low']
issue_summary = issue_summary.reindex(columns=[p for p in priority_order if p in issue_summary.columns])

priority_colors = {'Critical': RED, 'High': AMBER, 'Medium': BLUE, 'Low': TEAL}

fig, ax = plt.subplots(figsize=(11, 5))
bottom = np.zeros(len(issue_summary))
for priority in issue_summary.columns:
    ax.bar(issue_summary.index, issue_summary[priority],
           bottom=bottom, label=priority,
           color=priority_colors.get(priority, GRAY), edgecolor='white')
    bottom += issue_summary[priority].values

ax.set_title('Action Items by Status and Priority (Jira View)')
ax.set_xlabel('Issue Status')
ax.set_ylabel('Number of Issues')
ax.legend(title='Priority', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('outputs/03_action_items_jira.png', bbox_inches='tight')
plt.close()
print("Chart saved: 03_action_items_jira.png")

# =============================================================================
# 5. CHART 4 — Audit Compliance Status by Application Type
# =============================================================================
audit_merge = df_apps[['Application_Name', 'Application_Type', 'Audit_Status', 'GDPR_Compliance', 'IT_Audit_Status']]
compliance_summary = audit_merge.groupby('Application_Type').agg(
    Total=('Application_Name', 'count'),
    Compliant=('Audit_Status', lambda x: (x == 'Compliant').sum()),
    Non_Compliant=('Audit_Status', lambda x: (x == 'Non-Compliant').sum()),
    Pending=('Audit_Status', lambda x: (x == 'Pending Review').sum())
).reset_index()

x = np.arange(len(compliance_summary))
width = 0.25
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width, compliance_summary['Compliant'], width, label='Compliant', color=GREEN, edgecolor='white')
ax.bar(x, compliance_summary['Pending'], width, label='Pending Review', color=AMBER, edgecolor='white')
ax.bar(x + width, compliance_summary['Non_Compliant'], width, label='Non-Compliant', color=RED, edgecolor='white')
ax.set_xticks(x)
ax.set_xticklabels(compliance_summary['Application_Type'])
ax.set_ylabel('Number of Applications')
ax.set_title('Audit Compliance Status by Application Type')
ax.legend()
plt.tight_layout()
plt.savefig('outputs/04_audit_compliance.png', bbox_inches='tight')
plt.close()
print("Chart saved: 04_audit_compliance.png")

# =============================================================================
# 6. CHART 5 — Owner Alignment: Open Issues per Application Owner
# =============================================================================
open_issues = df_issues[df_issues['Status'].isin(['Open', 'In Progress', 'Under Review'])]
owner_issues = open_issues.groupby('Assignee').size().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(owner_issues.index, owner_issues.values,
               color=[RED if v > 10 else AMBER if v > 5 else BLUE for v in owner_issues.values],
               edgecolor='white', height=0.6)
for bar, val in zip(bars, owner_issues.values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
            str(val), va='center', fontsize=9)
ax.set_title('Owner Alignment: Open Action Items per Application Owner')
ax.set_xlabel('Number of Open Issues')
plt.tight_layout()
plt.savefig('outputs/05_owner_alignment.png', bbox_inches='tight')
plt.close()
print("Chart saved: 05_owner_alignment.png")

# =============================================================================
# 7. POWER BI EXPORT
# =============================================================================
df_apps.to_csv('outputs/portfolio_for_powerbi.csv', index=False)
df_issues.to_csv('outputs/issues_for_powerbi.csv', index=False)
df_audits.to_csv('outputs/audits_for_powerbi.csv', index=False)
print("\nPower BI exports saved.")

print()
print("=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
