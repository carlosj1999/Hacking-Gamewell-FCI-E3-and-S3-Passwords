import serial
import time

# Serial port configuration
SERIAL_PORT = "/dev/ttyS3"
BAUD_RATE = 115200
TIMEOUT = 2

# Commands to retrieve data from different nodes
COMMANDS = [
    "18 0b 0a 00 45 01 80 80 00 00 00 58 b4",
    "18 0b 05 00 45 01 80 00 01 00 00 50 5e",
    "18 0b 00 00 45 01 80 00 2f 00 00 97 c3",
    "18 0b 00 00 45 01 80 80 2f 00 00 af 1e",
    "18 0b 00 00 45 01 80 80 29 00 00 0f ac",
    "18 0b 00 00 45 01 80 80 2e 00 00 9f 29",
    "18 0b 00 00 45 01 80 80 33 00 00 ad 28",
]

def extract_password(response_hex):
    """Extracts potential password patterns from the raw response data."""
    hex_bytes = [response_hex[i:i + 2] for i in range(0, len(response_hex), 2)]

    # Check for patterns of repeated hex values indicating passwords
    patterns = {}
    for i in range(len(hex_bytes) - 2):
        if hex_bytes[i] == hex_bytes[i + 1] == hex_bytes[i + 2]:
            patterns[f"Level {len(patterns) + 1} Password"] = hex_bytes[i] * 3

    return patterns if patterns else {"Message": "No password pattern found"}

def send_hex_command(command, ser):
    """Sends a hex command to the panel and reads the response."""
    command_bytes = bytes.fromhex(command)
    ser.write(command_bytes + b'\r')  # Append a carriage return (CR)
    time.sleep(1)  # Allow time for the panel to respond
    response = ser.read(1024)  # Adjust buffer size as needed
    return response

def main():
    try:
        # Initialize serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
        print("Serial connection established.")

        # Send commands and extract password information
        for command in COMMANDS:
            print(f"Sending command: {command}")
            response_data = send_hex_command(command, ser)
            response_hex = response_data.hex()
            print(f"Received response: {response_hex}")

            # Analyze response
            extracted_passwords = extract_password(response_hex)
            for level, password in extracted_passwords.items():
                print(f"{level}: {password}")

        # Close the serial connection
        ser.close()
        print("Serial connection closed.")

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
