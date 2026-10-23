import asyncio
import subprocess
import aiohttp
import discord
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from django.test import TestCase, override_settings
from bot.utils import failure_webhook, flag_processor, run_local
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


class ErrorReportingTests(TestCase):
    """Failed rolls keep enough detail (API answer, fork, commit) to triage."""

    async def test_generate_v1_seed_keeps_api_error(self):
        response = MagicMock(status=400)
        response.json = AsyncMock(return_value={
            "errors": ["Seed generation failed. See server logs for details."],
            "stderr": "TypeError: boom",
            "request_id": "abc123",
        })
        session = MagicMock()
        session.post.return_value.__aenter__.return_value = response
        with patch("bot.functions.aiohttp.ClientSession") as mock_session:
            mock_session.return_value.__aenter__.return_value = session
            with self.assertRaises(functions.ApiRollError) as cm:
                await functions.generate_v1_seed("-nfh", None, "dev")

        error = cm.exception
        self.assertEqual(error.status, 400)
        self.assertEqual(error.request_id, "abc123")
        self.assertIn("TypeError: boom", error.details())
        # the bot sends its own request ID for the API to log
        sent_headers = session.post.call_args.kwargs["headers"]
        self.assertEqual(len(sent_headers["X-Request-ID"]), 12)

    def test_local_roll_failure_reports_fork_and_commit(self):
        def fake_run(command, **kwargs):
            if command[0] == "git":
                return subprocess.CompletedProcess(command, 0, stdout="1a2b3c4\n", stderr="")
            raise subprocess.CalledProcessError(1, command, output="", stderr="TypeError: boom")

        with patch("bot.utils.run_local.subprocess.run", side_effect=fake_run):
            with self.assertRaises(run_local.RollException) as cm:
                run_local.generate_local_seed("-cg", "dev", Path("."))

        error = cm.exception
        self.assertEqual(error.fork, "WorldsCollide_dev")
        self.assertEqual(error.fork_commit, "1a2b3c4")
        self.assertEqual(error.sperror, "TypeError: boom")
        self.assertIsNone(error.api_error)

    def test_get_fork_commit_never_raises(self):
        with patch("bot.utils.run_local.subprocess.run", side_effect=OSError("no git")):
            self.assertEqual(run_local.get_fork_commit(Path(".")), "unknown")

    async def test_both_rolls_failing_keeps_the_api_error_in_the_report(self):
        """The headline behaviour: when the API refuses and the local fallback
        also fails, the one report carries both answers."""
        from bot.cogs import seedgen

        api_error = functions.ApiRollError(
            "The API didn't return a seed.", status=400,
            errors=["Seed generation failed."], stderr="TypeError: boom", request_id="abc123",
        )
        local_error = run_local.RollException(
            "The randomizer script failed", "tmpname", "TypeError: boom",
            "WorldsCollide_dev", "1a2b3c4",
        )

        ctx = MagicMock(author=MagicMock(name="u", id=1))
        msg = MagicMock(edit=AsyncMock())
        options = {
            "is_flagsonly": False, "ap_option": None, "is_local": False,
            "flagstring": "-nfh", "seed_desc": None, "dev_type": "dev",
            "mtype": "dev", "silly": "enjoy",
        }

        with patch.object(seedgen, "_log_seed_roll", AsyncMock(return_value=MagicMock(id=7))), \
             patch.object(seedgen.functions, "generate_v1_seed", AsyncMock(side_effect=api_error)), \
             patch.object(seedgen, "_perform_local_roll", AsyncMock(side_effect=local_error)):
            with self.assertRaises(run_local.RollException) as cm:
                await seedgen._execute_roll(ctx, msg, options, ())

        # the API's answer rode along on the local failure
        self.assertIn("request_id=abc123", cm.exception.api_error)
        self.assertIn("TypeError: boom", cm.exception.api_error)
        self.assertEqual(cm.exception.fork, "WorldsCollide_dev")
        # a flag the randomizer rejected is not the API being down
        self.assertIn("couldn't roll this seed", msg.edit.call_args.kwargs["content"])

    async def test_gateway_error_reports_the_api_as_unavailable(self):
        """A 502 HTML page is infrastructure, not a bad flagset."""
        from bot.cogs import seedgen

        gateway_error = functions.ApiRollError(
            "The API returned a response that isn't JSON.", status=502,
            stderr="<html>502 Bad Gateway</html>", request_id="def456",
        )
        ctx = MagicMock(author=MagicMock(name="u", id=1))
        msg = MagicMock(edit=AsyncMock())
        options = {
            "is_flagsonly": False, "ap_option": None, "is_local": False,
            "flagstring": "-cg", "seed_desc": None, "dev_type": None,
            "mtype": "standard", "silly": "enjoy",
        }

        seed_log = MagicMock(id=7, asave=AsyncMock())
        with patch.object(seedgen, "_log_seed_roll", AsyncMock(return_value=seed_log)), \
             patch.object(seedgen.functions, "generate_v1_seed", AsyncMock(side_effect=gateway_error)), \
             patch.object(seedgen, "_perform_local_roll", AsyncMock(return_value=("u", "h", "s"))):
            await seedgen._execute_roll(ctx, msg, options, ())

        self.assertIn("currently unavailable", msg.edit.call_args.kwargs["content"])

    async def test_timeout_keeps_the_request_id_it_sent(self):
        """str(asyncio.TimeoutError()) is empty, so the ID is all triage has."""
        response = MagicMock(status=200)
        session = MagicMock()
        session.post.side_effect = asyncio.TimeoutError()
        with patch("bot.functions.aiohttp.ClientSession") as mock_session:
            mock_session.return_value.__aenter__.return_value = session
            with self.assertRaises(asyncio.TimeoutError) as cm:
                await functions.generate_v1_seed("-nfh", None, "dev")

        self.assertEqual(len(cm.exception.request_id), 12)

    async def test_non_utf8_response_still_falls_back(self):
        """UnicodeDecodeError is a ValueError, so a strict re-decode here would
        escape the caller's fallback tuple entirely."""
        response = MagicMock(status=200)
        response.json = AsyncMock(side_effect=UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid"))
        response.text = AsyncMock(return_value="� garbage")
        session = MagicMock()
        session.post.return_value.__aenter__.return_value = response
        with patch("bot.functions.aiohttp.ClientSession") as mock_session:
            mock_session.return_value.__aenter__.return_value = session
            with self.assertRaises(functions.ApiRollError) as cm:
                await functions.generate_v1_seed("-nfh", None, "dev")

        self.assertEqual(response.text.call_args.kwargs["errors"], "replace")
        self.assertIn("garbage", cm.exception.details())

    def test_timeout_output_is_decoded_for_the_report(self):
        """On POSIX, TimeoutExpired keeps bytes even under text=True."""
        def fake_run(command, **kwargs):
            if command[0] == "git":
                return subprocess.CompletedProcess(command, 0, stdout="1a2b3c4\n", stderr="")
            raise subprocess.TimeoutExpired(command, 180, output=b"", stderr=b"TypeError: boom")

        with patch("bot.utils.run_local.subprocess.run", side_effect=fake_run):
            with self.assertRaises(run_local.RollException) as cm:
                run_local.generate_local_seed("-cg", "dev", Path("."))

        self.assertEqual(cm.exception.sperror, "TypeError: boom")

    async def test_error_report_renders_fork_commit_and_api_error(self):
        """The report a user actually receives carries both failures."""
        from bot.cogs.seedgen import SeedGen

        error = run_local.RollException(
            "The randomizer script failed", "tmpname", "line one\nTypeError: boom",
            "WorldsCollide_dev", "1a2b3c4",
        )
        error.api_error = "The API didn't return a seed.; HTTP 400; request_id=abc123"

        written = {}

        def capture_file(path, *a, **kw):
            with open(path, encoding="utf-8") as f:
                written["report"] = f.read()
            return MagicMock()

        ctx = MagicMock(command="rollseed", message=MagicMock(content="!rollseed -nfh"), send=AsyncMock())
        cog = SeedGen(MagicMock())
        # pinned empty: a populated .env would otherwise send this test's
        # mocked report at a real webhook
        with override_settings(FAILURE_WEBHOOK_URL=""), \
             patch("bot.cogs.seedgen.discord.File", side_effect=capture_file):
            await cog.cog_command_error(ctx, error)

        report = written["report"]
        self.assertIn("Fork: WorldsCollide_dev @ 1a2b3c4", report)
        self.assertIn("request_id=abc123", report)
        self.assertIn("Message: !rollseed -nfh", report)
        self.assertIn("TypeError: boom", report)

    async def test_interaction_report_never_quotes_the_bots_own_message(self):
        """discord.Interaction declares 'message' in __slots__, so a hasattr check
        is always True: on a button click it holds the bot's own seed message, and
        otherwise None. Neither is the user's command, and the None case would
        raise AttributeError inside the error handler itself."""
        from bot.cogs.seedgen import SeedGen

        error = run_local.RollException("boom", "tmpname", "stderr", "WorldsCollide_dev", "1a2b3c4")

        # a button click (message set to the bot's own) and a non-component
        # interaction (message None) must both report 'Interaction'
        for label, message in (
            ("button click", MagicMock(content="Here's your dev seed - enjoy")),
            ("no parent message", None),
        ):
            with self.subTest(label):
                written = {}

                def capture_file(path, *a, **kw):
                    with open(path, encoding="utf-8") as f:
                        written["report"] = f.read()
                    return MagicMock()

                interaction = MagicMock(spec=discord.Interaction)
                interaction.command = "reroll"
                interaction.message = message
                interaction.response = MagicMock(is_done=MagicMock(return_value=True))
                interaction.followup = MagicMock(send=AsyncMock())

                cog = SeedGen(MagicMock())
                with override_settings(FAILURE_WEBHOOK_URL=""), \
                     patch("bot.cogs.seedgen.discord.File", side_effect=capture_file):
                    await cog.cog_command_error(interaction, error)

                self.assertIn("Message: Interaction", written["report"])
                self.assertNotIn("Here's your dev seed", written["report"])
                interaction.followup.send.assert_awaited()


class WebappApiFallbackTests(TestCase):
    """The webapp must not record a successful roll that produced no seed."""

    def test_api_answering_without_a_seed_falls_back_instead_of_logging_success(self):
        from webapp import tasks

        # a 200 whose body carries errors and no url: a flagset the randomizer
        # refused, which is exactly the -nfh case this work started from
        response = MagicMock(status_code=200)
        response.raise_for_status = MagicMock()
        response.json = MagicMock(return_value={"errors": ["Seed generation failed."]})
        response.text = '{"errors": ["Seed generation failed."]}'

        preset = MagicMock(preset_name="atma series", arguments="", flags="-nfh", doc_id=None)
        doc_snap = MagicMock(exists=True, id="doc1")
        doc_snap.to_dict.return_value = {}

        with patch.object(tasks.create_api_seed_task, "update_state"), \
             patch.object(tasks, "db") as firestore_db, \
             patch.object(tasks, "FirestorePresetAdapter", return_value=preset), \
             patch.object(tasks.flag_processor, "apply_args", return_value="-nfh"), \
             patch.object(tasks.requests, "post", return_value=response), \
             patch.object(tasks, "select_fork", return_value="dev"), \
             patch.object(tasks, "_generate_seed_core", return_value="local-url") as local_roll, \
             patch.object(tasks.SeedLog.objects, "create") as seedlog_create, \
             patch.object(tasks, "write_gsheets") as gsheets:
            firestore_db.collection.return_value.document.return_value.get.return_value = doc_snap
            result = tasks.create_api_seed_task.__wrapped__("doc1", "123", "someone")

        # the local fallback ran, and nothing was recorded for the empty answer
        local_roll.assert_called_once()
        seedlog_create.assert_not_called()
        gsheets.assert_not_called()
        self.assertEqual(result, "local-url")


TEST_WEBHOOK = "https://discord.com/api/webhooks/1/token"


def _patch_webhook():
    """Patch the network out, handing back the mock webhook that was sent to."""
    sent = MagicMock(send=AsyncMock())
    return patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent), sent


async def _real_api_error(status=502):
    """An api_error string built the way a failed roll builds it.

    generate_v1_seed mints a fresh request_id per request and it ends up in
    this string, so a hand-written fixture would hide whether two identical
    failures actually collapse. Built by calling the code that produces it.
    """
    response = MagicMock(status=status)
    response.json = AsyncMock(return_value={"errors": ["Seed generation failed."]})
    session = MagicMock()
    session.post.return_value.__aenter__.return_value = response
    with patch("bot.functions.aiohttp.ClientSession") as mock_session:
        mock_session.return_value.__aenter__.return_value = session
        try:
            await functions.generate_v1_seed("-nfh", None, "dev")
        except functions.ApiRollError as e:
            return e.details()
    raise AssertionError("generate_v1_seed was expected to fail")


class FailureWebhookTests(TestCase):
    """Failed rolls reach a private channel, without the reporting itself
    becoming a way for a roll to fail worse."""

    def setUp(self):
        failure_webhook.reset_throttle()

    async def test_no_webhook_configured_posts_nothing(self):
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=""), patcher:
            posted = await failure_webhook.send_failure_report(
                failure_id="a1b2c3d4", command="rollseed", user="someone", guild="a server",
            )

        self.assertFalse(posted)
        sent.send.assert_not_awaited()

    async def test_report_carries_the_reference_fork_and_stderr(self):
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            posted = await failure_webhook.send_failure_report(
                failure_id="a1b2c3d4", command="rollseed", user="someone", guild="a server",
                fork="WorldsCollide_dev", fork_commit="92c5c32",
                api_error="The API did not return a seed.; HTTP 400; request_id=abc123",
                stderr_tail="TypeError: boom",
            )

        self.assertTrue(posted)
        embed = sent.send.call_args.kwargs["embed"]
        rendered = embed.description + "".join(f"{f.name}{f.value}" for f in embed.fields)
        self.assertIn("a1b2c3d4", rendered)
        self.assertIn("WorldsCollide_dev @ 92c5c32", rendered)
        self.assertIn("request_id=abc123", rendered)
        self.assertIn("TypeError: boom", rendered)

    async def test_an_outage_collapses_into_one_post(self):
        """Every roll failing the same way must not spend the rate limit.

        The api_error comes from generate_v1_seed, which stamps a fresh
        request_id per request. A hand-written fixture without one made this
        test pass while the throttle collapsed nothing in production.
        """
        errors = [await _real_api_error() for _ in range(5)]
        self.assertEqual(len(set(errors)), 5, "each failure should carry its own request_id")

        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            results = [
                await failure_webhook.send_failure_report(
                    failure_id=f"id{n}", command="rollseed", user="someone", guild="a server",
                    api_error=api_error,
                )
                for n, api_error in enumerate(errors)
            ]

        self.assertEqual(results, [True, False, False, False, False])
        self.assertEqual(sent.send.await_count, 1)
        # and one signature tracked, not five
        self.assertEqual(failure_webhook._throttle.tracked, 1)

    async def test_the_tracked_set_stays_bounded(self):
        """Signatures come from error text, so the set must not grow forever."""
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            for n in range(failure_webhook.MAX_TRACKED * 2):
                await failure_webhook.send_failure_report(
                    failure_id="x", command="rollseed", user="u", guild="g",
                    stderr_tail=f"TypeError: distinct failure {n}",
                )

        self.assertLessEqual(failure_webhook._throttle.tracked, failure_webhook.MAX_TRACKED)

    async def test_the_next_post_says_what_it_stands_for(self):
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            await failure_webhook.send_failure_report(
                failure_id="first", command="rollseed", user="u", guild="g",
                api_error="ClientError: down",
            )
            for _ in range(3):
                await failure_webhook.send_failure_report(
                    failure_id="dupe", command="rollseed", user="u", guild="g",
                    api_error="ClientError: down",
                )
            # the window has passed, so the next identical failure reports again
            failure_webhook._throttle.cooldown = 0
            await failure_webhook.send_failure_report(
                failure_id="later", command="rollseed", user="u", guild="g",
                api_error="ClientError: down",
            )

        self.assertEqual(sent.send.await_count, 2)
        footer = sent.send.call_args.kwargs["embed"].footer.text
        self.assertIn("+3 identical", footer)
        # the window is when they were counted against, not how long ago
        self.assertIn("since the last report", footer)

    async def test_different_failures_are_not_collapsed(self):
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            await failure_webhook.send_failure_report(
                failure_id="one", command="rollseed", user="u", guild="g",
                stderr_tail="TypeError: boom",
            )
            await failure_webhook.send_failure_report(
                failure_id="two", command="rollseed", user="u", guild="g",
                stderr_tail="KeyError: other",
            )

        self.assertEqual(sent.send.await_count, 2)

    async def test_a_broken_webhook_is_swallowed(self):
        """The roll already failed; the notification must not raise on top."""
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url",
                          side_effect=aiohttp.ClientError("no route")):
            posted = await failure_webhook.send_failure_report(
                failure_id="a1b2c3d4", command="rollseed", user="u", guild="g",
            )

        self.assertFalse(posted)

    async def test_long_values_fit_the_discord_field_limit(self):
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            await failure_webhook.send_failure_report(
                failure_id="a1b2c3d4", command="rollseed", user="u", guild="g",
                api_error="x" * 5000, stderr_tail="y" * 5000,
            )

        for field in sent.send.call_args.kwargs["embed"].fields:
            self.assertLessEqual(len(field.value), 1024, field.name)


    async def test_a_failed_post_leaves_the_window_open_for_a_retry(self):
        """A transient 500 must not suppress the healthy failure behind it.
        from_url raising only covers the path before the POST; this covers
        send itself failing, which is what a revoked token does."""
        api_error = await _real_api_error()
        broken = MagicMock(send=AsyncMock(
            side_effect=discord.HTTPException(MagicMock(status=500), "boom")))
        healthy = MagicMock(send=AsyncMock())

        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK):
            with patch.object(failure_webhook.discord.Webhook, "from_url", return_value=broken):
                first = await failure_webhook.send_failure_report(
                    failure_id="a", command="rollseed", user="u", guild="g", api_error=api_error,
                )
            with patch.object(failure_webhook.discord.Webhook, "from_url", return_value=healthy):
                second = await failure_webhook.send_failure_report(
                    failure_id="b", command="rollseed", user="u", guild="g",
                    api_error=await _real_api_error(),
                )

        self.assertFalse(first)
        self.assertTrue(second, "the healthy retry was suppressed by a post that never landed")
        self.assertEqual(healthy.send.await_count, 1)

    async def test_a_failed_post_keeps_the_suppressed_tally(self):
        """The count the next post stands for must survive a failed delivery.

        A tally only accrues while posting works, so: one good post, two
        suppressed behind it, then the window reopens and that post fails.
        The two must still be there for the post after it.
        """
        healthy = MagicMock(send=AsyncMock())
        broken = MagicMock(send=AsyncMock(
            side_effect=discord.HTTPException(MagicMock(status=500), "boom")))
        kwargs = dict(command="rollseed", user="u", guild="g", stderr_tail="TypeError: boom")

        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK):
            with patch.object(failure_webhook.discord.Webhook, "from_url", return_value=healthy):
                await failure_webhook.send_failure_report(failure_id="first", **kwargs)
                for _ in range(2):
                    await failure_webhook.send_failure_report(failure_id="dupe", **kwargs)

            failure_webhook._throttle.cooldown = 0
            # the window reopens, and this one does not land
            with patch.object(failure_webhook.discord.Webhook, "from_url", return_value=broken):
                failed = await failure_webhook.send_failure_report(failure_id="lost", **kwargs)

            with patch.object(failure_webhook.discord.Webhook, "from_url", return_value=healthy):
                await failure_webhook.send_failure_report(failure_id="later", **kwargs)

        self.assertFalse(failed)
        footer = healthy.send.call_args.kwargs["embed"].footer.text
        self.assertIn("+2 identical", footer)

    async def test_error_type_separates_failures_with_nothing_else_to_go_on(self):
        """The cog always sends stderr_tail, so error_type is the fallback for
        a caller that has neither it nor an api_error. Without it they would
        all share one signature."""
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            for error_type in ("KeyError", "AttributeError", "KeyError"):
                await failure_webhook.send_failure_report(
                    failure_id="x", command="rollseed", user="u", guild="g",
                    api_error=None, stderr_tail=None, error_type=error_type,
                )

        # the two KeyErrors collapse, the AttributeError does not
        self.assertEqual(sent.send.await_count, 2)

    async def test_a_truncated_error_keeps_its_code_fence_closed(self):
        """An unbalanced fence would swallow every field after it."""
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher:
            await failure_webhook.send_failure_report(
                failure_id="a1b2c3d4", command="rollseed", user="u", guild="g",
                stderr_tail="y" * 5000,
            )

        value = [f.value for f in sent.send.call_args.kwargs["embed"].fields
                 if f.name == "Error"][0]
        self.assertEqual(value.count("```") % 2, 0, "unbalanced code fence")
        self.assertTrue(value.endswith("```"))
        self.assertLessEqual(len(value), 1024)

    async def test_a_formatting_bug_is_not_logged_as_a_network_failure(self):
        patcher, sent = _patch_webhook()
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), patcher, \
             patch.object(failure_webhook, "_build_embed", side_effect=TypeError("bad field")):
            with self.assertLogs("bot.utils.failure_webhook", level="ERROR") as logs:
                posted = await failure_webhook.send_failure_report(
                    failure_id="a1b2c3d4", command="rollseed", user="u", guild="g",
                )

        self.assertFalse(posted)
        sent.send.assert_not_awaited()
        self.assertIn("Could not build", "".join(logs.output))
        # the window was given back, so the next failure still reports
        self.assertEqual(failure_webhook._throttle.tracked, 0)

class FailureReportIntegrationTests(TestCase):
    """The handler's report, the user's message and the webhook all agree."""

    def setUp(self):
        failure_webhook.reset_throttle()

    async def _run_handler(self):
        from bot.cogs.seedgen import SeedGen

        error = run_local.RollException(
            "The randomizer script failed", "tmpname", "line one\nTypeError: boom",
            "WorldsCollide_dev", "92c5c32",
        )
        error.api_error = "The API did not return a seed.; HTTP 400; request_id=abc123"

        reports = []

        def capture_file(path, *a, **kw):
            with open(path, encoding="utf-8") as f:
                reports.append(f.read())
            return MagicMock()

        ctx = MagicMock(command="rollseed", message=MagicMock(content="!rollseed -nfh"),
                        send=AsyncMock())
        ctx.author.name = "someone"
        ctx.guild.name = "FF6WC"

        cog = SeedGen(MagicMock())
        with patch("bot.cogs.seedgen.discord.File", side_effect=capture_file):
            await cog.cog_command_error(ctx, error)
        return ctx, reports[0]

    async def test_unset_webhook_leaves_the_user_facing_behaviour_alone(self):
        sent = MagicMock(send=AsyncMock())
        with override_settings(FAILURE_WEBHOOK_URL=""), \
             patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent):
            ctx, report = await self._run_handler()

        sent.send.assert_not_awaited()
        ctx.send.assert_awaited()
        self.assertIn("Reference:", report)

    async def test_the_same_reference_reaches_the_user_and_the_channel(self):
        sent = MagicMock(send=AsyncMock())
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent):
            ctx, report = await self._run_handler()

        # the reference the user is told to quote
        quoted = ctx.send.call_args.kwargs["content"]
        reference = quoted.split("`")[1]
        self.assertEqual(len(reference), 8)

        # the same one in the attached report and in the private channel
        self.assertIn(f"Reference: {reference}", report)
        embed = sent.send.call_args.kwargs["embed"]
        self.assertIn(reference, embed.description)
        rendered = "".join(f"{f.name}{f.value}" for f in embed.fields)
        self.assertIn("WorldsCollide_dev @ 92c5c32", rendered)
        self.assertIn("FF6WC", rendered)
        self.assertIn("someone", rendered)

    async def test_a_broken_webhook_still_leaves_the_user_their_report(self):
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url",
                          side_effect=aiohttp.ClientError("no route")):
            ctx, report = await self._run_handler()

        ctx.send.assert_awaited()
        self.assertIn("Reference:", report)

    async def test_an_unexpected_error_is_also_referenced_and_reported(self):
        """The generic path matters most for triage: it is the errors nobody
        has anticipated, and it has no fork or API error to go on."""
        from bot.cogs.seedgen import SeedGen

        reports = []

        def capture_file(path, *a, **kw):
            with open(path, encoding="utf-8") as f:
                reports.append(f.read())
            return MagicMock()

        ctx = MagicMock(command="rollseed", message=MagicMock(content="!rollseed -cg"),
                        send=AsyncMock())
        ctx.author.name = "someone"
        ctx.guild.name = "FF6WC"

        sent = MagicMock(send=AsyncMock())
        cog = SeedGen(MagicMock())
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent), \
             patch("bot.cogs.seedgen.discord.File", side_effect=capture_file):
            await cog.cog_command_error(ctx, KeyError("something nobody expected"))

        reference = ctx.send.call_args.kwargs["content"].split("`")[1]
        self.assertEqual(len(reference), 8)
        self.assertIn(f"Reference: {reference}", reports[0])

        embed = sent.send.call_args.kwargs["embed"]
        self.assertIn(reference, embed.description)
        # no fork and no API error, and the embed renders anyway
        rendered = "".join(f"{f.name}{f.value}" for f in embed.fields)
        self.assertIn("n/a", rendered)


    async def test_the_channel_hears_about_it_when_the_user_cannot(self):
        """Missing Attach Files, an expired interaction token, an oversized
        report: the user is left with a command that did nothing, so the
        webhook is the only trace this roll happened."""
        from bot.cogs.seedgen import SeedGen

        error = run_local.RollException(
            "The randomizer script failed", "tmpname", "TypeError: boom",
            "WorldsCollide_dev", "92c5c32",
        )
        ctx = MagicMock(command="rollseed", message=MagicMock(content="!rollseed -nfh"))
        ctx.send = AsyncMock(
            side_effect=discord.Forbidden(MagicMock(status=403), "Missing Permissions"))
        ctx.author.name = "someone"
        ctx.guild.name = "FF6WC"

        sent = MagicMock(send=AsyncMock())
        cog = SeedGen(MagicMock())
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent), \
             patch("bot.cogs.seedgen.discord.File", return_value=MagicMock()):
            with self.assertRaises(discord.Forbidden):
                await cog.cog_command_error(ctx, error)

        sent.send.assert_awaited_once()
        embed = sent.send.call_args.kwargs["embed"]
        rendered = "".join(f"{f.value}" for f in embed.fields)
        self.assertIn("WorldsCollide_dev @ 92c5c32", rendered)

    async def test_two_unrelated_unexpected_errors_are_both_reported(self):
        """An unanticipated error is the one you most need to see twice."""
        from bot.cogs.seedgen import SeedGen

        sent = MagicMock(send=AsyncMock())
        cog = SeedGen(MagicMock())
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent), \
             patch("bot.cogs.seedgen.discord.File", return_value=MagicMock()):
            for err in (KeyError("missing thing"), AttributeError("other thing")):
                ctx = MagicMock(command="rollseed", message=MagicMock(content="!rollseed -cg"),
                                send=AsyncMock())
                ctx.author.name = "someone"
                ctx.guild.name = "FF6WC"
                await cog.cog_command_error(ctx, err)

        self.assertEqual(sent.send.await_count, 2)

    async def test_the_same_unexpected_error_twice_collapses(self):
        from bot.cogs.seedgen import SeedGen

        sent = MagicMock(send=AsyncMock())
        cog = SeedGen(MagicMock())
        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent), \
             patch("bot.cogs.seedgen.discord.File", return_value=MagicMock()):
            for _ in range(2):
                ctx = MagicMock(command="rollseed", message=MagicMock(content="!rollseed -cg"),
                                send=AsyncMock())
                ctx.author.name = "someone"
                ctx.guild.name = "FF6WC"
                await cog.cog_command_error(ctx, KeyError("same thing"))

        self.assertEqual(sent.send.await_count, 1)

    async def test_an_unexpected_error_is_named_in_the_log_and_the_embed(self):
        """The reference must reach the log on every path, and the embed must
        not claim a local roll when no roll was attempted."""
        from bot.cogs.seedgen import SeedGen

        sent = MagicMock(send=AsyncMock())
        cog = SeedGen(MagicMock())
        ctx = MagicMock(command="rollseed", message=MagicMock(content="!rollseed -cg"),
                        send=AsyncMock())
        ctx.author.name = "someone"
        ctx.guild.name = "FF6WC"

        with override_settings(FAILURE_WEBHOOK_URL=TEST_WEBHOOK), \
             patch.object(failure_webhook.discord.Webhook, "from_url", return_value=sent), \
             patch("bot.cogs.seedgen.discord.File", return_value=MagicMock()):
            with self.assertLogs("bot.cogs.seedgen", level="ERROR") as logs:
                await cog.cog_command_error(ctx, KeyError("missing thing"))

        reference = ctx.send.call_args.kwargs["content"].split("`")[1]
        logged = "".join(logs.output)
        self.assertIn(reference, logged)
        self.assertIn("KeyError", logged)

        rendered = "".join(f"{f.value}" for f in sent.send.call_args.kwargs["embed"].fields)
        self.assertIn("KeyError", rendered)
        self.assertNotIn("local roll only", rendered)
