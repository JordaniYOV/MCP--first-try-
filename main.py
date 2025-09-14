from fastmcp import FastMCP

mcp = FastMCP(name="helloServ")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}"

