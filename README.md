Simple Python Port Scanner è uno script Python multithread per la scansione rapida delle porte TCP di un host.
Scansiona un intervallo di porte e salva i risultati delle porte aperte in formato JSON.

Uso
Apri il terminale nella cartella del progetto e digita:
python scanner.py <IP> [--start PORTA_INIZIO] [--end PORTA_FINE]

Esempio
python scanner.py 192.168.1.85 --start 1 --end 1024

Output
Risultati salvati in open_ports.json, con elenco delle porte aperte.

Requisiti
- Python 3.x
- Moduli standard Python (nessuna installazione aggiuntiva)

Contributi
Pull request e segnalazioni issue sono benvenute.

Licenza
MIT License — vedi file LICENSE.
