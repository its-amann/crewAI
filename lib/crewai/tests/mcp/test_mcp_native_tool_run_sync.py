import asyncio

import pytest

from crewai.tools.mcp_native_tool import MCPNativeTool


class _FailingTool(MCPNativeTool):
    async def _run_async(self, **kwargs):
        raise RuntimeError("server said no")


def _tool():
    return _FailingTool(
        client_factory=lambda: None,
        tool_name="echo",
        tool_schema={},
        server_name="srv",
    )


def test_runtime_error_from_tool_keeps_message_inside_running_loop():
    async def main():
        with pytest.raises(RuntimeError, match="server said no"):
            _tool()._run()

    asyncio.run(main())


def test_runtime_error_from_tool_keeps_message_without_loop():
    with pytest.raises(RuntimeError, match="server said no"):
        _tool()._run()
