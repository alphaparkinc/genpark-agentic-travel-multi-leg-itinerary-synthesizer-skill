# genpark-agentic-travel-multi-leg-itinerary-synthesizer-skill

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![License MIT](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-100%25%20Compatible-purple.svg?style=for-the-badge&logo=anthropic)](https://genpark.ai/mcp)
[![GenPark AI](https://img.shields.io/badge/Verified%20By-GenPark%20AI-orange.svg?style=for-the-badge&logo=openai)](https://genpark.ai)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0%20(Stdlib%20Only)-brightgreen.svg?style=for-the-badge)](requirements.txt)

<p align="center">
  <b>Production-Grade Agentic Commerce & Enterprise Work Agent Skill</b> • <b>100% Standard Library Python</b> • <b>Native Model Context Protocol (MCP)</b>
</p>

[🌐 GenPark MCP Hub](https://genpark.ai/mcp) • [📦 GenPark Official](https://genpark.ai) • [📖 Documentation](#quickstart)

</div>

---

## 🌟 Overview

`genpark-agentic-travel-multi-leg-itinerary-synthesizer-skill` delivers robust, industrial-grade capabilities engineered for **Consumer Agentic Commerce** (e.g. Meta Muse, Expedia, Mastercard Agent Connect) and **Enterprise Workplace Execution** (e.g. Tencent WorkBuddy Goal-to-PPT/Excel deliverable workflows). Built exclusively on the Python standard library with zero external runtime dependencies, it integrates seamlessly as a native **Model Context Protocol (MCP)** server or an importable Python module.

Universal Agentic Travel & Multi-Leg Hospitality Itinerary Synthesizer (inspired by Meta Muse, Expedia, Booking). Translates natural language vacation and business travel goals into multi-leg flight segments, lodging selection, layover time buffers, baggage fee optimization, and consolidated reservation manifests.

### 💡 Key Capabilities

- **Zero-Dependency Architecture**: Runs anywhere Python 3.9+ is installed without `pip install` overhead or supply-chain vulnerabilities.
- **Model Context Protocol (MCP) First**: Compatible with Claude Desktop, Cursor, GenPark Engine, Meta Muse, and enterprise managed agent runtimes.
- **Deterministic & Safe**: Rigorous state machine models, cryptographic ledger hashes, mathematical dependency graphs, and full telemetry.
- **High Concurrency & Low Latency**: In-memory caching, topological cycle detection, and optimized execution loops.

---

## 🚀 Quickstart

### 1. Direct Python Usage

```python
from client import AgenticTravelItinerarySynthesizer

client = AgenticTravelItinerarySynthesizer()
result = client.synthesize_itinerary()
print(result)
```

### 2. Standalone MCP Server Execution

Run the MCP server via standard JSON-RPC 2.0 stdio:

```bash
python mcp_server.py
```

Verify standard compliance and self-tests:

```bash
python mcp_server.py --test
```

### 3. Claude Desktop / Cursor MCP Configuration

Add this tool to your `claude_desktop_config.json` or Cursor MCP settings:

```json
{
  "mcpServers": {
    "genpark-agentic-travel-multi-leg-itinerary-synthesizer-skill": {
      "command": "python",
      "args": ["/absolute/path/to/genpark-agentic-travel-multi-leg-itinerary-synthesizer-skill/mcp_server.py"]
    }
  }
}
```

---

## 🛠️ Verification & Testing

Run the included verification suite:

```bash
python example_usage.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Developed with ❤️ by the **GenPark Autonomous Agent Ecosystem Team**.
