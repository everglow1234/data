"""
LinkedIn Research Data Collector
For academic/research purposes only

LEGAL DISCLAIMER:
- This tool is for academic research only
- Use a dedicated research account, not your primary LinkedIn
- Respect rate limits and be gentle with requests
- Store only aggregate data, not individual profiles
- Comply with your institution's IRB guidelines if applicable

Based on hiQ Labs v. LinkedIn precedent for public data research
"""

import time
import random
import json
import csv
import re
import os
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
import logging

# Load environment variables from .env file
def load_env():
    """Load credentials from .env file"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_env()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# GENDER ESTIMATION FROM FIRST NAMES
# Research-standard approach using name databases
# ============================================================

# Common Indian first names and their typical gender
# This is a simplified version - for production, use:
# - Gender API (genderize.io)
# - Indian Census name data
# - NamSor API

INDIAN_NAMES_GENDER = {
    # Female names
    "priya": "F", "neha": "F", "pooja": "F", "anjali": "F", "divya": "F",
    "swati": "F", "kavita": "F", "sunita": "F", "meera": "F", "anita": "F",
    "deepika": "F", "shreya": "F", "nisha": "F", "rekha": "F", "geeta": "F",
    "shalini": "F", "preeti": "F", "manisha": "F", "rashmi": "F", "smita": "F",
    "archana": "F", "shweta": "F", "pallavi": "F", "jyoti": "F", "ritu": "F",
    "aarti": "F", "sneha": "F", "bhavna": "F", "garima": "F", "kriti": "F",
    "aditi": "F", "aishwarya": "F", "ananya": "F", "diya": "F", "isha": "F",
    "kiara": "F", "mira": "F", "nandini": "F", "riya": "F", "saanvi": "F",
    "tanvi": "F", "vedika": "F", "zara": "F", "anika": "F", "avni": "F",
    
    # Male names
    "rahul": "M", "amit": "M", "raj": "M", "suresh": "M", "rajesh": "M",
    "vijay": "M", "ajay": "M", "sanjay": "M", "deepak": "M", "manoj": "M",
    "arun": "M", "kumar": "M", "ravi": "M", "sandeep": "M", "vikram": "M",
    "ashok": "M", "ramesh": "M", "mukesh": "M", "dinesh": "M", "naresh": "M",
    "rohit": "M", "nikhil": "M", "varun": "M", "karan": "M", "arjun": "M",
    "aarav": "M", "advait": "M", "arnav": "M", "dev": "M", "harsh": "M",
    "ishaan": "M", "kabir": "M", "krishna": "M", "mohit": "M", "pranav": "M",
    "reyansh": "M", "siddharth": "M", "veer": "M", "yash": "M", "aditya": "M",
    "akash": "M", "ankit": "M", "gaurav": "M", "himanshu": "M", "manish": "M",
}

def estimate_gender(first_name: str) -> str:
    """
    Estimate gender from first name
    Returns: 'M', 'F', or 'U' (unknown)
    """
    if not first_name:
        return "U"
    
    name = first_name.lower().strip()
    
    # Direct lookup
    if name in INDIAN_NAMES_GENDER:
        return INDIAN_NAMES_GENDER[name]
    
    # Heuristic patterns for Indian names
    female_endings = ['a', 'i', 'ee', 'ti', 'ni', 'ya', 'ka', 'na', 'ri']
    male_endings = ['sh', 'raj', 'deep', 'kumar', 'esh', 'an', 'av']
    
    for ending in female_endings:
        if name.endswith(ending) and len(name) > 3:
            return "F"
    
    for ending in male_endings:
        if name.endswith(ending):
            return "M"
    
    return "U"


# ============================================================
# ROLE/TITLE CLASSIFICATION
# ============================================================

TITLE_TO_TIER = {
    # Tier 1: Board (check first - longest matches)
    "independent director": 1, "non-executive director": 1,
    "board member": 1, "board of director": 1, "chairman": 1, 
    "chairperson": 1, "chairwoman": 1,
    
    # Tier 2: C-Suite (check before general terms)
    "chief executive officer": 2, "chief financial officer": 2,
    "chief technology officer": 2, "chief operating officer": 2,
    "chief marketing officer": 2, "chief information officer": 2,
    "chief human resource": 2, "chief people officer": 2,
    "ceo": 2, "cfo": 2, "cto": 2, "coo": 2, "cmo": 2, "cio": 2, "chro": 2,
    "managing director": 2, "president": 2, "founder": 2, "co-founder": 2,
    "partner": 2, "chief": 2,
    
    # Tier 3: Senior Management (VP level)
    "executive vice president": 3, "senior vice president": 3,
    "vice president": 3, "evp": 3, "svp": 3, "vp ": 3, " vp": 3,
    "vp,": 3, "vp-": 3, "general manager": 3, "global head": 3,
    "country head": 3, "regional head": 3, "business head": 3,
    
    # Tier 4: Middle Management
    "senior director": 4, "associate director": 4, "director": 4,
    "senior manager": 4, "program manager": 4, "project manager": 4,
    "delivery manager": 4, "engagement manager": 4, "manager": 4,
    
    # Tier 5: Junior Management / Senior IC
    "team lead": 5, "tech lead": 5, "lead engineer": 5, "lead developer": 5,
    "lead analyst": 5, "supervisor": 5, "senior consultant": 5, 
    "senior analyst": 5, "senior engineer": 5, "senior developer": 5,
    "senior associate": 5, "principal": 5, "lead": 5,
    
    # Tier 6: Entry Level (check last)
    "analyst": 6, "associate": 6, "consultant": 6, "engineer": 6,
    "developer": 6, "executive": 6, "trainee": 6, "intern": 6,
    "fresher": 6, "graduate trainee": 6, "graduate": 6,
}

def classify_title(title: str) -> int:
    """
    Classify a job title into tier (1-6)
    Returns tier number or 0 if unknown
    
    Priority: Check higher tiers first, more specific patterns first
    """
    if not title:
        return 0
    
    title_lower = " " + title.lower() + " "  # Add spaces for word boundary matching
    
    # Tier 1: Board Level
    tier_1 = ["independent director", "non-executive director", "board member", 
              "board of director", " chairman ", "chairperson", "chairwoman"]
    for kw in tier_1:
        if kw in title_lower:
            return 1
    
    # Tier 2: C-Suite (check BEFORE senior VP)
    tier_2 = ["chief executive", "chief financial", "chief technology",
              "chief operating", "chief marketing", "chief information",
              "chief human", "chief people", "chief product", "chief revenue",
              " ceo ", " cfo ", " cto ", " coo ", " cmo ", " cio ", " chro ", " cpo ",
              "managing director", " president ", " founder", "co-founder"]
    for kw in tier_2:
        if kw in title_lower:
            return 2
    
    # Tier 3: VP Level / Senior Leadership
    tier_3 = ["executive vice president", "senior vice president", "vice president",
              " evp ", " svp ", " vp ", " vp,", ",vp ", "vp-", "general manager", 
              "global head", "country head", "regional head", "business head", 
              " head of ", " partner "]
    for kw in tier_3:
        if kw in title_lower:
            return 3
    
    # Tier 4: Director / Manager Level
    tier_4 = ["senior director", "associate director", " director ", " director,",
              "senior manager", "program manager", "project manager", "product manager",
              "delivery manager", "engagement manager", "engineering manager",
              " manager "]
    for kw in tier_4:
        if kw in title_lower:
            return 4
    
    # Tier 5: Senior IC / Lead Level (check BEFORE entry level)
    tier_5 = ["team lead", "tech lead", "lead engineer", "lead developer", "lead analyst",
              " supervisor ", "senior consultant", "senior analyst", "senior engineer",
              "senior developer", "senior associate", "senior specialist",
              "senior software engineer", "senior software developer",
              " principal ", " lead ", " staff engineer", " staff developer",
              "senior "]  # Catch-all for "Senior X" roles
    for kw in tier_5:
        if kw in title_lower:
            return 5
    
    # Tier 6: Entry Level / IC
    tier_6 = [" analyst ", " associate ", " consultant ", " engineer ", " developer ", 
              " executive ", " trainee ", " intern ", " fresher ", " graduate ",
              " specialist "]
    for kw in tier_6:
        if kw in title_lower:
            return 6
    
    return 0  # Unknown


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class AggregateCount:
    """Aggregate count - no individual data stored"""
    male: int = 0
    female: int = 0
    unknown: int = 0
    
    @property
    def total(self):
        return self.male + self.female + self.unknown
    
    @property
    def female_pct(self):
        known = self.male + self.female
        return round(self.female / known * 100, 1) if known > 0 else 0


@dataclass
class CompanyResearchData:
    """Aggregated research data for a company"""
    company_name: str
    company_linkedin_url: str
    data_collection_date: str
    
    # Aggregate counts by tier - NO individual data
    tier_1_board: AggregateCount = None
    tier_2_csuite: AggregateCount = None
    tier_3_senior: AggregateCount = None
    tier_4_middle: AggregateCount = None
    tier_5_junior: AggregateCount = None
    tier_6_entry: AggregateCount = None
    
    total_profiles_analyzed: int = 0
    methodology_notes: str = ""
    
    def __post_init__(self):
        if self.tier_1_board is None:
            self.tier_1_board = AggregateCount()
        if self.tier_2_csuite is None:
            self.tier_2_csuite = AggregateCount()
        if self.tier_3_senior is None:
            self.tier_3_senior = AggregateCount()
        if self.tier_4_middle is None:
            self.tier_4_middle = AggregateCount()
        if self.tier_5_junior is None:
            self.tier_5_junior = AggregateCount()
        if self.tier_6_entry is None:
            self.tier_6_entry = AggregateCount()


# ============================================================
# LINKEDIN COLLECTOR (Using Browser Automation)
# ============================================================

class LinkedInResearchCollector:
    """
    LinkedIn data collector for research purposes
    Uses Selenium for browser automation
    
    IMPORTANT: 
    - Use a dedicated research account
    - Implement generous delays
    - Store only aggregates, not individual profiles
    """
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = None
        self.is_logged_in = False
        
        # Rate limiting settings (be gentle!)
        self.min_delay = 3  # seconds
        self.max_delay = 8  # seconds
        self.page_delay = 10  # seconds between pages
        
    def _random_delay(self):
        """Random delay to appear more human-like"""
        delay = random.uniform(self.min_delay, self.max_delay)
        time.sleep(delay)
    
    def setup_driver(self):
        """Initialize Selenium WebDriver"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            
            # Make browser appear more human-like
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--start-maximized')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=options)
            
            # Remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("WebDriver initialized successfully")
            return True
            
        except ImportError:
            logger.error("Selenium not installed. Run: pip install selenium webdriver-manager")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            return False
    
    def login(self, email: str, password: str) -> bool:
        """
        Login to LinkedIn
        WARNING: Use a research account, not your primary account
        """
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(3)  # Let page load fully
            
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.keys import Keys
            
            # Try multiple selector strategies for email field
            email_field = None
            for selector in [
                (By.ID, "username"),
                (By.NAME, "session_key"),
                (By.CSS_SELECTOR, "input[autocomplete='username']"),
                (By.CSS_SELECTOR, "input[type='text']")
            ]:
                try:
                    email_field = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(selector)
                    )
                    if email_field:
                        break
                except:
                    continue
            
            if not email_field:
                logger.error("Could not find email field - LinkedIn may have changed their page")
                logger.info(f"Current URL: {self.driver.current_url}")
                return False
            
            email_field.clear()
            email_field.send_keys(email)
            time.sleep(1)
            
            # Try multiple selector strategies for password field
            password_field = None
            for selector in [
                (By.ID, "password"),
                (By.NAME, "session_password"),
                (By.CSS_SELECTOR, "input[autocomplete='current-password']"),
                (By.CSS_SELECTOR, "input[type='password']")
            ]:
                try:
                    password_field = self.driver.find_element(*selector)
                    if password_field:
                        break
                except:
                    continue
            
            if not password_field:
                logger.error("Could not find password field")
                return False
            
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(1)
            
            # Click login button or press Enter
            try:
                login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                login_button.click()
            except:
                password_field.send_keys(Keys.RETURN)
            
            # Wait for login to complete
            time.sleep(8)
            
            # Check for verification/captcha
            current_url = self.driver.current_url
            if "checkpoint" in current_url or "challenge" in current_url:
                logger.warning("LinkedIn requires verification - please complete it in the browser")
                input("Press Enter after completing verification...")
                time.sleep(3)
            
            # Check if login successful
            current_url = self.driver.current_url
            if "feed" in current_url or "mynetwork" in current_url or "in/" in current_url:
                self.is_logged_in = True
                logger.info("Successfully logged in to LinkedIn")
                return True
            else:
                logger.warning("Login may have failed or requires verification")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def search_company_employees(
        self, 
        company_name: str,
        max_pages: int = 5,
    ) -> CompanyResearchData:
        """
        Search for company employees and collect aggregate gender/role data
        
        IMPORTANT: Only aggregates are stored, not individual profiles
        """
        if not self.is_logged_in:
            logger.error("Not logged in to LinkedIn")
            return None
        
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        result = CompanyResearchData(
            company_name=company_name,
            company_linkedin_url="",
            data_collection_date=datetime.now().isoformat(),
            methodology_notes="Automated collection from LinkedIn public profiles"
        )
        
        # Store raw data for detailed CSV (name hidden, only first letter)
        raw_entries = []
        
        try:
            # Search for company employees
            search_query = f"{company_name} employees"
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_query.replace(' ', '%20')}&origin=GLOBAL_SEARCH_HEADER"
            
            print(f"\n🔍 Searching: {search_url}")
            self.driver.get(search_url)
            time.sleep(self.page_delay)
            
            for page in range(max_pages):
                print(f"\n📄 Processing page {page + 1}/{max_pages}...")
                
                # Scroll to load all results
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
                # Find all profile cards on the page - try multiple selectors
                profile_cards = []
                selectors_to_try = [
                    ".entity-result",
                    ".reusable-search__result-container",
                    "li.reusable-search__result-container",
                    "[data-chameleon-result-urn]",
                    ".search-result__wrapper",
                    "div.entity-result__item",
                    "li.artdeco-list__item",
                ]
                
                for selector in selectors_to_try:
                    try:
                        cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if cards:
                            profile_cards = cards
                            print(f"   Found {len(cards)} profiles using selector: {selector}")
                            break
                    except:
                        continue
                
                if not profile_cards:
                    # Debug: print page source snippet
                    print(f"   ⚠️ No profiles found with any selector")
                    print(f"   Current URL: {self.driver.current_url}")
                    # Take screenshot for debugging
                    screenshot_path = Path("data/linkedin_research") / f"debug_page{page+1}.png"
                    screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                    self.driver.save_screenshot(str(screenshot_path))
                    print(f"   Screenshot saved to: {screenshot_path}")
                    break
                
                page_count = 0
                for idx, card in enumerate(profile_cards):
                    try:
                        # Debug: print card's inner HTML snippet
                        if idx == 0 and page == 0:
                            card_html = card.get_attribute('innerHTML')[:500]
                            print(f"   Debug - First card HTML snippet:\n   {card_html[:200]}...")
                        
                        # Extract name - try multiple selectors
                        name = ""
                        name_selectors = [
                            "span.entity-result__title-text a span[aria-hidden='true']",
                            ".entity-result__title-text span[aria-hidden='true']",
                            ".entity-result__title-text a",
                            ".entity-result__title-text",
                            "a.app-aware-link span[aria-hidden='true']",
                            ".artdeco-entity-lockup__title span[aria-hidden='true']",
                            ".artdeco-entity-lockup__title",
                            "span[dir='ltr']",
                        ]
                        for sel in name_selectors:
                            try:
                                name_elem = card.find_element(By.CSS_SELECTOR, sel)
                                name = name_elem.text.split('\n')[0].strip()
                                if name and "linkedin member" not in name.lower() and len(name) > 2:
                                    if idx == 0 and page == 0:
                                        print(f"   Debug - Found name '{name}' with selector: {sel}")
                                    break
                            except:
                                continue
                        
                        # Skip if no name found
                        if not name or "linkedin member" in name.lower() or len(name) < 2:
                            continue
                        
                        # Extract title - try multiple approaches
                        title = ""
                        title_selectors = [
                            ".entity-result__primary-subtitle",
                            "div.entity-result__primary-subtitle",
                            ".artdeco-entity-lockup__subtitle span",
                            ".artdeco-entity-lockup__subtitle",
                            ".entity-result__summary",
                            "div.linked-area + div",
                        ]
                        for sel in title_selectors:
                            try:
                                title_elem = card.find_element(By.CSS_SELECTOR, sel)
                                title = title_elem.text.strip()
                                if title:
                                    break
                            except:
                                continue
                        
                        # Fallback: get all text from card and extract title-like content
                        if not title:
                            try:
                                all_spans = card.find_elements(By.TAG_NAME, "span")
                                for span in all_spans:
                                    span_text = span.text.strip()
                                    # Skip if it's the name or too short
                                    if span_text and span_text != name and len(span_text) > 5:
                                        # Check if it looks like a job title (contains keywords)
                                        title_keywords = ["at", "engineer", "manager", "director", "lead", 
                                                         "analyst", "developer", "consultant", "vp", "head",
                                                         "chief", "ceo", "cto", "founder", "president",
                                                         "associate", "senior", "junior", "intern", "executive"]
                                        if any(kw in span_text.lower() for kw in title_keywords):
                                            title = span_text
                                            break
                            except:
                                pass
                        
                        # Extract first name and estimate gender
                        first_name = name.split()[0] if name else ""
                        gender = estimate_gender(first_name)
                        
                        # Classify role tier
                        tier = classify_title(title)
                        
                        # Print progress (anonymized - only first letter of name)
                        gender_sym = {"M": "♂", "F": "♀", "U": "?"}[gender]
                        tier_name = {1: "Board", 2: "C-Suite", 3: "Senior", 4: "Middle", 5: "Junior", 6: "Entry", 0: "Unknown"}
                        print(f"   {first_name[0]}*** | {gender_sym} | Tier {tier} ({tier_name[tier]}) | {title[:40]}...")
                        
                        # Store for CSV (anonymized)
                        raw_entries.append({
                            "first_initial": first_name[0] if first_name else "?",
                            "gender": gender,
                            "tier": tier,
                            "tier_name": tier_name[tier],
                            "title": title
                        })
                        
                        # Update aggregate counts (NO individual data stored)
                        tier_map = {
                            1: result.tier_1_board,
                            2: result.tier_2_csuite,
                            3: result.tier_3_senior,
                            4: result.tier_4_middle,
                            5: result.tier_5_junior,
                            6: result.tier_6_entry,
                        }
                        
                        if tier in tier_map:
                            tier_obj = tier_map[tier]
                            if gender == "M":
                                tier_obj.male += 1
                            elif gender == "F":
                                tier_obj.female += 1
                            else:
                                tier_obj.unknown += 1
                        
                        result.total_profiles_analyzed += 1
                        page_count += 1
                        
                    except Exception as e:
                        continue  # Skip problematic cards
                
                print(f"   ✓ Processed {page_count} profiles from page {page + 1}")
                
                self._random_delay()
                
                # Try to go to next page
                if page < max_pages - 1:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next']")
                        if next_button.is_enabled():
                            print(f"\n   ➡️ Going to page {page + 2}...")
                            next_button.click()
                            time.sleep(self.page_delay)
                        else:
                            print("   No more pages available")
                            break
                    except:
                        print("   No more pages available")
                        break
            
            # Store raw entries in result for detailed export
            result._raw_entries = raw_entries
            
            print(f"\n✅ Collection complete! Total: {result.total_profiles_analyzed} profiles")
            return result
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            import traceback
            traceback.print_exc()
            return result
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")


# ============================================================
# ALTERNATIVE: PUBLIC PROFILE URL APPROACH
# (No login required, but limited data)
# ============================================================

class PublicProfileCollector:
    """
    Collect data from public LinkedIn profiles without login
    More limited but lower risk
    """
    
    def __init__(self):
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_company_page(self, company_slug: str) -> dict:
        """
        Get public company page info
        Example: company_slug = "tcs" for TCS
        """
        url = f"https://www.linkedin.com/company/{company_slug}"
        
        try:
            response = self.session.get(url, timeout=10)
            # Note: LinkedIn may block this or require login
            # This is for demonstration of the approach
            return {"status": "check_manually", "url": url}
        except Exception as e:
            return {"error": str(e)}


# ============================================================
# SAVE RESULTS
# ============================================================

def save_research_data(data: CompanyResearchData, output_dir: str = "data/linkedin_research"):
    """Save research data to files (JSON and CSV)"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f"{data.company_name.replace(' ', '_')}_{timestamp}"
    
    # Save as JSON
    json_path = output_path / f"{base_filename}.json"
    
    # Convert to dict
    data_dict = {
        "company_name": data.company_name,
        "data_collection_date": data.data_collection_date,
        "total_profiles_analyzed": data.total_profiles_analyzed,
        "methodology_notes": data.methodology_notes,
        "tiers": {
            "tier_1_board": asdict(data.tier_1_board),
            "tier_2_csuite": asdict(data.tier_2_csuite),
            "tier_3_senior": asdict(data.tier_3_senior),
            "tier_4_middle": asdict(data.tier_4_middle),
            "tier_5_junior": asdict(data.tier_5_junior),
            "tier_6_entry": asdict(data.tier_6_entry),
        }
    }
    
    with open(json_path, "w") as f:
        json.dump(data_dict, f, indent=2)
    
    # Save as CSV (for easy analysis in Excel/Sheets)
    csv_path = output_path / f"{base_filename}.csv"
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Header row
        writer.writerow([
            "Company", "Tier", "Tier_Name", "Male", "Female", "Unknown", 
            "Total", "Female_Pct", "Collection_Date"
        ])
        
        # Data rows
        tiers = [
            (1, "Board", data.tier_1_board),
            (2, "C-Suite", data.tier_2_csuite),
            (3, "Senior Management", data.tier_3_senior),
            (4, "Middle Management", data.tier_4_middle),
            (5, "Junior Management", data.tier_5_junior),
            (6, "Entry Level", data.tier_6_entry),
        ]
        
        for tier_num, tier_name, tier_data in tiers:
            writer.writerow([
                data.company_name,
                tier_num,
                tier_name,
                tier_data.male,
                tier_data.female,
                tier_data.unknown,
                tier_data.total,
                tier_data.female_pct,
                data.data_collection_date
            ])
    
    logger.info(f"JSON saved to: {json_path}")
    logger.info(f"CSV saved to: {csv_path}")
    
    # Save detailed entries if available (anonymized)
    if hasattr(data, '_raw_entries') and data._raw_entries:
        detailed_csv = output_path / f"{base_filename}_detailed.csv"
        with open(detailed_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Company", "First_Initial", "Gender", "Tier", "Tier_Name", "Title"])
            for entry in data._raw_entries:
                writer.writerow([
                    data.company_name,
                    entry["first_initial"],
                    entry["gender"],
                    entry["tier"],
                    entry["tier_name"],
                    entry["title"]
                ])
        logger.info(f"Detailed CSV saved to: {detailed_csv}")
        return {"json": str(json_path), "csv": str(csv_path), "detailed_csv": str(detailed_csv)}
    
    return {"json": str(json_path), "csv": str(csv_path)}


def print_research_summary(data: CompanyResearchData):
    """Print summary of collected data"""
    print(f"\n{'='*60}")
    print(f"📊 RESEARCH DATA: {data.company_name}")
    print(f"{'='*60}")
    print(f"Date collected: {data.data_collection_date}")
    print(f"Total profiles analyzed: {data.total_profiles_analyzed}")
    print(f"\n{'Tier':<25} {'Male':<8} {'Female':<8} {'Unknown':<8} {'%Female':<8}")
    print("-" * 60)
    
    tiers = [
        ("Board", data.tier_1_board),
        ("C-Suite", data.tier_2_csuite),
        ("Senior Management", data.tier_3_senior),
        ("Middle Management", data.tier_4_middle),
        ("Junior Management", data.tier_5_junior),
        ("Entry Level", data.tier_6_entry),
    ]
    
    for name, tier in tiers:
        print(f"{name:<25} {tier.male:<8} {tier.female:<8} {tier.unknown:<8} {tier.female_pct:<8.1f}%")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║         LINKEDIN RESEARCH DATA COLLECTOR                          ║
    ║                                                                    ║
    ║  ⚠️  FOR ACADEMIC RESEARCH PURPOSES ONLY                          ║
    ║                                                                    ║
    ║  Before running:                                                   ║
    ║  1. Install: pip install selenium webdriver-manager               ║
    ║  2. Use a DEDICATED RESEARCH ACCOUNT (not your primary!)          ║
    ║  3. Review your institution's research ethics guidelines          ║
    ║                                                                    ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("""
    USAGE:
    
    from linkedin_collector import LinkedInResearchCollector
    
    collector = LinkedInResearchCollector()
    collector.login("research_email@example.com", "password")
    
    # Collect aggregate data (no individual profiles stored)
    data = collector.search_company_employees("Infosys", max_pages=5)
    
    # Save results
    save_research_data(data)
    print_research_summary(data)
    
    collector.close()
    """)
    
    # Demo with gender estimation
    print("\n" + "="*60)
    print("📋 GENDER ESTIMATION DEMO (from names)")
    print("="*60)
    
    test_names = [
        "Priya Sharma", "Rahul Gupta", "Ananya Singh", "Vikram Patel",
        "Neha Kapoor", "Arjun Reddy", "Divya Nair", "Karan Mehta"
    ]
    
    for name in test_names:
        first = name.split()[0]
        gender = estimate_gender(first)
        gender_label = {"M": "Male", "F": "Female", "U": "Unknown"}[gender]
        print(f"  {name:<20} → {gender_label}")
    
    print("\n" + "="*60)
    print("📋 TITLE CLASSIFICATION DEMO")
    print("="*60)
    
    test_titles = [
        "Chief Executive Officer",
        "Vice President, Engineering", 
        "Senior Software Engineer",
        "Product Manager",
        "Software Developer",
        "Data Analyst Intern",
    ]
    
    tier_names = {1: "Board", 2: "C-Suite", 3: "Senior", 4: "Middle", 5: "Junior", 6: "Entry", 0: "Unknown"}
    
    for title in test_titles:
        tier = classify_title(title)
        print(f"  {title:<35} → Tier {tier} ({tier_names[tier]})")
