import csv
from lib.Conversions import Conversions


class CanData:
    def __init__(self):
        self.messages = []
        self.results = {}

    def read_can_sample(self, file):
        with open(file, 'r') as f:
            reader = csv.reader(f)

            for r in reader:
                if len(r) == 0:
                    continue
                cid = r.pop(0)
                m = SampleMessage(cid, r)
                self.messages.append(m)
        print("read sample data file")

    def process_sample_data(self, message_parser):
        print(f"Going to process {len(self.messages)} messages")
        for m in self.messages:
            message_parser.parse_data_message(m)

        res = message_parser.result()
        for r in res:
            pass
            # Conversions.dispatch(r)


class SampleMessage:
    def __init__(self, cid, data):
        self.cid = cid
        self.data = data
