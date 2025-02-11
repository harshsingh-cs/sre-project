from locust import HttpUser, task, between

class WebUser(HttpUser):
    wait_time = between(1, 3)

    
    host = "http://localhost:7100"  

    @task(3)
    def load_homepage(self):
        """Request the home page."""
        self.client.get("/", allow_redirects=False)  

    @task(1)
    def health_check(self):
        """Call the health check endpoint without a trailing slash."""
        self.client.get("/health", allow_redirects=False)  

    @task(2)
    def send_post_request(self):
        """Simulate sending a POST request."""
        self.client.post("/health", json={"message": "test payload"}, allow_redirects=False)  
