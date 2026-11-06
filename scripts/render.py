#!/usr/bin/env python3
"""Render public HTML/README from catalog and daily MQTT observations."""
from collections import Counter
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    "LIVE_MESH_TOPIC": ("LIVE · MESH", "live"),
    "LIVE_OTHER": ("LIVE / OTHER", "live"),
    "IDLE": ("ONLINE / IDLE", "idle"),
    "SUBSCRIBE_DENIED": ("SUBSCRIBE DENIED", "blocked"),
    "AUTH_REJECTED": ("ACCESS DENIED", "blocked"),
    "MQTT_REJECTED": ("CONNECTION REJECTED", "blocked"),
    "SUBSCRIBE_ERROR": ("SUBSCRIBE ERROR", "blocked"),
    "CONNECT_ERROR": ("TCP ERROR", "down"),
    "TCP_TIMEOUT": ("TCP TIMEOUT", "down"),
    "DNS_ERROR": ("DNS ERROR", "down"),
    "TLS_ERROR": ("TLS ERROR", "down"),
    "TIMEOUT": ("MQTT TIMEOUT", "down"),
    "SUBACK_TIMEOUT": ("SUBACK TIMEOUT", "down"),
    "DISCONNECTED": ("DISCONNECTED", "down"),
    "UNSAFE_ADDRESS": ("NON-PUBLIC IP", "blocked"),
    "PROBE_ERROR": ("PROBE ERROR", "down"),
    "UNTESTED": ("UNTESTED", "unknown"),
}
ONLINE = {"LIVE_MESH_TOPIC", "LIVE_OTHER", "IDLE"}


def page():
    catalog = json.loads((ROOT / 'catalog/brokers.json').read_text())
    status = json.loads((ROOT / 'data/status.json').read_text())
    history = json.loads((ROOT / 'data/history.json').read_text())
    observed = status.get('results', {})
    at = status.get('checked_at') or 'No checks have run yet'
    counts = Counter((observed.get(e['id']) or {}).get('status', 'UNTESTED') for e in catalog)
    live = counts['LIVE_MESH_TOPIC'] + counts['LIVE_OTHER']
    online = live + counts['IDLE']
    denied = sum(v for k, v in counts.items() if k in ('AUTH_REJECTED','MQTT_REJECTED','SUBSCRIBE_DENIED','SUBSCRIBE_ERROR'))
    table = []
    md = []
    for e in sorted(catalog, key=lambda x: (x['country'], x['name'])):
        r = observed.get(e['id'], {})
        code = r.get('status', 'UNTESTED')
        label, css = LABELS.get(code, (code, 'unknown'))
        records = history.get(e['id'], [])[-30:]
        uptime = f"{sum(x['status'] in ONLINE for x in records)/len(records)*100:.0f}%" if records else '—'
        last = (r.get('checked_at') or '—').replace('T', ' ').replace('+00:00',' UTC')
        tls = 'TLS' if e['tls'] else 'MQTT'
        sample = f"{r.get('mesh_messages', 0)} / {r.get('other_messages', 0)}" if r else '—'
        c = escape
        link = (f'<a href="{c(e["source_url"], quote=True)}" target="_blank" rel="noopener noreferrer">Source ↗</a>'
                if e.get('source_url') else '—')
        table.append(f'''<tr data-filter="{c((e['country']+' '+e['region']+' '+e['name']+' '+e['host']).lower(), quote=True)}" data-status="{css}">
<td><span class="country">{c(e['country'])}</span> <strong>{c(e['name'])}</strong><small>{c(e['region'])}</small></td>
<td><code>{c(e['host'])}:{e['port']}</code><small>{tls} · <code>{c(e['topic'])}</code></small></td>
<td><span class="status {css}">{c(label)}</span><small>{c(r.get('detail',''))}</small></td>
<td class="numeric">{c(sample)}</td><td class="numeric">{uptime}</td><td><small>{c(last)}</small>{link}</td></tr>''')
        md.append(f"| {e['country']} | `{e['host']}:{e['port']}` | `{e['topic']}` | **{label}** | {uptime} |")
    css = '''
:root{color-scheme:dark;font:15px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#0b1320;color:#e8edf5}
*{box-sizing:border-box}body{margin:0}a{color:#7cc2ff;text-decoration:none}a:hover{text-decoration:underline}
main{max-width:1440px;margin:auto;padding:34px 24px 80px}.eyebrow{color:#7cc2ff;text-transform:uppercase;font-size:12px;letter-spacing:.15em;font-weight:700}
h1{font-size:clamp(30px,4vw,48px);letter-spacing:-.04em;line-height:1.1;margin:10px 0 14px}p{color:#acb9ca;max-width:1000px}
.summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:26px 0}.tile{border:1px solid #263850;border-radius:12px;padding:18px;background:#111e30}
.tile .number{font-size:31px;font-weight:750;letter-spacing:-.05em}.tile .detail{font-size:12px;color:#aebcd0}.toolbar{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0 12px}
input,select{background:#0f1a2b;color:#e8edf5;border:1px solid #324762;border-radius:8px;font:inherit;padding:11px 13px}input{flex:1;min-width:230px}select{min-width:160px}
.tablewrap{overflow-x:auto;border:1px solid #29394f;border-radius:12px}table{width:100%;border-collapse:collapse;min-width:980px}th{position:sticky;top:0;background:#18273b;color:#abc0da;text-transform:uppercase;letter-spacing:.08em;font-size:11px;text-align:left;padding:12px 14px}td{padding:13px 14px;border-top:1px solid #25364a;vertical-align:top}tr:hover{background:#15253a}td strong{font-weight:650}small{display:block;font-size:12px;color:#93a7bf;margin-top:4px;max-width:490px;overflow-wrap:anywhere}code{font-size:12px;color:#d5e3f6;overflow-wrap:anywhere}.country{display:inline-block;border:1px solid #41546d;border-radius:4px;font-size:11px;padding:1px 5px;margin-right:7px;color:#a9c6e1}
.status{display:inline-block;font-size:11px;letter-spacing:.03em;font-weight:750;border-radius:6px;padding:4px 7px;white-space:nowrap}.live{background:#153f35;color:#77e4b3}.idle{background:#203951;color:#9fcaff}.blocked{background:#50331d;color:#ffcc91}.down{background:#4d2431;color:#ffa6b7}.unknown{background:#2b3442;color:#c7d2de}.numeric{font-variant-numeric:tabular-nums;white-space:nowrap}
footer{margin-top:25px;border-top:1px solid #27374a;padding-top:20px;font-size:13px;color:#a8b8cc}h2{font-size:19px;margin-top:30px} .muted{color:#91a7be}
@media(max-width:780px){main{padding:24px 12px 60px}.summary{grid-template-columns:repeat(2,1fr)}.tile{padding:12px}.tile .number{font-size:25px}}
'''
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Meshtastic MQTT Directory · Community broker status</title><meta name="description" content="Independent directory of community-operated Meshtastic MQTT brokers with daily checks from GitHub Actions."><style>{css}</style></head>
<body><main><div class="eyebrow">Open directory · MQTT · Meshtastic</div><h1>Meshtastic MQTT Directory</h1>
<p>An open, independent directory of Meshtastic community MQTT brokers, automatically checked <strong>once per day</strong> from GitHub Actions. Read-only connections and subscriptions; no publishing and no private MQTT servers.</p>
<p><strong>Public network map:</strong> Explore Meshtastic MQTT network activity on <a href="https://worldmap.niccomale.it" target="_blank" rel="noopener noreferrer">worldmap.niccomale.it ↗</a>. The map is a separate visualization; broker checks are performed independently.</p>
<section class="summary"><div class="tile"><div class="number">{len(catalog)}</div><div class="detail">Registered brokers</div></div><div class="tile"><div class="number">{online}</div><div class="detail">Accessible subscriptions</div></div><div class="tile"><div class="number">{live}</div><div class="detail">Live traffic observed</div></div><div class="tile"><div class="number">{denied}</div><div class="detail">Access restricted (not offline)</div></div></section>
<p class="muted"><strong>Access restricted is not offline:</strong> a broker may be reachable but deny the public account or topic. This directory respects operator access controls and never attempts to bypass them.</p>
<p class="muted">Last checked: <strong>{escape(at)}</strong> · Probe location: GitHub Actions (reachability may differ from other networks). 30-check availability = share of tests with successful MQTT connection and subscription; not an SLA.</p>
<div class="toolbar"><input id="find" type="search" placeholder="Search country, community or hostname…" aria-label="Search brokers"><select id="filter" aria-label="Filter by status"><option value="all">All statuses</option><option value="live">Live traffic</option><option value="idle">Online / idle</option><option value="blocked">Access denied</option><option value="down">Connection issues</option><option value="unknown">Not yet tested</option></select></div>
<div class="tablewrap"><table><thead><tr><th>Community</th><th>Endpoint and topic</th><th>MQTT status</th><th>Mesh / other messages</th><th>Last 30 checks</th><th>Last checked / source</th></tr></thead><tbody id="rows">{''.join(table)}</tbody></table></div>
<h2>How to read the statuses</h2><p><strong>LIVE · MESH</strong> = non-retained PUBLISH observed on <code>msh/.../2/e/...</code> (Protobuf content is not validated). <strong>LIVE / OTHER</strong> = live traffic on other topics. <strong>ONLINE / IDLE</strong> = CONNACK and SUBACK accepted, but no live message received during the observation window. TCP, DNS, TLS and ACL errors are reported separately. One failed probe does not establish a global outage.</p>
<footer>The directory uses only operator-published public community accounts; it does not store private credentials, MQTT payloads, node identifiers or private broker information. To add or correct a server, open a pull request. <a href="https://github.com/Nicco-Male/Meshtastic-MQTT">Source on GitHub ↗</a></footer>
</main><script>
const input=document.getElementById('find'),sel=document.getElementById('filter');
function apply(){{const q=input.value.trim().toLowerCase(),s=sel.value;for(const tr of document.querySelectorAll('#rows tr')){{tr.hidden=!(tr.dataset.filter.includes(q)&&(s==='all'||tr.dataset.status===s));}}}}
input.addEventListener('input',apply);sel.addEventListener('change',apply);
</script></body></html>'''
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs/index.html').write_text(html)
    readme = (ROOT / 'README.md').read_text()
    start = '<!-- STATUS_TABLE_START -->'
    end = '<!-- STATUS_TABLE_END -->'
    if start not in readme or end not in readme:
        raise ValueError('README status markers missing')
    formatted = '| Country | Broker | Topic | Status | Last 30 checks |\n|---|---|---|---|---|\n' + '\n'.join(md)
    readme = readme.split(start)[0] + start + '\n' + formatted + '\n' + end + readme.split(end, 1)[1]
    (ROOT / 'README.md').write_text(readme)
    print('Rendered docs/index.html and README.md from', len(catalog), 'broker records')


if __name__ == '__main__':
    page()
