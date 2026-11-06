# Meshtastic MQTT Directory

[![Daily MQTT checks](https://github.com/Nicco-Male/Meshtastic-MQTT/actions/workflows/check.yml/badge.svg)](https://github.com/Nicco-Male/Meshtastic-MQTT/actions/workflows/check.yml)

**The open, community-maintained directory of Meshtastic MQTT brokers — checked automatically every day.**

Catalogo internazionale, indipendente e open source dei broker MQTT pubblici delle comunità Meshtastic. Monitoraggio giornaliero, storico, dashboard e fonti verificabili.

[Dashboard pubblica](https://nicco-male.github.io/Meshtastic-MQTT/) · [Catalogo JSON](catalog/brokers.json) · [Ultimo test JSON](data/status.json) · [Storico 90 giorni](data/history.json)

## Come funziona

- Ogni giorno alle **05:17 UTC**, GitHub Actions interroga direttamente gli endpoint remoti registrati in `catalog/brokers.json`.
- Connessione MQTT 3.1.1, con **Client ID esplicito** e account **pubblici forniti dalle comunità**, oppure anonimo dove consentito. TLS con verifica del certificato quando configurato.
- **Solo SUBSCRIBE** al topic documentato: non invia pacchetti, non pubblica dati, non scrive sui broker. Le sonde non utilizzano alcun bridge privato o broker locale.
- Un broker senza messaggi in 25 secondi è **ONLINE · SILENZIOSO** se `CONNACK` e `SUBACK` sono validi; non OFFLINE.
- Registra codici di stato e conteggi, **mai payload MQTT o credenziali private**. La presenza di `msh/.../2/e/...` è una verifica della struttura del topic, non una decodifica Protobuf.

## Stato corrente

<!-- STATUS_TABLE_START -->
| Paese | Broker | Topic | Stato | Ultimi 30 test |
|---|---|---|---|---|
| AM | `mqtt.msh.am:1883` | `msh/#` | **DA VERIFICARE** | — |
| AU | `mqtt.peeringsa.net:1883` | `msh/ANZ/SA/#` | **DA VERIFICARE** | — |
| BG | `bgmesh.swat-bg.org:1883` | `msh/#` | **DA VERIFICARE** | — |
| BG | `meshqtt.motaba.net:1883` | `msh/Bulgaria/#` | **DA VERIFICARE** | — |
| CL | `mqtt.meshchile.cl:1883` | `msh/CL/#` | **DA VERIFICARE** | — |
| CN | `mqtt.mess.host:1883` | `msh/CN/#` | **DA VERIFICARE** | — |
| CO | `mqtt.meshcolombia.co:1883` | `msh/CO/#` | **DA VERIFICARE** | — |
| CZ | `mqtt.aperturelab.cz:1883` | `msh/CZ/#` | **DA VERIFICARE** | — |
| DE | `nrw.iot-root.de:1883` | `msh/#` | **DA VERIFICARE** | — |
| DE | `mqtt.mesh-sh.de:1883` | `msh/EU_868/DE/S-H/#` | **DA VERIFICARE** | — |
| ES | `mqtt.mesh.comunidadeozulo.org:1883` | `msh/EU_868/#` | **DA VERIFICARE** | — |
| ES | `mqtt.meshtastic.es:1883` | `msh/EU_868/#` | **DA VERIFICARE** | — |
| GB | `mqtt.cumbriacq.com:1883` | `msh/EU_868/#` | **DA VERIFICARE** | — |
| HR | `mqtt.cromesh.eu:1883` | `msh/EU_868/9A/#` | **DA VERIFICARE** | — |
| IT | `mqtt.loraitalia.it:1883` | `msh/EU_868/IT/#` | **DA VERIFICARE** | — |
| NL | `mqtt.meshnet.nl:1883` | `msh/EU_868/NL/#` | **DA VERIFICARE** | — |
| NL | `mqtt.meshtnet.nl:1883` | `msh/EU_868/NL/#` | **DA VERIFICARE** | — |
| PL | `loranet.pl:1883` | `msh/PL/#` | **DA VERIFICARE** | — |
| PT | `mqtt.meshtastic.pt:1883` | `msh/#` | **DA VERIFICARE** | — |
| PT | `iot.meshtastic.pt:1883` | `msh/#` | **DA VERIFICARE** | — |
| RO | `mqtt.meshmap.ro:1883` | `msh/EU_868/#` | **DA VERIFICARE** | — |
| SE | `mqtt.meshat.se:1883` | `msh/#` | **DA VERIFICARE** | — |
| SI | `mqtt.meshnet.si:1883` | `msh/EU_868/SI/#` | **DA VERIFICARE** | — |
| US | `mqtt.csramsh.net:1883` | `msh/US/GA/csramsh/#` | **DA VERIFICARE** | — |
| US | `mqtt.ctmesh.org:1883` | `msh/US/CT/#` | **DA VERIFICARE** | — |
| US | `mqtt.chimesh.org:1883` | `msh/US/IL/Chi/#` | **DA VERIFICARE** | — |
| US | `mqtt.meshstl.org:1883` | `msh/US/MeshSTL/#` | **DA VERIFICARE** | — |
| US | `mqtt.neomesh.org:1883` | `msh/#` | **DA VERIFICARE** | — |
| US | `mqtt.nyme.sh:1883` | `msh/US/NY/#` | **DA VERIFICARE** | — |
| US | `mqtt.nashme.sh:1883` | `msh/#` | **DA VERIFICARE** | — |
| US | `mqtt.northernmichmesh.org:8883` | `msh/US/MI/NMI/#` | **DA VERIFICARE** | — |
| US | `mqtt.rrmesh.net:1883` | `msh/#` | **DA VERIFICARE** | — |
| US | `mqtt.scmesh.us:1883` | `msh/US/SC/#` | **DA VERIFICARE** | — |
| US | `mqtt.socalmesh.org:1883` | `msh/US/CA/socalmesh/#` | **DA VERIFICARE** | — |
<!-- STATUS_TABLE_END -->

## Aggiungere o correggere un broker

[Contribution guide (English)](CONTRIBUTING.md)


1. Apri una pull request modificando `catalog/brokers.json`.
2. Includi un endpoint pubblico autorizzato alla lettura, una radice topic ristretta quando possibile e un riferimento pubblico (`source_url`).
3. Usa **soltanto credenziali che il gestore ha esplicitamente pubblicato per la comunità**. Non aggiungere password personali, token, IP LAN o broker privati.
4. Non includere dump di pacchetti, messaggi personali, posizioni o identificativi dei nodi nei report.

Per test locale (non è necessario un broker privato):

```bash
python -m pip install -r requirements.txt
python scripts/check_brokers.py --only colombia --wait 15
python scripts/render.py
```

## Attivazione GitHub Actions e GitHub Pages

1. In **Actions → Check community MQTT brokers → Run workflow**, avvia la prima scansione. Il job aggiorna `data/status.json`, `data/history.json`, README e dashboard.
2. In **Settings → Pages → Build and deployment**, seleziona **Deploy from a branch** → `main` → `/docs` → **Save**.
3. Per aggiungere un broker, apri una pull request modificando il catalogo: ogni proposta deve documentare una credenziale comunitaria pubblica o accesso anonimo autorizzato.

L'azione usa il `GITHUB_TOKEN` integrato con permesso di scrittura ai contenuti e non ha bisogno di secret per broker personali.

## Limiti e affidabilità

- I test misurano **l'accessibilità da un runner GitHub**, non da tutti i paesi e non la disponibilità LoRa.
- `LIVE · MESH`: è stato osservato almeno un PUBLISH non-retained su `/2/e/`. Non certifica il contenuto Protobuf.
- `LIVE · ALTRO`: sono stati osservati topic non-retained di stato, mappe o applicazioni diverse.
- `ONLINE · SILENZIOSO`: MQTT accessibile, SUBACK accettato, senza nuove pubblicazioni nella finestra di ascolto.
- Errori DNS, TLS, TCP, autenticazione e ACL restano distinti. Un singolo errore non prova un outage permanente.
- Lo storico conserva gli ultimi 90 controlli giornalieri; l'indicatore 30-test misura la quota con connessione e sottoscrizione funzionanti, **non** una percentuale SLA di uptime.
- GitHub può ritardare le esecuzioni programmate. I workflow schedulati dei repository pubblici possono essere disabilitati dopo 60 giorni di inattività. Vedi [documentazione GitHub](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#schedule).

## Licenza

Dati e codice: [MIT](LICENSE). I marchi e i broker appartengono alle rispettive comunità. Progetto indipendente, non affiliato a Meshtastic.