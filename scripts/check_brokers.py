#!/usr/bin/env python3
"""Daily, subscribe-only probe of community-published Meshtastic MQTT brokers.

No local broker and no traffic publishing. No MQTT payloads or private credentials
are emitted into reports. Results describe this probe vantage, not global uptime.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import ipaddress
import json
import re
import socket
import ssl
import threading
import time
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONLINE = {"LIVE_MESH_TOPIC", "LIVE_OTHER", "IDLE"}
HOST = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9.-]{0,251}[a-zA-Z0-9]$")


def validate(entry):
    required = {"id", "name", "country", "region", "host", "port", "tls", "username", "password", "topic"}
    missing = required - entry.keys()
    if missing:
        raise ValueError(f"{entry.get('id', '?')}: missing {sorted(missing)}")
    host = entry["host"]
    if not isinstance(host, str) or not HOST.fullmatch(host) or ".." in host or host.lower() == "localhost":
        raise ValueError(f"{entry['id']}: invalid host")
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if not ip.is_global:
            raise ValueError(f"{entry['id']}: non-public IP prohibited")
    if not isinstance(entry["port"], int) or not 1 <= entry["port"] <= 65535:
        raise ValueError(f"{entry['id']}: invalid port")
    if not isinstance(entry["tls"], bool):
        raise ValueError(f"{entry['id']}: tls must be boolean")
    if not isinstance(entry["topic"], str) or not entry["topic"].startswith("msh/"):
        raise ValueError(f"{entry['id']}: topic must begin with msh/")
    if not isinstance(entry["username"], str) or not isinstance(entry["password"], str):
        raise ValueError(f"{entry['id']}: invalid public credential fields")
    if "#" in entry["topic"] and not entry["topic"].endswith("/#"):
        raise ValueError(f"{entry['id']}: bad MQTT wildcard")
    if entry.get("source_url"):
        from urllib.parse import urlsplit
        source = urlsplit(entry["source_url"])
        if source.scheme != "https" or not source.hostname or source.username or source.password:
            raise ValueError(f"{entry['id']}: source_url must be a public HTTPS URL")
    if entry["id"] in ("", ".", "..") or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["id"]):
        raise ValueError(f"{entry['id']}: invalid id")


def probe(entry, listen_seconds):
    import paho.mqtt.client as mqtt

    start = time.monotonic()
    state = {"status": "UNKNOWN", "detail": "", "mesh_messages": 0,
             "other_messages": 0, "retained_messages": 0, "last_live_at": None}
    connected = threading.Event()
    subscribed = threading.Event()
    disconnected = threading.Event()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    client = None

    def on_connect(c, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            code = reason_code.value
            state["status"] = "AUTH_REJECTED" if code in (4, 5, 134, 135) else "MQTT_REJECTED"
            state["detail"] = f"CONNACK {code}"
        else:
            result, _ = c.subscribe(entry["topic"], qos=0)
            if result != mqtt.MQTT_ERR_SUCCESS:
                state["status"] = "SUBSCRIBE_ERROR"
                state["detail"] = f"subscribe() returned {result}"
                subscribed.set()
        connected.set()

    def on_subscribe(c, userdata, mid, reason_codes, properties):
        if not reason_codes or reason_codes[0].is_failure:
            state["status"] = "SUBSCRIBE_DENIED"
            state["detail"] = "SUBACK denied"
        else:
            state["status"] = "IDLE"
            state["detail"] = "SUBACK accepted; no non-retained PUBLISH observed"
        subscribed.set()

    def on_message(c, userdata, msg):
        if msg.retain:
            state["retained_messages"] += 1
            return
        if msg.topic.startswith("msh/") and "/2/e/" in msg.topic:
            state["mesh_messages"] += 1
        else:
            state["other_messages"] += 1
        state["last_live_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    def on_disconnect(c, userdata, disconnect_flags, reason_code, properties):
        disconnected.set()

    try:
        # DNS screening prevents accidental probing of loopback/private endpoints.
        addresses = socket.getaddrinfo(entry["host"], entry["port"], type=socket.SOCK_STREAM)
        if not addresses:
            raise socket.gaierror("no DNS records")
        if any(not ipaddress.ip_address(record[4][0]).is_global for record in addresses):
            state.update(status="UNSAFE_ADDRESS", detail="DNS returned non-public address")
            return state

        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id="MeshDirectory-" + uuid.uuid4().hex[:12],
            clean_session=True,
            protocol=mqtt.MQTTv311,
            reconnect_on_failure=False,
        )
        if entry["username"]:
            client.username_pw_set(entry["username"], entry["password"])
        if entry["tls"]:
            client.tls_set_context(ssl.create_default_context())
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        client.connect(entry["host"], entry["port"], keepalive=20)
        client.loop_start()

        if not connected.wait(10):
            state.update(status="TIMEOUT", detail="No CONNACK within 10s")
        elif state["status"] in ("AUTH_REJECTED", "MQTT_REJECTED"):
            pass
        elif not subscribed.wait(10):
            state.update(status="SUBACK_TIMEOUT", detail="No SUBACK within 10s")
        elif state["status"] == "IDLE":
            # Ignore retained messages. An idle broker is NOT offline.
            disconnected.wait(listen_seconds)
            if state["mesh_messages"]:
                state.update(status="LIVE_MESH_TOPIC", detail="Non-retained msh/.../2/e/... PUBLISH received")
            elif state["other_messages"]:
                state.update(status="LIVE_OTHER", detail="Non-retained PUBLISH received, not on msh/.../2/e/...")
            elif disconnected.is_set():
                state.update(status="DISCONNECTED", detail="Disconnected before observation window ended")
    except socket.gaierror:
        state.update(status="DNS_ERROR", detail="DNS resolution failed")
    except (ssl.SSLCertVerificationError, ssl.SSLError):
        state.update(status="TLS_ERROR", detail="TLS negotiation or certificate validation failed")
    except (OSError, TimeoutError) as exc:
        label = "TCP_TIMEOUT" if isinstance(exc, TimeoutError) or isinstance(exc, socket.timeout) else "CONNECT_ERROR"
        state.update(status=label, detail=f"Network connection failed ({type(exc).__name__})")
    except Exception as exc:
        state.update(status="PROBE_ERROR", detail=f"Probe failed ({type(exc).__name__})")
    finally:
        if client is not None:
            try:
                client.disconnect()
                client.loop_stop()
            except Exception:
                pass
        state["duration_ms"] = round((time.monotonic() - start) * 1000)
        state["checked_at"] = now
    return state


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait", type=int, default=25, help="seconds to listen for new MQTT PUBLISH (max 60)")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--only", nargs="*", help="optional broker ids")
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog/brokers.json")
    parser.add_argument("--output", type=Path, default=ROOT / "data/status.json")
    parser.add_argument("--history", type=Path, default=ROOT / "data/history.json")
    args = parser.parse_args()
    if not (1 <= args.wait <= 60 and 1 <= args.workers <= 12):
        parser.error("--wait must be 1-60 and --workers 1-12")
    entries = json.loads(args.catalog.read_text())
    ids = set()
    for entry in entries:
        validate(entry)
        if entry["id"] in ids:
            raise ValueError("duplicate broker ID: " + entry["id"])
        ids.add(entry["id"])
    if args.only:
        unknown = set(args.only) - ids
        if unknown:
            parser.error(f"unknown broker IDs: {sorted(unknown)}")
        entries = [e for e in entries if e["id"] in args.only]

    previous = json.loads(args.output.read_text()) if args.output.exists() else {"results": {}}
    results = previous.get("results", {}).copy()
    history = json.loads(args.history.read_text()) if args.history.exists() else {}
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    day = checked_at[:10]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        tasks = {pool.submit(probe, e, args.wait): e for e in entries}
        for task in as_completed(tasks):
            entry = tasks[task]
            result = task.result()
            old = results.get(entry["id"], {})
            if result["last_live_at"] is None:
                result["last_live_at"] = old.get("last_live_at")
            results[entry["id"]] = result
            daily = history.get(entry["id"], [])
            daily = [x for x in daily if x.get("date") != day]
            daily.append({"date": day, "status": result["status"], "mesh_messages": result["mesh_messages"]})
            history[entry["id"]] = sorted(daily, key=lambda x: x["date"])[-90:]
            print(f"{entry['id']:<23} {result['status']:<23} mesh={result['mesh_messages']} other={result['other_messages']}", flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"checked_at": checked_at, "probe_location": "GitHub Actions ubuntu-latest", "results": results}, indent=2, ensure_ascii=False) + "\n")
    args.history.write_text(json.dumps(history, indent=2, ensure_ascii=False) + "\n")
    print(f"Checked {len(entries)} remote community brokers. No MQTT payloads published or stored.")


if __name__ == "__main__":
    main()
