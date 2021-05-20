import json


class MessageParser:
    def __init__(self):
        self.can_messages = []
        self.data_message_counter = 0
        self.results = {}

    def register_can_message(self, can_message):
        self.can_messages.append(can_message)

    def state(self):
        return f"Currently registered {len(self.can_messages)} template can messages"

    def parse_data_message(self, message):
        for tm in self.can_messages:
            if tm.cid == message.cid:
                print(f"Parsing message {message.cid}")
                self.results[self.data_message_counter] = tm.handle_data(message.data)
                self.data_message_counter += 1
            else:
                print(f"Message unknown ({message.cid})")

    def result(self):
        return self.results

    def load_messages(self, file):
        with open(file, 'r') as f:
            raw_messages = json.loads(f.read())

        for m in raw_messages:
            cid = m
            clen = raw_messages[m]['clen']
            desc = raw_messages[m]['desc']
            source = raw_messages[m]['source']

            # load up the message itself
            message = CanMessage(cid, clen, desc, source)

            for df in raw_messages[m]['data_frames']:
                offset = df
                length = raw_messages[m]['data_frames'][df]['length']
                descr = raw_messages[m]['data_frames'][df]['desc']
                pname = raw_messages[m]['data_frames'][df]['phonetic_name']

                # build data frame and register it
                data_frame = DataFrame(offset, length, descr, pname)
                message.register_data_frame(data_frame)

            # register the message itself
            self.register_can_message(message)


class CanMessage:
    def __init__(self, cid, clen_expected, desc, source):
        self.cid = cid
        self.clen_expected = clen_expected
        self.desc = desc
        self.source = source
        self.data_frames = []
        self.results = {}

    def register_data_frame(self, data_frame):
        self.data_frames.append(data_frame)

    def handle_data(self, data):
        for df in self.data_frames:
            self.results[df.phonetic_name] = df.extract_data(data)

        r = self.results
        self.results = {}
        return r


class DataFrame:
    def __init__(self, offset, length, desc, phonetic_name):
        self.offset = int(offset)
        self.length = int(length)
        self.desc = str(desc)
        self.phonetic_name = str(phonetic_name)

    def extract_data(self, data):
        hex_data = data[self.offset:self.offset+self.length]
        dec_data = []
        bin_data = []
        for h in hex_data:
            target = int(h, 16)
            dec_data.append(target)
            bin_data.append(bin(target))

        return {
            "phonetic_name": self.phonetic_name,
            "hex_data": hex_data,
            "dec_data": dec_data,
            "bin_data": bin_data,
        }
