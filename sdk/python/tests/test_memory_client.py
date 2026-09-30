"""Unit tests for Calera Agent Memory client and LangChain adapter."""

import unittest
from unittest.mock import patch, MagicMock
import json
from calera_agent_memory.client import CaleraMemoryClient
from calera_agent_memory.langchain_memory import CaleraMemorySubstrate


class TestCaleraMemoryClient(unittest.TestCase):

    @patch("urllib.request.urlopen")
    def test_claim_free_vault(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "status": "PROVISIONED",
            "vaultId": "vault_u123",
            "capacity": 1000000,
            "statutoryRef": "Delaware UETA § 14"
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        client = CaleraMemoryClient()
        res = client.claim_free_vault("test@caleralabs.com", agent_name="test-bot")
        self.assertEqual(res["status"], "PROVISIONED")
        self.assertEqual(client.vault_id, "vault_u123")

    @patch("urllib.request.urlopen")
    def test_store_and_query(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "status": "STORED",
            "nodeId": "node_abc456"
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        client = CaleraMemoryClient(vault_id="vault_u123")
        store_res = client.store("AAPL", "Revenue $383B")
        self.assertEqual(store_res["status"], "STORED")

    @patch("urllib.request.urlopen")
    def test_query_ribbon_format(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "status": "OK",
            "format": "ribbon",
            "ribbon": '<nav:ribbon premise="AAPL_REV" target="FREE_CASH_FLOW" steps=4 action=5.6600>\nAAPL_REV -> OPERATING_INCOME -> TAX_EXPENSE -> NOPAT -> FREE_CASH_FLOW\n</nav:ribbon>'
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        client = CaleraMemoryClient(vault_id="vault_u123")
        res = client.query_ribbon("How does Apple revenue translate to free cash flow?")
        self.assertEqual(res["format"], "ribbon")
        self.assertIn("<nav:ribbon", res["ribbon"])

    @patch("urllib.request.urlopen")
    def test_geodesic_navigation(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "status": "VERIFIED_GEODESIC",
            "premise": "AAPL_REV",
            "target": "FREE_CASH_FLOW",
            "pathway": ["AAPL_REV", "OPERATING_INCOME", "TAX_EXPENSE", "NOPAT", "FREE_CASH_FLOW"],
            "stationary_action": 5.66,
            "ribbon": '<nav:ribbon premise="AAPL_REV" target="FREE_CASH_FLOW" steps=4 action=5.6600>\nAAPL_REV -> OPERATING_INCOME -> TAX_EXPENSE -> NOPAT -> FREE_CASH_FLOW\n</nav:ribbon>'
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        client = CaleraMemoryClient(vault_id="vault_u123")
        res = client.geodesic(premise="AAPL_REV", target="FREE_CASH_FLOW")
        self.assertEqual(res["status"], "VERIFIED_GEODESIC")
        self.assertEqual(len(res["pathway"]), 5)
        self.assertIn("steps=4", res["ribbon"])

    @patch("urllib.request.urlopen")
    def test_langchain_adapter(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({
            "status": "OK",
            "associations": ["AAPL FY23 Revenue was $383,285,000,000"]
        }).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        memory = CaleraMemorySubstrate(vault_id="v1")
        vars = memory.load_memory_variables({"input": "What was Apple's revenue?"})
        self.assertIn("AAPL FY23 Revenue", vars["history"])


if __name__ == "__main__":
    unittest.main()
