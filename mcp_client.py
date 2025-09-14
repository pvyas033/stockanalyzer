import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def fetch_tool_identifier_prompt():

    tool_identifier_prompt = """ 
        You have access to the following MCP Server Tools: 
        
        {tools_description} 
        
        You must identify the appropriate tool only from the above tools required 
        to resolve the user query along with the arguments. 
        
        {user_query} 
        
        Your output must be in JSON like below: 
        
        {{
            "user_query": "User Query",
            "tool_identified": "Tool Name",
            "arguments": {{"symbol1": "TICKER1", "symbol2": "TICKER2"}}
        }}
        
        IMPORTANT:
        - Stock tickers should be actual exchange symbols (e.g., "AAPL" for Apple, "MSFT" for Microsoft).
        - Do not output placeholders like "stock1" or "stock2".
        - Always assume the user query contains company names or stock tickers.
        - If only company names are given, map them to likely tickers.
    """

    return tool_identifier_prompt

async def generate_response(user_query: str, tools_description: str):
    """
    Generative AI response to identify appropriate tool for user query.

    This funtion uses Google's gemini AI model to analyze the user query against
    available MCP server tools and returns the identifies tool with its arguments.

    Args:
        user_query (str): The user's input query that needs to be resolved
        tools_description (str): Description of available MCP server tools

    Returns:
        Exception: If API key is missing or AI model fails to respond
        json.JSONDecodeError: If the AI respond cannot be parsed as JSON

    Example:
        >>> await generate_response("What's the weather?", "get_weather: Gets weather data")
        {
            "user_query": "What's the weather?",
            "tool_identified": "get_weather",
            "arguments": {{"location": "default"}}
        }
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    tool_identifier_prompt = fetch_tool_identifier_prompt()
    tool_identifier_prompt = tool_identifier_prompt.format(user_query=user_query, tools_description=tools_description)

    model = genai.GenerativeModel('gemini-2.0-flash-001')
    response = model.generate_content(tool_identifier_prompt)

    raw = response.text.strip()
    raw = raw.replace("```json", "").replace("```","")
    data = json.loads(raw)

    if isinstance(data["arguments"], str):
        try:
            # try parsing if it's actually a JSON string
            data["arguments"] = json.loads(data["arguments"])
        except:
            args_list = [arg.strip() for arg in data["arguments"].split(",")]
            data["arguments"] = {args_list[0]: args_list[1]} if len(args_list) > 1 else {args_list[0]: True}

    return data

async def main(user_input: str):
    """
    Main function to handle MCP client session and tool execution.

    This function establishe a connection to the MCP server, initializes a session,
    lists available tools, identifies the appropriate tool using AI, and executes
    the identifies tool with the provided arguments.

    Args:
        user_input (str): The user's query to be processed

    Returns:
         None: Prints results to console

    Raises:
        Exception: Various exception related to MCP server connection,
                  Session initialization, or tool execution

    Note:
        The server parameters are hardcoded and should be configured for your
        specific environment. Update the 'cwd' parameter to match your project path.

    Example:`
        >>> await main("What is the weather in New York?")
        # Connects to MCP server, identifies weather tool, executes it

    """

    print("-"* 50)
    print("The user input is : ", user_input)

    server_params = StdioServerParameters(
        command = "python",
        args = ["mcp_Server.py"],
        cwd = "."
    )

    try:
        async with stdio_client(server_params) as [read, write]:
            print("Connection established, creation session started.")
            try:
                async with ClientSession(read, write) as session:
                    print("[agent] Session created, initializing MCP server...")
                    try:
                        await session.initialize()
                        print("[agent] MCP server initialized.")
                        tools = await session.list_tools()
                        tools_description = ""
                        for each_tool in tools.tools:
                            current_tool_description = "Tool - "+each_tool.name + ":" + "\n"
                            current_tool_description += each_tool.description + "\n"
                            tools_description += current_tool_description + "\n"

                        request_json = await generate_response(user_query = user_input, tools_description = tools_description)
                        print(f"To execute  the User Query: {user_input} -\n The Identifies tool is {request_json['tool_identified']},\nclea and the parameters required are {request_json['arguments']}")
                        response = await session.call_tool(request_json['tool_identified'], arguments = request_json['arguments'])
                        print(f"{response.content[0].text}")
                        print("-"*50)
                        print("\n\n")
                    except Exception as e:
                        print(f"[agent] Session initialization error: {str(e)}")
            except Exception as e:
                print(f"[agent] Session creation error: {str(e)}")
    except Exception as e:
        print(f"[agent] Connection error: {str(e)}")

if __name__ == "__main__":

    while True:
        query = input("What is your query? : ")
        if(query == "exit"):
            break
        asyncio.run(main(query))


