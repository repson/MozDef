# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# Copyright (c) 2017 Mozilla Corporation


from alerts.plugins.geomodel_tor_vpn_enrichment import enrich


class TestGeoModelEnrichment:
    def test_enrichment(self):
        test_alert = {
            'details': {
                'hops': [
                    {
                        'ip': '1.2.3.4'
                    },
                    {
                        'ip': '4.3.2.1'
                    },
                    {
                        'ip': '1.4.2.3'
                    }
                ]
            }
        }

        test_intel = {
            '1.2.3.4': {
                'TorNode': 127,
            },
            '4.3.2.1': {
                'Spam': 32,
                'CnC': 80,
            }
        }

        enriched = enrich(test_alert, test_intel)

        # Make sure nothing previously present was changed.
        assert 'details' in test_alert
        assert 'hops' in test_alert['details']
        assert len(test_alert['details']['hops']) == 3

        # Make sure info for the known IPs was added.
        assert 'ipintel' in test_alert['details']
        assert len(alert['details']['ipintel']) == 3
        assert {
            'ip': '1.2.3.4',
            'classificiation': 'TorNode',
            'threatscore': 127
        } in alert['details']['ipintel']
        assert {
            'ip': '4.3.2.1',
            'classificiation': 'Spam',
            'threatscore': 32
        } in alert['details']['ipintel']
        assert {
            'ip': '4.3.2.1',
            'classificiation': 'CnC',
            'threatscore': 80
        } in alert['details']['ipintel']
