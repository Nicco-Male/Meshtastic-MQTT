# Contributing broker entries

This is a **public, read-only** Meshtastic community MQTT directory. The checks do not rely on personal servers or private credentials.

## New broker entry

Submit a pull request updating `catalog/brokers.json`. Provide:

- `id`: a unique lowercase slug; `name`, ISO 3166-1 alpha-2 `country` and `region`.
- `host`, `port`, `tls`: the public broker endpoint; no loopback, private IP or LAN name.
- `topic`: the narrowest practical public subscribe path starting with `msh/`.
- `username`, `password`: **only** when the broker operator explicitly publishes a shared public account. Otherwise use empty strings for an anonymous endpoint, or do not add the endpoint until you have permission.
- `source_url`: a public HTTPS page documenting the endpoint and preferably its read-access policy.

Do **not** publish personal credentials, access tokens, MQTT message bodies, private messages, location traces, or third-party data dumps. Please do not suggest high-volume subscriptions just to make a broker appear LIVE.

## Monitoring interpretation

The probes use GitHub-hosted runners and a 25-second MQTT subscribe window once per day. `IDLE` does not mean down. A `LIVE_MESH_TOPIC` result only identifies a non-retained PUBLISH whose topic contains `/2/e/`; it is **not** a verified Protobuf decoder. A failed probe can be caused by geographical access policies or runner network restrictions.

Run a local catalog validation with:

```bash
python -m unittest discover -s tests -v
```

## Operator requests

If you operate a listed broker and want it removed, corrected, or tested with a narrower topic, open an issue or a pull request. We will respect publicly documented access conditions.
