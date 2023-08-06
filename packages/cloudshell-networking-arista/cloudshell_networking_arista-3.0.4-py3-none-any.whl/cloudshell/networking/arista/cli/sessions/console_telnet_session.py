from collections import OrderedDict

from cloudshell.cli.session.telnet_session import TelnetSession


class ConsoleTelnetSession(TelnetSession):
    SESSION_TYPE = "CONSOLE_TELNET"
    _START_WITH_NEW_LINE = False

    def __init__(
        self,
        host,
        username,
        password,
        port=None,
        on_session_start=None,
        *args,
        **kwargs
    ):
        super().__init__(
            host,
            username,
            password,
            port,
            on_session_start,
            loop_detector_max_action_loops=5,
            *args,
            **kwargs
        )

    def _connect_actions(self, prompt, logger):
        """Open connection to device / create session.

        :param prompt:
        :param logger:
        """
        action_map = OrderedDict()
        action_map[
            "[Ll]ogin:|[Uu]ser:|[Uu]sername:"
        ] = lambda session, logger: session.send_line(session.username, logger)
        action_map["[Pp]assword:"] = lambda session, logger: session.send_line(
            session.password, logger
        )
        empty_key = r".*"

        def empty_action(ses, log):
            ses.send_line("", log)
            if empty_key in action_map:
                del action_map[empty_key]

        action_map[empty_key] = empty_action
        cmd = None
        if self._START_WITH_NEW_LINE:
            cmd = ""
        self.hardware_expect(
            cmd,
            expected_string=prompt,
            timeout=self._timeout,
            logger=logger,
            action_map=action_map,
        )
        self._on_session_start(logger)


class ConsoleTelnetSessionNewLine(ConsoleTelnetSession):
    _START_WITH_NEW_LINE = True
