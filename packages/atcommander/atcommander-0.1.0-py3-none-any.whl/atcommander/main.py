import time
import serial
import csv

from .arg_parser import get_parser


def read_all(ser, chunk_size=200):
    """Read all characters on the serial port and return them."""
    if not ser.timeout:
        raise TypeError('Port needs to have a timeout set!')

    read_buffer = b''

    while True:
        # Read in chunks. Each chunk will wait as long as specified by
        # timeout. Increase chunk_size to fail quicker
        byte_chunk = ser.read(size=chunk_size)
        read_buffer += byte_chunk
        if not len(byte_chunk) == chunk_size:
            break

    return read_buffer


def app(name="ATCommander"):
    print(f"{name} start...")

    # parse args
    args = get_parser().parse_args()

    with open(args.config, "r") as f:
        f.seek(0)
        csv_reader = csv.reader(f)
        with serial.Serial(args.serial_port, args.baudrate, parity=args.parity, timeout=args.interval) as ser:
            for row in csv_reader:
                if not row or len(row) == 0:
                    continue
                command = row[0]
                print(f"write: {command}")
                ser.write((command + '\r\n').encode())
                ser.flush()
                response = read_all(ser)
                print(f"receive: {response.decode()}")
                time.sleep(args.interval)


if __name__ == "__main__":
    app()
