import unittest
from unittest.mock import MagicMock
from django.test import TestCase
from bot.utils import flag_processor
from bot.utils.run_local import resolve_fork_dir, FORK_DIRECTORIES, ARG_TO_FORK_MAP
from bot import functions


class RuinationEasyModeTests(TestCase):
    def test_fork_directories_ruin_variants(self):
        """Ensure FORK_DIRECTORIES has all ruin variants mapped to WorldsCollide_ruination."""
        self.assertEqual(FORK_DIRECTORIES.get("ruin"), "WorldsCollide_ruination")
        self.assertEqual(FORK_DIRECTORIES.get("ruinhard"), "WorldsCollide_ruination")
        self.assertEqual(FORK_DIRECTORIES.get("ruineasy"), "WorldsCollide_ruination")

    def test_arg_to_fork_map(self):
        """Ensure ARG_TO_FORK_MAP maps ruineasy and ruinhard to ruin fork."""
        self.assertEqual(ARG_TO_FORK_MAP.get("ruin"), "ruin")
        self.assertEqual(ARG_TO_FORK_MAP.get("ruinhard"), "ruin")
        self.assertEqual(ARG_TO_FORK_MAP.get("ruineasy"), "ruin")

    def test_resolve_fork_dir_ruineasy(self):
        """Test fork directory resolution with ruineasy arguments or flags."""
        self.assertEqual(resolve_fork_dir(arguments=["ruineasy"]), "WorldsCollide_ruination")
        self.assertEqual(resolve_fork_dir(arguments=["ruinhard"]), "WorldsCollide_ruination")
        self.assertEqual(resolve_fork_dir(flags="-ruin easy"), "WorldsCollide_ruination")
        self.assertEqual(resolve_fork_dir(flags="-ruin hard"), "WorldsCollide_ruination")

    def test_arg_action_map_ruineasy(self):
        """Test ARG_ACTION_MAP applies -ruin easy correctly."""
        action = flag_processor.ARG_ACTION_MAP.get("ruineasy")
        self.assertIsNotNone(action)
        self.assertEqual(action(""), " -ruin easy")
        self.assertEqual(action("-cg -open"), "-cg -open -ruin easy")
        # Should not append if -ruin is already in flags
        self.assertEqual(action("-ruin"), "-ruin")
        self.assertEqual(action("-ruin easy"), "-ruin easy")

    def test_apply_args_ruineasy(self):
        """Test apply_args properly processes ruineasy arguments."""
        result = flag_processor.apply_args("", ["ruineasy"])
        self.assertTrue(result.startswith("-ruin easy") or "-ruin easy" in result)

        # Test with existing -ruin easy flags
        result_existing = flag_processor.apply_args("-ruin easy", [])
        self.assertTrue(result_existing.startswith("-ruin easy"))

        # Test with existing -ruin hard flags
        result_hard = flag_processor.apply_args("-ruin hard", [])
        self.assertTrue(result_hard.startswith("-ruin hard"))

    async def test_argparse_ruineasy_command(self):
        """Test functions.argparse with ruineasy mtype and base flags."""
        mock_ctx = MagicMock()
        mock_ctx.author = "TestUser"

        # Simulating !ruineasy
        options = await functions.argparse(mock_ctx, "-ruin easy", [], "ruin_easy")
        self.assertEqual(options["mtype"], "ruin_easy")
        self.assertEqual(options["dev_type"], "ruin")
        self.assertTrue(options["is_local"])
        self.assertTrue(options["flagstring"].startswith("-ruin easy"))

        # Simulating !ruin easy
        options_ruin_easy = await functions.argparse(mock_ctx, "-ruin easy", ["easy"], "ruin")
        self.assertEqual(options_ruin_easy["mtype"], "ruin_easy")
        self.assertEqual(options_ruin_easy["dev_type"], "ruin")
        self.assertTrue(options_ruin_easy["is_local"])
        self.assertTrue(options_ruin_easy["flagstring"].startswith("-ruin easy"))

        # Simulating !ruineasy &tunes
        options_tunes = await functions.argparse(mock_ctx, "-ruin easy", ["tunes"], "ruin_easy")
        self.assertIn("ruin_easy", options_tunes["mtype"])
        self.assertEqual(options_tunes["dev_type"], "ruin")
        self.assertEqual(options_tunes["tunes_type"], "tunes")
        self.assertTrue(options_tunes["is_local"])
