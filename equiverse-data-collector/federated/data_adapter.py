"""
Equiverse Federated Learning - Data Adapter Layer
Handles different HR data formats and maps to standard schema

Supports:
- CSV/Excel files
- SAP SuccessFactors (API)
- Workday (API)
- Darwinbox (API)
- Custom database connections
"""

import os
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from pathlib import Path


# ============================================================
# STANDARD SCHEMA - What we need from ANY system
# ============================================================

@dataclass
class StandardEmployee:
    """
    Minimal standard record - just what's needed for aggregation
    NO personal identifiers stored
    """
    gender: str      # "M", "F", "O" (other/non-binary)
    tier: int        # 1=Board, 2=C-Suite, 3=Senior, 4=Middle, 5=Junior, 6=Entry
    is_active: bool  # Currently employed
    
    # Optional for richer analysis (still anonymous)
    tenure_band: Optional[str] = None      # "0-2y", "2-5y", "5-10y", "10+y"
    department_type: Optional[str] = None  # "Tech", "Sales", "HR", "Finance", "Ops"


# ============================================================
# TIER MAPPING - How to classify job levels
# ============================================================

DEFAULT_TIER_KEYWORDS = {
    1: {  # Board
        "keywords": ["board", "director", "non-executive", "independent director", 
                     "chairman", "chairperson"],
        "grades": []
    },
    2: {  # C-Suite
        "keywords": ["ceo", "cfo", "cto", "coo", "cmo", "cpo", "chro", "cio",
                     "chief", "managing director", "md", "president",
                     "executive director", "ed", "svp", "senior vice president"],
        "grades": ["E1", "E2", "L10", "L9"]
    },
    3: {  # Senior Management
        "keywords": ["vice president", "vp ", "avp", "associate vice president",
                     "general manager", "gm", "senior director", "head of",
                     "principal", "evp"],
        "grades": ["E3", "E4", "L8", "L7", "M5", "M4"]
    },
    4: {  # Middle Management
        "keywords": ["director", "senior manager", "manager", "associate director",
                     "program manager", "delivery manager", "project manager"],
        "grades": ["M3", "M2", "L6", "L5"]
    },
    5: {  # Junior Management / Senior IC
        "keywords": ["lead", "team lead", "tech lead", "senior consultant",
                     "senior analyst", "senior engineer", "senior developer",
                     "senior associate", "supervisor", "assistant manager"],
        "grades": ["M1", "L4", "L3", "A4", "A3"]
    },
    6: {  # Entry Level
        "keywords": ["analyst", "associate", "engineer", "developer", "consultant",
                     "executive", "trainee", "intern", "graduate", "fresher"],
        "grades": ["A2", "A1", "L2", "L1", "T1", "T2"]
    }
}


# ============================================================
# BASE ADAPTER CLASS
# ============================================================

class DataAdapter(ABC):
    """
    Abstract base class for all data adapters
    Each adapter converts source data to StandardEmployee records
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.tier_mapping = config.get("tier_mapping", DEFAULT_TIER_KEYWORDS)
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to data source"""
        pass
    
    @abstractmethod
    def fetch_employees(self) -> List[StandardEmployee]:
        """Fetch and convert all employees to standard format"""
        pass
    
    def classify_tier(self, title: str, grade: str = "") -> int:
        """
        Classify job title/grade into tier (1-6)
        Returns 0 if cannot classify
        """
        title_lower = (title or "").lower()
        grade_upper = (grade or "").upper()
        
        # Check each tier in order (highest first)
        for tier in range(1, 7):
            tier_config = self.tier_mapping.get(tier, {})
            
            # Check keywords in title
            for keyword in tier_config.get("keywords", []):
                if keyword in title_lower:
                    return tier
            
            # Check grade codes
            if grade_upper in tier_config.get("grades", []):
                return tier
        
        return 0  # Unknown
    
    def normalize_gender(self, value: str) -> str:
        """Normalize gender value to M/F/O"""
        if not value:
            return "O"
        
        v = value.strip().upper()
        
        if v in ["M", "MALE", "1", "MAN", "HE"]:
            return "M"
        elif v in ["F", "FEMALE", "2", "WOMAN", "SHE"]:
            return "F"
        else:
            return "O"  # Other / non-binary / unknown


# ============================================================
# CSV/EXCEL ADAPTER
# ============================================================

class CSVAdapter(DataAdapter):
    """
    Adapter for CSV or Excel files
    Most flexible - works with any exported HR data
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Config should include:
        - file_path: Path to CSV/Excel file
        - field_mapping: Dict mapping our fields to their column names
          {
            "gender": "their_gender_column",
            "title": "their_title_column",
            "grade": "their_grade_column",  # optional
            "status": "their_status_column"  # optional
          }
        - gender_values: Dict mapping their values to M/F
          {"male": ["M", "Male"], "female": ["F", "Female"]}
        - active_values: List of values meaning "active employee"
        """
        super().__init__(config)
        self.file_path = config.get("file_path")
        self.field_mapping = config.get("field_mapping", {})
        self.gender_values = config.get("gender_values", {
            "male": ["M", "Male", "MALE", "1", "Man"],
            "female": ["F", "Female", "FEMALE", "2", "Woman"]
        })
        self.active_values = config.get("active_values", 
            ["Active", "ACTIVE", "1", "Y", "Yes", "TRUE", "Current"])
        self.df = None
    
    def connect(self) -> bool:
        """Load the CSV/Excel file"""
        try:
            import pandas as pd
            
            file_path = Path(self.file_path)
            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                return False
            
            if file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.df = pd.read_excel(file_path)
            else:
                self.df = pd.read_csv(file_path)
            
            print(f"✅ Loaded {len(self.df)} records from {file_path.name}")
            print(f"   Columns: {list(self.df.columns)}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load file: {e}")
            return False
    
    def fetch_employees(self) -> List[StandardEmployee]:
        """Convert CSV data to StandardEmployee records"""
        if self.df is None:
            return []
        
        employees = []
        
        gender_col = self.field_mapping.get("gender")
        title_col = self.field_mapping.get("title")
        grade_col = self.field_mapping.get("grade")
        status_col = self.field_mapping.get("status")
        dept_col = self.field_mapping.get("department")
        
        for _, row in self.df.iterrows():
            # Get gender
            raw_gender = str(row.get(gender_col, "")) if gender_col else ""
            gender = self._map_gender(raw_gender)
            
            # Get tier from title and/or grade
            title = str(row.get(title_col, "")) if title_col else ""
            grade = str(row.get(grade_col, "")) if grade_col else ""
            tier = self.classify_tier(title, grade)
            
            # Check if active
            if status_col:
                status = str(row.get(status_col, ""))
                is_active = status in self.active_values
            else:
                is_active = True  # Assume active if no status column
            
            # Get department type (optional)
            dept = str(row.get(dept_col, "")) if dept_col else None
            
            if tier > 0:  # Only include if we could classify
                employees.append(StandardEmployee(
                    gender=gender,
                    tier=tier,
                    is_active=is_active,
                    department_type=dept
                ))
        
        return employees
    
    def _map_gender(self, value: str) -> str:
        """Map source gender value to M/F/O"""
        v = value.strip()
        
        if v in self.gender_values.get("male", []):
            return "M"
        elif v in self.gender_values.get("female", []):
            return "F"
        else:
            return "O"


# ============================================================
# CONFIGURATION WIZARD
# ============================================================

def auto_detect_columns(file_path: str) -> Dict[str, str]:
    """
    Attempt to auto-detect column mappings from file
    Returns suggested field_mapping
    """
    import pandas as pd
    
    # Load sample
    path = Path(file_path)
    if path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(path, nrows=100)
    else:
        df = pd.read_csv(path, nrows=100)
    
    suggestions = {}
    
    # Patterns to look for
    gender_patterns = ["gender", "sex", "m/f", "male/female"]
    title_patterns = ["title", "designation", "position", "job", "role"]
    grade_patterns = ["grade", "level", "band", "job_level", "joblevel"]
    status_patterns = ["status", "active", "employment", "emp_status"]
    dept_patterns = ["department", "dept", "function", "division"]
    
    for col in df.columns:
        col_lower = col.lower()
        
        for pattern in gender_patterns:
            if pattern in col_lower:
                suggestions["gender"] = col
                break
        
        for pattern in title_patterns:
            if pattern in col_lower:
                suggestions["title"] = col
                break
        
        for pattern in grade_patterns:
            if pattern in col_lower:
                suggestions["grade"] = col
                break
        
        for pattern in status_patterns:
            if pattern in col_lower:
                suggestions["status"] = col
                break
        
        for pattern in dept_patterns:
            if pattern in col_lower:
                suggestions["department"] = col
                break
    
    return suggestions


def create_config_wizard():
    """
    Interactive wizard to help company set up their data mapping
    """
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║         EQUIVERSE DATA MAPPING WIZARD                            ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Get file path
    file_path = input("Enter path to your HR data file (CSV/Excel): ").strip()
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    # Auto-detect columns
    print("\n🔍 Analyzing file structure...")
    suggestions = auto_detect_columns(file_path)
    
    print("\n📋 Detected columns:")
    import pandas as pd
    path = Path(file_path)
    if path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(path, nrows=5)
    else:
        df = pd.read_csv(path, nrows=5)
    
    for i, col in enumerate(df.columns):
        print(f"   [{i+1}] {col}")
    
    print("\n💡 Auto-detected mappings:")
    for field, col in suggestions.items():
        print(f"   {field} → {col}")
    
    # Confirm or adjust
    use_suggestions = input("\nUse these mappings? (y/n): ").strip().lower()
    
    if use_suggestions == 'y':
        field_mapping = suggestions
    else:
        field_mapping = {}
        print("\nEnter column names for each field (press Enter to skip):")
        field_mapping["gender"] = input("  Gender column: ").strip() or None
        field_mapping["title"] = input("  Job Title column: ").strip() or None
        field_mapping["grade"] = input("  Grade/Level column: ").strip() or None
        field_mapping["status"] = input("  Status column: ").strip() or None
        field_mapping = {k: v for k, v in field_mapping.items() if v}
    
    # Create config
    config = {
        "file_path": file_path,
        "field_mapping": field_mapping,
        "gender_values": {
            "male": ["M", "Male", "MALE", "1"],
            "female": ["F", "Female", "FEMALE", "2"]
        },
        "active_values": ["Active", "ACTIVE", "1", "Y", "Yes"]
    }
    
    # Save config
    config_path = Path(file_path).parent / "equiverse_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to: {config_path}")
    return config


# ============================================================
# DEMO: Test with sample data
# ============================================================

if __name__ == "__main__":
    # Create sample HR data for testing
    sample_data = """emp_id,name,gender,designation,grade,department,status
1001,Priya Sharma,F,Senior Manager,M3,Engineering,Active
1002,Rahul Verma,M,VP Engineering,E3,Engineering,Active
1003,Neha Gupta,F,Software Engineer,A2,Engineering,Active
1004,Amit Kumar,M,Director,M4,Sales,Active
1005,Sneha Patel,F,Analyst,A1,Finance,Active
1006,Vikram Singh,M,CEO,E1,Executive,Active
1007,Anjali Reddy,F,Team Lead,M1,Engineering,Active
1008,Manoj Iyer,M,Associate,A1,Operations,Active
1009,Divya Nair,F,Senior Analyst,A3,Finance,Active
1010,Arjun Menon,M,Manager,M2,Sales,Active
"""
    
    # Save sample
    sample_path = Path(__file__).parent / "sample_hr_data.csv"
    with open(sample_path, 'w') as f:
        f.write(sample_data)
    
    print("📊 Testing CSV Adapter with sample data...")
    print("-" * 60)
    
    # Configure adapter
    config = {
        "file_path": str(sample_path),
        "field_mapping": {
            "gender": "gender",
            "title": "designation",
            "grade": "grade",
            "status": "status",
            "department": "department"
        }
    }
    
    # Run adapter
    adapter = CSVAdapter(config)
    if adapter.connect():
        employees = adapter.fetch_employees()
        
        print(f"\n✅ Processed {len(employees)} employees")
        print("\nTier Distribution:")
        
        tier_counts = {}
        for emp in employees:
            key = (emp.tier, emp.gender)
            tier_counts[key] = tier_counts.get(key, 0) + 1
        
        tier_names = {1: "Board", 2: "C-Suite", 3: "Senior", 
                      4: "Middle", 5: "Junior", 6: "Entry"}
        
        for tier in range(1, 7):
            m = tier_counts.get((tier, "M"), 0)
            f = tier_counts.get((tier, "F"), 0)
            total = m + f
            if total > 0:
                f_pct = f / total * 100
                print(f"  Tier {tier} ({tier_names[tier]:8}): {m}M, {f}F ({f_pct:.0f}% female)")
