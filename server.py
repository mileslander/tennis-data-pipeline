from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

mcp = MCPServer("Tennis Players")

player_list = {
    "Rafael Nadal" : "Spain",
    "Roger Federer" : "Switzerland",
    "Novak Djokovic" : "Serbia",
    "Andy Murray" : "Great Britain",
    "Carlos Alcaraz" : "Spain",
    "Jannik Sinner" : "Italy",
    "Arthur Fils": "France",
    "Learner Tien" : "USA"
}

@mcp.resource("player_list://player_names")
def get_players() -> str:
    """Full player list, one name per line"""
    return "\n".join(player_list)

@mcp.tool()
def get_players_of_nationality(nationality: str) -> list[str]:
    """Return list of players of the provided nationality"""
    if nationality not in player_list.values():
        raise ToolError(f"No players found representing {nationality}")
    return [key for key, value in player_list.items() if value == nationality]

@mcp.tool()
def get_nationality(name: str) -> str:
    """Get nationality of provided player"""
    if name not in player_list:
        raise ToolError(f"{name} not found")
    return player_list[name]

if __name__ == "__main__":
    mcp.run()