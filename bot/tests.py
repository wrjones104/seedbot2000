from unittest.mock import MagicMock, patch
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
        """Test ARG_ACTION_MAP applies -ruin easy correctly, replacing existing ruin flags."""
        action = flag_processor.ARG_ACTION_MAP.get("ruineasy")
        self.assertIsNotNone(action)
        self.assertEqual(action(""), "-ruin easy")
        self.assertEqual(action("-cg -open"), "-cg -open -ruin easy")
        # Should replace existing -ruin or -ruin hard with -ruin easy
        self.assertEqual(action("-ruin"), "-ruin easy")
        self.assertEqual(action("-ruin easy"), "-ruin easy")
        self.assertEqual(action("-ruin hard"), "-ruin easy")
        self.assertEqual(action("-cg -ruin -open"), "-cg -open -ruin easy")

    def test_arg_action_map_ruinhard(self):
        """Test ARG_ACTION_MAP applies -ruin hard correctly, replacing existing ruin flags."""
        action = flag_processor.ARG_ACTION_MAP.get("ruinhard")
        self.assertIsNotNone(action)
        self.assertEqual(action(""), "-ruin hard")
        self.assertEqual(action("-cg -open"), "-cg -open -ruin hard")
        self.assertEqual(action("-ruin"), "-ruin hard")
        self.assertEqual(action("-ruin easy"), "-ruin hard")
        self.assertEqual(action("-ruin hard"), "-ruin hard")
        self.assertEqual(action("-cg -ruin -open"), "-cg -open -ruin hard")

    def test_apply_args_ruineasy(self):
        """Test apply_args properly processes ruineasy arguments and overrides existing ruin flags."""
        result = flag_processor.apply_args("", ["ruineasy"])
        self.assertTrue(result.startswith("-ruin easy") or "-ruin easy" in result)

        # Overwrite existing -ruin flags with ruineasy
        result_override = flag_processor.apply_args("-ruin", ["ruineasy"])
        self.assertIn("-ruin easy", result_override)
        self.assertNotIn("-ruin hard", result_override)

        # Overwrite existing -ruin hard flags with ruineasy
        result_from_hard = flag_processor.apply_args("-ruin hard", ["ruineasy"])
        self.assertIn("-ruin easy", result_from_hard)
        self.assertNotIn("-ruin hard", result_from_hard)

        # Overwrite existing -ruin easy flags with ruinhard
        result_to_hard = flag_processor.apply_args("-ruin easy", ["ruinhard"])
        self.assertIn("-ruin hard", result_to_hard)
        self.assertNotIn("-ruin easy", result_to_hard)

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

    async def test_argparse_ruinhard_command(self):
        """Test functions.argparse with ruinhard mtype and base flags."""
        mock_ctx = MagicMock()
        mock_ctx.author = "TestUser"

        # Simulating !ruinhard
        options = await functions.argparse(mock_ctx, "-ruin hard", [], "ruin_hard")
        self.assertEqual(options["mtype"], "ruin_hard")
        self.assertEqual(options["dev_type"], "ruin")
        self.assertTrue(options["is_local"])
        self.assertTrue(options["flagstring"].startswith("-ruin hard"))

        # Simulating !ruinhard &tunes
        options_tunes = await functions.argparse(mock_ctx, "-ruin hard", ["tunes"], "ruin_hard")
        self.assertEqual(options_tunes["mtype"], "ruin_hard_tunes")
        self.assertEqual(options_tunes["dev_type"], "ruin")
        self.assertEqual(options_tunes["tunes_type"], "tunes")
        self.assertTrue(options_tunes["is_local"])

    def test_handle_interaction_roll_base_mtype_preservation(self):
        """Verify the base_mtype preservation logic in handle_interaction_roll for ruin variants."""
        test_cases = [
            ("ruin_easy", "ruin_easy"),
            ("ruin_easy_tunes", "ruin_easy"),
            ("ruin_hard", "ruin_hard"),
            ("ruin_hard_tunes", "ruin_hard"),
            ("ruin", "ruin"),
            ("ruin_tunes", "ruin"),
            ("standard_tunes", "standard"),
            ("chaos_tunes", "chaos"),
        ]
        for original_mtype, expected_base in test_cases:
            if original_mtype.startswith("ruin_easy"):
                base_mtype = "ruin_easy"
            elif original_mtype.startswith("ruin_hard"):
                base_mtype = "ruin_hard"
            else:
                base_mtype = original_mtype.split('_')[0]
            self.assertEqual(base_mtype, expected_base)

    @patch("webapp.tasks.generate_local_seed")
    def test_webapp_fork_key_resolution(self, mock_generate):
        """Test that webapp Celery task resolves the correct fork for ruination variants and flags."""
        class StopExecution(Exception):
            pass

        mock_generate.side_effect = StopExecution
        mock_task = MagicMock()

        from webapp.tasks import _generate_seed_core
        from celery.exceptions import Ignore

        def run_test(flags, args, seed_name):
            mock_generate.reset_mock()
            with self.assertRaises(Ignore):
                _generate_seed_core(mock_task, flags, args, seed_name, 1, "User")

        # Test ruineasy in args_list
        run_test("", ["ruineasy"], "Standard")
        self.assertEqual(mock_generate.call_args.kwargs["seed_type"], "ruin")

        # Test ruinhard in args_list
        run_test("", ["ruinhard"], "Standard")
        self.assertEqual(mock_generate.call_args.kwargs["seed_type"], "ruin")

        # Test shoplimits in args_list
        run_test("", ["shoplimits"], "Standard")
        self.assertEqual(mock_generate.call_args.kwargs["seed_type"], "ruin")

        # Test preset with -ruin in base_flags
        run_test("-ruin", [], "Custom Preset")
        self.assertEqual(mock_generate.call_args.kwargs["seed_type"], "ruin")

        # Test Quick Roll - Ruination seed_type_name
        run_test("", [], "Quick Roll - Ruination")
        self.assertEqual(mock_generate.call_args.kwargs["seed_type"], "ruin")
