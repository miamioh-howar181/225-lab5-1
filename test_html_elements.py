from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import unittest
import time

class TestTasks(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_tasks_display(self):
        driver = self.driver
        driver.get("http://10.48.10.181")  # Update with your app’s URL

        # Wait briefly for the page to load
        time.sleep(2)

        # Check that the page title or header indicates the task app
        self.assertIn("Task", driver.page_source)

        # Optionally: Check if any pre-existing task elements are present
        task_rows = driver.find_elements(By.XPATH, "//table//tr")
        self.assertGreater(len(task_rows), 1, "No tasks found in the table")

    def test_add_task(self):
        driver = self.driver
        driver.get("http://10.48.10.181")
        time.sleep(2)

        # Enter task description
        desc_input = driver.find_element(By.NAME, "description")
        desc_input.send_keys("Test Task")

        # Select status from dropdown
        status_dropdown = driver.find_element(By.NAME, "status")
        for option in status_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.text == "Pending":
                option.click()
                break

        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit_button.click()

        time.sleep(2)  # Wait for reload

        # Verify that the new task appears on the page
        self.assertIn("Test Task", driver.page_source)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
