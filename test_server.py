import pytest
from inline_snapshot import snapshot
from mcp import Client
from mcp.types import CallToolResult, TextContent, ReadResourceResult, TextResourceContents

from server import mcp

@pytest.fixture
def anyio_backend():  
    return "asyncio"


@pytest.fixture
async def client():  
    async with Client(mcp, raise_exceptions=True) as c:
        yield c

@pytest.mark.anyio
@pytest.mark.parametrize("player,nationality", [
    ("Rafael Nadal", "Spain"),
    ("Jannik Sinner", "Italy"),
    ("Roger Federer", "Switzerland"),
    ("Novak Djokovic", "Serbia"),
    ("Carlos Alcaraz", "Spain"),
    ("Andy Murray", "Great Britain"),
    ("Learner Tien", "USA"),
    ("Arthur Fils", "France")
])
async def test_call_get_nationality_tool(client: Client, player, nationality):
    result = await client.call_tool("get_nationality", {"name": player})
    result.meta = None
    assert result == CallToolResult(
        content = [TextContent(type = "text", text = nationality)],
        structured_content = {"result" : nationality}
    )


@pytest.mark.anyio
async def test_call_get_players_of_nationality_tool(client: Client):
    result = await client.call_tool("get_players_of_nationality", {"nationality": "Serbia"})
    result.meta = None
    assert result == snapshot(
        CallToolResult(
            content = [TextContent(type = "text", text = "Novak Djokovic")],
            structured_content = {"result" : ["Novak Djokovic"]}
        )
    )

@pytest.mark.anyio
async def test_get_players(client: Client):
    result = await client.read_resource("player_list://player_names")
    result.meta = None
    assert result == snapshot(
        ReadResourceResult(
            ttl_ms = 0,
            cache_scope = "private",
            contents = [TextResourceContents(
                uri = "player_list://player_names",
                mime_type = "text/plain",
                text = "Rafael Nadal\nRoger Federer\nNovak Djokovic\nAndy Murray\nCarlos Alcaraz\nJannik Sinner\nArthur Fils\nLearner Tien"
            )],
            result_type = "complete"
        )
    )