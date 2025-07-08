# 🔎 Port Scanner v2.0

Scanner di porte TCP/UDP multithreaded sviluppato in Python.  
Progetto creato per esercizio personale in ambito **cybersecurity** e **network scanning**.

## 🚀 Caratteristiche
- ✅ Scansione **TCP e UDP**
- ✅ Report **HTML** generato automaticamente
- ✅ Logging su file `.log` con timestamp
- ✅ Output in formato **JSON**
- ✅ Multithreading con limite dinamico basato su CPU

## ⚙️ Utilizzo

```bash
python scanner.py <IP> --start <porta_iniziale> --end <porta_finale> [--udp]
python scanner.py 127.0.0.1 --start 20 --end 1024 --udp

