from locust import HttpUser, task


class QuickstartUser(HttpUser):
    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/accounts/jwt/create/",
            data={"email": "admin@admin.com", "password": "useradmin123"},
        ).json()
        self.client.headers = {"Authorization": f"Bearer {response.get('access')}"}

    @task
    def post_list_api(self):
        self.client.get("/blog/api/v1/posts/")

    @task
    def post_category_api(self):
        self.client.get("/blog/api/v1/categories/")
