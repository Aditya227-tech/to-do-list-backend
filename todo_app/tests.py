import datetime
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .models import TodoItem, TodoStatus

# Unit Tests
class TodoItemModelTests(TestCase):
    def setUp(self):
        self.todo_item = TodoItem.objects.create(
            title="Test Todo",
            description="Test Description",
            due_date=timezone.now() + datetime.timedelta(days=1)
        )

    def test_todo_item_creation(self):
        """
        Test that a TodoItem can be created successfully
        """
        self.assertEqual(self.todo_item.title, "Test Todo")
        self.assertEqual(self.todo_item.status, TodoStatus.OPEN)

    def test_todo_item_overdue_status(self):
        """
        Test automatic status change to OVERDUE
        """
        past_due_date = timezone.now() - datetime.timedelta(days=1)
        self.todo_item.due_date = past_due_date
        self.todo_item.save()

        self.assertEqual(self.todo_item.status, TodoStatus.OVERDUE)

# Integration Tests
class TodoItemAPITests(APITestCase):
    def setUp(self):
        """
        Set up test user and initial todo item
        """
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword123'
        )
        self.client.force_authenticate(user=self.user)

        self.todo_item = TodoItem.objects.create(
            title="Test API Todo",
            description="Test API Description",
            due_date=timezone.now() + datetime.timedelta(days=1),
            status=TodoStatus.OPEN
        )

    def test_create_todo_item(self):
        """
        Test creating a new todo item via API
        """
        data = {
            'title': 'New Todo Item',
            'description': 'Test Create API Endpoint',
            'status': TodoStatus.OPEN
        }
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Todo Item')

    def test_update_todo_item(self):
        """
        Test updating an existing todo item via API
        """
        update_data = {
            'status': TodoStatus.WORKING
        }
        response = self.client.patch(f'/api/todos/{self.todo_item.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], TodoStatus.WORKING)

    def test_delete_todo_item(self):
        """
        Test deleting a todo item via API
        """
        response = self.client.delete(f'/api/todos/{self.todo_item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TodoItem.objects.filter(id=self.todo_item.id).exists())

# End-to-End (E2E) Tests using Selenium
class TodoItemE2ETests(TestCase):
    def setUp(self):
        """
        Set up Selenium WebDriver for E2E testing
        """
        # Use headless Chrome for testing
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=chrome_options)

        # Create a test user
        self.user = User.objects.create_user(
            username='e2euser', 
            password='e2epassword123'
        )

    def test_create_todo_item(self):
        """
        E2E test to create a todo item
        """
        self.driver.get('http://localhost:8000/login/')

        # Login
        username_input = self.driver.find_element(By.ID, 'id_username')
        password_input = self.driver.find_element(By.ID, 'id_password')
        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_input.send_keys('e2euser')
        password_input.send_keys('e2epassword123')
        submit_button.click()

        # Navigate to todo creation page
        self.driver.get('http://localhost:8000/todos/create/')

        # Fill out todo form
        title_input = self.driver.find_element(By.ID, 'id_title')
        description_input = self.driver.find_element(By.ID, 'id_description')
        submit_todo_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')

        title_input.send_keys('E2E Test Todo')
        description_input.send_keys('This is an end-to-end test todo item')
        submit_todo_button.click()

        # Verify todo item was created
        todo_list = self.driver.find_element(By.ID, 'todo-list')
        self.assertIn('E2E Test Todo', todo_list.text)

    def test_update_todo_item(self):
        """
        E2E test to update a todo item
        """
        # Create a todo item first
        todo_item = TodoItem.objects.create(
            title='Update Test',
            description='Item to be updated',
            user=self.user
        )

        self.driver.get(f'http://localhost:8000/todos/{todo_item.id}/edit/')

        # Update todo item
        description_input = self.driver.find_element(By.ID, 'id_description')
        description_input.clear()
        description_input.send_keys('Updated description for E2E test')

        submit_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()

        # Verify update
        updated_todo = TodoItem.objects.get(id=todo_item.id)
        self.assertEqual(updated_todo.description, 'Updated description for E2E test')

    def tearDown(self):
        """
        Close the browser after tests
        """
        self.driver.quit()

# Selenium dependencies check
def test_selenium_dependencies():
    """
    Verify Selenium and webdriver are properly installed
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        return True
    except ImportError:
        return False