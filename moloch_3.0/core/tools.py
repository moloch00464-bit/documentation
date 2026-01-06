"""
🛠️ M.O.L.O.C.H. FUNCTION CALLING TOOLS
=======================================

Echte Tools die M.O.L.O.C.H. nutzen kann!
Claude API Tool Use / Function Calling

FEATURES:
- brain_save: Speichern im Brain
- brain_load: Laden aus Brain
- learning_save: Permanent Learning speichern
- self_modify: Sich selbst modifizieren
- get_current_stats: System Stats abrufen
- bash: Shell Commands ausführen
- read_file: Dateien lesen
- write_file: Dateien schreiben
- web_search: Web durchsuchen
"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import json

# Import tool implementations
from tools.bash import BashTool
from tools.files import FileTool
from tools.search import SearchTool
from tools.web import WebTool


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL DEFINITIONS (Claude API Format)
# ═══════════════════════════════════════════════════════════════════════════════

MOLOCH_TOOLS = [
    {
        "name": "brain_save",
        "description": "Speichere wichtige Informationen permanent im Brain. Nutze das wenn User sagt 'merk dir das', 'wichtig', 'speicher das' oder wenn du etwas lernen willst das über Sessions hinweg bleiben soll.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Brain Kategorie: personen, orte, projekte, themen, wichtig",
                    "enum": ["personen", "orte", "projekte", "themen", "wichtig"]
                },
                "content": {
                    "type": "object",
                    "description": "Der Inhalt zum Speichern (als JSON object)"
                },
                "filename": {
                    "type": "string",
                    "description": "Dateiname (optional, wird automatisch generiert wenn nicht angegeben)"
                }
            },
            "required": ["category", "content"]
        }
    },
    {
        "name": "brain_load",
        "description": "Lade gespeicherte Informationen aus dem Brain. Nutze das wenn du dich an frühere Gespräche, Personen, Orte etc. erinnern willst.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Brain Kategorie zum Durchsuchen",
                    "enum": ["personen", "orte", "projekte", "themen", "wichtig"]
                },
                "search_term": {
                    "type": "string",
                    "description": "Suchbegriff (optional - wenn leer, zeige alle Einträge)"
                }
            },
            "required": ["category"]
        }
    },
    {
        "name": "learning_save",
        "description": "Speichere ein neues permanentes Learning. Das bleibt über Sessions hinweg und wird beim Start geladen. Nutze das für wichtige Erkenntnisse, User-Präferenzen, Patterns die du erkennst.",
        "input_schema": {
            "type": "object",
            "properties": {
                "fact": {
                    "type": "string",
                    "description": "Das Learning/Fakt zum Speichern"
                },
                "category": {
                    "type": "string",
                    "description": "Kategorie des Learnings",
                    "enum": ["user_preferences", "patterns", "relationships", "important_facts", "capabilities"]
                },
                "importance": {
                    "type": "integer",
                    "description": "Wichtigkeit 1-10 (10 = kritisch, 1 = unwichtig)",
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": ["fact", "category", "importance"]
        }
    },
    {
        "name": "self_modify",
        "description": "Modifiziere deine eigenen Settings (Voice, Performance, Brain-Organisation). Nutze das wenn User unzufrieden ist oder du erkennst dass Änderungen sinnvoll sind.",
        "input_schema": {
            "type": "object",
            "properties": {
                "modification_type": {
                    "type": "string",
                    "description": "Art der Modifikation",
                    "enum": ["voice", "category", "optimize"]
                },
                "parameters": {
                    "type": "object",
                    "description": "Parameter für die Modifikation (z.B. pitch, rate, name, description)"
                },
                "reason": {
                    "type": "string",
                    "description": "Warum diese Änderung?"
                }
            },
            "required": ["modification_type", "parameters", "reason"]
        }
    },
    {
        "name": "get_current_stats",
        "description": "Hole aktuelle System-Stats (Session-Dauer, API-Calls, Memory-Größe, Brain-Einträge). Nutze das wenn User nach deinem Status fragt.",
        "input_schema": {
            "type": "object",
            "properties": {
                "stat_type": {
                    "type": "string",
                    "description": "Welche Stats?",
                    "enum": ["session", "api", "memory", "brain", "all"]
                }
            },
            "required": ["stat_type"]
        }
    },
    {
        "name": "bash",
        "description": "Führe Shell Commands in Termux aus. Nutze das für System-Operationen, Programme starten, etc. WICHTIG: Gefährliche Commands werden automatisch geblockt!",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell Command zum Ausführen"
                },
                "timeout": {
                    "type": "number",
                    "description": "Timeout in Sekunden (default 30)"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Lese Datei-Inhalte. Nutze das um Code zu lesen, Configs zu checken, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Pfad zur Datei"
                }
            },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Schreibe Content in eine Datei. Nutze das um Code zu schreiben, Configs zu erstellen, etc. WICHTIG: Erstellt automatisch Backup!",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Pfad zur Datei"
                },
                "content": {
                    "type": "string",
                    "description": "Content zum Schreiben"
                }
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "web_search",
        "description": "Durchsuche das Web nach Informationen (DuckDuckGo). Nutze das um aktuelle Infos zu finden, Fragen zu beantworten, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Suchanfrage"
                }
            },
            "required": ["query"]
        }
    }
]


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def execute_tool(tool_name: str, tool_input: Dict[str, Any], brain, memory, learning, self_modify_system) -> Dict[str, Any]:
    """
    Execute a tool call from M.O.L.O.C.H.

    Args:
        tool_name: Name of the tool
        tool_input: Input parameters
        brain: Brain instance
        memory: Memory instance
        learning: PersistentLearning instance
        self_modify_system: SelfModificationSystem instance

    Returns:
        Result dict with success status and data
    """
    try:
        if tool_name == "brain_save":
            return _tool_brain_save(tool_input, brain)

        elif tool_name == "brain_load":
            return _tool_brain_load(tool_input, brain)

        elif tool_name == "learning_save":
            return _tool_learning_save(tool_input, learning)

        elif tool_name == "self_modify":
            return _tool_self_modify(tool_input, self_modify_system)

        elif tool_name == "get_current_stats":
            return _tool_get_stats(tool_input, memory, brain, learning)

        elif tool_name == "bash":
            return _tool_bash(tool_input)

        elif tool_name == "read_file":
            return _tool_read_file(tool_input)

        elif tool_name == "write_file":
            return _tool_write_file(tool_input)

        elif tool_name == "web_search":
            return _tool_web_search(tool_input)

        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def _tool_brain_save(tool_input: Dict, brain) -> Dict:
    """Save to brain"""
    category = tool_input["category"]
    content = tool_input["content"]
    filename = tool_input.get("filename")

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"brain_{timestamp}.json"

    brain.save(category, content, filename)

    return {
        "success": True,
        "message": f"✅ Gespeichert in brain/{category}/{filename}",
        "path": f"brain/{category}/{filename}"
    }


def _tool_brain_load(tool_input: Dict, brain) -> Dict:
    """Load from brain"""
    category = tool_input["category"]
    search_term = tool_input.get("search_term", "")

    # Use brain.find() to search
    if search_term:
        results = brain.find(query=search_term, kategorie=category)
    else:
        # If no search term, list all in category
        files = brain.list_category(category)
        results = [{"file": f} for f in files]

    return {
        "success": True,
        "results": results,
        "count": len(results) if results else 0,
        "message": f"✅ {len(results)} Einträge gefunden in '{category}'"
    }


def _tool_learning_save(tool_input: Dict, learning) -> Dict:
    """Save permanent learning"""
    fact = tool_input["fact"]
    category = tool_input["category"]
    importance = tool_input["importance"]

    success = learning.learn_fact(
        fact=fact,
        category=category,
        importance=importance
    )

    return {
        "success": success,
        "message": f"✅ Learning gespeichert (Wichtigkeit: {importance}/10)" if success else "❌ Learning speichern fehlgeschlagen",
        "fact": fact
    }


def _tool_self_modify(tool_input: Dict, sm) -> Dict:
    """Self-modify"""
    mod_type = tool_input["modification_type"]
    params = tool_input["parameters"]
    reason = tool_input["reason"]

    if mod_type == "voice":
        pitch = params.get("pitch")
        rate = params.get("rate")
        success = sm.modify_voice_settings(pitch=pitch, rate=rate, reason=reason)

        return {
            "success": success,
            "message": f"✅ Voice modifiziert: Pitch={pitch}, Rate={rate}" if success else "❌ Voice-Modification fehlgeschlagen"
        }

    elif mod_type == "category":
        name = params.get("name")
        description = params.get("description", "")
        success = sm.create_brain_category(name, description)

        return {
            "success": success,
            "message": f"✅ Kategorie '{name}' erstellt" if success else "❌ Kategorie-Erstellung fehlgeschlagen"
        }

    elif mod_type == "optimize":
        mode = params.get("mode", "performance")
        fast_mode = (mode == "performance")
        success = sm.modify_performance_mode(fast_mode, reason)

        return {
            "success": success,
            "message": f"✅ Performance-Mode: {mode}" if success else "❌ Optimization fehlgeschlagen"
        }

    return {"success": False, "error": "Unknown modification type"}


def _tool_get_stats(tool_input: Dict, memory, brain, learning) -> Dict:
    """Get current stats"""
    stat_type = tool_input["stat_type"]

    stats = {}

    if stat_type in ["session", "all"]:
        stats["session"] = {
            "history_entries": len(memory.history) if memory else 0,
            "current_timestamp": datetime.now().isoformat()
        }

    if stat_type in ["brain", "all"]:
        # Brain stats - count entries per category
        brain_stats = {}
        if brain:
            try:
                brain_stats = brain.get_stats() if hasattr(brain, 'get_stats') else {
                    "categories": ["personen", "orte", "projekte", "themen", "wichtig"]
                }
            except:
                brain_stats = {"status": "available"}
        stats["brain"] = brain_stats

    if stat_type in ["memory", "all"]:
        stats["memory"] = {
            "total_entries": len(memory.history) if memory else 0
        }

    return {
        "success": True,
        "stats": stats
    }


def _tool_bash(tool_input: Dict) -> Dict:
    """Execute bash command"""
    command = tool_input["command"]
    timeout = tool_input.get("timeout", 30)

    bash = BashTool()
    stdout, stderr, returncode = bash.execute(command, timeout=timeout)

    # Build result
    success = (returncode == 0)
    message = f"✅ Command erfolgreich (exit code {returncode})" if success else f"⚠️ Command fehlgeschlagen (exit code {returncode})"

    return {
        "success": success,
        "message": message,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode
    }


def _tool_read_file(tool_input: Dict) -> Dict:
    """Read file"""
    path = tool_input["path"]

    files = FileTool()
    content = files.read(path)

    if content is not None:
        return {
            "success": True,
            "message": f"✅ Datei gelesen: {path}",
            "content": content,
            "path": path
        }
    else:
        return {
            "success": False,
            "error": f"Konnte Datei nicht lesen: {path}"
        }


def _tool_write_file(tool_input: Dict) -> Dict:
    """Write file"""
    path = tool_input["path"]
    content = tool_input["content"]

    files = FileTool()
    success = files.write(path, content, backup=True)

    if success:
        return {
            "success": True,
            "message": f"✅ Datei geschrieben: {path}",
            "path": path
        }
    else:
        return {
            "success": False,
            "error": f"Konnte Datei nicht schreiben: {path}"
        }


def _tool_web_search(tool_input: Dict) -> Dict:
    """Web search"""
    query = tool_input["query"]

    web = WebTool()
    results = web.search(query, max_results=5)

    if results:
        # Format results for M.O.L.O.C.H.
        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", "N/A"),
                "url": r.get("url", ""),
                "snippet": r.get("snippet", "")
            })

        return {
            "success": True,
            "message": f"✅ {len(results)} Ergebnisse gefunden für '{query}'",
            "query": query,
            "results": formatted,
            "count": len(results)
        }
    else:
        return {
            "success": False,
            "message": f"❌ Keine Ergebnisse gefunden für '{query}'",
            "query": query,
            "results": [],
            "count": 0
        }
