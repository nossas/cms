from locust import HttpUser, task

class SimulateRequestOverUser(HttpUser):
    
    @task
    def index(self):
        self.client.get("/")

    @task
    def list(self):
        self.client.get("/candidaturas/")
    
    @task
    def admin(self):
        self.client.get("/admin")
    
    @task
    def not_found(self):
        self.client.get("/not_found/asdasdasd")
    
    @task
    def form(self):
        self.client.get("/candidaturas/cadastro/")