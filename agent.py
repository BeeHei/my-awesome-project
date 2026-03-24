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

        elif status == 400:
            decision = "Page not found. Check the URL."

        else:
            decision = f"Problem (Status: {status}). I will try to send a report through API..."
            # Here could have been logic of sending messages in Telegram/Slack
            if self.api_key:
                decision += f"[Using API_KEY: {self.api_key[:5]}***]"

        self.logs.append(decision)
        print(f"[{self.name}] Decision: {decision}")


# Running our first agent
if __name__ == "__main__":
    my_agent = WebAgent(name="Watcher -01")

    # Giving agent a task
    my_agent.run_task("https://google.com")
    my_agent.run_task("https://google.com/non-existent-page")
