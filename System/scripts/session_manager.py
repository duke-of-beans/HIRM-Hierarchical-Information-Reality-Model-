#!/usr/bin/env python3
"""
HIRM Session Manager
Manages session lifecycle: start, checkpoint, end.
Synchronizes BUILD_STATUS.md <-> CURRENT_STATUS.md <-> PROJECT_DNA.yaml

Created: 2026-01-17
Version: 1.0
"""

import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class SessionManager:
    """Manages HIRM research session lifecycle"""
    
    def __init__(self, corpus_root: Path):
        self.corpus_root = corpus_root
        self.build_status_path = corpus_root / "Logs" / "BUILD_STATUS.md"
        self.current_status_path = corpus_root / "CURRENT_STATUS.md"
        self.project_dna_path = corpus_root / "PROJECT_DNA.yaml"
    
    def start_session(self) -> Dict:
        """Initialize a new session"""
        print("=" * 60)
        print("HIRM Session Start")
        print("=" * 60)
        
        # Load PROJECT_DNA to get session number
        project_dna = self.load_project_dna()
        session_number = project_dna['current_state']['session_number'] + 1
        
        print(f"\n[START] Session {session_number}")
        
        # Check for crash recovery
        crash_status = self.check_crash_recovery()
        if crash_status['crashed']:
            print(f"\n[WARN] Previous session crashed!")
            print(f"[INFO] Last action: {crash_status['last_action']}")
            print(f"[INFO] Resume from: {crash_status['resume_from']}")
            print("\nWaiting for user confirmation to resume...")
            return {
                'session': session_number,
                'crashed': True,
                'crash_info': crash_status
            }
        
        # Normal start
        self.update_build_status(f"[START] Session {session_number} initialized", session_number)
        
        # Load current status
        current_status = self.load_current_status()
        
        print(f"\n[OK] Session {session_number} ready")
        print(f"Phase: {current_status.get('research_phase', 'Unknown')}")
        print(f"Health: {current_status.get('health_score', 'Unknown')}")
        
        return {
            'session': session_number,
            'crashed': False,
            'phase': current_status.get('research_phase'),
            'priorities': current_status.get('next_priorities', [])
        }
    
    def checkpoint(self, action: str, session_number: int):
        """Create a checkpoint during session"""
        self.update_build_status(f"[WIP] {action}", session_number)
    
    def complete_action(self, action: str, session_number: int):
        """Mark action as complete"""
        self.update_build_status(f"[DONE] {action}", session_number)
    
    def end_session(self, session_number: int, summary: Dict) -> Dict:
        """End session and create summary"""
        print("\n" + "=" * 60)
        print(f"HIRM Session {session_number} End")
        print("=" * 60)
        
        # Update PROJECT_DNA session number
        self.update_project_dna_session(session_number, summary.get('milestone'))
        
        # Update CURRENT_STATUS
        self.update_current_status(summary)
        
        # Create session summary file
        summary_path = self.create_session_summary(session_number, summary)
        
        # Final checkpoint
        self.update_build_status(f"[DONE] Session {session_number} complete", session_number)
        
        print(f"\n[OK] Session {session_number} completed")
        print(f"[INFO] Summary: {summary_path}")
        
        return {
            'session': session_number,
            'summary_path': str(summary_path),
            'next_session': session_number + 1
        }
    
    def check_crash_recovery(self) -> Dict:
        """Check if previous session crashed"""
        try:
            content = self.build_status_path.read_text(encoding='utf-8')
            
            # Look for last [WIP] or [TODO] without matching [DONE]
            wip_matches = list(re.finditer(r'\[WIP\]\s+(.+)', content))
            done_matches = list(re.finditer(r'\[DONE\]\s+(.+)', content))
            
            if wip_matches:
                last_wip = wip_matches[-1].group(1)
                
                # Check if there's a [DONE] after the last [WIP]
                if done_matches and done_matches[-1].start() < wip_matches[-1].start():
                    return {
                        'crashed': True,
                        'last_action': last_wip,
                        'resume_from': last_wip
                    }
            
            return {'crashed': False}
        
        except Exception as e:
            print(f"[WARN] Could not check crash recovery: {e}")
            return {'crashed': False}
    
    def update_build_status(self, message: str, session_number: int):
        """Append to BUILD_STATUS.md"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entry = f"{message} - {timestamp}\n"
            
            # Read current content
            content = self.build_status_path.read_text(encoding='utf-8')
            
            # Find session section or create it
            session_marker = f"## SESSION {session_number}"
            if session_marker not in content:
                # Add new session section
                content += f"\n\n{session_marker}\n\n{entry}"
            else:
                # Append to existing session
                content += entry
            
            self.build_status_path.write_text(content, encoding='utf-8')
        
        except Exception as e:
            print(f"[WARN] Could not update BUILD_STATUS: {e}")
    
    def load_project_dna(self) -> Dict:
        """Load PROJECT_DNA.yaml"""
        try:
            with open(self.project_dna_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[WARN] Could not load PROJECT_DNA: {e}")
            return {'current_state': {'session_number': 0}}
    
    def load_current_status(self) -> Dict:
        """Parse CURRENT_STATUS.md"""
        try:
            content = self.current_status_path.read_text(encoding='utf-8')
            
            # Extract key info
            status = {}
            
            if match := re.search(r'Research Phase:\s*(.+)', content):
                status['research_phase'] = match.group(1)
            
            if match := re.search(r'Session:\s*(\d+)', content):
                status['session'] = int(match.group(1))
            
            if match := re.search(r'Health.*?(\d+)/(\d+)', content):
                status['health_score'] = f"{match.group(1)}/{match.group(2)}"
            
            return status
        
        except Exception as e:
            print(f"[WARN] Could not load CURRENT_STATUS: {e}")
            return {}
    
    def update_project_dna_session(self, session_number: int, milestone: Optional[str] = None):
        """Update session number in PROJECT_DNA.yaml"""
        try:
            project_dna = self.load_project_dna()
            project_dna['current_state']['session_number'] = session_number
            project_dna['current_state']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            
            if milestone:
                project_dna['current_state']['last_major_milestone'] = milestone
            
            with open(self.project_dna_path, 'w', encoding='utf-8') as f:
                yaml.dump(project_dna, f, default_flow_style=False, allow_unicode=True)
            
            print(f"[OK] Updated PROJECT_DNA session to {session_number}")
        
        except Exception as e:
            print(f"[WARN] Could not update PROJECT_DNA: {e}")
    
    def update_current_status(self, summary: Dict):
        """Update CURRENT_STATUS.md with session results"""
        try:
            content = self.current_status_path.read_text(encoding='utf-8')
            
            # Update session number
            content = re.sub(
                r'Session:\s*\d+',
                f"Session: {summary.get('session', 'Unknown')}",
                content
            )
            
            # Update last updated date
            content = re.sub(
                r'Last Updated:\s*\d{4}-\d{2}-\d{2}',
                f"Last Updated: {datetime.now().strftime('%Y-%m-%d')}",
                content
            )
            
            self.current_status_path.write_text(content, encoding='utf-8')
            print(f"[OK] Updated CURRENT_STATUS")
        
        except Exception as e:
            print(f"[WARN] Could not update CURRENT_STATUS: {e}")
    
    def create_session_summary(self, session_number: int, summary: Dict) -> Path:
        """Create SESSION_N_SUMMARY.md"""
        summary_path = self.corpus_root / "Logs" / "Sessions" / f"SESSION_{session_number}_SUMMARY.md"
        
        summary_text = [
            f"# Session {session_number} Summary",
            "",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            f"**Phase:** {summary.get('phase', 'Unknown')}",
            "",
            "## Accomplishments",
            ""
        ]
        
        for item in summary.get('accomplishments', []):
            summary_text.append(f"- {item}")
        
        summary_text.extend([
            "",
            "## Decisions Made",
            ""
        ])
        
        for item in summary.get('decisions', []):
            summary_text.append(f"- {item}")
        
        summary_text.extend([
            "",
            "## Next Priorities",
            ""
        ])
        
        for item in summary.get('next_priorities', []):
            summary_text.append(f"- {item}")
        
        summary_text.extend([
            "",
            "---",
            "",
            f"**Generated by:** session_manager.py v1.0"
        ])
        
        summary_path.write_text('\n'.join(summary_text), encoding='utf-8')
        return summary_path

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HIRM Session Manager')
    parser.add_argument('action', choices=['start', 'end', 'checkpoint'], help='Session action')
    parser.add_argument('--session', type=int, help='Session number (for end/checkpoint)')
    parser.add_argument('--message', type=str, help='Checkpoint message')
    args = parser.parse_args()
    
    corpus_root = Path("D:/Research/HIRM")
    manager = SessionManager(corpus_root)
    
    if args.action == 'start':
        result = manager.start_session()
        return 0
    
    elif args.action == 'checkpoint':
        if not args.session or not args.message:
            print("[FAIL] --session and --message required for checkpoint")
            return 1
        manager.checkpoint(args.message, args.session)
        return 0
    
    elif args.action == 'end':
        if not args.session:
            print("[FAIL] --session required for end")
            return 1
        
        # Minimal summary for CLI usage
        summary = {
            'session': args.session,
            'phase': 'Unknown',
            'accomplishments': [],
            'decisions': [],
            'next_priorities': []
        }
        
        result = manager.end_session(args.session, summary)
        return 0

if __name__ == "__main__":
    exit(main())
