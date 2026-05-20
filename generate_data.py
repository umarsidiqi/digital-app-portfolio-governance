import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# Application Portfolio Data
business_units = ['Sales & Marketing', 'Finance & Controlling', 'Supply Chain', 'HR & People', 'IT & Infrastructure', 'Customer Solutions', 'Operations']
regions = ['DACH', 'Western Europe', 'Eastern Europe', 'North America', 'Asia Pacific']
lifecycle_stages = ['Active', 'Active', 'Active', 'Under Review', 'Phase-Out', 'Planned', 'Pilot']
tech_fit = ['Excellent', 'Good', 'Adequate', 'Poor']
business_fit = ['Mission Critical', 'Important', 'Useful', 'Low Value']
app_types = ['SaaS', 'On-Premise', 'Hybrid', 'Custom Built']
audit_status = ['Compliant', 'Compliant', 'Pending Review', 'Non-Compliant', 'In Progress']
owners = ['Thomas Müller', 'Anna Schmidt', 'Klaus Weber', 'Maria Fischer', 'Stefan Hoffmann',
          'Julia Becker', 'Michael Wagner', 'Sarah Neumann', 'Peter Braun', 'Laura Zimmermann']

app_names = [
    'SAP S/4HANA', 'Salesforce CRM', 'LeanIX EA Suite', 'ServiceNow ITSM', 'Workday HCM',
    'Microsoft 365', 'Power BI Premium', 'Azure DevOps', 'Jira Software', 'Confluence',
    'SAP Ariba', 'Tableau Server', 'Veeva Vault', 'Oracle EPM', 'SAP SuccessFactors',
    'Adobe Experience Manager', 'Pega Platform', 'MuleSoft Anypoint', 'Celonis Process Mining',
    'SharePoint Online', 'Teams Voice', 'DocuSign', 'Coupa Procurement', 'Anaplan Planning',
    'Snowflake Data Cloud', 'DataStage ETL', 'SolarWinds ITSM', 'Dynatrace APM',
    'CyberArk PAM', 'Qualys VM', 'SAP GRC', 'RSA Archer', 'OneTrust Privacy',
    'Knauf Customer Portal', 'Knauf Product Configurator', 'Knauf Dealer App',
    'Knauf Analytics Hub', 'Knauf Order Management', 'Knauf Field Service'
]

n = len(app_names)
base_date = datetime(2024, 1, 1)

apps = []
for i, name in enumerate(app_names):
    bu = random.choice(business_units)
    region = random.choices(regions, weights=[3, 2, 1.5, 1, 0.5])[0]
    lifecycle = random.choice(lifecycle_stages)
    last_review = base_date + timedelta(days=random.randint(0, 500))
    next_review = last_review + timedelta(days=random.randint(90, 365))
    annual_cost = round(random.uniform(10000, 500000), 2)
    users = random.randint(10, 5000)
    tech = random.choice(tech_fit)
    biz = random.choice(business_fit)
    app_type = random.choice(app_types)
    audit = random.choice(audit_status)
    owner = random.choice(owners)
    data_sensitivity = random.choice(['High', 'High', 'Medium', 'Low'])
    gdpr = random.choice(['Compliant', 'Compliant', 'Pending', 'Non-Compliant'])
    it_audit = random.choice(['Passed', 'Passed', 'In Progress', 'Failed'])
    open_issues = random.randint(0, 15)

    apps.append({
        'Application_ID': f'APP-{1000 + i}',
        'Application_Name': name,
        'Business_Unit': bu,
        'Region': region,
        'Application_Owner': owner,
        'Lifecycle_Stage': lifecycle,
        'Application_Type': app_type,
        'Technical_Fit': tech,
        'Business_Fit': biz,
        'Annual_Cost_EUR': annual_cost,
        'Active_Users': users,
        'Last_Review_Date': last_review.strftime('%Y-%m-%d'),
        'Next_Review_Date': next_review.strftime('%Y-%m-%d'),
        'Audit_Status': audit,
        'GDPR_Compliance': gdpr,
        'IT_Audit_Status': it_audit,
        'Data_Sensitivity': data_sensitivity,
        'Open_Issues': open_issues
    })

df_apps = pd.DataFrame(apps)
df_apps.to_csv('/home/claude/knauf_project/data/application_portfolio.csv', index=False)
print(f"Application portfolio: {len(df_apps)} records")

# Jira-style Action Items
priorities = ['Critical', 'High', 'Medium', 'Low']
issue_types = ['Compliance Gap', 'Owner Alignment', 'License Review', 'Security Audit', 'Data Governance', 'Architecture Review', 'Cost Optimisation']
statuses = ['Open', 'In Progress', 'Under Review', 'Resolved', 'Closed']
assignees = owners

issues = []
for i in range(150):
    app = random.choice(app_names)
    created = base_date + timedelta(days=random.randint(0, 400))
    due = created + timedelta(days=random.randint(7, 90))
    resolved = due + timedelta(days=random.randint(-10, 30)) if random.random() > 0.4 else None
    status = random.choice(statuses)
    if resolved:
        status = random.choice(['Resolved', 'Closed'])

    issues.append({
        'Issue_ID': f'KD-{100 + i}',
        'Application_Name': app,
        'Issue_Type': random.choice(issue_types),
        'Priority': random.choice(priorities),
        'Status': status,
        'Assignee': random.choice(assignees),
        'Created_Date': created.strftime('%Y-%m-%d'),
        'Due_Date': due.strftime('%Y-%m-%d'),
        'Resolved_Date': resolved.strftime('%Y-%m-%d') if resolved else None,
        'Days_Open': (datetime.now() - created).days if status in ['Open', 'In Progress', 'Under Review'] else None
    })

df_issues = pd.DataFrame(issues)
df_issues.to_csv('/home/claude/knauf_project/data/action_items.csv', index=False)
print(f"Action items: {len(df_issues)} records")

# Audit Trail
audit_types = ['IT Security Audit', 'GDPR Compliance Review', 'Application Governance Review', 'Data Sensitivity Assessment', 'License Compliance Audit']
audit_results = ['Passed', 'Passed', 'Passed', 'Minor Findings', 'Major Findings', 'Failed']

audits = []
for i in range(80):
    app = random.choice(app_names)
    audit_date = base_date + timedelta(days=random.randint(0, 500))
    auditor = random.choice(owners)
    result = random.choice(audit_results)
    findings = random.randint(0, 10) if result != 'Passed' else 0
    next_audit = audit_date + timedelta(days=random.randint(180, 365))

    audits.append({
        'Audit_ID': f'AUD-{200 + i}',
        'Application_Name': app,
        'Audit_Type': random.choice(audit_types),
        'Audit_Date': audit_date.strftime('%Y-%m-%d'),
        'Auditor': auditor,
        'Result': result,
        'Findings_Count': findings,
        'Next_Audit_Date': next_audit.strftime('%Y-%m-%d'),
        'Status': 'Closed' if result in ['Passed', 'Minor Findings'] else 'Open'
    })

df_audits = pd.DataFrame(audits)
df_audits.to_csv('/home/claude/knauf_project/data/audit_trail.csv', index=False)
print(f"Audit trail: {len(df_audits)} records")

print("\nAll datasets generated successfully.")
