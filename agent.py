import requests
from dotenv import load_dotenv
import os
import time

# Loading environment variable
load_dotenv()


class WebAgent:
    def __init__(self, name):
        self.name = name
        self.api_key = os.getenv("API_KEY")
        self.logs = []

    # Agents instrument
    def check_site(self, url):
        print(f"[{self.name}] Checking website: [{url}]...")
        try:
            response = requests.get(url, timeout=5)
            return response.status_code
        except Exception as e:
            return f"Error: {e}"

    # The agents brain (logic of decision making)
    def run_task(self, target_url):
        status = self.check_site(target_url)

        if status == 200:
            decision = "All is great! Continue watching."

        elif status == 404:
            decision = "Page not found. Check the URL."

        else:
            decision = f"Problem (Status: {status}). I will try to send a report through API..."
            # Here could have been logic of sending messages in Telegram/Slack
            if self.api_key:
                decision += f"[Using API_KEY: {self.api_key[:5]}***]"

        self.logs.append(decision)
        print(f"[{self.name}] Decision: {decision}")

    def run_multiple_tasks(self, urls):
        print(f"\n--- [{self.name}] Starting mass cehck ---")
        for url in urls:
            self.run_task(url)
        print(f"---Checking complete. Logs summary: {len(self.logs)} ---\n")

    def show_logs(self):
        print("--- Agent's work history ---")
        for log in self.logs:
            print(log)


# Running our first agent
if __name__ == "__main__":
    my_agent = WebAgent(name="Watcher -01")

    # Creating list of sites for checking
    sites_to_check = [
        "https://google.com",
        "https://github.com",
        "https://yandex.ru",
        "https://google.com/error-page",
    ]

    # Launching mass check
    my_agent.run_multiple_tasks(sites_to_check)
    my_agent.show_logs()
