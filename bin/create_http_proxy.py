#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Set up Firefox WebDriver
firefox_options = Options()
firefox_options.headless = True
firefox_options.add_argument("--disable-gpu")
browser = webdriver.Firefox(options=firefox_options)

# Navigate to Nexus login page
nexus_host = os.environ.get("NEXUS_HOST")
browser.get(f"https://{nexus_host}")

# Log in to Nexus
username = os.environ.get("NEXUS_USERNAME")
password = os.environ.get("NEXUS_PASSWORD")
username_field = browser.find_element(By.ID, "username")
password_field = browser.find_element(By.ID, "password")
username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

# Wait for login to complete
WebDriverWait(browser, 10).until(EC.url_contains("dashboard"))

# Navigate to HTTP Proxy settings page
browser.get(f"https://{nexus_host}/#admin/system/http")

# Enable HTTP Proxy
enable_http_proxy_checkbox = browser.find_element(By.ID, "enable-http-proxy")
enable_http_proxy_checkbox.click()

# Fill in HTTP Proxy Host and Port
http_proxy_host_field = browser.find_element(By.ID, "http-proxy-host")
http_proxy_port_field = browser.find_element(By.ID, "http-proxy-port")
http_proxy_host = os.environ.get("NEXUS_PROXY_HOST")
http_proxy_port = os.environ.get("NEXUS_PROXY_PORT")
http_proxy_host_field.clear()
http_proxy_host_field.send_keys(http_proxy_host)
http_proxy_port_field.clear()
http_proxy_port_field.send_keys(http_proxy_port)

# Enable HTTPS Proxy
enable_https_proxy_checkbox = browser.find_element(By.ID, "enable-https-proxy")
enable_https_proxy_checkbox.click()

# Fill in HTTPS Proxy Host and Port
https_proxy_host_field = browser.find_element(By.ID, "https-proxy-host")
https_proxy_port_field = browser.find_element(By.ID, "https-proxy-port")
https_proxy_host_field.clear()
https_proxy_host_field.send_keys(http_proxy_host)
https_proxy_port_field.clear()
https_proxy_port_field.send_keys(http_proxy_port)

# Save changes
save_button = browser.find_element(By.XPATH, '//button[@data-cy="button-primary"]')
save_button.click()

# Close the browser
browser.quit()

