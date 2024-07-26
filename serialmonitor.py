import serial
import os
import csv
import time

SERIAL_PORT = "/dev/cu.STR-DH190"
OUT_FILEPATH = "./out/readings.csv"
READING_TIME_SECONDS = 60
READING_INTERVAL_SECONDS = 2 # Cannot be zero

NUM_SEGMENTS = 4
NUM_CELLS = 18
ROWS = [f"V{i}" for i in range(0, NUM_SEGMENTS * NUM_CELLS)]

def create_path(filepath):
    d = os.path.dirname(filepath)
    os.makedirs(d, exist_ok=True)

# https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def print_rows(data, num_rows):
    pad = len(max(data, key=len))
    for i, row in enumerate(split(data, num_rows)):
        padded_row = [s.ljust(pad) for s in row]
        print(f"Segment {i}: {" ".join(padded_row)}")

def main():
    start_time = time.time()
    num_readings = 0
    try:
        ser = serial.Serial(SERIAL_PORT, timeout=2)
        print(f"Connected to serial port `{ser.name}`")
    except serial.SerialException as e:
        print(f"Error opening serial port: \n{e}")
        return

    create_path(OUT_FILEPATH)
    try:
        with open(OUT_FILEPATH, "w") as f:
            writer = csv.writer(f)
            writer.writerow(ROWS)
            print_rows(ROWS, NUM_SEGMENTS)

            while True:
                try:
                    line = ser.readline().decode().strip()
                    if line:
                        values = line.split(',')
                        writer.writerow(values)
                        num_readings += 1

                        if len(values) == NUM_SEGMENTS * NUM_CELLS:
                            print_rows(values, NUM_SEGMENTS)
                        else:
                            print(values)
                except KeyboardInterrupt:
                    print("Interrupted by user. Exiting...")
                    break
                except Exception as e:
                    print(f"Error reading from serial port: \n{e}")
                finally:
                    if time.time() - start_time >= READING_TIME_SECONDS or num_readings == round(READING_TIME_SECONDS / READING_INTERVAL_SECONDS):
                        break
                    time.sleep(READING_INTERVAL_SECONDS)
    except IOError as e:
        print(f"IOError when opening {OUT_FILEPATH}:\n{e}")
    finally:
        print("Closing serial port")
        ser.close()


if __name__ == "__main__":
    main()
