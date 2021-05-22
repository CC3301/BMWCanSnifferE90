import argparse
from lib.CanMessage import *
from lib.CanData import *


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    args = parser.parse_args()

    # setup the templates and message parser
    message_parser = MessageParser()
    message_parser.load_messages("data/messages.json")

    # setup the data handler to handle the CAN-Sample
    data_handler = CanData()
    data_handler.read_can_sample(args.file)

    # parse the sample data
    data_handler.process_sample_data(message_parser)


if __name__ == "__main__":
    main()
