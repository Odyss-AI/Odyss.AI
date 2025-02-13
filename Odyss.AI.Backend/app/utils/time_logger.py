import time
import logging

class TimeLogger:
    def __init__(self, name: str):
        self.name = name
        self.start_time = time.time()
        self.part_time = time.time()

    def exit_func(self, label, next_label):
        print(f"{label} took {time.time() - self.part_time} seconds")
        logging.info(f"{label} took {time.time() - self.part_time} seconds")
        self.part_time = time.time()
        print(f"Next step: {next_label}")

    def exit_process(self):
        print(f"Total time for {self.name} was {time.time() - self.start_time} seconds")
        logging.info(f"Total time for {self.name} was {time.time() - self.start_time} seconds")