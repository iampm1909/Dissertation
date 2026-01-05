"""
COMPREHENSIVE ANALYSIS SCRIPT FOR SYSTEMATIC REVIEW
====================================================
Input: DissertationIncluded.csv (81 studies exported from Rayyan)
Output: All statistics, frequencies, and percentages reported in the dissertation
Note: This analysis was done early on in the project and supported the base for visualisations, however, liberty has been taken to make minimal changes based on manual verification so the numbers on visualisations might differ accordingly.
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("="*80)
print("SYSTEMATIC REVIEW COMPREHENSIVE ANALYSIS")
print("Blockchain Integration in Electric Vehicle Charging Ecosystems")
print("="*80)

# ==============================================================================
# SECTION 1: DATA LOADING
# ==============================================================================
print("\n" + "="*80)
print("SECTION 1: LOADING DATA")
print("="*80)

df = pd.read_csv('DissertationIncluded.csv', encoding='utf-8')
print(f"\n✓ Loaded {len(df)} studies from DissertationIncluded.csv")

# Display column names
print(f"\nColumns in dataset: {list(df.columns)}")

# ==============================================================================
# SECTION 2: TEMPORAL DISTRIBUTION
# ==============================================================================
print("\n" + "="*80)
print("SECTION 2: TEMPORAL DISTRIBUTION")
print("="*80)

# Count studies by year
year_counts = df['year'].value_counts().sort_index()
print("\nStudies by year:")
for year, count in year_counts.items():
    percentage = (count / len(df)) * 100
    print(f"  {year}: {count} studies ({percentage:.1f}%)")

# Calculate growth rates
print("\nYear-over-year growth rates:")
years_sorted = sorted(year_counts.index)
for i in range(1, len(years_sorted)):
    prev_year = years_sorted[i-1]
    curr_year = years_sorted[i]
    prev_count = year_counts[prev_year]
    curr_count = year_counts[curr_year]
    growth = ((curr_count - prev_count) / prev_count) * 100
    print(f"  {prev_year} → {curr_year}: {growth:.1f}% growth")

# Studies in 2024-2026 period
recent_studies = df[df['year'].isin([2024, 2025, 2026])]
recent_percentage = (len(recent_studies) / len(df)) * 100
print(f"\nStudies in 2024-2026 period: {len(recent_studies)} ({recent_percentage:.1f}%)")

# ==============================================================================
# SECTION 3: RESEARCH METHODOLOGIES
# ==============================================================================
print("\n" + "="*80)
print("SECTION 3: RESEARCH METHODOLOGIES")
print("="*80)

# Combine title and abstract for analysis
df['combined_text'] = df['title'].fillna('') + ' ' + df['abstract'].fillna('')
df['combined_text'] = df['combined_text'].str.lower()

# Define methodology keywords
methodology_keywords = {
    'Theoretical/Conceptual': ['theoretical', 'conceptual', 'framework', 'model', 'architecture', 'proposed'],
    'Experimental': ['experiment', 'experimental', 'test', 'evaluation'],
    'Prototype/Implementation': ['prototype', 'implementation', 'deployed', 'developed system'],
    'Simulation': ['simulation', 'simulated', 'simulate'],
    'Survey/Review': ['survey', 'review', 'systematic review', 'literature']
}

print("\nResearch Methodologies:")
methodology_counts = {}

for methodology, keywords in methodology_keywords.items():
    count = 0
    for idx, text in df['combined_text'].items():
        if any(keyword in text for keyword in keywords):
            count += 1
    methodology_counts[methodology] = count
    percentage = (count / len(df)) * 100
    print(f"  {methodology}: {count} studies ({percentage:.1f}%)")

print("\nNote: Percentages may exceed 100% as studies can employ multiple methodologies")

# ==============================================================================
# SECTION 4: PUBLICATION OUTLETS
# ==============================================================================
print("\n" + "="*80)
print("SECTION 4: PUBLICATION OUTLETS")
print("="*80)

# Count studies with journal information
if 'journal' in df.columns:
    studies_with_journal = df['journal'].notna().sum()
    percentage = (studies_with_journal / len(df)) * 100
    print(f"\nStudies with journal information: {studies_with_journal} ({percentage:.1f}%)")
else:
    print("\nNo 'journal' column found in dataset")

# ==============================================================================
# SECTION 5: AUTHOR COLLABORATION
# ==============================================================================
print("\n" + "="*80)
print("SECTION 5: AUTHOR COLLABORATION PATTERNS")
print("="*80)

# Count authors per paper (approximation based on 'and' or ';' in authors field)
df['author_count'] = df['authors'].str.count(';') + 1  # assuming semicolon-separated

mean_authors = df['author_count'].mean()
min_authors = df['author_count'].min()
max_authors = df['author_count'].max()
mode_authors = df['author_count'].mode()[0]
mode_count = (df['author_count'] == mode_authors).sum()

print(f"\nAuthor collaboration statistics:")
print(f"  Average authors per study: {mean_authors:.2f}")
print(f"  Range: {min_authors} to {max_authors} authors")
print(f"  Most common: {mode_authors} authors ({mode_count} papers, {(mode_count/len(df)*100):.1f}%)")

# ==============================================================================
# SECTION 6: THEMATIC SYNTHESIS 
# ==============================================================================
print("\n" + "="*80)
print("SECTION 6: THEMATIC SYNTHESIS - 8 MAJOR THEMES")
print("="*80)

# Define theme keywords
theme_keywords = {
    'Security & Privacy': ['security', 'privacy', 'authentication', 'encryption', 'attack', 'vulnerability', 'trust', 'cyber'],
    'Payment & Transaction Systems': ['payment', 'transaction', 'billing', 'cryptocurrency', 'micropayment', 'settlement'],
    'Scalability & Performance': ['scalability', 'scalable', 'performance', 'throughput', 'latency', 'optimization'],
    'Energy Trading': ['energy trading', 'peer-to-peer energy', 'p2p energy', 'energy market', 'trading'],
    'Sustainability': ['sustainability', 'sustainable', 'carbon', 'renewable', 'green', 'environmental'],
    'Smart Contracts': ['smart contract'],
    'IoT Integration': ['iot', 'internet of things', 'sensor', 'device'],
    'V2G/V2V Integration': ['vehicle-to-grid', 'v2g', 'vehicle-to-vehicle', 'v2v', 'bidirectional']
}

print("\nResearch Themes (studies can address multiple themes):")
theme_counts = {}

for theme, keywords in theme_keywords.items():
    count = 0
    for idx, text in df['combined_text'].items():
        if any(keyword in text for keyword in keywords):
            count += 1
    theme_counts[theme] = count
    percentage = (count / len(df)) * 100
    print(f"  {theme}: {count} studies ({percentage:.1f}%)")

# ==============================================================================
# SECTION 7: APPLICATION DOMAINS 
# ==============================================================================
print("\n" + "="*80)
print("SECTION 7: APPLICATION DOMAINS")
print("="*80)

application_keywords = {
    'Payment Systems': ['payment', 'transaction', 'billing', 'financial'],
    'Charging Infrastructure Management': ['charging infrastructure', 'charging station', 'charging network'],
    'Energy Trading Platforms': ['energy trading', 'trading platform', 'energy market'],
    'Supply Chain Traceability': ['supply chain', 'traceability', 'provenance', 'battery lifecycle'],
    'Authentication & Access Control': ['authentication', 'access control', 'authorization'],
    'Traffic Management': ['traffic', 'routing', 'navigation'],
    'V2G Operational Systems': ['v2g', 'vehicle-to-grid operation']
}

print("\nApplication Domains:")
application_counts = {}

for application, keywords in application_keywords.items():
    count = 0
    for idx, text in df['combined_text'].items():
        if any(keyword in text for keyword in keywords):
            count += 1
    application_counts[application] = count
    percentage = (count / len(df)) * 100
    print(f"  {application}: {count} studies ({percentage:.1f}%)")

# ==============================================================================
# SECTION 8: BLOCKCHAIN PLATFORMS 
# ==============================================================================
print("\n" + "="*80)
print("SECTION 8: BLOCKCHAIN PLATFORMS")
print("="*80)

platform_keywords = {
    'Ethereum': ['ethereum'],
    'Hyperledger Fabric': ['hyperledger fabric', 'hyperledger'],
    'Consortium/Private': ['consortium', 'private blockchain', 'permissioned'],
    'DAG-based': ['dag', 'directed acyclic graph', 'tangle', 'iota']
}

print("\nBlockchain Platforms mentioned:")
platform_counts = {}

for platform, keywords in platform_keywords.items():
    count = 0
    for idx, text in df['combined_text'].items():
        if any(keyword in text for keyword in keywords):
            count += 1
    platform_counts[platform] = count
    percentage = (count / len(df)) * 100
    print(f"  {platform}: {count} studies ({percentage:.1f}%)")

# ==============================================================================
# SECTION 9: IMPLEMENTATION CHALLENGES 
# ==============================================================================
print("\n" + "="*80)
print("SECTION 9: IMPLEMENTATION CHALLENGES")
print("="*80)

challenge_keywords = {
    'Latency & Real-time Performance': ['latency', 'real-time', 'delay', 'response time'],
    'Scalability Limitations': ['scalability challenge', 'scalability issue', 'scalability limitation', 'throughput limitation'],
    'Energy Consumption': ['energy consumption', 'power consumption', 'energy intensive', 'computational cost'],
    'Security Vulnerabilities': ['security vulnerability', 'security risk', 'attack vector', '51% attack'],
    'Regulatory Uncertainty': ['regulation', 'regulatory', 'policy', 'legal', 'compliance'],
    'Privacy Concerns': ['privacy concern', 'privacy challenge', 'data protection'],
    'Interoperability': ['interoperability challenge', 'interoperability issue', 'compatibility'],
    'Adoption Barriers': ['adoption barrier', 'adoption challenge']
}

print("\nImplementation Challenges identified:")
challenge_counts = {}

for challenge, keywords in challenge_keywords.items():
    count = 0
    for idx, text in df['combined_text'].items():
        if any(keyword in text for keyword in keywords):
            count += 1
    challenge_counts[challenge] = count
    percentage = (count / len(df)) * 100
    print(f"  {challenge}: {count} studies ({percentage:.1f}%)")

# ==============================================================================
# SECTION 10: SAVE RESULTS TO FILES
# ==============================================================================
print("\n" + "="*80)
print("SECTION 10: SAVING RESULTS TO OUTPUT FILES")
print("="*80)

# Save all results to CSV files for easy reference
results_summary = {
    'Metric': [],
    'Value': [],
    'Percentage': []
}

# Add temporal data
for year, count in year_counts.items():
    results_summary['Metric'].append(f'Studies in {year}')
    results_summary['Value'].append(count)
    results_summary['Percentage'].append(f'{(count/len(df)*100):.1f}%')

# Add methodology data
for methodology, count in methodology_counts.items():
    results_summary['Metric'].append(methodology)
    results_summary['Value'].append(count)
    results_summary['Percentage'].append(f'{(count/len(df)*100):.1f}%')

# Add theme data
for theme, count in theme_counts.items():
    results_summary['Metric'].append(f'Theme: {theme}')
    results_summary['Value'].append(count)
    results_summary['Percentage'].append(f'{(count/len(df)*100):.1f}%')

# Save to CSV
results_df = pd.DataFrame(results_summary)
results_df.to_csv('comprehensive_analysis_results.csv', index=False)
print("\n✓ Results saved to: comprehensive_analysis_results.csv")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================
print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nTotal studies analyzed: {len(df)}")
print(f"Publication period: {df['year'].min()} - {df['year'].max()}")
print("\nAll results correspond to Chapter 4: Results in the dissertation")
print("\nOutput files generated:")
print("  1. comprehensive_analysis_results.csv - All metrics and percentages")
print("  2. keyword_frequencies.csv - Keyword frequency counts")
print("\n" + "="*80)
