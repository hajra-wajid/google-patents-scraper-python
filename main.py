import time
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# 0. Configure WebDriver with Enhanced Headless Settings
# -------------------------------
gecko_driver_path = r"C:\firefox_webdriver\geckodriver.exe"
service = Service(gecko_driver_path)

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

# Anti-detection and performance preferences
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("useAutomationExtension", False)
options.set_preference("general.useragent.override", 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0")
options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("javascript.enabled", True)
options.set_preference("browser.cache.disk.enable", False)
options.set_preference("browser.cache.memory.enable", False)

driver = webdriver.Firefox(
    service=service,
    options=options
)
driver.implicitly_wait(10)  # Global implicit wait

# -------------------------------
# 1. Read patent numbers from file
# -------------------------------
with open(r'Northrop Grumman Newport News_patents.txt', 'r') as f:
    patent_numbers = [line.strip() for line in f]

# -------------------------------
# 2. Initialize data storage
# -------------------------------
data = []

# -------------------------------
# 3. Patent Processing Loop
# -------------------------------
for patent_num in patent_numbers:
    try:
        print(f"\nProcessing {patent_num}...")
        
        # -------------------------------
        # 3a. Page Navigation
        # -------------------------------
        url = f"https://patents.google.com/patent/{patent_num}"
        driver.get(url)
        
        # Verify page load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.scroll-target")))
        except:
            print(f"Core content failed to load for {patent_num}")
            continue

        # -------------------------------
        # 3b. Data Extraction Sections
        # -------------------------------
        # Publication Number
        pub_num = ""
        try:
            pub_num = driver.find_element(By.ID, "pubnum").text
            print(f"Found publication number: {pub_num}")
        except:
            pass

        # Applicant (Patent Holder)
        applicant = ""
        try:
            assignee = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//dt[contains(., 'Current Assignee')]/following-sibling::dd[1]"))
            ).text.strip()
            applicant = assignee
            print(f"Found applicant: {applicant}")
        except:
            pass

        # Patent Family: Child Applications
        child_apps = []
        child_country = ""
        try:
            child_h3 = driver.find_element(By.XPATH, "//h3[contains(text(), 'Child Applications')]")
            table_div = child_h3.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'responsive-table')]")
            app_elements = table_div.find_elements(By.XPATH, ".//span[@class='td nowrap style-scope patent-result']/state-modifier/a")
            child_apps = [elem.text for elem in app_elements]
            if child_apps:
                first_app = child_apps[0].split(';')[0].strip()
                match = re.match(r"([A-Za-z]+)", first_app)
                child_country = match.group(1) if match else ""
            print(f"Found {len(child_apps)} child applications")
        except:
            pass

        # Patent Family: Priority Applications
        priority_apps = []
        priority_country = ""
        try:
            priority_h3 = driver.find_element(By.XPATH, "//h3[contains(text(), 'Priority Applications')]")
            table_div = priority_h3.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'responsive-table')]")
            app_elements = table_div.find_elements(By.XPATH, ".//span[@class='td nowrap style-scope patent-result']/state-modifier/a")
            priority_apps = [elem.text for elem in app_elements]
            if priority_apps:
                first_app1 = priority_apps[0].split(';')[0].strip()
                match = re.match(r"([A-Za-z]+)", first_app1)
                priority_country = match.group(1) if match else ""
            print(f"Found {len(priority_apps)} priority applications")
        except:
            pass

        # Invention Name
        invention_name = ""
        try:
            title_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.scroll-target"))
            )
            invention_name = title_element.text.strip()
            print(f"Found invention name: {invention_name}")
        except:
            pass

        # Abstract
        abstract = ""
        try:
            abstract_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "div.abstract.style-scope.patent-text"))
            )
            abstract = abstract_element.text.strip()
        except:
            pass

        # Description
        description = ""
        try:
            desc_elements = driver.find_elements(By.CSS_SELECTOR, "#description")
            description = "\n".join([elem.text for elem in desc_elements if elem.text])
            print(f"Description length: {len(description)} characters")
        except:
            pass

        # Claims
        claims = ""
        try:
            claim_elements = driver.find_elements(By.CSS_SELECTOR, "div.flex:nth-child(2)")
            claims = "\n".join([elem.text for elem in claim_elements if elem.text])
            print(f"Claims length: {len(claims)} characters")
        except:
            pass

        # CPC Classification
        cpc_classes = []
        try:
            more_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "more"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_button)
            driver.execute_script("arguments[0].click();", more_button)
            
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'state-modifier.code a')))
            codes = driver.find_elements(By.CSS_SELECTOR, 'state-modifier.code a')
            cpc_classes = [code.text.strip() for code in codes if code.text.strip()]
            print(f"Found {len(cpc_classes)} CPC classes")
        except Exception as e:
            print(f"CPC extraction error: {str(e)}")

        # Inventors
        inventors = []
        try:
            people_section = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "important-people")))
            inventor_elements = people_section.find_elements(By.XPATH, './/dt[contains(text(), "Inventor")]/following-sibling::dd//a[@id="link"]')
            inventors = [inventor.text for inventor in inventor_elements]
            print(f"Found {len(inventors)} inventors")
        except:
            pass

        # -------------------------------
        # 3c. Timeline Events Processing
        # -------------------------------
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        application_date = pub_date = status_txt = anticipated_date = ""

        events = soup.select('div.event.layout.horizontal.style-scope.application-timeline[critical]')
        for event in events:
            title_el = event.select_one("span.title-text.style-scope.application-timeline")
            # Application Date
            if title_el and "Application filed" in title_el.text:
                date_el = event.select_one("div.filed.style-scope.application-timeline")
                application_date = date_el.text.strip() if date_el else ""
            
            # Publication Date
            if title_el and "Publication of " in title_el.text:
                pub_title = title_el.text.strip().replace("Publication of ", "")
                pub_date_elem = event.select_one("div.publication.style-scope.application-timeline")
                if pub_date_elem and pub_title == pub_num:
                    pub_date = pub_date_elem.text.strip()
            
            # Status
            if title_el and any(word in title_el.text for word in ["Active", "Pending", "Expired","Abandoned"]):
                status_txt = title_el.text.strip()
            
            # Anticipated Expiration
            anticipated_expiration = event.select_one("div.legal-status.style-scope.application-timeline")
            if anticipated_expiration and "Status" not in (ant_date := anticipated_expiration.text.strip()):
                anticipated_date = ant_date

        # -------------------------------
        # 3d. Data Structuring
        # -------------------------------
        for inventor in inventors:
            parts = inventor.split()
            if len(parts) >= 3 and parts[1].endswith('.'):
                first_name = ' '.join(parts[:2])
                last_name = ' '.join(parts[2:])
            elif len(parts) >= 2:
                first_name = parts[0]
                last_name = ' '.join(parts[1:])
            else:
                first_name = inventor
                last_name = ''

            researcher = f"{first_name}, {last_name}".strip()

            row = {
                "Patent Application #": patent_num,
                "Application Date": application_date,
                "Applicant (patent holder)": applicant,
                "Patent Family: Child": "; ".join(child_apps),
                "Patent Family Country": child_country,
                "Patent Family: Priority": "; ".join(priority_apps),
                "Patent Family Country (Priority)": priority_country,
                "Invention Name": invention_name,
                "Summary / Abstract": abstract,
                "Description": description,
                "Claims": claims,
                "Publication #": pub_num,
                "Publication Date": pub_date,
                "CPC Classification Number": "; ".join(cpc_classes),
                "Status": status_txt,
                "Anticipated expiration": anticipated_date,
                "Researcher": researcher,
                "First Name": first_name,
                "Last Name": last_name
            }
            data.append(row)
            print(f"Added entry for inventor: {researcher}")

    except Exception as e:
        print(f"Critical error processing {patent_num}: {str(e)}")
        continue

# -------------------------------
# 4. Save Results
# -------------------------------
df = pd.DataFrame(data)
df.to_excel("Un2_patents_data.xlsx", index=False)
print("\nSaved data to Un2_patents_data.xlsx")

# -------------------------------
# 5. Cleanup
# -------------------------------
driver.quit()
print("Process completed successfully")