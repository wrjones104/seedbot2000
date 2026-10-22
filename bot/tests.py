import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch
from django.test import TestCase
from bot.utils import flag_processor, run_local
from bot.utils.run_local import (
    resolve_fork_dir, select_fork, dev_only_flags, get_fork_flags, FORK_DIRECTORIES, ARG_TO_FORK_MAP
)
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

    async def test_argparse_ruin_specflags(self):
        """Simulating !ruin &specflags -open -sc1 umaro: flags reach the flagstring, not the mtype."""
        mock_ctx = MagicMock()
        mock_ctx.author = "TestUser"

        options = await functions.argparse(mock_ctx, "-ruin", ["specflags -open -sc1 umaro"], "ruin")
        self.assertEqual(options["mtype"], "ruin")
        self.assertIn("-open", options["flagstring"])
        self.assertIn("-sc1 umaro", options["flagstring"])

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

    @patch("bot.utils.run_local.get_fork_flags", side_effect=lambda name: _FAKE_FORK_FLAGS.get(name, frozenset()))
    @patch("webapp.tasks.generate_local_seed")
    def test_webapp_fork_key_dev_only_flags(self, mock_generate, _mock_flags):
        """Webapp local rolls send flags only the dev fork knows to dev."""
        class StopExecution(Exception):
            pass

        mock_generate.side_effect = StopExecution
        from webapp.tasks import _generate_seed_core
        from celery.exceptions import Ignore

        for flags, expected in (("-cg -nfh", "dev"), ("-cg -sli", "dev"), ("-cg -sl", None)):
            with self.assertRaises(Ignore):
                _generate_seed_core(MagicMock(), flags, [], "Custom Preset", 1, "User")
            self.assertEqual(mock_generate.call_args.kwargs["seed_type"], expected, flags)


# Fixed flag sets, so routing tests don't depend on which commits the
# randomizer_forks submodules have checked out.
_MAIN_FLAGS = frozenset({"-i", "-o", "-s", "-sl", "-cg", "-open", "-sc1"})
_DEV_FLAGS = _MAIN_FLAGS | {"-nfh", "-sli"}
_FAKE_FORK_FLAGS = {
    "WorldsCollide": _MAIN_FLAGS,
    "WorldsCollide_dev": _DEV_FLAGS,
    "WorldsCollide_ruination": _DEV_FLAGS | {"-ruin"},
}


class ForkFlagsSmokeTests(TestCase):
    def test_get_fork_flags_reads_real_parsers(self):
        """The flag dump works on the checked-out main and dev forks' parsers."""
        for fork in ("WorldsCollide", FORK_DIRECTORIES["dev"]):
            self.assertIn("-sl", get_fork_flags(fork), fork)


class DevRoutingTests(TestCase):
    """!devseed and flags that only the dev fork knows (e.g. -nfh, -sli)."""

    def setUp(self):
        self.mock_ctx = MagicMock()
        self.mock_ctx.author = "TestUser"
        patcher = patch(
            "bot.utils.run_local.get_fork_flags",
            side_effect=lambda name: _FAKE_FORK_FLAGS.get(name, frozenset()),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_select_fork(self):
        self.assertEqual(dev_only_flags("-cg -nfh -sli -sl"), ["-nfh", "-sli"])
        self.assertEqual(select_fork([], "-cg -nfh"), "dev")
        self.assertEqual(select_fork(["tunes"], "-cg -sli"), "dev")
        self.assertIsNone(select_fork([], "-cg -sl"))
        # An explicit fork argument or -ruin wins over dev-only flags
        self.assertEqual(select_fork(["ruin"], "-cg -sli"), "ruin")
        self.assertEqual(select_fork(["shoplimits"], "-cg"), "ruin")
        self.assertEqual(select_fork([], "-ruin -nfh"), "ruin")
        self.assertEqual(select_fork(["jones"], "-nfh"), "jones")
        # -ruin in the flags wins over a fork argument
        self.assertEqual(select_fork(["jones"], "-ruin"), "ruin")
        # 'new' is an alias for dev
        self.assertEqual(select_fork(["new"], "-cg"), "dev")
        # A bare '=' argument is ignored rather than crashing
        self.assertIsNone(select_fork(["=", "&="], "-cg"))
        self.assertEqual(resolve_fork_dir(flags="-cg -nfh"), "WorldsCollide_dev")

    def test_unreadable_fork_disables_flag_routing(self):
        with patch("bot.utils.run_local.get_fork_flags", return_value=frozenset()):
            self.assertIsNone(select_fork([], "-cg -nfh"))

    def test_get_fork_flags_caches_failures(self):
        """A fork whose flags can't be read isn't re-run on every call."""
        self.addCleanup(run_local._fork_flags_cache.pop, "WorldsCollide_dev", None)
        run_local._fork_flags_cache.pop("WorldsCollide_dev", None)
        error = subprocess.CalledProcessError(1, "python")
        # get_fork_flags here is the real function, imported before setUp patched the module
        with patch("bot.utils.run_local.subprocess.run", side_effect=error) as mock_run:
            self.assertEqual(get_fork_flags("WorldsCollide_dev"), frozenset())
            self.assertEqual(get_fork_flags("WorldsCollide_dev"), frozenset())
        self.assertEqual(mock_run.call_count, 1)

    async def test_argparse_devseed(self):
        """Simulating !devseed -cg -nfh -sl: rolls on dev, flags are not treated as args."""
        options = await functions.argparse(self.mock_ctx, "-cg -nfh -sl", [], "dev")
        self.assertEqual(options["dev_type"], "dev")
        self.assertEqual(options["mtype"], "dev")
        self.assertFalse(options["is_local"])
        self.assertIn("-nfh", options["flagstring"].split())

        # !devseed ... &tunes rolls locally on the dev fork
        options_tunes = await functions.argparse(self.mock_ctx, "-cg -nfh", ["tunes"], "dev")
        self.assertEqual(options_tunes["dev_type"], "dev")
        self.assertEqual(options_tunes["mtype"], "dev_tunes")
        self.assertTrue(options_tunes["is_local"])

    async def test_argparse_devseed_sli(self):
        """-sli on dev no longer forces the ruination fork (which raised an incompatible-forks error)."""
        options = await functions.argparse(self.mock_ctx, "-cg -sli", [], "dev")
        self.assertEqual(options["dev_type"], "dev")
        self.assertIn("-sli", options["flagstring"].split())

    async def test_argparse_specflags_routes_to_dev(self):
        """Simulating !preset X &specflags -nfh and !rollseed -cg -sli: sent to the dev API."""
        options = await functions.argparse(self.mock_ctx, "-cg -sl", ["specflags -nfh"], "preset_X")
        self.assertEqual(options["dev_type"], "dev")
        self.assertFalse(options["is_local"])
        self.assertIn("-nfh", options["flagstring"].split())

        options_sli = await functions.argparse(self.mock_ctx, "-cg -sli", [], "manually rolled")
        self.assertEqual(options_sli["dev_type"], "dev")
        self.assertIn("-sli", options_sli["flagstring"].split())

    async def test_argparse_plain_flags_stay_on_main(self):
        options = await functions.argparse(self.mock_ctx, "-cg -sl", [], "manually rolled")
        self.assertIsNone(options["dev_type"])

    async def test_argparse_ruin_keeps_ruin_fork(self):
        options = await functions.argparse(self.mock_ctx, "-ruin -nfh", [], "ruin")
        self.assertEqual(options["dev_type"], "ruin")

    def test_generate_local_seed_sli_filter(self):
        """-sli is kept for forks whose parser has it and stripped for the rest."""
        class StopExecution(Exception):
            pass

        def roll_command(seed_type):
            with patch("bot.utils.run_local.subprocess.run", side_effect=StopExecution) as mock_run:
                with self.assertRaises(StopExecution):
                    run_local.generate_local_seed("-cg -sli", seed_type, Path("."))
            return mock_run.call_args.args[0]

        for seed_type, keeps_sli in (("dev", True), ("ruin", True), (None, False)):
            self.assertEqual("-sli" in roll_command(seed_type), keeps_sli, seed_type)

        # If a fork's flags can't be read, only the ruination fork keeps -sli
        with patch("bot.utils.run_local.get_fork_flags", return_value=frozenset()):
            for seed_type, keeps_sli in (("dev", False), ("ruin", True), (None, False)):
                self.assertEqual("-sli" in roll_command(seed_type), keeps_sli, seed_type)
