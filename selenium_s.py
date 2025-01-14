import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pymongo
import uuid

# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://jokerdeva18:zTXXIMgCE6kdvqIB@cluster0.31bwl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["twitter_trends"]
collection = db["trending_topics"]

# ProxyMesh credentials
proxymesh_username = "Arise"  # Replace with your ProxyMesh username
proxymesh_password = "Arise@123"  # Replace with your ProxyMesh password

# ProxyMesh setup
proxy = f"http://{proxymesh_username}:{proxymesh_password}@us-ca.proxymesh.com:31280"
options = webdriver.ChromeOptions()
# options.add_argument(f"--proxy-server={proxy}")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")

# Test ProxyMesh connectivity
try:
    response = requests.get("https://api.ipify.org?format=json", proxies={"http": proxy, "https": proxy}, timeout=10)
    if response.status_code == 200:
        print("ProxyMesh is working!")
        print("IP via ProxyMesh:", response.json()["ip"])
    else:
        print(f"Failed ProxyMesh test with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error testing ProxyMesh: {e}")
    exit()

# Selenium WebDriver setup
driver = webdriver.Chrome(options=options)
print("Selenium WebDriver initialized with ProxyMesh.")

try:
    # Step 1: Open Twitter Login Page
    driver.get("https://x.com/i/flow/login")

    # Step 2: Enter Username
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    username.send_keys("jokerdeva18@gmail.com")  # Replace with your Twitter username
    username.send_keys(Keys.RETURN)

    try:
        email_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email_field.clear()
        email_field.send_keys("@Arise286327")  # Replace with your email or username
        email_field.send_keys(Keys.RETURN)
    except Exception:
        try:
              username = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, "text"))
    )
              username.send_keys("Arise286327")  # Replace with your username
              username.send_keys(Keys.RETURN)
        except Exception:
           print("No additional email/username verification required.")
    

    # Step 3: Enter Password
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password.send_keys("Arise@123")  # Replace with your Twitter password
    password.send_keys(Keys.RETURN)

    # Step 4: Wait for Homepage to Load
    # Wait for the "Trending now" section
    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']"))
    # )

    # Scrape the top 5 trending topics
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='trend']"))
    )
    
    trending_topics = []
    for element in driver.find_elements(By.XPATH, "//div[@data-testid='trend']"):
          trend_text = element.text  
          if trend_text:  
              trend_data = trend_text.split("\n")  # Split by newline to separate the sections
              topic = trend_data[0]  # Extract the category (e.g., Entertainment, Politics)
              name = trend_data[1]  # Extract the trend name
              posts = trend_data[2] if len(trend_data) > 2 else "N/A"  # Extract posts count if available
              trending_topics.append({"category": topic, "name": name, "posts": posts})

    # Step 6: Store Data in MongoDB
    unique_id = str(uuid.uuid4())
    end_time = datetime.now()
    record = {
        "_id": unique_id,
        "trending_topics": trending_topics,
        "end_time": end_time,
        "ip_address": response.json()["ip"]  # Save the IP obtained via ProxyMesh
    }
    collection.insert_one(record)
    print("Data saved:", record)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
