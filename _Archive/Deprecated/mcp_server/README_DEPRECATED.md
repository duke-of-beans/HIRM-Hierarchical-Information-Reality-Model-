# DEPRECATED: MCP Server

## Why Deprecated (December 20, 2025)

The MCP (Model Context Protocol) server has been deprecated in favor of:
1. **Filesystem connector** - Direct file system access
2. **Desktop Commander** - Process execution and file operations

## Reasons for Change
- MCP adds unnecessary abstraction layer
- Filesystem/Desktop Commander tools are more efficient
- Direct Python script execution provides better automation
- Database queries work directly through scripts

## Replacement
All functionality has been migrated to:
- `D:\HIRM\System\scripts\hirm_core.py` - Core utilities
- `D:\HIRM\System\scripts\quality_gate.py` - Document validation
- `D:\HIRM\System\scripts\pattern_detector.py` - Pattern detection
- `D:\HIRM\System\scripts\corpus_sync.py` - Sync operations
- `D:\HIRM\System\scripts\orchestrator.py` - Master controller

## Do NOT Restore
This MCP server is retained for historical reference only.
The HIRM system now uses direct Python automation scripts.
