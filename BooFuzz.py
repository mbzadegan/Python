import os
import sys
from boofuzz import *
from boofuzz.connections import TCPSocketConnection

def main():
    if len(sys.argv) != 3:
        print("Usage: python boofuzz.py <target_ip> <port>")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])

    # Create logs directory
    log_dir = "./boofuzz_logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "http_fuzz.log")

    # Set up target
    target = Target(connection=TCPSocketConnection(target_ip, target_port))

    # Set up logger
    log_file = open(log_path, "w")

    # Define session
    session = Session(
        target=target,
        session_filename=os.path.join(log_dir, "session.json"),
        fuzz_loggers=[FuzzLoggerText(log_file)],
        crash_threshold_request=1,
        sleep_time=0.25,
    )

    # Define HTTP GET fuzz
    s_initialize("HTTP GET Fuzz")
    if s_block_start("request-line"):
        s_string("GET", fuzzable=False)
        s_delim(" ", fuzzable=False)
        s_string("/", name="path")
        s_delim(" ", fuzzable=False)
        s_string("HTTP/1.1", fuzzable=False)
        s_static("\r\n")
    s_block_end("request-line")

    s_string("Host: fuzzed\r\n", fuzzable=False)
    s_string("User-Agent: boofuzz\r\n", fuzzable=True)
    s_string("Accept: */*\r\n", fuzzable=True)
    s_static("\r\n")

    # Run fuzz
    session.connect(s_get("HTTP GET Fuzz"))
    try:
        session.fuzz()
    except Exception as e:
        print(f"Fuzzing stopped: {e}")

if __name__ == "__main__":
    main()
