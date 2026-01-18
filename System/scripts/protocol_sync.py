#!/usr/bin/env python3
"""
HIRM Protocol Version Synchronizer
Propagates protocol version changes across all referencing files.
Triggered when Protocols/HIRM_RESEARCH_PROTOCOLS_vX.X.md is renamed.

Created: 2026-01-17
Version: 1.0
"""

import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional

class ProtocolVersionSync:
    """Synchronizes protocol version across HIRM corpus"""
    
    def __init__(self, corpus_root: Path):
        self.corpus_root = corpus_root
        self.current_version = self.detect_current_version()
        self.key_files = [
            "PROJECT_DNA.yaml",
            "CURRENT_STATUS.md",
            "HIRM_INSTRUCTIONS_PROJECT.md",
            "Logs/BUILD_STATUS.md",
            "Documentation/START_HERE.md"
        ]
        self.updates_made: List[Dict] = []
    
    def detect_current_version(self) -> str:
        """Detect current protocol version from filename"""
        protocols_dir = self.corpus_root / "Protocols"
        
        for file in protocols_dir.glob("HIRM_RESEARCH_PROTOCOLS_v*.md"):
            if match := re.search(r"v(\d+\.\d+)", file.name):
                version = match.group(1)
                print(f"[OK] Detected protocol version: v{version}")
                return version
        
        print("[WARN] Could not detect protocol version, using v2.3")
        return "2.3"
    
    def find_version_references(self, file_path: Path) -> List[Dict]:
        """Find all version references in a file"""
        references = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Find all version patterns
            patterns = [
                r'HIRM_RESEARCH_PROTOCOLS_v(\d+\.\d+)',
                r'Protocol[s]?\s+v(\d+\.\d+)',
                r'version:\s*"?(\d+\.\d+)"?',  # YAML style
                r'Version:\s+(\d+\.\d+)',      # Markdown style
            ]
            
            for pattern in patterns:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    version_found = match.group(1)
                    line_num = content[:match.start()].count('\n') + 1
                    
                    references.append({
                        'file': str(file_path.relative_to(self.corpus_root)),
                        'version': version_found,
                        'line_number': line_num,
                        'match': match.group(0),
                        'position': match.start()
                    })
        
        except Exception as e:
            print(f"[WARN] Error reading {file_path}: {e}")
        
        return references
    
    def scan_key_files(self) -> List[Dict]:
        """Scan key files for version references"""
        print(f"\n[START] Scanning key files for version references")
        
        all_references = []
        
        for file_rel_path in self.key_files:
            file_path = self.corpus_root / file_rel_path
            
            if not file_path.exists():
                print(f"[WARN] File not found: {file_rel_path}")
                continue
            
            refs = self.find_version_references(file_path)
            all_references.extend(refs)
            
            if refs:
                print(f"[OK] {file_rel_path}: {len(refs)} version references")
        
        return all_references
    
    def update_version(self, file_path: Path, old_version: str, new_version: str, dry_run: bool = True) -> int:
        """Update version in a file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Replace version patterns
            patterns = [
                (r'HIRM_RESEARCH_PROTOCOLS_v\d+\.\d+', f'HIRM_RESEARCH_PROTOCOLS_v{new_version}'),
                (r'(Protocol[s]?\s+)v\d+\.\d+', rf'\1v{new_version}'),
                (r'(version:\s*"?)\d+\.\d+("?)', rf'\1{new_version}\2'),  # YAML
                (r'(Version:\s+)\d+\.\d+', rf'\1{new_version}'),          # Markdown
            ]
            
            replacements = 0
            for pattern, replacement in patterns:
                content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
                replacements += count
            
            if content != original_content:
                if not dry_run:
                    file_path.write_text(content, encoding='utf-8')
                
                self.updates_made.append({
                    'file': str(file_path.relative_to(self.corpus_root)),
                    'old_version': old_version,
                    'new_version': new_version,
                    'replacements': replacements
                })
                
                return replacements
        
        except Exception as e:
            print(f"[WARN] Error updating {file_path}: {e}")
        
        return 0
    
    def sync_all(self, new_version: str, dry_run: bool = True) -> List[Dict]:
        """Synchronize protocol version across all key files"""
        print(f"\n[START] Syncing protocol version to v{new_version} ({'DRY RUN' if dry_run else 'LIVE'})")
        
        total_replacements = 0
        
        for file_rel_path in self.key_files:
            file_path = self.corpus_root / file_rel_path
            
            if not file_path.exists():
                continue
            
            count = self.update_version(file_path, self.current_version, new_version, dry_run)
            total_replacements += count
            
            if count > 0:
                status = "[DRY RUN]" if dry_run else "[OK]"
                print(f"{status} {file_rel_path}: {count} replacements")
        
        if dry_run:
            print(f"\n[DRY RUN] Would update {total_replacements} version references")
        else:
            print(f"\n[OK] Updated {total_replacements} version references")
        
        return self.updates_made
    
    def generate_report(self, output_path: Path = None) -> str:
        """Generate version sync report"""
        report = [
            "# Protocol Version Synchronization Report",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Current Version:** v{self.current_version}",
            ""
        ]
        
        if not self.updates_made:
            report.extend([
                "**Status:** ✅ NO UPDATES NEEDED",
                "",
                "All files already reference the current protocol version.",
                ""
            ])
        else:
            report.extend([
                f"**Status:** {'✅ UPDATES APPLIED' if self.updates_made else '⚠️ DRY RUN'}",
                "",
                "## Updates Made",
                "",
                f"- Total files updated: {len(self.updates_made)}",
                f"- Total replacements: {sum(u['replacements'] for u in self.updates_made)}",
                ""
            ])
            
            for update in self.updates_made:
                report.append(f"### {update['file']}")
                report.append("")
                report.append(f"- Old version: v{update['old_version']}")
                report.append(f"- New version: v{update['new_version']}")
                report.append(f"- Replacements: {update['replacements']}")
                report.append("")
        
        report.extend([
            "## Key Files Monitored",
            ""
        ])
        
        for file in self.key_files:
            file_path = self.corpus_root / file
            status = "✅" if file_path.exists() else "❌"
            report.append(f"- {status} {file}")
        
        report.extend([
            "",
            "---",
            "",
            "**Generated by:** protocol_sync.py v1.0"
        ])
        
        report_text = '\n'.join(report)
        
        if output_path:
            output_path.write_text(report_text, encoding='utf-8')
            print(f"[OK] Report saved to {output_path}")
        
        return report_text

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HIRM Protocol Version Synchronizer')
    parser.add_argument('--new-version', type=str, help='New version to sync to (e.g., 2.4)')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default is dry-run)')
    parser.add_argument('--scan-only', action='store_true', help='Only scan for references')
    args = parser.parse_args()
    
    corpus_root = Path("D:/Research/HIRM")
    
    print("=" * 60)
    print("HIRM Protocol Version Synchronizer v1.0")
    print("=" * 60)
    
    syncer = ProtocolVersionSync(corpus_root)
    
    if args.scan_only:
        # Just scan
        references = syncer.scan_key_files()
        
        print("\n" + "=" * 60)
        print(f"[INFO] Found {len(references)} version references")
        
        by_file = {}
        for ref in references:
            file = ref['file']
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(ref)
        
        for file, refs in sorted(by_file.items()):
            print(f"\n{file}:")
            for ref in refs:
                print(f"  Line {ref['line_number']}: {ref['match']} (v{ref['version']})")
        
        return 0
    
    # Determine new version
    if args.new_version:
        new_version = args.new_version
    else:
        new_version = syncer.current_version
        print(f"[INFO] No new version specified, using current: v{new_version}")
    
    # Sync
    updates = syncer.sync_all(new_version, dry_run=not args.apply)
    
    # Generate report
    report_path = corpus_root / "Logs" / f"protocol_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report = syncer.generate_report(report_path)
    
    # Print summary
    print("\n" + "=" * 60)
    if updates:
        if args.apply:
            print(f"[OK] Applied {sum(u['replacements'] for u in updates)} updates")
        else:
            print(f"[DRY RUN] Would apply {sum(u['replacements'] for u in updates)} updates")
            print("[INFO] Run with --apply to make changes")
    else:
        print("[OK] No updates needed - all files current")
    
    print(f"[INFO] See report: {report_path}")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    exit(main())
