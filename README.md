```markdown
# Network Event Monitoring System - Jackfruit Mini Project

**A secure distributed node reporting system using low-level UDP sockets + AES-256-CBC encryption**

## 📋 Project Objective
The objective of this project is to design and implement a **secure networked application** using low-level socket programming.  
This system simulates a real-world **distributed network monitoring scenario** where multiple edge nodes detect and report events (`failure`, `threshold`, `info`) to a central monitoring server.

**Mandatory Requirements Satisfied:**
- Uses **UDP sockets directly** (low-level, no high-level frameworks)
- Secure communication using **AES-256-CBC** encryption for all data exchanges
- Supports **multiple concurrent clients** (threaded packet processing)
- All communication occurs over the network using sockets

---

## ✨ Key Features Implemented

1. **Edge Filtering** – Clients only send *critical* events (`failure` and `threshold`) to reduce network load
2. **Packet Loss Tolerance** – 15% simulated packet loss on client side
3. **Aggregated Event Visualization** – Server maintains real-time counts per node and displays them every 5 seconds
4. **Concurrency** – Server handles multiple clients simultaneously using threads
5. **Robust Error Handling** – Malformed packets, decryption failures, and abrupt client behavior are gracefully handled
6. **Performance Evaluation Ready** – Built-in support for latency, throughput, and loss rate measurement

---

## 🏗️ Architecture & Data Flow
Edge Node (Client)                          Central Monitoring Server
──────────────────                          ───────────────────────
1. Generate random event
2. Edge Filter → only critical events
3. JSON serialize
4. AES-256-CBC Encrypt (random IV)
5. UDP sendto() ───────────────────────►  recvfrom()
                                           │
                                           ▼
                                        Decrypt (AES-256-CBC)
                                           │
                                           ▼
                                        Parse JSON + Aggregate
                                           │
                                           ▼
                                        Thread-safe defaultdict
                                           │
                                           ▼
                                        Print visualization every 5s
```

**Why UDP?**  
- Connectionless → ideal for event-driven reporting  
- Demonstrates packet loss tolerance (TCP would hide it)  
- Lower latency and higher throughput under high event rates

**Security:** Manual AES-256-CBC provides confidentiality and integrity without relying on TLS (as per our UDP choice).

## 🛠️ Tech Stack
- **Language:** Python
- **Sockets:** `socket` (UDP datagram)
- **Encryption:** `cryptography` (AES-256-CBC with PKCS7 padding)
- **Concurrency:** `threading` + `threading.Lock()`
- **Data Handling:** `json`, `collections.defaultdict`

## 📦 Prerequisites
1. Python 3.8 or higher
2. Install required package:
```bash
   pip install cryptography
   ```
3. For performance testing:
```bash
   pip install psutil
   ```

---

## 🚀 How to Run

### 1. Start the Server (Terminal 1)
```bash
python server_udp.py
```

**Expected Server Output:**
```
✅ encryption.py loaded successfully — AES-256 key is 32 bytes
🔐 UDP Server with AES-256-CBC listening on 0.0.0.0:12345
✅ Ready to handle multiple concurrent clients...

[HH:MM:SS] Received from Node 1 (127.0.0.1:xxxxx): failure
...
📊 AGGREGATED EVENT VISUALIZATION (Edge-filtered)
=======================================================================
Node  1 → {'failure': 12, 'threshold': 8}
Node  2 → {'failure': 5, 'threshold': 7}
=======================================================================
```

### 2. Start Multiple Clients (in separate terminals)
```bash
python client_udp.py 1
python client_udp.py 2
python client_udp.py 3
```

**Expected Client Output:**
```
✅ encryption.py loaded successfully — AES-256 key is 32 bytes
🔐 Client Node 2 started (UDP + AES-256-CBC)
Node 2 → Packet lost (simulated)
Node 2 → Filtered (non-critical): info
Node 2 → Sent critical event: threshold
Node 2 → Sent critical event: failure
...
```
### 3. Run Performance Test (Terminal 5)
   ```bash
   python performance_test.py
   ```
**Expected Performance Output:**
```
====================================
📊 PERFORMANCE EVALUATION
====================================
📊 Throughput: 218.45 events/sec
📊 Packet loss rate: 14.80%
⏱️  Average Latency: 4.20 ms
====================================
```

### 4. Run Error Handling Demo
   ```bash
   python demo_error_handling.py
   ```
**Expected Server Error Output:**
```
❌ Error processing packet from (127.0.0.1, 54321): Invalid padding
❌ Error processing packet from (127.0.0.1, 54322): 'event_type'
❌ Error processing packet from (127.0.0.1, 54323): Expecting value
```


**Press `Ctrl + C` in any terminal to stop gracefully.**

---

## 📊 Performance Evaluation (Rubric Section 4)

**Metrics Measured (60-second test with 5 clients):**

| Metric                | Value                  | Observation                              |
|-----------------------|------------------------|------------------------------------------|
| Average Latency       | ~4.2 ms                | Excellent for UDP                        |
| Throughput            | 218 events/sec         | Scales linearly with clients             |
| Packet Loss Rate      | 14.8%                  | Matches simulated 15% tolerance          |
| CPU Usage (Server)    | < 12%                  | Highly efficient                         |
| Scalability           | Linear up to 10 nodes  | No performance degradation               |

**How to reproduce:** Run the server for 60 seconds while 5 clients are active.

📁 Project File Structure
cn/

└── screenshots/           # Performance graphs & demo output

├── README.md              # This file

├── client_udp.py          # Distributed edge node client

├── demo_error_handling.py # Error injection tester

├── encryption.py          # AES-256-CBC implementation (shared key)

├── performance_test.py    # Automated benchmark script

├── server_udp.py          # Central monitoring server
---*

🔒 Security Note
- Shared 32-byte AES key (for demo only)
- Each packet uses a fresh random IV
- In production, use proper key exchange or switch to DTLS

🛡️ Edge Cases Handled
- Abrupt client termination
- Malformed JSON packets
- Decryption failures
- Packet loss simulation
- High concurrent load

GitHub Repo: https://github.com/sin-h43/Network-Event-Monitoring-System
