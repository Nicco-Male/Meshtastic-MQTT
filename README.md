# Meshtastic MQTT Directory

[![Daily MQTT checks](https://github.com/Nicco-Male/Meshtastic-MQTT/actions/workflows/check.yml/badge.svg)](https://github.com/Nicco-Male/Meshtastic-MQTT/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**An open, community-maintained directory of public Meshtastic MQTT brokers, with automated daily connectivity checks.**

Find community-operated MQTT brokers around the world, check their current status, and contribute corrections or new endpoints. The directory is independent of the Meshtastic project and does not operate any of the listed brokers.

**[Live dashboard](https://nicco-male.github.io/Meshtastic-MQTT/)** · **[Broker registry](catalog/brokers.json)** · **[Latest checks (JSON)](data/status.json)** · **[90-day history (JSON)](data/history.json)** · **[Contribute](CONTRIBUTING.md)**

## What is monitored?

The `Check community MQTT brokers` GitHub Actions workflow runs daily at **05:17 UTC** (subject to GitHub scheduling delays) and can also be started manually. It directly connects to registered public broker endpoints using only **operator-published community credentials**, or anonymous access when explicitly available.

- **Read-only MQTT:** CONNECT and SUBSCRIBE only. No PUBLISH, message forwarding, local MQTT bridges, or access to private servers.
- **Safe credentials:** Only shared accounts publicly authorized by the operator may be listed. Never submit personal accounts, access tokens, LAN addresses, or private broker credentials.
- **Minimal data:** Save connection and subscription outcomes, counts of observed messages, and timestamps; **never collect or publish message payloads**.
- **Meaningful health states:** A broker that accepts connections and subscriptions but has no messages during the observation window is **ONLINE / IDLE**, not offline.
- **Limited claims:** A non-retained message on an MQTT topic containing `/2/e/` suggests Meshtastic traffic; payloads are not decoded or authenticated.

## Latest broker checks

The table below is generated automatically from the registry and latest daily observations. **UNTESTED** means GitHub Actions has not completed a check yet. An error observed from a GitHub-hosted runner does not mean the broker is unavailable everywhere.

<!-- STATUS_TABLE_START -->
| Country | Broker | Topic | Status | Last 30 checks |
|---|---|---|---|---|
| AM | `mqtt.msh.am:1883` | `msh/#` | **ONLINE / IDLE** | 100% |
| AU | `mqtt.peeringsa.net:1883` | `msh/ANZ/SA/#` | **SUBSCRIBE DENIED** | 0% |
| BG | `bgmesh.swat-bg.org:1883` | `msh/#` | **SUBSCRIBE DENIED** | 0% |
| BG | `meshqtt.motaba.net:1883` | `msh/Bulgaria/#` | **LIVE · MESH** | 100% |
| CL | `mqtt.meshchile.cl:1883` | `msh/CL/#` | **LIVE · MESH** | 100% |
| CN | `mqtt.mess.host:1883` | `msh/CN/#` | **DNS ERROR** | 0% |
| CO | `mqtt.meshcolombia.co:1883` | `msh/CO/#` | **LIVE · MESH** | 100% |
| CZ | `mqtt.aperturelab.cz:1883` | `msh/CZ/#` | **ONLINE / IDLE** | 100% |
| DE | `nrw.iot-root.de:1883` | `msh/#` | **ACCESS DENIED** | 0% |
| DE | `mqtt.mesh-sh.de:1883` | `msh/EU_868/DE/S-H/#` | **LIVE · MESH** | 100% |
| ES | `mqtt.mesh.comunidadeozulo.org:1883` | `msh/EU_868/#` | **LIVE / OTHER** | 100% |
| ES | `mqtt.meshtastic.es:1883` | `msh/EU_868/#` | **ACCESS DENIED** | 0% |
| GB | `mqtt.cumbriacq.com:1883` | `msh/EU_868/#` | **TCP TIMEOUT** | 0% |
| HR | `mqtt.cromesh.eu:1883` | `msh/EU_868/9A/#` | **ONLINE / IDLE** | 100% |
| IT | `mqtt.loraitalia.it:1883` | `msh/EU_868/IT/#` | **SUBSCRIBE DENIED** | 0% |
| NL | `mqtt.meshnet.nl:1883` | `msh/EU_868/NL/#` | **DNS ERROR** | 0% |
| NL | `mqtt.meshtnet.nl:1883` | `msh/EU_868/NL/#` | **DNS ERROR** | 0% |
| PL | `loranet.pl:1883` | `msh/PL/#` | **LIVE · MESH** | 100% |
| PT | `mqtt.meshtastic.pt:1883` | `msh/#` | **TCP TIMEOUT** | 0% |
| PT | `iot.meshtastic.pt:1883` | `msh/#` | **TCP TIMEOUT** | 0% |
| RO | `mqtt.meshmap.ro:1883` | `msh/EU_868/#` | **LIVE · MESH** | 100% |
| SE | `mqtt.meshat.se:1883` | `msh/#` | **LIVE · MESH** | 100% |
| SI | `mqtt.meshnet.si:1883` | `msh/EU_868/SI/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.csramsh.net:1883` | `msh/US/GA/csramsh/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.ctmesh.org:1883` | `msh/US/CT/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.chimesh.org:1883` | `msh/US/IL/Chi/#` | **LIVE · MESH** | 100% |
| US | `mqtt.meshstl.org:1883` | `msh/US/MeshSTL/#` | **LIVE · MESH** | 100% |
| US | `mqtt.neomesh.org:1883` | `msh/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.nyme.sh:1883` | `msh/US/NY/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.nashme.sh:1883` | `msh/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.northernmichmesh.org:8883` | `msh/US/MI/NMI/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.rrmesh.net:1883` | `msh/#` | **ONLINE / IDLE** | 100% |
| US | `mqtt.scmesh.us:1883` | `msh/US/SC/#` | **LIVE · MESH** | 100% |
| US | `mqtt.socalmesh.org:1883` | `msh/US/CA/socalmesh/#` | **LIVE · MESH** | 100% |
<!-- STATUS_TABLE_END -->

## Status definitions

| Status | Meaning |
|---|---|
| **LIVE / MESH TOPIC** | A non-retained PUBLISH was observed on a `msh/.../2/e/...`-style topic. |
| **LIVE / OTHER** | A non-retained PUBLISH was observed on another topic, such as a status or map topic. |
| **ONLINE / IDLE** | MQTT CONNACK and SUBACK succeeded, but no new messages appeared during the listening window. |
| **ACCESS DENIED** | The broker rejected authentication or a subscription. |
| **CONNECTION ERROR** | DNS, TCP, TLS, protocol or timeout error. This is a single probe result, not an uptime guarantee. |
| **UNTESTED** | The broker has not yet been checked by GitHub Actions. |

The 30-check indicator in the dashboard is the percentage of recent tests with successful connection and subscription, **not an independently audited SLA**.

## Add or update a broker

Open a pull request modifying [`catalog/brokers.json`](catalog/brokers.json), and include a public source documenting the broker and its access policy. Prefer a restricted read-only topic to a broad `#` subscription. See the [contribution guidelines](CONTRIBUTING.md).

To validate locally, no private broker is required:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/check_brokers.py --only colombia --wait 15
python scripts/render.py
```

The sample probe contacts a public broker on the Internet. To validate the registry without making network requests, run only the unit tests.

## Run the directory on GitHub

1. Use **Actions → Check community MQTT brokers → Run workflow** for an initial check.
2. Under **Settings → Pages → Build and deployment**, select **Deploy from a branch**, then choose `main` and `/docs`.
3. The workflow commits refreshed `README.md`, `data/status.json`, `data/history.json` and `docs/index.html` to the default branch, using GitHub's built-in `GITHUB_TOKEN` and `contents: write` permission.

No user-operated MQTT server or third-party tokens are required. If commits are rejected, check branch protection and repository Actions settings.

## Limitations and operator policy

- The monitor measures accessibility **from GitHub-hosted runners**, not RF coverage or worldwide connectivity. Operators may intentionally block public-cloud IP ranges.
- Tests run daily and listen only briefly. Lack of observed traffic does **not** mean a broker is inactive.
- GitHub may delay scheduled runs; scheduled workflows in inactive public repositories may be disabled after 60 days without repository activity. See [GitHub Actions scheduling documentation](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#schedule).
- **Broker operators:** If your endpoint is incorrectly listed or you would like it removed, open an issue or a pull request. We respect operator-defined access limitations.

## License and attribution

[MIT License](LICENSE). Software and directory data are provided as-is. Meshtastic is a separate project and its trademarks belong to their respective owners. This directory is not officially affiliated with Meshtastic.