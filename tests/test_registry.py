import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_brokers import validate  # noqa E402


class RegistryTests(unittest.TestCase):
    def test_every_endpoint_is_valid_and_unique(self):
        entries = json.loads((ROOT / 'catalog/brokers.json').read_text())
        self.assertGreater(len(entries), 20)
        self.assertEqual(len({e['id'] for e in entries}), len(entries))
        for entry in entries:
            with self.subTest(entry=entry['id']):
                validate(entry)

    def test_no_personal_broker_or_private_credentials_in_catalog(self):
        raw = (ROOT / 'catalog/brokers.json').read_text().lower()
        for fragment in ['127.0.0.1', 'sources/', 'tette2', 'tettebelle2', 'mqtt-mosquito']:
            self.assertNotIn(fragment, raw)

    def test_rejects_private_ip(self):
        sample = json.loads((ROOT / 'catalog/brokers.json').read_text())[0].copy()
        sample['host'] = '192.168.1.13'
        with self.assertRaises(ValueError):
            validate(sample)

    def test_rejects_url_with_credentials(self):
        sample = json.loads((ROOT / 'catalog/brokers.json').read_text())[0].copy()
        sample['source_url'] = 'https://user:pass@example.com'
        with self.assertRaises(ValueError):
            validate(sample)


if __name__ == '__main__':
    unittest.main()
