import argparse
import sys
import time
import serial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--serial')
    parser.add_argument('-b', '--baud')
    parser.add_argument('-f', '--file')

    args = parser.parse_args()
    ser = open_serial(args.serial, args.baud)

    last_second = time.time()
    time_started = time.time()
    last_second_bytes = 0
    total_kilo_bytes = 0

    with open(args.file, 'w') as outfile:
        try:
            while True:
                try:
                    data_raw = ser.readline()
                except serial.serialutil.SerialException:
                    print(f"Connection to arduino lost after {(time.time() - time_started) / 60} minutes "
                          f"and {total_kilo_bytes} KB of data")
                    sys.exit(1)

                # calculate the speed at which data is coming from the arduino
                current_time = time.time()
                if current_time - last_second > 1:
                    print(f"reading Kbps: {last_second_bytes / 1000}", end="\r")
                    last_second = current_time
                    total_kilo_bytes += last_second_bytes/1000
                    last_second_bytes = 0
                else:
                    last_second_bytes += len(data_raw)

                # decode the data and store it in the file
                try:
                    string = data_raw.decode('UTF-8')
                    outfile.write(str(string.rstrip()) + "\n")
                except UnicodeDecodeError as e:
                    pass
        except KeyboardInterrupt:
            print(f"Connection to arduino lost after {(time.time() - time_started) / 60} minutes "
                  f"and {total_kilo_bytes} KB of data")
            sys.exit(1)


def open_serial(port, baud):
    ser = serial.Serial(str(port), str(baud))
    ser.flushInput()
    ser.flushOutput()
    return ser


if __name__ == "__main__":
    main()
