from crawling import run_crawling
from vectorization import run_vectorization

class Workflow:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def run(self):
        for step in self.steps:
            print(f"Starting step: {step.__name__}")
            step()
            print(f"Completed step: {step.__name__}")

if __name__ == "__main__":
    workflow = Workflow()
    workflow.add_step(run_crawling)
    workflow.add_step(run_vectorization)

    workflow.run()
