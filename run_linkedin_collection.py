"""
Run LinkedIn Research Collection
Interactive script for collecting gender/role data from LinkedIn
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_collector import (
    LinkedInResearchCollector,
    save_research_data,
    print_research_summary,
    estimate_gender,
    classify_title,
)


def run_collection():
    """Interactive collection process"""
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║         LINKEDIN RESEARCH COLLECTOR - INTERACTIVE MODE            ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for Selenium
    try:
        from selenium import webdriver
        print("✓ Selenium is installed")
    except ImportError:
        print("✗ Selenium not installed")
        print("\nInstall with: pip install selenium webdriver-manager")
        return
    
    # Get credentials
    print("\n⚠️  USE A DEDICATED RESEARCH ACCOUNT - NOT YOUR PRIMARY!")
    print("-" * 60)
    
    email = input("LinkedIn Email (research account): ").strip()
    password = input("LinkedIn Password: ").strip()
    
    if not email or not password:
        print("Email and password required")
        return
    
    # Get company to search
    company = input("\nCompany to analyze (e.g., 'Infosys'): ").strip()
    if not company:
        company = "Infosys"
    
    max_pages = input("Max pages to scan (default 5): ").strip()
    max_pages = int(max_pages) if max_pages.isdigit() else 5
    
    print(f"\n📊 Will collect data for: {company}")
    print(f"   Max pages: {max_pages}")
    print(f"   Estimated time: {max_pages * 15} seconds")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled")
        return
    
    # Run collection
    print("\n🚀 Starting collection...")
    print("-" * 60)
    
    collector = LinkedInResearchCollector(headless=False)  # Set True for headless
    
    try:
        if collector.login(email, password):
            data = collector.search_company_employees(company, max_pages=max_pages)
            
            if data:
                print_research_summary(data)
                
                # Save results
                save_path = save_research_data(data)
                print(f"\n✅ Data saved to: {save_path}")
        else:
            print("❌ Login failed. Check credentials or verify manually.")
    
    except KeyboardInterrupt:
        print("\n⚠️ Collection interrupted by user")
    
    finally:
        collector.close()


def test_components():
    """Test the gender estimation and title classification"""
    
    print("\n" + "="*60)
    print("🧪 COMPONENT TESTS")
    print("="*60)
    
    # Test gender estimation
    print("\n1️⃣ Gender Estimation from Names:")
    names = ["Priya", "Rahul", "Neha", "Vikram", "Ananya", "Arjun", "Sunita", "Manoj"]
    for name in names:
        gender = estimate_gender(name)
        symbol = {"M": "♂", "F": "♀", "U": "?"}[gender]
        print(f"   {name:<12} → {symbol}")
    
    # Test title classification
    print("\n2️⃣ Title Classification:")
    titles = [
        "CEO", 
        "VP Engineering", 
        "Vice President, Sales",
        "Senior Vice President",
        "Senior Manager", 
        "Software Engineer", 
        "Senior Software Engineer",
        "Analyst", 
        "Intern",
        "Director of Product",
    ]
    tier_names = {1: "Board", 2: "C-Suite", 3: "Senior", 4: "Middle", 5: "Junior", 6: "Entry", 0: "Unknown"}
    for title in titles:
        tier = classify_title(title)
        print(f"   {title:<30} → Tier {tier} ({tier_names[tier]})")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="LinkedIn Research Collector")
    parser.add_argument("--test", action="store_true", help="Run component tests only")
    parser.add_argument("--company", type=str, help="Company to analyze")
    parser.add_argument("--pages", type=int, default=5, help="Max pages to scan")
    
    args = parser.parse_args()
    
    if args.test:
        test_components()
    else:
        run_collection()
