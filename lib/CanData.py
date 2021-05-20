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
                cid = r.pop(0)
                m = SampleMessage(cid, r)
                self.messages.append(m)

    def state(self):
        return f"Going to process {len(self.messages)} messages"

    def process_sample_data(self, message_parser):
        for m in self.messages:
            message_parser.parse_data_message(m)

        res = message_parser.result()
        print(res)
        for r in res:
            Conversions.dispatch(r)


class SampleMessage:
    def __init__(self, cid, data):
        self.cid = cid
        self.data = data
