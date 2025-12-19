# Equiverse Index - The Simple Explanation
## Explaining to Anyone in 5 Minutes

---

## 📌 THE PROBLEM (1 min)

**We want to know:** How many women are at each level in Indian companies?

```
Board      → ? women
C-Suite    → ? women  
Senior     → ? women     WE DON'T KNOW
Middle     → ? women     THESE NUMBERS
Junior     → ? women
Entry      → ? women
```

**But companies won't share their employee data.**

Why?
- "What if we look bad?"
- "Competitors will see"
- "HR data is private"

**So we're stuck. No data = No solution.**

---

## 💡 OUR IDEA (2 mins)

### Step 1: We make a small program

We write code that:
- Reads HR data (names, gender, job level)
- Counts: "How many men? How many women? At each level?"
- Creates a SMALL summary file

```
INPUT (Company's HR data - STAYS WITH THEM):
┌────────────────────────────────────────┐
│ Name          Gender    Level          │
│ Priya Kumar   F         Manager        │
│ Rahul Singh   M         Director       │
│ Neha Sharma   F         Analyst        │
│ ... 5000 more rows ...                 │
└────────────────────────────────────────┘

OUTPUT (Small summary - THIS IS WHAT WE GET):
┌────────────────────────────────────────┐
│ company_id: TCS                        │
│ sector: IT                             │
│ tier_1_board: {male: 8, female: 2}     │
│ tier_2_csuite: {male: 12, female: 3}   │
│ tier_3_senior: {male: 150, female: 45} │
│ tier_4_middle: {male: 800, female: 320}│
│ tier_5_junior: {male: 1200, female: 600│
│ tier_6_entry: {male: 2000, female: 1400│
└────────────────────────────────────────┘
```

**We NEVER see: Priya, Rahul, Neha... Just counts.**

---

### Step 2: Give the program to each company

```
    TCS         Infosys       Wipro        HCL
     │            │             │           │
     ▼            ▼             ▼           ▼
  ┌──────┐    ┌──────┐      ┌──────┐    ┌──────┐
  │ Our  │    │ Our  │      │ Our  │    │ Our  │
  │ Code │    │ Code │      │ Code │    │ Code │
  └──────┘    └──────┘      └──────┘    └──────┘
     │            │             │           │
     ▼            ▼             ▼           ▼
  Runs on     Runs on       Runs on     Runs on
  THEIR       THEIR         THEIR       THEIR
  computer    computer      computer    computer
```

**Company's raw data NEVER leaves their office.**

---

### Step 3: They send us ONLY the small result

Each company sends a tiny file (JSON or CSV):

```json
{
  "company_id": "TCS",
  "company_name": "Tata Consultancy Services",
  "sector": "IT",
  "year": 2025,
  "data": {
    "board":    {"male": 8,    "female": 2},
    "csuite":   {"male": 12,   "female": 3},
    "senior":   {"male": 150,  "female": 45},
    "middle":   {"male": 800,  "female": 320},
    "junior":   {"male": 1200, "female": 600},
    "entry":    {"male": 2000, "female": 1400}
  }
}
```

**Size: ~500 bytes. That's smaller than this sentence.**

---

### Step 4: We COMBINE all the results

We DON'T aggregate (average out). We UNION (stack together):

```
┌─────────────────────────────────────────────────────────────┐
│ COMBINED DATASET (what we build)                            │
├─────────────────────────────────────────────────────────────┤
│ company    sector   tier      male    female   female_pct   │
├─────────────────────────────────────────────────────────────┤
│ TCS        IT       board     8       2        20%          │
│ TCS        IT       csuite    12      3        20%          │
│ TCS        IT       senior    150     45       23%          │
│ Infosys    IT       board     7       3        30%          │
│ Infosys    IT       csuite    10      4        29%          │
│ Infosys    IT       senior    120     50       29%          │
│ Wipro      IT       board     9       1        10%          │
│ HDFC       BFSI     board     10      2        17%          │
│ ICICI      BFSI     board     8       4        33%          │
│ ... 100s more rows ...                                      │
└─────────────────────────────────────────────────────────────┘
```

**Now we have a FULL DATASET to analyze!**

---

### Step 5: We analyze EVERYTHING

With the combined data, we can answer:

| Question | Answer |
|----------|--------|
| Which sector has most women in leadership? | BFSI: 25% at C-Suite |
| Where do women drop off most? | Between Middle → Senior (biggest gap) |
| Which company is best for women? | Company X: Top 10% |
| Is it improving year over year? | Yes, 2% increase since 2023 |

---

## 🎨 THE PICTURE VERSION

```
    COMPANY A          COMPANY B          COMPANY C
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │ 5000    │        │ 8000    │        │ 3000    │
   │ employee│        │ employee│        │ employee│
   │ records │        │ records │        │ records │
   └────┬────┘        └────┬────┘        └────┬────┘
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │   OUR   │        │   OUR   │        │   OUR   │
   │  CODE   │        │  CODE   │        │  CODE   │
   │ (runs   │        │ (runs   │        │ (runs   │
   │  there) │        │  there) │        │  there) │
   └────┬────┘        └────┬────┘        └────┬────┘
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │ Small   │        │ Small   │        │ Small   │
   │ Summary │        │ Summary │        │ Summary │
   │ (6 rows)│        │ (6 rows)│        │ (6 rows)│
   └────┬────┘        └────┬────┘        └────┬────┘
        │                  │                  │
        └────────────┬─────┴──────────────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  OUR SERVER     │
            │                 │
            │  UNION all      │
            │  summaries      │
            │  into ONE       │
            │  big dataset    │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  ANALYSIS       │
            │                 │
            │  Charts         │
            │  Insights       │
            │  Rankings       │
            │  Reports        │
            └─────────────────┘
```

---

## 🔐 WHY IT'S SAFE

| What We See | What We DON'T See |
|-------------|-------------------|
| "TCS has 2 women on board" | Who those 2 women are |
| "45 women in senior roles" | Their names, salaries |
| Counts and percentages | Individual employee data |

**It's like knowing the class average without seeing anyone's answer sheet.**

---

## 🗣️ THE 30-SECOND VERSION

> "Companies won't share employee data. So we give them a small program. 
> 
> The program counts men and women at each level - just counts, no names.
> 
> They send us those counts. We combine everyone's counts into one big dataset.
> 
> Now we can analyze gender gaps across all of Indian industry.
> 
> Companies share nothing sensitive. We learn everything important."

---

## ❓ SIMPLE Q&A

**"Why would companies do this?"**
→ They want to know how they compare. Like students wanting to know the class average.

**"Can you figure out who the employees are?"**
→ No. If I tell you "10 women in senior roles at TCS" - you can't figure out who they are. TCS has 600,000 employees.

**"What if a company lies?"**
→ We cross-check with public data (BRSR reports have totals). If their total doesn't match, we know something's wrong.

**"Why not just ask companies directly?"**
→ We tried. They say no. This way, they keep their data private AND contribute to the bigger picture.

---

## 🎯 ONE LINE SUMMARY

> **"We don't take their data. We give them a calculator. They tell us the result."**

---

*For TalentNomics Pitch - December 2025*
