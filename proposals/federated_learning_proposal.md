# Federated Learning for Gender Parity Analytics
## A Privacy-Preserving Industry-Wide Equiverse Index

**Proposal by:** TalentNomics  
**Version:** 1.0  
**Date:** December 2025

---

## Executive Summary

We propose a **federated learning infrastructure** that enables companies to contribute to an industry-wide Gender Parity Index **without exposing individual employee data**. Companies run analytics locally, share only aggregate statistics, and receive benchmarking insights in return.

**The result:** India's first privacy-preserving, real-time Gender Parity Dashboard at sector and tier level.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│    "What if every company could see how they compare on        │
│     gender diversity — without revealing their data?"           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Table of Contents

1. [The Problem](#1-the-problem)
2. [Our Solution: Federated Learning](#2-our-solution-federated-learning)
3. [How It Works](#3-how-it-works)
4. [Technical Architecture](#4-technical-architecture)
5. [Data Privacy & Security](#5-data-privacy--security)
6. [What Companies Get](#6-what-companies-get)
7. [What the Industry Gets](#7-what-the-industry-gets)
8. [Implementation Roadmap](#8-implementation-roadmap)
9. [Pilot Program Proposal](#9-pilot-program-proposal)
10. [FAQ](#10-faq)
11. [Call to Action](#11-call-to-action)

---

## 1. The Problem

### 1.1 The Data Gap

Despite SEBI's BRSR mandates, we lack **tier-level gender data** across Indian corporations.

| What We Know | What We Don't Know |
|--------------|-------------------|
| Total employees by gender | Gender split at C-Suite |
| Board composition | Gender split at Senior Management |
| | Gender split at Middle Management |
| | Where exactly women "drop off" |

### 1.2 The "Leaky Pipeline" Mystery

```
                    Women Representation (Illustrative)
    
    Board          ████░░░░░░░░░░░░░░░░  20%
    C-Suite        ███░░░░░░░░░░░░░░░░░  15%
    Senior Mgmt    ████░░░░░░░░░░░░░░░░  20%    ← WHERE IS THE DROP?
    Middle Mgmt    █████░░░░░░░░░░░░░░░  25%    ← WE DON'T KNOW
    Junior Mgmt    ███████░░░░░░░░░░░░░  35%
    Entry Level    ████████░░░░░░░░░░░░  40%
```

**We see the outcome (few women at top), but not the process (where they leave).**

### 1.3 Why Current Approaches Fail

| Approach | Why It Fails |
|----------|--------------|
| Surveys | Low response rate, PR-sanitized answers |
| BRSR Reports | Only totals, no tier breakdown |
| LinkedIn Scraping | ToS violation, inaccurate |
| Direct Requests | Companies won't share competitive data |

### 1.4 The Trust Problem

Companies are reluctant to share detailed workforce data because:

- **Competitive sensitivity** — reveals talent strategy
- **Legal exposure** — could be used against them
- **PR risk** — numbers might look bad
- **Data privacy** — employee information concerns

---

## 2. Our Solution: Federated Learning

### 2.1 The Core Idea

**Federated Learning** is an AI technique where:
- Data **never leaves** the company
- Only **aggregated insights** are shared
- A central system learns from **patterns, not raw data**

```
    Traditional Approach              Federated Approach
    ──────────────────────            ─────────────────────
    
    Companies send data →             Companies keep data
           ↓                                  ↓
    Central database ←                Run analytics locally
           ↓                                  ↓
    Single point of risk              Share only: "28% women at Tier 3"
                                              ↓
                                      Central aggregates patterns
                                              ↓
                                      Everyone sees benchmarks
```

### 2.2 Analogy: Credit Bureaus

Think of it like **CIBIL for gender diversity**:

- Banks don't share raw customer data with each other
- But they all contribute to a scoring system
- Everyone benefits from aggregate credit insights

Similarly:
- Companies don't share employee lists
- But they contribute aggregate gender-tier statistics
- Everyone benefits from industry benchmarks

---

## 3. How It Works

### 3.1 The Process (Simplified)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  STEP 1: Company installs lightweight analytics tool                         │
│          (runs behind firewall, accesses HRMS data)                          │
│                                                                              │
│  STEP 2: Tool computes LOCAL aggregates                                      │
│          "Tier 3 has 45 men, 18 women = 28.6% female"                        │
│                                                                              │
│  STEP 3: Only AGGREGATES sent to central server                              │
│          No names, no employee IDs, no raw data                              │
│                                                                              │
│  STEP 4: Central server computes SECTOR benchmarks                           │
│          "IT Sector Tier 3 average: 24.2% female"                            │
│                                                                              │
│  STEP 5: Company receives ANONYMOUS ranking                                  │
│          "You are in top 30% for Tier 3 gender parity"                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Visual Flow

```
         ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
         │   TCS       │         │   Infosys   │         │   Wipro     │
         │   ┌─────┐   │         │   ┌─────┐   │         │   ┌─────┐   │
         │   │HRMS │   │         │   │HRMS │   │         │   │HRMS │   │
         │   └──┬──┘   │         │   └──┬──┘   │         │   └──┬──┘   │
         │      │      │         │      │      │         │      │      │
         │   ┌──▼──┐   │         │   ┌──▼──┐   │         │   ┌──▼──┐   │
         │   │Tool │   │         │   │Tool │   │         │   │Tool │   │
         │   └──┬──┘   │         │   └──┬──┘   │         │   └──┬──┘   │
         └──────┼──────┘         └──────┼──────┘         └──────┼──────┘
                │                       │                       │
                │ {tier3: 28.6%}        │ {tier3: 31.2%}        │ {tier3: 26.1%}
                │                       │                       │
                └───────────────────────┼───────────────────────┘
                                        │
                                        ▼
                          ┌─────────────────────────────┐
                          │     EQUIVERSE AGGREGATOR    │
                          │                             │
                          │  IT Sector Tier 3 Average:  │
                          │        28.6% female         │
                          │                             │
                          │  Participating: 47 companies│
                          │  Total employees: 2.3M      │
                          └─────────────────────────────┘
                                        │
                                        ▼
                          ┌─────────────────────────────┐
                          │   PUBLIC DASHBOARD          │
                          │   (sector averages only)    │
                          └─────────────────────────────┘
                                        +
                          ┌─────────────────────────────┐
                          │   PRIVATE COMPANY REPORTS   │
                          │   (your rank vs. industry)  │
                          └─────────────────────────────┘
```

---

## 4. Technical Architecture

### 4.1 System Components

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EQUIVERSE FEDERATED SYSTEM                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     COMPANY SIDE (On-Premise)                        │   │
│  │                                                                      │   │
│  │   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      │   │
│  │   │  HRMS/SAP/   │      │  EQUIVERSE   │      │  OUTPUT:     │      │   │
│  │   │  Workday     │ ───► │  LOCAL       │ ───► │  Aggregates  │      │   │
│  │   │  Connector   │      │  ANALYZER    │      │  Only        │      │   │
│  │   └──────────────┘      └──────────────┘      └──────────────┘      │   │
│  │                                                      │               │   │
│  │   Data stays here ◄───────────────────────────────────               │   │
│  └──────────────────────────────────────────────────────┼───────────────┘   │
│                                                         │                   │
│                                                         │ Encrypted         │
│                                                         │ Aggregates        │
│                                                         ▼                   │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     CENTRAL SIDE (Cloud)                              │  │
│  │                                                                       │  │
│  │   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐       │  │
│  │   │  AGGREGATE   │      │  BENCHMARK   │      │  DASHBOARD   │       │  │
│  │   │  COLLECTOR   │ ───► │  ENGINE      │ ───► │  GENERATOR   │       │  │
│  │   └──────────────┘      └──────────────┘      └──────────────┘       │  │
│  │                                                                       │  │
│  │   Cannot reverse-engineer individual company data                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Data Schema (What's Computed Locally)

```python
# Example: What the local tool computes
company_aggregate = {
    "company_id": "anonymized_hash",  # Not actual company name
    "sector": "IT",
    "reporting_period": "Q4 2025",
    
    "tier_data": {
        "board": {"total": 12, "female": 3, "female_pct": 25.0},
        "c_suite": {"total": 8, "female": 1, "female_pct": 12.5},
        "senior_mgmt": {"total": 156, "female": 35, "female_pct": 22.4},
        "middle_mgmt": {"total": 2340, "female": 655, "female_pct": 28.0},
        "junior_mgmt": {"total": 12500, "female": 4125, "female_pct": 33.0},
        "entry_level": {"total": 45000, "female": 16200, "female_pct": 36.0},
    },
    
    # Differential privacy noise added
    "noise_factor": 0.02,
    "min_bucket_size": 50,  # No tier reported if < 50 employees
}
```

### 4.3 What's NEVER Shared

| Never Shared | Reason |
|--------------|--------|
| Employee names | PII |
| Employee IDs | PII |
| Individual salaries | Sensitive |
| Department breakdown | Competitive |
| Exact company identity | In public reports |
| Raw HRMS data | Everything |

---

## 5. Data Privacy & Security

### 5.1 Privacy Techniques Used

| Technique | How It Protects |
|-----------|-----------------|
| **Differential Privacy** | Adds statistical noise so individual contributions can't be identified |
| **K-Anonymity** | Only reports data if tier has >50 employees |
| **Secure Aggregation** | Central server can't see individual company submissions |
| **Homomorphic Encryption** | Computations on encrypted data (advanced option) |

### 5.2 Differential Privacy Explained

```
Actual Tier 3 female %:  28.6%

With Differential Privacy: 28.6% + random_noise(-2%, +2%)

Reported: Could be 26.8% to 30.4%

Result: True value is hidden, but aggregate patterns remain accurate
```

When you aggregate 50+ companies, the noise cancels out, but no single company can be identified.

### 5.3 Compliance

| Regulation | How We Comply |
|------------|---------------|
| **DPDP Act 2023** | No personal data leaves company |
| **IT Act** | Encrypted transmission, audit logs |
| **GDPR** (if global) | Privacy by design, data minimization |
| **SOC 2** | Can obtain certification |

### 5.4 Trust Architecture

```
                    TRUST BOUNDARIES
    
    ┌──────────────────────────────────────┐
    │                                      │
    │   COMPANY ZONE (Full Trust)          │
    │   ───────────────────────────        │
    │   • Raw employee data                │
    │   • HRMS access                      │
    │   • Individual records               │
    │                                      │
    │   Only the company sees this         │
    │                                      │
    └───────────────┬──────────────────────┘
                    │
                    │ Aggregates only
                    │ (with noise)
                    ▼
    ┌──────────────────────────────────────┐
    │                                      │
    │   NASSCOM/EQUIVERSE ZONE             │
    │   ─────────────────────────          │
    │   • Company-level aggregates         │
    │   • Anonymized company IDs           │
    │   • Can compute sector averages      │
    │                                      │
    │   Cannot identify individuals        │
    │   Cannot reverse-engineer companies  │
    │                                      │
    └───────────────┬──────────────────────┘
                    │
                    │ Sector averages only
                    ▼
    ┌──────────────────────────────────────┐
    │                                      │
    │   PUBLIC ZONE                        │
    │   ───────────                        │
    │   • "IT sector averages 28% at T3"   │
    │   • Industry trends                  │
    │   • No company identification        │
    │                                      │
    └──────────────────────────────────────┘
```

---

## 6. What Companies Get

### 6.1 Private Benchmarking Report

Each participating company receives:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│               CONFIDENTIAL: [Your Company] Gender Parity Report             │
│                           Q4 2025 | IT Sector                               │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   YOUR POSITION vs INDUSTRY                                                 │
│   ─────────────────────────                                                 │
│                                                                             │
│   Tier          You      Industry    Your Rank    Trend                     │
│   ─────────────────────────────────────────────────────                     │
│   Board         25.0%    22.3%       Top 35%      ↑ +2.1%                   │
│   C-Suite       12.5%    15.8%       Bottom 40%   ↓ -1.2%   ⚠️              │
│   Senior Mgmt   22.4%    24.2%       Middle 50%   → flat                    │
│   Middle Mgmt   28.0%    26.8%       Top 40%      ↑ +1.5%                   │
│   Entry Level   36.0%    38.2%       Bottom 45%   → flat                    │
│                                                                             │
│   🚨 BOTTLENECK ALERT: C-Suite                                              │
│   Your drop from Senior Mgmt (22.4%) to C-Suite (12.5%) is                  │
│   larger than industry average drop (24.2% → 15.8%)                         │
│                                                                             │
│   💡 RECOMMENDATION:                                                        │
│   Review promotion patterns at Director → VP transition                     │
│   Top performers in your sector have sponsorship programs                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Benefits to Companies

| Benefit | Description |
|---------|-------------|
| **Anonymous Benchmarking** | See where you stand without revealing identity |
| **Bottleneck Identification** | Know exactly WHERE women drop off in YOUR org |
| **Best Practice Insights** | What top performers do differently |
| **ESG Reporting Support** | Pre-computed metrics for sustainability reports |
| **Board Presentation Ready** | Executive dashboards for leadership |

### 6.3 Gamification & Recognition

```
🏆 SECTOR LEADERS (Anonymous until they opt-in)

Gold Tier (Top 10%):   ████████████████████  5 companies
Silver Tier (Top 25%): ████████████████      12 companies
Bronze Tier (Top 40%): ████████████          18 companies

Companies can choose to:
✓ Remain anonymous
✓ Reveal identity to get "Gender Parity Leader" badge
✓ Share in annual NASSCOM report
```

---

## 7. What the Industry Gets

### 7.1 Public Dashboard (Sector Averages)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                    EQUIVERSE INDEX - PUBLIC DASHBOARD                       │
│                              IT Sector | Q4 2025                            │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   SECTOR GENDER PYRAMID                                                     │
│   ─────────────────────                                                     │
│                                                                             │
│   Board         ████████████░░░░░░░░░░░░░░░░░░  22.3% (↑ 1.2% YoY)         │
│   C-Suite       ██████████░░░░░░░░░░░░░░░░░░░░  15.8% (↑ 0.8% YoY)         │
│   Senior Mgmt   █████████████░░░░░░░░░░░░░░░░░  24.2% (↑ 0.5% YoY)         │
│   Middle Mgmt   ███████████████░░░░░░░░░░░░░░░  26.8% (↑ 0.3% YoY)         │
│   Junior Mgmt   █████████████████░░░░░░░░░░░░░  33.5% (→ flat)             │
│   Entry Level   ███████████████████░░░░░░░░░░░  38.2% (↓ -0.5% YoY)        │
│                                                                             │
│   📊 Participating Companies: 47 | Employees Covered: 2.3M                  │
│                                                                             │
│   🔴 BIGGEST BOTTLENECK: Senior Mgmt → C-Suite (-8.4%)                      │
│   🟢 IMPROVING: Board diversity up 1.2% year-over-year                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Cross-Sector Comparison

```
SECTOR COMPARISON - C-Suite Female Representation

IT & Services      ████████████████░░░░  15.8%
BFSI              ██████████████████░░  18.2%
Pharma            ████████████████████  20.1%
Manufacturing     ████████░░░░░░░░░░░░   8.3%
Professional Svcs ██████████████░░░░░░  14.5%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target (Parity)   ██████████████████████████████████████████████████  50%
```

### 7.3 Policy Insights

For Ministry of Women & Child Development / SEBI:

```
POLICY BRIEF: Where Intervention is Most Needed

1. CRITICAL BOTTLENECK: Middle Mgmt → Senior Mgmt transition
   - 8.4% drop in female representation
   - Consistent across 4/5 sectors
   - Recommendation: Mandate sponsorship programs

2. ENTRY LEVEL STAGNATION: Despite 50% female graduates
   - Entry level stuck at 38%, not improving
   - Possible cause: Work flexibility, location constraints
   - Recommendation: Hybrid work policy incentives

3. MANUFACTURING OUTLIER: 8.3% C-Suite vs 15%+ in other sectors
   - Historical male-dominated culture
   - Recommendation: Sector-specific intervention
```

---

## 8. Implementation Roadmap

### 8.1 Timeline

```
        2025                          2026                          2027
          │                             │                             │
    Q4    │    Q1         Q2         Q3 │ Q4         Q1         Q2    │
    ──────┼────────────────────────────────────────────────────────────
          │                             │                             │
  ┌───────┴───────┐                     │                             │
  │ PHASE 1       │                     │                             │
  │ Pilot (5 co.) │                     │                             │
  └───────────────┘                     │                             │
                  ┌─────────────────────┴───────┐                     │
                  │ PHASE 2                     │                     │
                  │ Expand (50 companies)       │                     │
                  │ Launch public dashboard     │                     │
                  └─────────────────────────────┘                     │
                                                ┌─────────────────────┴─────┐
                                                │ PHASE 3                   │
                                                │ Scale (500+ companies)    │
                                                │ Cross-sector benchmarks   │
                                                │ Policy recommendations    │
                                                └───────────────────────────┘
```

### 8.2 Phase Details

#### Phase 1: Pilot (3 months)
- Partner with 5 progressive IT companies
- Deploy local analytics tool
- Validate privacy guarantees
- Collect initial benchmarks
- **Success metric:** 5 companies contributing data

#### Phase 2: Expand (6 months)
- Scale to 50 companies
- Launch public dashboard
- NASSCOM integration
- Media launch
- **Success metric:** 50 companies, 500K+ employees covered

#### Phase 3: Scale (12 months)
- 500+ companies across sectors
- SEBI integration discussions
- Annual Equiverse Index Report
- **Success metric:** Becomes industry standard

---

## 9. Pilot Program Proposal

### 9.1 Pilot Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PILOT PROGRAM PROPOSAL                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PARTICIPANTS: 5 IT companies (mix of sizes)                               │
│   DURATION: 3 months                                                        │
│   INVESTMENT: Zero cost for pilot participants                              │
│                                                                             │
│   WHAT COMPANIES DO:                                                        │
│   ─────────────────                                                         │
│   1. Install lightweight tool (1 day IT effort)                             │
│   2. Connect to HRMS (read-only access)                                     │
│   3. Review and approve aggregate output                                    │
│   4. Receive benchmarking report                                            │
│                                                                             │
│   WHAT COMPANIES GET:                                                       │
│   ────────────────────                                                      │
│   ✓ Free gender parity diagnostic                                           │
│   ✓ Benchmarking against pilot peers                                        │
│   ✓ "Founding Partner" recognition                                          │
│   ✓ Input on final product design                                           │
│   ✓ Priority access when scaled                                             │
│                                                                             │
│   WHAT WE DELIVER:                                                          │
│   ────────────────                                                          │
│   ✓ Validated privacy model                                                 │
│   ✓ Working prototype                                                       │
│   ✓ Pilot report                                                            │
│   ✓ Recommendations for scale                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Ideal Pilot Partners

| Type | Example Companies | Why |
|------|-------------------|-----|
| Large IT | TCS, Infosys, Wipro | Scale validation |
| Mid-size IT | Persistent, Coforge | Different dynamics |
| Startup/Unicorn | Razorpay, Zerodha | Modern HRMS systems |

### 9.3 Ask from NASSCOM

```
PARTNERSHIP REQUEST

We request NASSCOM to:

1. ENDORSE the pilot program
   - Lends credibility for company outreach
   - Signals industry alignment

2. FACILITATE introductions to 5 pilot companies
   - Leverage existing relationships
   - D&I council connections

3. CO-BRAND the Equiverse Index
   - "Powered by NASSCOM x TalentNomics"
   - Integrate with existing diversity initiatives

4. HOST the public dashboard (optional)
   - On NASSCOM digital infrastructure
   - Or link from NASSCOM website

In return:
- NASSCOM becomes owner of industry's first privacy-preserving diversity index
- Positions NASSCOM as leader in responsible AI/data initiatives
- Creates new engagement touchpoint with member companies
```

---

## 10. FAQ

### Q1: Why would companies participate?
**A:** Because they get **free benchmarking** without exposing data. It's like getting a diagnostic report for free. Companies with good numbers can opt-in for recognition.

### Q2: How do we ensure companies don't game the system?
**A:** 
- Data validation against BRSR totals (cross-check)
- Statistical anomaly detection
- Annual audit option for badge-seekers
- Reputation mechanism (consistent over time)

### Q3: What if only "good" companies participate?
**A:** We address selection bias by:
- Starting with NASSCOM-endorsed pilot (diverse participants)
- Making participation low-friction
- Eventually pushing for regulatory encouragement

### Q4: Is 50 companies enough for meaningful benchmarks?
**A:** Yes. With 50 companies in IT sector covering 500K+ employees, the statistical power is high. Each tier has thousands of data points.

### Q5: What about non-IT sectors?
**A:** We start with IT (best data infrastructure), then expand to BFSI, Pharma based on pilot success.

### Q6: How is this different from existing diversity reports?
**A:** Existing reports are:
- Self-reported (our data is system-generated)
- Aggregate only (we have tier breakdown)
- Inconsistent definitions (we standardize)
- One-time (we're continuous)

### Q7: What about international companies?
**A:** The system can accommodate global companies for India operations. Future: expand to APAC, then global.

---

## 11. Call to Action

### For NASSCOM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   🤝 PARTNERSHIP PROPOSAL                                                    │
│                                                                             │
│   We invite NASSCOM to become the founding partner of the                   │
│   Equiverse Index — India's first privacy-preserving gender                 │
│   parity benchmark.                                                         │
│                                                                             │
│   NEXT STEPS:                                                               │
│   1. 30-minute presentation to D&I Council                                  │
│   2. Technical review with NASSCOM data team                                │
│   3. Joint announcement of pilot program                                    │
│   4. Launch with 5 founding companies                                       │
│                                                                             │
│   CONTACT:                                                                  │
│   [TalentNomics Team]                                                       │
│   [Email]                                                                   │
│   [Phone]                                                                   │
│                                                                             │
│   "Let's build the infrastructure for an Equiverse together."               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### For Companies

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   🏢 BECOME A FOUNDING PARTNER                                              │
│                                                                             │
│   Join 5 progressive companies in piloting the Equiverse Index.             │
│                                                                             │
│   YOU GET:                                                                  │
│   ✓ Free diagnostic of your gender pipeline                                 │
│   ✓ Anonymous benchmarking against peers                                    │
│   ✓ "Founding Partner" badge for ESG reports                                │
│   ✓ Shape the future of diversity measurement                               │
│                                                                             │
│   WE ASK:                                                                   │
│   • 1 day of IT time for deployment                                         │
│   • Read-only HRMS access (on-premise, your control)                        │
│   • 30-minute monthly sync during pilot                                     │
│                                                                             │
│   Zero cost. Zero data exposure. Full insights.                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Appendix A: Technical Specifications

### A.1 Local Analytics Tool

```
Language:        Python 3.10+
Deployment:      Docker container (on-premise)
HRMS Connectors: SAP SuccessFactors, Workday, Oracle HCM, Darwinbox
Data Access:     Read-only, scheduled batch
Output Format:   JSON (encrypted)
Size:            < 100MB
Dependencies:    Minimal (no GPU required)
```

### A.2 Privacy Parameters

```python
PRIVACY_CONFIG = {
    "differential_privacy": {
        "epsilon": 1.0,          # Privacy budget (lower = more private)
        "delta": 1e-5,           # Probability of privacy breach
    },
    "k_anonymity": {
        "min_group_size": 50,    # Don't report tiers with < 50 employees
    },
    "reporting": {
        "round_to": 5,           # Round percentages to nearest 5%
        "noise_range": 0.02,     # ±2% noise on reported figures
    }
}
```

---

## Appendix B: Sample Outputs

### B.1 Raw Output (from local tool)

```json
{
  "submission_id": "a3f8c2e1-...",
  "timestamp": "2025-12-15T10:30:00Z",
  "sector": "IT",
  "size_bucket": "Large (10K+)",
  "tiers": {
    "board": {"female_pct_noisy": 25.0},
    "c_suite": {"female_pct_noisy": 15.0},
    "senior_mgmt": {"female_pct_noisy": 22.5},
    "middle_mgmt": {"female_pct_noisy": 27.5},
    "junior_mgmt": {"female_pct_noisy": 32.5},
    "entry_level": {"female_pct_noisy": 37.5}
  },
  "validation_hash": "sha256:..."
}
```

### B.2 Aggregated Sector Output

```json
{
  "sector": "IT",
  "period": "Q4 2025",
  "companies_count": 47,
  "employees_covered": 2340000,
  "tiers": {
    "board": {"avg_female_pct": 22.3, "std_dev": 5.2, "trend_yoy": 1.2},
    "c_suite": {"avg_female_pct": 15.8, "std_dev": 4.8, "trend_yoy": 0.8},
    "senior_mgmt": {"avg_female_pct": 24.2, "std_dev": 4.1, "trend_yoy": 0.5},
    "middle_mgmt": {"avg_female_pct": 26.8, "std_dev": 3.5, "trend_yoy": 0.3},
    "junior_mgmt": {"avg_female_pct": 33.5, "std_dev": 4.2, "trend_yoy": 0.0},
    "entry_level": {"avg_female_pct": 38.2, "std_dev": 5.1, "trend_yoy": -0.5}
  }
}
```

---

## Appendix C: Comparison with Alternatives

| Feature | Equiverse (FL) | Traditional Survey | BRSR Scraping | LinkedIn Data |
|---------|----------------|-------------------|---------------|---------------|
| Data accuracy | High | Medium | High | Low |
| Tier breakdown | ✅ Yes | Sometimes | ❌ No | Estimated |
| Privacy | ✅ Preserved | ❌ Exposed | N/A | ⚠️ Gray area |
| Company effort | Low | High | None | None |
| Scalability | ✅ High | ❌ Low | ✅ High | ⚠️ Limited |
| Real-time | ✅ Quarterly | ❌ Annual | ❌ Annual | ✅ Near-real-time |
| Legal risk | ✅ None | ✅ None | ✅ None | ⚠️ ToS issues |

---

*Document prepared by TalentNomics | December 2025*  
*For the Equiverse Initiative — Restoring Gender Parity*

---

**END OF PROPOSAL**
