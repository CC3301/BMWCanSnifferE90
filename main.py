import json
from lib.CanMessage import *
from lib.CanData import *


def main():

    # setup the templates and message parser
    message_parser = MessageParser()
    message_parser.load_messages("data/messages.json")
    print(message_parser.state())

    # setup the data handler to handle the CAN-Sample
    data_handler = CanData()
    data_handler.read_can_sample("data/sample_messages.csv")
    print(data_handler.state())

    # parse the sample data
    data_handler.process_sample_data(message_parser)



if __name__ == "__main__":
    main()
