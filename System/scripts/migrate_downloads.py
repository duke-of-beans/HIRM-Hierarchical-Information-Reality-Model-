import shutil
from pathlib import Path

# Source and destination roots
downloads = Path(r'D:\Downloads')
hirm = Path(r'D:\HIRM')

# Files to migrate with their destinations
migrations = {
    # Theory documents -> Theory/Extensions or Theory/Core
    'HIRM_Bifurcation_Theory_Comprehensive_Framework.md': 'Theory/Extensions',
    'HIRM_Bifurcation_Theory_Enhanced.md': 'Theory/Extensions',
    'HIRM_Complete_RG_Framework.md': 'Theory/Mathematical_Tools',
    'HIRM_Comprehensive_Research_Synthesis.md': 'Publications/Manuscripts',
    'HIRM_Comprehensive_Research_Synthesis_PUBLICATION_READY.md': 'Publications/Manuscripts',
    'HIRM_CORPUS_MASTER_INVENTORY.md': 'Corpus/Index',
    'HIRM_Information_Geometry_Framework.md': 'Theory/Mathematical_Tools',
    'HIRM_Master_Executive_Summary.md': 'Documentation',
    'HIRM_Master_Research_Agenda.md': 'Documentation',
    'HIRM_Master_Research_Agenda_ENHANCED.md': 'Documentation',
    'HIRM_Persistent_Homology_Analysis_Summary.md': 'Theory/Mathematical_Tools',
    'HIRM_Phase_Transition_Framework_PUBLICATION_READY.md': 'Publications/Manuscripts',
    'HIRM_Retrospective_Analysis_Report.md': 'Documentation',
    'HIRM_RG_Framework_Executive_Summary.md': 'Theory/Mathematical_Tools',
    'HIRM_RG_Quick_Reference.md': 'Theory/Mathematical_Tools',
    'HIRM_Statistical_Mechanics_Framework.md': 'Theory/Mathematical_Tools',
    'HIRM_StatMech_Executive_Summary.md': 'Theory/Mathematical_Tools',
    'HIRM_Strategic_Foundation_PUBLICATION_READY.md': 'Publications/Manuscripts',
    'HIRM_Theoretical_Research_Agenda_ENHANCED.md': 'Documentation',
    'HIRM_Theoretical_Research_Agenda_With_Prompts.md': 'Documentation',
    'HIRM_Deliverables_Completion_Summary.md': 'Documentation',
    'HIRM_Figure_Work_Order.md': 'Figures/Working',
    
    # Python scripts -> Code/Tools
    'hirm_bifurcation_toolkit.py': 'Code/Tools',
    'hirm_rg_complete_toolkit.py': 'Code/Tools',
    'hirm_statistical_mechanics.py': 'Code/Tools',
    'information_geometry_toolkit.py': 'Code/Tools',
    
    # Figures -> Figures/Working
    'hirm_critical_scaling.png': 'Figures/Working',
    'hirm_full_simulation.png': 'Figures/Working',
    'hirm_multiscale_rg.png': 'Figures/Working',
    'HIRM_persistent_homology_analysis.png': 'Figures/Working',
    'hirm_phase_transition.png': 'Figures/Working',
    'hirm_retrospective_analysis.png': 'Figures/Working',
    'hirm_rg_flow_complete.png': 'Figures/Working',
    'HIRM_Sleep_EDF_Empirical_Results.png': 'Figures/Working',
    'hirm_topology_predictions_demo.png': 'Figures/Working',
    
    # Brain Criticality reviews
    'Brain_Criticality_Self_Reference_Consciousness_Comprehensive_Review.md': 'Corpus/Reviews',
    
    # Thesis documents
    'When_Reality_Splits_Complete_Thesis.md': 'Publications/Manuscripts',
    
    # Work orders
    'HIRM_COMPLETE_WORK_ORDER.tsv': 'Documentation',
}

# Legacy Ouroboros files -> Archive
legacy_files = [
    'ouroboros_observer_theory_layman_guide.md',
    'The_Ouroboros_Observer.docx',
    'The_Ouroboros_Observer_POPULAR_SCIENCE_ARCHIVE.md',
]

# Perform migrations
migrated = 0
skipped = 0
errors = []

print("=== MIGRATING HIRM FILES FROM DOWNLOADS ===\n")

for filename, dest_folder in migrations.items():
    src = downloads / filename
    if src.exists():
        dest_dir = hirm / dest_folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / filename
        
        if dest.exists():
            print(f"SKIP (exists): {filename}")
            skipped += 1
        else:
            try:
                shutil.copy2(src, dest)
                print(f"COPIED: {filename} -> {dest_folder}/")
                migrated += 1
            except Exception as e:
                errors.append((filename, str(e)))
                print(f"ERROR: {filename} - {e}")
    else:
        print(f"NOT FOUND: {filename}")

# Handle legacy files
print("\n=== ARCHIVING LEGACY OUROBOROS FILES ===\n")
archive_dir = hirm / '_Archive' / 'Deprecated' / 'Ouroboros_Legacy'
archive_dir.mkdir(parents=True, exist_ok=True)

for filename in legacy_files:
    src = downloads / filename
    if src.exists():
        dest = archive_dir / filename
        if not dest.exists():
            try:
                shutil.copy2(src, dest)
                print(f"ARCHIVED: {filename}")
                migrated += 1
            except Exception as e:
                errors.append((filename, str(e)))
        else:
            print(f"SKIP (exists): {filename}")
            skipped += 1

print(f"\n=== SUMMARY ===")
print(f"Migrated: {migrated}")
print(f"Skipped (already exist): {skipped}")
print(f"Errors: {len(errors)}")
if errors:
    print("\nErrors:")
    for f, e in errors:
        print(f"  - {f}: {e}")
