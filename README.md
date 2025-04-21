# Playing with MCP and Coruña Buses

**Real-time bus data for A Coruña, powered by LLMs and the Model Context Protocol (MCP)**

---

## Overview

This project demonstrates how to connect a Language Model (LLM) to real-time public transport data using the **Model Context Protocol (MCP)**. The goal: enable an LLM to answer questions like "When is the next bus from Abente y Lago?" by directly querying the city's bus backend.

- **Author:** Fernando Souto  
- **Category:** AI, Tools, MCP, Public Transport  

---

## Architecture

- **Backend:** Python, using [fastmcp](https://github.com/jlowin/fastmcp) to expose tools via MCP.
- **Data:** Bus lines and stops are stored as JSON files.
- **LLM Integration:** Any MCP-compatible LLM (Claude, OpenAI, etc.) can interact with the tools.

### Key Tools

- `get_stop_code_by_location`:  
  Fuzzy-matches a stop name/location to its code by searching all stop JSON files.
- `get_bus_timetable`:  
  Fetches real-time arrival times for a given stop code from the Coruña bus API.

---

## Example: Tool Definitions

```python
from fastmcp import FastMCP

mcp = FastMCP("bus-finder")

@mcp.tool()
def get_stop_code_by_location(location: str) -> dict:
    """Return stop code(s) for a given location using fuzzy matching."""
    # Implementation in repo
    return {"matches": [...]}

@mcp.tool()
def get_bus_timetable(stop: int) -> dict:
    """Get real-time timetable for a stop code."""
    # Implementation in repo
    return {...}

if __name__ == "__main__":
    mcp.run()
```

---

## Data Structure

Bus lines and stops are defined in JSON files, e.g.:

```json
{
  "line": "1",
  "directions": [
    {
      "from": "Abente y Lago",
      "to": "Castrillón",
      "stops": [
        { "code": 523, "name": "Abente y Lago" },
        { "code": 598, "name": "Avenida Porto, A Terraza" }
        // ...
      ]
    }
    // ...
  ]
}
```

---

## How It Works

1. **User Query:**  
   The LLM receives a question like "When is the next bus from Abente y Lago?"
2. **Tool Invocation:**  
   The LLM uses `get_stop_code_by_location` to resolve the stop name to a code.
3. **Real-Time Data:**  
   The LLM calls `get_bus_timetable` with the stop code to fetch live arrival times.
4. **Emergent Reasoning:**  
   The LLM can even deduce routes between two locations by chaining tool calls, without explicit programming for itineraries.

---

## Technical Highlights

- **MCP** provides a clean, structured way to expose backend tools to LLMs.
- **Fuzzy Matching:**  
  The stop code tool uses substring and similarity matching to handle user typos or variations.
- **Real-Time API:**  
  Timetable data is fetched live from the Coruña bus API.
- **Minimal Code, Maximum Power:**  
  With just a few well-defined tools, the LLM can perform complex reasoning and data retrieval.

---

## Getting Started

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/ficiverson/mcp-bus-coruna
   cd mcp-bus-coruna
   ```
2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Install the MCP server into Claude:**  
   ```bash
   fastmcp install bus_coruna.py
   ```
4. **Ask questions:**  
   Try queries like "When is the next bus from Abente y Lago?" or "How do I get from Castrillón to Pza. de Ourense?"

---

## Resources

- [Sample conversation (simple)](https://claude.ai/share/6dbf72ea-921c-40b6-a593-4c6c8dcf95c5)
- [Sample conversation (itinerary)](https://claude.ai/share/dccbf7e7-66ed-4492-b8bc-a140cff63eae)

---

## Why MCP + LLMs?

By exposing just a couple of well-designed tools, you empower LLMs to:

- Access and reason over real-time data.
- Chain tool calls to answer complex queries (e.g., full itineraries).
- Adapt to new use cases with minimal backend changes.

**MCP bridges the gap between language models and the real world.**

---

Ready to give your LLMs real-time superpowers? 🚍🤖

---

Let me know if you want a more detailed API reference or deployment instructions!
