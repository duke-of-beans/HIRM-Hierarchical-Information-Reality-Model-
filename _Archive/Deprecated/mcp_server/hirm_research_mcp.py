#!/usr/bin/env python3
"""
HIRM Research MCP Server
========================

Model Context Protocol server for accessing and analyzing the Hierarchical
Information-Reality Model (HIRM) consciousness research directory.

This server provides tools for:
- File system navigation and search
- Content analysis across research corpus
- Citation tracking and literature integration
- Research workflow support
- HIRM-specific context awareness

Directory: D:/Ouroboros Observer (and all subfolders)
Research Focus: Consciousness emergence through self-reference phase transitions
Corpus: 193-213 papers across 6 domains
"""

import os
import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, field_validator, ConfigDict

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Base directory for HIRM research
HIRM_BASE_DIR = Path(r"D:\Ouroboros Observer")

# File extensions to include in searches
SEARCHABLE_EXTENSIONS = {
    '.md', '.txt', '.py', '.ipynb', '.json',
    '.pdf', '.docx', '.tex', '.bib',
    '.csv', '.xlsx', '.yaml', '.yml'
}

# Maximum file size to read (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Pagination defaults
DEFAULT_LIMIT = 20
MAX_LIMIT = 100

# ==============================================================================
# INITIALIZE MCP SERVER
# ==============================================================================

mcp = FastMCP("hirm_research_mcp")

# ==============================================================================
# SHARED MODELS AND ENUMS
# ==============================================================================

class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class FileType(str, Enum):
    """File type categories for filtering."""
    ALL = "all"
    MARKDOWN = "markdown"
    CODE = "code"
    NOTEBOOK = "notebook"
    DATA = "data"
    DOCUMENT = "document"
    BIBLIOGRAPHY = "bibliography"


class SortOrder(str, Enum):
    """Sort order for file listings."""
    NAME_ASC = "name_asc"
    NAME_DESC = "name_desc"
    DATE_ASC = "date_asc"
    DATE_DESC = "date_desc"
    SIZE_ASC = "size_asc"
    SIZE_DESC = "size_desc"


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def _validate_path(path: str) -> Path:
    """
    Validate and resolve a path within HIRM directory.
    
    Prevents directory traversal attacks and ensures path is within base directory.
    """
    try:
        # Resolve to absolute path
        abs_path = Path(path).resolve()
        
        # If path is relative, resolve against base directory
        if not abs_path.is_absolute():
            abs_path = (HIRM_BASE_DIR / path).resolve()
        
        # Ensure path is within base directory
        try:
            abs_path.relative_to(HIRM_BASE_DIR)
        except ValueError:
            raise ValueError(f"Path must be within HIRM directory: {HIRM_BASE_DIR}")
        
        return abs_path
    except Exception as e:
        raise ValueError(f"Invalid path: {e}")


def _get_file_type(path: Path) -> str:
    """Determine file type category from extension."""
    ext = path.suffix.lower()
    
    if ext in {'.md', '.txt', '.rst'}:
        return 'markdown'
    elif ext in {'.py', '.js', '.ts', '.cpp', '.c', '.java'}:
        return 'code'
    elif ext in {'.ipynb'}:
        return 'notebook'
    elif ext in {'.csv', '.xlsx', '.json', '.yaml', '.yml'}:
        return 'data'
    elif ext in {'.pdf', '.docx', '.doc', '.tex'}:
        return 'document'
    elif ext in {'.bib', '.ris'}:
        return 'bibliography'
    else:
        return 'other'


def _format_file_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def _format_timestamp(timestamp: float) -> str:
    """Format Unix timestamp to human-readable format."""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _match_file_type_filter(path: Path, file_type: FileType) -> bool:
    """Check if file matches type filter."""
    if file_type == FileType.ALL:
        return True
    
    actual_type = _get_file_type(path)
    return actual_type == file_type.value


def _search_in_file(file_path: Path, pattern: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
    """
    Search for pattern in file and return matching lines with context.
    
    Returns list of matches with line numbers and surrounding context.
    """
    matches = []
    
    try:
        # Skip binary files and large files
        if file_path.stat().st_size > MAX_FILE_SIZE:
            return matches
        
        # Try to read file as text
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return matches
        
        # Compile regex pattern
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error:
            # If pattern is not valid regex, treat as literal string
            regex = re.compile(re.escape(pattern), flags)
        
        # Search through lines
        for i, line in enumerate(lines, start=1):
            if regex.search(line):
                # Get context (1 line before and after)
                context_start = max(0, i - 2)
                context_end = min(len(lines), i + 1)
                context = ''.join(lines[context_start:context_end])
                
                matches.append({
                    'line_number': i,
                    'line': line.strip(),
                    'context': context.strip()
                })
        
    except Exception:
        pass
    
    return matches


def _format_search_results_markdown(results: List[Dict[str, Any]]) -> str:
    """Format search results as markdown."""
    if not results:
        return "No results found."
    
    output = [f"# Search Results ({len(results)} files)\n"]
    
    for result in results:
        output.append(f"## {result['path']}")
        output.append(f"**File Type:** {result['type']} | **Size:** {result['size']}\n")
        
        if result['matches']:
            output.append(f"**Matches:** {len(result['matches'])}\n")
            for match in result['matches'][:5]:  # Show first 5 matches
                output.append(f"**Line {match['line_number']}:** {match['line']}\n")
            
            if len(result['matches']) > 5:
                output.append(f"*... and {len(result['matches']) - 5} more matches*\n")
        
        output.append("")
    
    return "\n".join(output)


def _format_file_list_markdown(files: List[Dict[str, Any]], total: int, offset: int, 
                                has_more: bool) -> str:
    """Format file list as markdown."""
    output = [f"# File Listing ({len(files)} of {total})\n"]
    
    if offset > 0:
        output.append(f"*Showing results {offset + 1}-{offset + len(files)} of {total}*\n")
    
    for file_info in files:
        output.append(f"## {file_info['name']}")
        output.append(f"- **Path:** `{file_info['path']}`")
        output.append(f"- **Type:** {file_info['type']}")
        output.append(f"- **Size:** {file_info['size']}")
        output.append(f"- **Modified:** {file_info['modified']}")
        output.append("")
    
    if has_more:
        output.append(f"\n*Use offset={offset + len(files)} to see more results*")
    
    return "\n".join(output)


# ==============================================================================
# TOOL IMPLEMENTATIONS
# ==============================================================================

# ------------------------------------------------------------------------------
# File System Navigation Tools
# ------------------------------------------------------------------------------

class ListFilesInput(BaseModel):
    """Input parameters for listing files in a directory."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    directory: str = Field(
        default=".",
        description="Directory path relative to HIRM base directory (e.g., 'papers', 'code', '.')"
    )
    recursive: bool = Field(
        default=False,
        description="Whether to recursively list files in subdirectories"
    )
    file_type: FileType = Field(
        default=FileType.ALL,
        description="Filter by file type: all, markdown, code, notebook, data, document, bibliography"
    )
    sort_by: SortOrder = Field(
        default=SortOrder.NAME_ASC,
        description="Sort order for results"
    )
    limit: int = Field(
        default=DEFAULT_LIMIT,
        description="Maximum number of files to return",
        ge=1,
        le=MAX_LIMIT
    )
    offset: int = Field(
        default=0,
        description="Number of results to skip for pagination",
        ge=0
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for machine-readable"
    )


@mcp.tool(
    name="hirm_list_files",
    annotations={
        "title": "List Files in HIRM Directory",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def hirm_list_files(params: ListFilesInput) -> str:
    """
    List files in the HIRM research directory with filtering and pagination.
    
    This tool helps navigate the research corpus by listing files in specified
    directories with support for recursive listing, file type filtering, and sorting.
    
    Args:
        params (ListFilesInput): Validated input parameters containing:
            - directory (str): Target directory path
            - recursive (bool): Whether to list recursively
            - file_type (FileType): Filter by file type category
            - sort_by (SortOrder): Sort order for results
            - limit (int): Maximum results to return
            - offset (int): Pagination offset
            - response_format (ResponseFormat): Output format
    
    Returns:
        str: Formatted file listing with pagination information
    """
    try:
        # Validate and resolve directory path
        target_dir = _validate_path(params.directory)
        
        if not target_dir.exists():
            return json.dumps({
                "error": f"Directory not found: {params.directory}",
                "suggestion": "Check the path and try again. Use '.' for base directory."
            }, indent=2)
        
        if not target_dir.is_dir():
            return json.dumps({
                "error": f"Path is not a directory: {params.directory}",
                "suggestion": "Provide a directory path, not a file path."
            }, indent=2)
        
        # Collect files
        files = []
        
        if params.recursive:
            # Recursive listing
            for root, _, filenames in os.walk(target_dir):
                for filename in filenames:
                    file_path = Path(root) / filename
                    if _match_file_type_filter(file_path, params.file_type):
                        try:
                            stat = file_path.stat()
                            files.append({
                                'path': file_path,
                                'name': filename,
                                'size': stat.st_size,
                                'modified': stat.st_mtime
                            })
                        except Exception:
                            continue
        else:
            # Non-recursive listing
            for item in target_dir.iterdir():
                if item.is_file() and _match_file_type_filter(item, params.file_type):
                    try:
                        stat = item.stat()
                        files.append({
                            'path': item,
                            'name': item.name,
                            'size': stat.st_size,
                            'modified': stat.st_mtime
                        })
                    except Exception:
                        continue
        
        # Sort files
        sort_key_map = {
            SortOrder.NAME_ASC: lambda x: x['name'].lower(),
            SortOrder.NAME_DESC: lambda x: x['name'].lower(),
            SortOrder.DATE_ASC: lambda x: x['modified'],
            SortOrder.DATE_DESC: lambda x: x['modified'],
            SortOrder.SIZE_ASC: lambda x: x['size'],
            SortOrder.SIZE_DESC: lambda x: x['size']
        }
        
        reverse_sort = params.sort_by in {
            SortOrder.NAME_DESC, SortOrder.DATE_DESC, SortOrder.SIZE_DESC
        }
        
        files.sort(key=sort_key_map[params.sort_by], reverse=reverse_sort)
        
        # Apply pagination
        total_files = len(files)
        paginated_files = files[params.offset:params.offset + params.limit]
        
        # Format results
        result_list = []
        for file_info in paginated_files:
            relative_path = file_info['path'].relative_to(HIRM_BASE_DIR)
            result_list.append({
                'name': file_info['name'],
                'path': str(relative_path),
                'type': _get_file_type(file_info['path']),
                'size': _format_file_size(file_info['size']),
                'size_bytes': file_info['size'],
                'modified': _format_timestamp(file_info['modified']),
                'modified_timestamp': file_info['modified']
            })
        
        # Pagination info
        has_more = (params.offset + len(paginated_files)) < total_files
        next_offset = params.offset + len(paginated_files) if has_more else None
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                'total': total_files,
                'count': len(result_list),
                'offset': params.offset,
                'has_more': has_more,
                'next_offset': next_offset,
                'files': result_list
            }, indent=2)
        else:
            return _format_file_list_markdown(result_list, total_files, 
                                             params.offset, has_more)
    
    except ValueError as e:
        return json.dumps({
            "error": str(e),
            "suggestion": "Ensure path is valid and within HIRM directory."
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Unexpected error: {type(e).__name__}: {str(e)}",
            "suggestion": "Check the parameters and try again."
        }, indent=2)


# ------------------------------------------------------------------------------
# File Reading Tools
# ------------------------------------------------------------------------------

class ReadFileInput(BaseModel):
    """Input parameters for reading file contents."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    file_path: str = Field(
        ...,
        description="Path to file relative to HIRM base directory (e.g., 'README.md', 'papers/consciousness.pdf')",
        min_length=1
    )
    start_line: Optional[int] = Field(
        default=None,
        description="Starting line number for partial read (1-indexed)",
        ge=1
    )
    end_line: Optional[int] = Field(
        default=None,
        description="Ending line number for partial read (1-indexed, inclusive)",
        ge=1
    )
    max_lines: Optional[int] = Field(
        default=None,
        description="Maximum number of lines to return (overrides end_line)",
        ge=1,
        le=10000
    )


@mcp.tool(
    name="hirm_read_file",
    annotations={
        "title": "Read File from HIRM Directory",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def hirm_read_file(params: ReadFileInput) -> str:
    """
    Read contents of a file from the HIRM research directory.
    
    Supports reading entire files or specific line ranges. For large files,
    use line range parameters to read specific sections.
    
    Args:
        params (ReadFileInput): Validated input parameters containing:
            - file_path (str): Path to file
            - start_line (Optional[int]): Starting line number
            - end_line (Optional[int]): Ending line number
            - max_lines (Optional[int]): Maximum lines to return
    
    Returns:
        str: File contents or error message
    """
    try:
        # Validate and resolve file path
        target_file = _validate_path(params.file_path)
        
        if not target_file.exists():
            return json.dumps({
                "error": f"File not found: {params.file_path}",
                "suggestion": "Check the file path and try again. Use hirm_list_files to browse available files."
            }, indent=2)
        
        if not target_file.is_file():
            return json.dumps({
                "error": f"Path is not a file: {params.file_path}",
                "suggestion": "Provide a file path, not a directory path."
            }, indent=2)
        
        # Check file size
        file_size = target_file.stat().st_size
        if file_size > MAX_FILE_SIZE:
            return json.dumps({
                "error": f"File too large: {_format_file_size(file_size)} (max: {_format_file_size(MAX_FILE_SIZE)})",
                "suggestion": "Use start_line and end_line parameters to read specific sections."
            }, indent=2)
        
        # Read file
        try:
            with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
                if params.start_line or params.end_line or params.max_lines:
                    # Read specific lines
                    lines = f.readlines()
                    
                    start = (params.start_line - 1) if params.start_line else 0
                    
                    if params.max_lines:
                        end = start + params.max_lines
                    elif params.end_line:
                        end = params.end_line
                    else:
                        end = len(lines)
                    
                    selected_lines = lines[start:end]
                    content = ''.join(selected_lines)
                    
                    return json.dumps({
                        "file_path": str(target_file.relative_to(HIRM_BASE_DIR)),
                        "line_range": f"{start + 1}-{start + len(selected_lines)}",
                        "total_lines": len(lines),
                        "returned_lines": len(selected_lines),
                        "content": content
                    }, indent=2)
                else:
                    # Read entire file
                    content = f.read()
                    
                    return json.dumps({
                        "file_path": str(target_file.relative_to(HIRM_BASE_DIR)),
                        "size": _format_file_size(file_size),
                        "content": content
                    }, indent=2)
        
        except UnicodeDecodeError:
            return json.dumps({
                "error": "File appears to be binary or uses unsupported encoding",
                "suggestion": "This tool is for text files. Binary files may require specialized tools."
            }, indent=2)
    
    except ValueError as e:
        return json.dumps({
            "error": str(e),
            "suggestion": "Ensure path is valid and within HIRM directory."
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Unexpected error: {type(e).__name__}: {str(e)}",
            "suggestion": "Check the file path and try again."
        }, indent=2)


# ------------------------------------------------------------------------------
# Search Tools
# ------------------------------------------------------------------------------

class SearchContentInput(BaseModel):
    """Input parameters for searching content across files."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    query: str = Field(
        ...,
        description="Search query (supports regex patterns)",
        min_length=1,
        max_length=500
    )
    directory: str = Field(
        default=".",
        description="Directory to search in (default: entire HIRM directory)"
    )
    file_type: FileType = Field(
        default=FileType.ALL,
        description="Filter by file type"
    )
    case_sensitive: bool = Field(
        default=False,
        description="Whether search should be case-sensitive"
    )
    max_results: int = Field(
        default=50,
        description="Maximum number of files to return",
        ge=1,
        le=200
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


@mcp.tool(
    name="hirm_search_content",
    annotations={
        "title": "Search Content Across HIRM Files",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def hirm_search_content(params: SearchContentInput, ctx: Context) -> str:
    """
    Search for text content across all files in the HIRM directory.
    
    Performs recursive search through files, returning matching lines with context.
    Supports regex patterns for advanced searching.
    
    Args:
        params (SearchContentInput): Validated input parameters containing:
            - query (str): Search query or regex pattern
            - directory (str): Directory to search in
            - file_type (FileType): File type filter
            - case_sensitive (bool): Case sensitivity
            - max_results (int): Maximum files to return
            - response_format (ResponseFormat): Output format
    
    Returns:
        str: Search results with matches and context
    """
    try:
        # Validate directory
        search_dir = _validate_path(params.directory)
        
        if not search_dir.exists() or not search_dir.is_dir():
            return json.dumps({
                "error": f"Invalid directory: {params.directory}",
                "suggestion": "Provide a valid directory path."
            }, indent=2)
        
        # Report progress
        await ctx.report_progress(0.1, "Scanning directory structure...")
        
        # Collect files to search
        files_to_search = []
        for root, _, filenames in os.walk(search_dir):
            for filename in filenames:
                file_path = Path(root) / filename
                if (file_path.suffix.lower() in SEARCHABLE_EXTENSIONS and
                    _match_file_type_filter(file_path, params.file_type)):
                    files_to_search.append(file_path)
        
        await ctx.report_progress(0.2, f"Searching {len(files_to_search)} files...")
        
        # Search files
        results = []
        for i, file_path in enumerate(files_to_search):
            if len(results) >= params.max_results:
                break
            
            matches = _search_in_file(file_path, params.query, params.case_sensitive)
            
            if matches:
                results.append({
                    'path': str(file_path.relative_to(HIRM_BASE_DIR)),
                    'type': _get_file_type(file_path),
                    'size': _format_file_size(file_path.stat().st_size),
                    'match_count': len(matches),
                    'matches': matches
                })
            
            # Update progress
            if i % 10 == 0:
                progress = 0.2 + (0.7 * i / len(files_to_search))
                await ctx.report_progress(progress, f"Searched {i}/{len(files_to_search)} files...")
        
        await ctx.report_progress(1.0, "Search complete")
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                'query': params.query,
                'total_files_searched': len(files_to_search),
                'files_with_matches': len(results),
                'results': results
            }, indent=2)
        else:
            return _format_search_results_markdown(results)
    
    except ValueError as e:
        return json.dumps({
            "error": str(e),
            "suggestion": "Check the directory path and try again."
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "error": f"Search error: {type(e).__name__}: {str(e)}",
            "suggestion": "Try simplifying the search query or narrowing the directory scope."
        }, indent=2)


# ------------------------------------------------------------------------------
# HIRM-Specific Analysis Tools
# ------------------------------------------------------------------------------

class FindCitationsInput(BaseModel):
    """Input parameters for finding citations in papers."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    author: Optional[str] = Field(
        default=None,
        description="Filter by author name (e.g., 'Tononi', 'Beggs')"
    )
    year: Optional[int] = Field(
        default=None,
        description="Filter by publication year",
        ge=1900,
        le=2030
    )
    topic: Optional[str] = Field(
        default=None,
        description="Search for topic keywords (e.g., 'criticality', 'consciousness', 'IIT')"
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


@mcp.tool(
    name="hirm_find_citations",
    annotations={
        "title": "Find Citations in HIRM Corpus",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False
    }
)
async def hirm_find_citations(params: FindCitationsInput) -> str:
    """
    Find and analyze citations across the HIRM research corpus.
    
    Searches through bibliography files, papers, and documentation to find
    citations matching specified criteria. Useful for literature synthesis
    and tracking theoretical connections.
    
    Args:
        params (FindCitationsInput): Validated input parameters containing:
            - author (Optional[str]): Author name filter
            - year (Optional[int]): Publication year filter
            - topic (Optional[str]): Topic keyword filter
            - response_format (ResponseFormat): Output format
    
    Returns:
        str: List of matching citations with context
    """
    try:
        # Search for citation-related files
        bib_files = []
        citation_files = []
        
        for root, _, filenames in os.walk(HIRM_BASE_DIR):
            for filename in filenames:
                file_path = Path(root) / filename
                if file_path.suffix.lower() in {'.bib', '.json'}:
                    bib_files.append(file_path)
                elif 'citation' in filename.lower() or 'reference' in filename.lower():
                    citation_files.append(file_path)
        
        results = []
        
        # Build search patterns
        search_patterns = []
        if params.author:
            search_patterns.append(params.author)
        if params.year:
            search_patterns.append(str(params.year))
        if params.topic:
            search_patterns.append(params.topic)
        
        # Search bibliography files
        for bib_file in bib_files:
            try:
                with open(bib_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Check if any pattern matches
                    if not search_patterns or any(
                        re.search(pattern, content, re.IGNORECASE)
                        for pattern in search_patterns
                    ):
                        # Extract entries (simple heuristic)
                        entries = re.findall(
                            r'@\w+\{[^@]+',
                            content,
                            re.DOTALL
                        )
                        
                        for entry in entries:
                            if all(
                                re.search(pattern, entry, re.IGNORECASE)
                                for pattern in search_patterns
                            ):
                                results.append({
                                    'file': str(bib_file.relative_to(HIRM_BASE_DIR)),
                                    'type': 'bibliography',
                                    'entry': entry[:500] + ('...' if len(entry) > 500 else '')
                                })
            except Exception:
                continue
        
        # Search citation files
        for cite_file in citation_files:
            for pattern in search_patterns:
                matches = _search_in_file(cite_file, pattern, False)
                if matches:
                    results.append({
                        'file': str(cite_file.relative_to(HIRM_BASE_DIR)),
                        'type': 'citation_file',
                        'matches': matches[:5]  # First 5 matches
                    })
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                'filters': {
                    'author': params.author,
                    'year': params.year,
                    'topic': params.topic
                },
                'results_count': len(results),
                'results': results
            }, indent=2)
        else:
            output = [f"# Citation Search Results ({len(results)} found)\n"]
            
            if params.author or params.year or params.topic:
                output.append("**Filters:**")
                if params.author:
                    output.append(f"- Author: {params.author}")
                if params.year:
                    output.append(f"- Year: {params.year}")
                if params.topic:
                    output.append(f"- Topic: {params.topic}")
                output.append("")
            
            for result in results[:20]:  # Show first 20
                output.append(f"## {result['file']}")
                output.append(f"**Type:** {result['type']}\n")
                
                if 'entry' in result:
                    output.append(f"```\n{result['entry']}\n```\n")
                elif 'matches' in result:
                    for match in result['matches']:
                        output.append(f"- Line {match['line_number']}: {match['line']}\n")
                
                output.append("")
            
            if len(results) > 20:
                output.append(f"\n*... and {len(results) - 20} more results*")
            
            return "\n".join(output)
    
    except Exception as e:
        return json.dumps({
            "error": f"Citation search error: {type(e).__name__}: {str(e)}",
            "suggestion": "Check search parameters and try again."
        }, indent=2)


class GetProjectStatsInput(BaseModel):
    """Input parameters for project statistics."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format"
    )


@mcp.tool(
    name="hirm_get_stats",
    annotations={
        "title": "Get HIRM Project Statistics",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def hirm_get_stats(params: GetProjectStatsInput) -> str:
    """
    Get comprehensive statistics about the HIRM research project.
    
    Provides overview of file counts, types, sizes, and research corpus metrics.
    Useful for understanding project scope and organization.
    
    Args:
        params (GetProjectStatsInput): Validated input parameters containing:
            - response_format (ResponseFormat): Output format
    
    Returns:
        str: Project statistics and metrics
    """
    try:
        stats = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'directories': set(),
            'largest_files': [],
            'recently_modified': []
        }
        
        all_files = []
        
        # Collect statistics
        for root, _, filenames in os.walk(HIRM_BASE_DIR):
            stats['directories'].add(root)
            
            for filename in filenames:
                file_path = Path(root) / filename
                try:
                    stat = file_path.stat()
                    file_type = _get_file_type(file_path)
                    
                    stats['total_files'] += 1
                    stats['total_size'] += stat.st_size
                    
                    if file_type not in stats['file_types']:
                        stats['file_types'][file_type] = {'count': 0, 'size': 0}
                    
                    stats['file_types'][file_type]['count'] += 1
                    stats['file_types'][file_type]['size'] += stat.st_size
                    
                    all_files.append({
                        'path': str(file_path.relative_to(HIRM_BASE_DIR)),
                        'size': stat.st_size,
                        'modified': stat.st_mtime
                    })
                except Exception:
                    continue
        
        # Get largest files
        all_files.sort(key=lambda x: x['size'], reverse=True)
        stats['largest_files'] = [
            {
                'path': f['path'],
                'size': _format_file_size(f['size'])
            }
            for f in all_files[:10]
        ]
        
        # Get recently modified
        all_files.sort(key=lambda x: x['modified'], reverse=True)
        stats['recently_modified'] = [
            {
                'path': f['path'],
                'modified': _format_timestamp(f['modified'])
            }
            for f in all_files[:10]
        ]
        
        # Format file type stats
        formatted_types = []
        for ftype, data in stats['file_types'].items():
            formatted_types.append({
                'type': ftype,
                'count': data['count'],
                'total_size': _format_file_size(data['size'])
            })
        
        formatted_types.sort(key=lambda x: x['count'], reverse=True)
        
        if params.response_format == ResponseFormat.JSON:
            return json.dumps({
                'total_files': stats['total_files'],
                'total_size': _format_file_size(stats['total_size']),
                'total_size_bytes': stats['total_size'],
                'total_directories': len(stats['directories']),
                'file_types': formatted_types,
                'largest_files': stats['largest_files'],
                'recently_modified': stats['recently_modified']
            }, indent=2)
        else:
            output = ["# HIRM Project Statistics\n"]
            output.append(f"**Total Files:** {stats['total_files']:,}")
            output.append(f"**Total Size:** {_format_file_size(stats['total_size'])}")
            output.append(f"**Directories:** {len(stats['directories'])}\n")
            
            output.append("## File Types\n")
            for ftype in formatted_types:
                output.append(f"- **{ftype['type'].title()}:** {ftype['count']} files ({ftype['total_size']})")
            
            output.append("\n## Largest Files\n")
            for f in stats['largest_files']:
                output.append(f"- `{f['path']}` ({f['size']})")
            
            output.append("\n## Recently Modified\n")
            for f in stats['recently_modified']:
                output.append(f"- `{f['path']}` ({f['modified']})")
            
            return "\n".join(output)
    
    except Exception as e:
        return json.dumps({
            "error": f"Statistics error: {type(e).__name__}: {str(e)}",
            "suggestion": "Ensure HIRM directory is accessible."
        }, indent=2)


# ==============================================================================
# SERVER EXECUTION
# ==============================================================================

if __name__ == "__main__":
    # Run with stdio transport (local integration)
    mcp.run()
