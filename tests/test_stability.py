import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.action_loader import ActionRecord, ActionRegistry
from core.audit import clear_events, read_events, write_event
from core.health import collect_startup_health
from core.degraded import model_status, normalize_model_state
from core.setup_wizard import collect_setup_state, load_progress, save_progress
from core.permissions import EXPLANATIONS, explanation_for, reset_policy, save_level
from memory import memory_manager
from core import llm_client


class StabilityTests(unittest.TestCase):
    def test_health_reports_readiness_without_secret_value(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "api_keys.json"
            config_path.write_text(
                json.dumps({"gemini_api_key": "super-secret", "input_device": "Mic", "output_device": "Speaker"}),
                encoding="utf-8",
            )
            health = collect_startup_health(config_path, action_count=3, plugin_count=2)

        self.assertEqual(health["api_key"], "configured")
        self.assertEqual(health["model"], "configured")
        self.assertEqual(health["input_audio"], "selected")
        self.assertEqual(health["output_audio"], "selected")
        self.assertEqual(health["actions"], "3")
        self.assertEqual(health["plugins"], "2")
        self.assertNotIn("super-secret", json.dumps(health))

    def test_audit_record_is_bounded_and_excludes_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            write_event("action", "computer_control", "succeeded", path=path)
            record = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(record["event"], "action")
        self.assertEqual(record["status"], "succeeded")
        self.assertLessEqual(len(record["action"]), 120)
        self.assertEqual(set(record), {"timestamp", "event", "action", "status"})

    def test_action_registry_logs_success_and_failure_without_parameters(self):
        def handler(parameters):
            return "done"

        registry = ActionRegistry(
            {"demo": ActionRecord(name="demo", handler=handler, valid=True)},
            logger=lambda message: None,
        )
        with patch("core.action_loader.write_event") as audit:
            result = registry.run("demo", {"secret": "do-not-log"})

        self.assertEqual(result, "done")
        self.assertEqual(
            [call.args for call in audit.call_args_list],
            [("action", "demo", "started"), ("action", "demo", "succeeded")],
        )

    def test_setup_state_reports_missing_key_and_unavailable_audio(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "api_keys.json"
            config_path.write_text(
                json.dumps({"gemini_api_key": "", "input_device": "USB Mic"}),
                encoding="utf-8",
            )
            state = collect_setup_state(
                config_path,
                audio_devices={"input": ["Built-in Mic"], "output": ["Speakers"]},
                plugin_counts=(2, 1),
            )

        self.assertEqual(state["api_key"]["status"], "blocked")
        self.assertEqual(state["model"]["status"], "blocked")
        self.assertEqual(state["microphone"]["status"], "attention")
        self.assertEqual(state["speaker"]["status"], "ready")
        self.assertEqual(state["plugins"]["status"], "attention")
        self.assertEqual(state["permissions"]["status"], "manual")
        self.assertNotIn("USB Mic", json.dumps(state))

    def test_setup_progress_round_trips_only_known_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "setup_progress.json"
            save_progress(path, {"api_key": True, "unexpected_secret": "value"})
            loaded = load_progress(path)
            raw_progress = path.read_text(encoding="utf-8")

        self.assertTrue(loaded["completed"]["api_key"])
        self.assertFalse(loaded["completed"]["model"])
        self.assertNotIn("unexpected_secret", raw_progress)

    def test_blocked_permission_never_calls_handler(self):
        calls = []

        def handler(parameters):
            calls.append(parameters)
            return "changed"

        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "api_keys.json"
            save_level(config_path, "demo", "blocked")
            registry = ActionRegistry(
                {"demo": ActionRecord(name="demo", handler=handler, valid=True)},
                logger=lambda message: None,
            )
            with patch("core.action_loader.default_config_path", return_value=config_path):
                result = registry.run("demo", {"value": "secret"})

        self.assertIn("blocked", result)
        self.assertEqual(calls, [])

    def test_confirm_permission_uses_human_gate(self):
        def handler(parameters):
            return "changed"

        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "api_keys.json"
            save_level(config_path, "demo", "confirm")
            registry = ActionRegistry(
                {"demo": ActionRecord(name="demo", handler=handler, valid=True)},
                logger=lambda message: None,
            )
            with patch("core.action_loader.default_config_path", return_value=config_path), patch(
                "core.action_loader.request_confirmation", return_value="pending"
            ) as request:
                result = registry.run("demo", {})

        self.assertEqual(result, "pending")
        request.assert_called_once()

    def test_audit_filters_and_clear_are_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audit.jsonl"
            write_event("action", "computer_control", "succeeded", path=path)
            write_event("confirmation", "computer_shutdown", "cancelled", path=path)
            self.assertEqual(len(read_events(path, event="action")), 1)
            self.assertEqual(read_events(path, status="cancelled")[0]["action"], "computer_shutdown")
            self.assertTrue(clear_events(path))
            self.assertEqual(read_events(path), [])

    def test_memory_update_export_and_forget(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            with patch.object(memory_manager, "MEMORY_PATH", path):
                memory_manager.update_memory({"notes": {"coffee": {"value": "black"}}})
                self.assertIn("Updated", memory_manager.update_entry("notes", "coffee", "espresso"))
                self.assertIn("espresso", memory_manager.export_memory())
                self.assertIn("Forgotten", memory_manager.forget("coffee", "notes"))
                self.assertNotIn("coffee", memory_manager.export_memory())

    def test_mocked_openai_response_normalizes_model_output(self):
        class Response:
            def raise_for_status(self):
                return None

            def json(self):
                return {"choices": [{"message": {"content": " hello ", "tool_calls": []}}]}

        with patch.object(llm_client, "get_llm_provider", return_value="openai"), \
             patch.object(llm_client, "get_llm_settings", return_value=("http://model", "demo")), \
             patch.object(llm_client.requests, "post", return_value=Response()) as post:
            result = llm_client.call_llm([{"role": "user", "content": "hi"}])

        self.assertEqual(result, {"content": "hello", "tool_calls": []})
        self.assertEqual(post.call_args.args[0], "http://model/v1/chat/completions")

    def test_degraded_model_state_keeps_local_features_available(self):
        self.assertEqual(normalize_model_state("network failure"), "offline")
        self.assertEqual(model_status("offline"), {
            "state": "offline",
            "local_features": "available",
            "natural_language": "unavailable",
        })

    def test_health_reports_reconnecting_model_without_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            health = collect_startup_health(
                Path(directory) / "missing.json",
                action_count=1,
                plugin_count=0,
                model_connection="reconnecting",
                dashboard_status="available",
            )

        self.assertEqual(health["model_connection"], "reconnecting")
        self.assertEqual(health["dashboard"], "available")
        self.assertNotIn("gemini_api_key", json.dumps(health))

    def test_permission_explanations_and_reset_preserve_other_config(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "api_keys.json"
            config_path.write_text(
                json.dumps({"gemini_api_key": "secret", "permissions": {"messaging": "blocked"}}),
                encoding="utf-8",
            )
            reset_policy(config_path)
            config = json.loads(config_path.read_text(encoding="utf-8"))

        self.assertEqual(set(EXPLANATIONS), {
            "computer_control", "file_delete", "computer_shutdown",
            "computer_restart", "computer_toggle_wifi", "messaging",
        })
        self.assertTrue(explanation_for("messaging"))
        self.assertNotIn("permissions", config)
        self.assertEqual(config["gemini_api_key"], "secret")

    def test_dashboard_exposes_authenticated_control_routes(self):
        from dashboard.server import DashboardServer

        paths = {route.path for route in DashboardServer().app.routes}
        self.assertTrue({
            "/api/health", "/api/audit", "/api/audit/clear",
            "/api/permissions", "/api/permissions/reset",
        } <= paths)


if __name__ == "__main__":
    unittest.main()
