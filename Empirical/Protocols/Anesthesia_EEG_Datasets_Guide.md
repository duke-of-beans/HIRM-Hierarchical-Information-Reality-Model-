# Anesthesia EEG Datasets for Consciousness Transition Research

**The Cambridge Propofol Study by Chennu et al. (2016) stands out as immediately accessible with 91-channel high-density EEG from 20 subjects, complete behavioral LOC/ROC markers, and full documentation**—downloadable now without barriers. Beyond this gold standard, we identified 12+ additional datasets ranging from the massive Harvard EEG Database (109,000+ patients) to specialized propofol studies, though most require data requests. PhysioNet and OpenNeuro, despite their prominence, offer limited options: PhysioNet provides only processed power spectra (not raw EEG), while OpenNeuro currently hosts no human anesthesia EEG datasets at all. VitalDB contains 5,566 cases with EEG but critically lacks precise LOC/ROC timestamps. The field shows strong open science momentum with recent BIDS standardization and growing data sharing culture.

## Immediately accessible datasets with complete specifications

The search uncovered one exceptional publicly available dataset and revealed that major repositories have significant gaps. The **Chennu et al. 2016 Cambridge dataset** provides the most accessible path forward, while several high-quality datasets require direct author contact. VitalDB's massive scale comes with the significant caveat of approximate rather than precise consciousness transition markers.

### Dataset 1: Cambridge Propofol Sedation Study (Chennu et al. 2016)

This represents the highest-quality immediately accessible option. The 91-channel EEG recordings span four consciousness states per subject with behavioral responsiveness clearly documented. Researchers have successfully reused this data across 200+ citations, establishing its reliability. The preprocessing is publication-ready (0.5-45 Hz filtered, artifact-removed, EEGLAB format), and blood plasma propofol concentrations provide pharmacokinetic validation.

Seven participants became behaviorally drowsy at moderate sedation while 13 remained responsive, enabling analysis of individual variability in consciousness transitions. Each condition includes approximately 7 minutes of continuous recording, segmented into 10-second epochs with 38-40 epochs retained per condition after quality control.

**Access mechanism:** Direct download from https://www.repository.cam.ac.uk/handle/1810/252736 under CC BY 2.0 UK license. The 3.44 GB dataset includes complete metadata in datainfo.mat with propofol concentrations, reaction times, and hit rates. BIDS-converted versions are available through the FieldTrip toolbox.

**Technical specifications:** 128-channel Net Amps 300 amplifier (EGI) recording at 250 Hz, vertex reference during acquisition then re-referenced to average. Target-controlled infusion using the Marsh model with actual plasma concentrations verified by blood sampling (5 samples per participant).

**Limitations:** Gradual sedation rather than rapid induction means LOC/ROC timing requires binomial modeling of behavioral responses rather than single-point markers. The study focused on mild-to-moderate sedation, not surgical-level anesthesia.

### Dataset 2: VitalDB Multi-Parameter Surgical Database

VitalDB provides unprecedented scale with 5,566 cases containing BIS/EEG monitoring across diverse surgical procedures. Both EEG waveforms (128 Hz, 2 channels) and processed indices (BIS, suppression ratio, spectral edge frequency) are available alongside complete drug administration records including target-controlled infusion parameters.

The database spans multiple anesthetic regimens: 3,498 cases with propofol TCI (54.8%), 2,537 sevoflurane cases (39.7%), 1,383 desflurane cases (21.6%), and 4,835 remifentanil cases (75.7%). Effect-site concentrations, plasma concentrations, and infusion rates are tracked continuously.

**Critical limitation for HIRM validation:** No precise LOC/ROC behavioral timestamps exist. Anesthesia start/end times from electronic medical records have only 5-minute resolution. Researchers must infer consciousness transitions from BIS threshold crossings (e.g., BIS < 60), drug bolus timing, or anesthetic gas introduction—introducing uncertainty into transition detection.

**Access pathway:** Free download from https://vitaldb.net after accepting the CC BY-NC-SA 4.0 data use agreement. Python library (vitaldb package) provides convenient API access. Total dataset is 103.4 GB with standardized .vital binary format plus CSV clinical data.

**Best use cases:** Training ML models for anesthetic depth prediction, studying maintenance-phase EEG dynamics, pharmacokinetic-pharmacodynamic modeling, or comparative agent studies. Less suitable for precise LOC/ROC transition validation due to timing uncertainty.

### Dataset 3: PhysioNet Multitaper Spectra During GABAergic Anesthesia

This 54-subject dataset (10 volunteers, 44 OR patients) provides EEG power spectra from 0-50 Hz during propofol and sevoflurane anesthesia. Volunteers received controlled propofol infusions with precise LOC/ROC determination based on probability of response to auditory cues dropping below 5%.

**Major constraint:** Only multitaper spectral estimates are provided, not raw continuous EEG signals. Each 2-second epoch yields a power spectrum (dB units) across 0.5 Hz bins. This enables frequency-domain analysis but precludes time-domain connectivity, phase-based measures, or temporal dynamics requiring continuous signals.

Volunteers were recorded with 64-channel BrainVision (5,000 Hz, analyzed using Fp1 only). OR patients used Sedline monitors (Fp1, Fp2, F7, F8 approximations at 250 Hz). Consciousness state labels are binary: 0 (unconscious), 1 (conscious), NaN (uncertain).

**Access requirements:** PhysioNet restricted access requiring user registration and signed data use agreement. Dataset DOI: 10.13026/m792-h077. Associated publication: Abel et al., PLOS ONE 2021.

**Suitability assessment:** Moderate for spectral HIRM predictions, unsuitable for connectivity or time-domain analyses. OR patient LOC timing approximates surgery start rather than precise behavioral assessment. No ROC markers for surgical patients.

## Major datasets requiring author contact

Several landmark studies offer high-quality data through reasonable request protocols. These datasets shaped current understanding of anesthetic EEG signatures but predate widespread open data mandates.

### Dataset 4: Purdon et al. 2013 MIT/MGH Propofol Study

The foundational study establishing electroencephalogram signatures of propofol-induced unconsciousness. Ten healthy volunteers underwent gradual propofol infusion from 0 to 5 μg/mL and back with 64-channel high-density EEG. The ~2-hour recording per subject captures complete induction/emergence cycles with behavioral assessments every 4 seconds using name recognition, words, and click stimuli.

This dataset established the alpha oscillations, frontal-parietal connectivity disruption, and slow-delta wave patterns that define modern anesthetic monitoring. The study demonstrated phase-amplitude coupling changes and characterized burst suppression patterns during deep anesthesia.

**Accessing the data:** Contact Massachusetts General Hospital Department of Anesthesia. Primary investigators: Patrick L. Purdon (ppurdon@mgh.harvard.edu likely) and Emery N. Brown. The paper states data available upon reasonable request. With 800+ citations, this dataset has established precedent for sharing.

**Why it matters:** Gold-standard behavioral markers with 4-second resolution, high temporal coverage, and the highest citation impact in the field. Gradual concentration increase allows precise correlation of EEG changes with effect-site propofol levels.

### Dataset 5: Michigan ReCCognition Study (Multiple Publications 2017-2021)

The University of Michigan Center for Consciousness Science conducted comprehensive studies with 20-30 healthy volunteers receiving isoflurane (1.3 age-adjusted MAC) with 128-channel EEG. Uniquely, this protocol included extensive cognitive testing across 6 domains during recovery, providing fine-grained characterization of consciousness return.

Multiple publications emerged from this infrastructure examining permutation entropy, Lempel-Ziv complexity, network connectivity, and cognitive recovery trajectories. The dataset includes sleep-wake actigraphy from the week prior to anesthesia, enabling vulnerability assessment.

**Contact pathway:** consciousness-research@med.umich.edu or visit https://consciousness.med.umich.edu/. Lead investigators: George Mashour, Anthony Hudetz, Dinesh Pal. Reference ClinicalTrials.gov NCT01911195.

**Distinctive features:** The comprehensive cognitive battery distinguishes this from simple LOC/ROC binary classification. Recovery timing varies across cognitive domains, revealing consciousness as multidimensional. The isoflurane agent differs from most propofol-focused datasets, enabling cross-agent validation.

### Dataset 6: Murphy et al. 2011 Wisconsin High-Density Study

The highest spatial resolution anesthesia EEG dataset in the literature with 256 channels. University of Wisconsin-Madison investigators recorded propofol anesthesia and compared it with natural NREM sleep in the same subjects. Source localization and default network propagation analyses were possible with this density.

**Data request:** Contact University of Wisconsin-Madison (Marcello Massimini, Giulio Tononi group). No public repository identified, but the 283 citations suggest successful data sharing. DOI: 10.5665/SLEEP.946.

**Applications:** The extreme spatial resolution enables detailed cortical mapping impossible with standard montages. Direct sleep-anesthesia comparison in identical subjects controls for individual variability better than between-subject designs.

### Dataset 7: TU München Multi-Agent Comparison (Lipp et al. 2024)

Recent 43-patient dataset comparing propofol+remifentanil, sevoflurane+sufentanil, and isoflurane+sufentanil using Isolated Forearm Technique for LOC/ROC determination. BIS, Narcotrend, and Entropy monitors recorded simultaneously, enabling cross-validation of processed indices.

**Access:** Department of Anesthesiology, Technische Universität München. Lead: Matthias Kreuzer group. DOI: 10.1007/s10877-023-01117-1 (J Clin Monit Comput 2024).

**Strategic value:** Direct multi-agent comparison with identical protocols. IFT provides gold-standard behavioral assessment. Emergence phase emphasis matches HIRM hysteresis predictions.

## Repository and database options

### Harvard EEG Database v4.1

Massive clinical database updated February 2025 containing 284,343 EEG studies from 109,178 patients across four Harvard-affiliated hospitals. ICU/LTM recordings include anesthesia monitoring during sedation. BIDS-EEG v1.7.0 standardized format with complete EHR integration (ICD codes, labs, vitals, medications, clinical notes).

**Access mechanism:** Credentialed access through Brain Data Science Platform (https://bdsp.io/content/harvard-eeg-db/4.1/) requiring data use agreement. DOI: 10.60508/k85b-fc87.

**Anesthesia relevance:** ICU sedation monitoring provides real-world data at scale. Mixed agents and patient populations enable robust ML model development. Variable consciousness assessments across clinical settings.

**Limitations:** Clinical data quality varies; consciousness assessments not standardized research protocols. Electrode montages heterogeneous across sites and clinical indications.

### Zenodo Machine Learning-Ready Dataset

Combined dataset from seven prior studies with 290 samples (1,197 after SMOTE augmentation) representing eight anesthesia-induced transition states. Graph neural network preprocessing completed with 714,610 edges constructed.

**Direct download:** https://zenodo.org/records/8348272 under open license. Published 2024, cited in Niu et al., PLOS ONE 2025.

**Use case:** Pre-processed for deep learning applications. Mixed anesthetic agents. Ready for model training without extensive preprocessing. Augmentation addresses class imbalance.

**Caveat:** Derivative dataset combining multiple sources. Original raw data characteristics vary. Augmentation may introduce artifacts for some analyses.

## Dataset inventory with complete specifications

| Dataset Name | Lead Researcher/Institution | Subjects | Anesthetic | EEG Specs | LOC/ROC Precision | Access Method | Status | Priority |
|-------------|----------------------------|----------|------------|-----------|------------------|---------------|---------|----------|
| Cambridge Propofol Study | Chennu/Cambridge | 20 | Propofol (0.6-1.2 μg/mL) | 91 ch, 250 Hz | Behavioral task responses, binomial model | Public download | ✓ Available now | **1** |
| VitalDB | Lee/Jung, Seoul National | 5,566 | Propofol, sevoflurane, desflurane | 2 ch (BIS), 128 Hz | ~5 min resolution only | Free download | ✓ Available now | **3** |
| PhysioNet Multitaper | Abel/Purdon/Brown, MGH/MIT | 54 | Propofol, sevoflurane | Spectra only (0-50 Hz) | Volunteers: 5% response threshold | Restricted (DUA) | ✓ Available | **5** |
| Purdon 2013 Propofol | Purdon/Brown, MGH/MIT | 10 | Propofol (0-5 μg/mL) | 64 ch, high density | Auditory task q4sec | On request | Contact needed | **2** |
| Michigan ReCCognition | Mashour/Hudetz, Michigan | 20-30 | Isoflurane (1.3 MAC) | 128 ch | Cognitive battery | On request | Contact needed | **4** |
| Murphy 2011 Wisconsin | Massimini/Tononi, Wisconsin | ~10 | Propofol | 256 ch (highest density) | Sleep comparison | On request | Contact needed | **6** |
| TU München Multi-Agent | Kreuzer, TU München | 43 | Propofol/Sevo/Iso + opioids | Frontal EEG | IFT (gold standard) | On request | Contact needed | **7** |
| Harvard EEG Database | Harvard Medical School | 109,178 | Mixed (ICU sedation) | Variable clinical | Clinical assessments | Credentialed | DUA required | **8** |
| Zenodo ML-Ready | Niu et al., compiled | 290→1197 | Various | Mixed sources | Variable | Public download | ✓ Available now | **9** |

## Access pathways and contact templates

### Immediate download (no permission needed)

**For Cambridge Propofol Study:**
1. Navigate to https://www.repository.cam.ac.uk/handle/1810/252736
2. Click "sedation-restingstate.zip" (3.44 GB) to download
3. Extract EEGLAB .set files and datainfo.mat
4. Optional: Download BIDS-converted version from FieldTrip download server

**For VitalDB:**
1. Visit https://vitaldb.net
2. Accept CC BY-NC-SA 4.0 data use agreement
3. Download via web interface, Python API (pip install vitaldb), or direct data files
4. EEG parameters: BIS/EEG1_WAV and BIS/EEG2_WAV tracks at 128 Hz

**For Zenodo ML Dataset:**
1. Access https://zenodo.org/records/8348272
2. Download preprocessed graph neural network dataset
3. Review Niu et al. PLOS ONE 2025 for data provenance

### Credentialed access

**For PhysioNet Restricted Datasets:**
1. Create account at https://physionet.org/
2. Complete CITI training on human research protection
3. Sign data use agreement for specific dataset
4. Access granted within 1-2 weeks for credentialed researchers

**For Harvard EEG Database:**
1. Request access at https://bdsp.io/content/harvard-eeg-db/4.1/
2. Institutional credentialing required (academic or clinical)
3. Sign data use agreement
4. Expect 2-4 weeks for approval

### Data request contact templates

**Template 1: For landmark studies (Purdon, Murphy, Michigan)**

Subject: Data access request for [Study Name] dataset - consciousness phase transition research

Dear Dr. [Author Name],

I am writing to request access to the EEG dataset from your [Year] publication in [Journal] ([DOI]). Your paper states data are available upon reasonable request.

I am conducting research on consciousness phase transitions during anesthesia, specifically testing predictions of the Holographic-Integrated Representation Model (HIRM) framework regarding:
- Critical thresholds at C ≈ 8.3 bits with sharp transitions (ΔC/Δt > 1 bit/sec)
- Hysteresis between induction and emergence (C_crit difference of 10-20%)
- Critical slowing near transition points (1.5x autocorrelation increase)

Your dataset's [specific feature: precise LOC/ROC markers, high density, continuous recording, etc.] is essential for validating these predictions. We will fully acknowledge your contribution and are open to co-authorship if substantial dataset reuse merits it.

Would you be able to share [raw EEG / processed data / specific parameters]? I am happy to sign a data use agreement and provide additional information about our analysis plans.

Thank you for considering this request.

**Template 2: For recent datasets (TU München, Harvard, others)**

Subject: Collaboration inquiry - [Dataset Name] for consciousness transition validation

Dear [Research Group],

I am reaching out regarding your recent work on [brief description]. We are conducting systematic validation of consciousness phase transition predictions and your dataset with [key feature] would be invaluable.

Specifically, we need datasets with:
✓ Precise LOC/ROC event timestamps (behavioral or pharmacokinetic markers)
✓ Continuous EEG through consciousness transitions  
✓ Known anesthetic agent concentrations
✓ Ideally >19 channels and >200 Hz sampling

Your [Year] publication indicates such data exists. Would data sharing be possible under a standard agreement? We have experience with [EEGLAB/FieldTrip/Python MNE] and can work with various formats.

We're also interested in potential collaboration opportunities if our analytical framework yields insights applicable to your ongoing research.

Looking forward to your response.

## Priority rankings with detailed rationale

### Tier 1: Immediate use (download today)

**Rank 1: Cambridge Propofol Study (Chennu et al. 2016)**
- **Accessibility score:** 10/10 (public, no barriers)
- **Data quality:** 9/10 (91 channels, professional preprocessing, validated)
- **Sample size:** 8/10 (n=20, good power)
- **LOC/ROC precision:** 8/10 (behavioral responses, binomial modeling)
- **Metadata completeness:** 10/10 (plasma concentrations, extensive documentation)

**Why it's #1:** Begin analysis immediately. The dataset has proven reusability (200+ citations), excellent documentation, and BIDS conversion available. Propofol gradual sedation suits HIRM critical slowing predictions. Individual variability is well-characterized (responsive vs. drowsy groups).

**Start here:** Download, extract, run initial spectral analysis and connectivity measures within hours. Test alpha power evolution and cross-frequency coupling across consciousness states.

### Tier 2: High priority contact

**Rank 2: Purdon 2013 MGH/MIT Dataset**
- **Accessibility score:** 6/10 (requires contact, but established sharing history)
- **Data quality:** 10/10 (64 channels, 2-hour continuous recording, definitive study)
- **Sample size:** 6/10 (n=10, adequate for proof-of-concept)
- **LOC/ROC precision:** 10/10 (4-second behavioral assessments, gold standard)
- **Metadata completeness:** 9/10 (effect-site concentrations, full timecourse)

**Why pursue:** The 4-second temporal resolution of behavioral assessments provides unmatched precision for identifying exact transition points. Gradual 0-5 μg/mL propofol infusion allows correlation analysis between EEG and concentration. This is the paper clinicians cite for anesthetic monitoring—foundational dataset.

**Expected timeline:** 2-4 weeks for data access after contacting MGH Anesthesia. High success probability given 800+ citations and established data sharing.

**Rank 3: VitalDB (Seoul National)**
- **Accessibility score:** 10/10 (free download, no barriers)
- **Data quality:** 7/10 (2-channel BIS only, 128 Hz adequate, real-world artifacts)
- **Sample size:** 10/10 (n=5,566, unmatched statistical power)
- **LOC/ROC precision:** 4/10 (major limitation: ~5 min resolution, indirect inference)
- **Metadata completeness:** 9/10 (complete TCI parameters, multi-parameter vitals)

**Strategic use:** Complement high-precision datasets with large-scale validation. Test if HIRM predictions hold across diverse agents (propofol, sevoflurane, desflurane combinations). Use BIS threshold crossings as proxy LOC/ROC despite imprecision. Train ML models for consciousness classification.

**Workaround for LOC/ROC:** Define transition windows using BIS < 60 crossings coincident with propofol effect-site concentration > threshold. Analyze multiple cases to identify consistent patterns despite individual timing uncertainty.

### Tier 3: Valuable additions

**Rank 4: Michigan ReCCognition Dataset**
- **Accessibility score:** 7/10 (contact required, but active research group)
- **Data quality:** 9/10 (128 channels, comprehensive)
- **Sample size:** 8/10 (n=20-30)
- **LOC/ROC precision:** 7/10 (cognitive battery, multidimensional consciousness)
- **Metadata completeness:** 9/10 (cognitive scores, actigraphy, full clinical)

**Unique value:** Isoflurane agent enables cross-validation of HIRM predictions beyond propofol. Cognitive battery during emergence tests if predicted hysteresis manifests differently across cognitive domains. Recovery trajectory data suits critical slowing analysis.

**Contact:** consciousness-research@med.umich.edu or directly through https://consciousness.med.umich.edu/ publications page.

**Rank 5: PhysioNet Multitaper Spectra**
- **Accessibility score:** 8/10 (requires DUA but straightforward)
- **Data quality:** 6/10 (spectra only, limits analyses)
- **Sample size:** 9/10 (n=54)
- **LOC/ROC precision:** 7/10 volunteers, 4/10 OR patients
- **Metadata completeness:** 7/10 (good for volunteers)

**When to use:** If frequency-domain HIRM predictions can be tested without time-domain connectivity. The 0.5 Hz spectral resolution across 0-50 Hz suits alpha power, slow-delta evolution, and spectral edge frequency analyses. Combined volunteer + OR data enables generalization testing.

**Limitation:** Cannot compute phase-based connectivity (wPLI, PLV) or instantaneous amplitude coupling from power spectra alone. Time-domain entropy measures impossible.

### Tier 4: Specialized applications

**Rank 6-9:** Murphy Wisconsin (256-channel), TU München (multi-agent), Harvard EEG DB (ML scale), Zenodo ML-ready

These datasets serve specific purposes: Murphy for spatial localization requiring maximum density, TU München for direct agent comparisons using IFT gold standard, Harvard for large-scale ML model training, Zenodo for immediate deep learning experiments without preprocessing.

## Critical findings on data availability

### The repository gap: PhysioNet and OpenNeuro

Despite being premier neurophysiology data repositories, both have minimal anesthesia EEG content with LOC/ROC markers. PhysioNet offers one dataset (power spectra only). OpenNeuro hosts zero human anesthesia EEG datasets, only fMRI anesthesia studies and sleep EEG.

**Why this matters:** Landmark papers (Purdon 2013, Murphy 2011, Chennu 2016) established field knowledge but only Chennu deposited public data. This creates reproducibility challenges and forces redundant data collection. The field needs cultural shift toward preregistered data sharing mandates.

**Positive trends:** BIDS-EEG standardization growing (Harvard DB, OpenNeuro sleep datasets). Zenodo and institutional repositories increasingly used. Recent papers (2023-2025) show improved data availability statements.

### The VitalDB trade-off: Scale versus precision

VitalDB's 5,566 EEG cases represent remarkable open data contribution, yet the 5-minute LOC/ROC resolution fundamentally limits consciousness transition research. For HIRM validation requiring ΔC/Δt > 1 bit/sec sharp transitions, this temporal imprecision is problematic.

**Recommendation:** Use VitalDB for maintenance-phase dynamics, agent comparisons, and ML model pre-training. Combine with high-precision datasets (Chennu, Purdon) for transition-specific validation.

### Datasets already used for consciousness threshold studies

Literature review revealed the Chennu 2016 dataset appears in multiple consciousness network studies but hasn't been explicitly used for phase transition threshold analysis. The Purdon 2013 data shaped clinical anesthetic monitoring recommendations based on frontal alpha emergence. Michigan studies examined recovery trajectory timing.

**Gap identified:** No existing studies have systematically tested sharp transition predictions (ΔC/Δt > 1 bit/sec) or empirically measured critical threshold in the 7.5-9.0 bit range across datasets. HIRM validation represents novel analysis even for existing public data.

## Known preprocessing pipelines and limitations

### EEGLAB/FieldTrip standard pipeline

The Chennu dataset uses canonical preprocessing: high-pass 0.5 Hz (removes DC drift), low-pass 45 Hz (removes line noise), average reference, ICA artifact removal for eye movements and muscle activity. FieldTrip provides complete tutorial using this exact dataset at https://www.fieldtriptoolbox.org/workshop/madrid2019/eeg_sedation/.

**Reproducing analysis:** Download tutorial scripts, verify filtering parameters match (0.5-45 Hz), check epoch rejection criteria (typically amplitude thresholds), compute power spectra using multitaper method (5-7 tapers typical for alpha band).

### Multitaper spectral estimation

Purdon/Brown group uses multitaper methods (Chronux toolbox) providing superior frequency resolution compared to FFT-based approaches. Typical parameters: 2-second windows, 3 tapers, 1 Hz bandwidth. This reduces spectral leakage enabling precise alpha peak identification.

**For HIRM validation:** Multitaper spectra suit information-theoretic measures requiring accurate spectral density estimates. Shannon entropy calculations from power spectra benefit from reduced estimation variance.

### Common data quality issues

**Burst suppression detection:** Variable algorithms across studies. Some use amplitude thresholds, others wavelet decomposition. Chennu dataset at moderate sedation avoids burst suppression entirely (propofol 0.6-1.2 μg/mL maintains continuous activity).

**Reference choices:** Average reference (Chennu) versus linked mastoids (some clinical studies) affects connectivity measures. Re-reference raw data consistently for cross-dataset comparisons.

**Age effects:** EEG slowing with age is well-documented. Michigan data includes age-adjusted MAC calculations. Pure volunteer datasets (Purdon, Chennu) use young healthy adults (mean age ~30), limiting geriatric generalization.

**Individual variability:** Chennu identified alpha connectivity predicts sedation susceptibility. Purdon showed consistent population patterns with individual timing differences. HIRM validation should account for both population-level thresholds and individual variation.

## Recommendations for immediate HIRM validation

### Week 1: Cambridge dataset analysis

Download Chennu 2016 data immediately and begin pilot analysis. Test HIRM predictions:

1. **Sharp transition prediction:** Compute information-theoretic complexity measure (approximate Shannon entropy, Lempel-Ziv complexity, or permutation entropy) across the four conditions. Calculate ΔC/Δt between baseline-to-mild and mild-to-moderate transitions. Hypothesis: Should observe > 1 bit/sec changes.

2. **Critical threshold identification:** If drowsy subjects (n=7) show LOC signatures while responsive subjects (n=13) don't at moderate sedation, test if complexity C ~7.5-9.0 bits separates groups.

3. **Critical slowing:** Compute autocorrelation functions in alpha band approaching moderate sedation. Hypothesis: 1.5x increase in autocorrelation time near transition for drowsy subjects.

4. **Frequency-domain signatures:** Replicate known findings (frontal alpha emergence, slow-delta increase) as validation before novel analyses.

**Timeline:** Initial results possible within 1-2 weeks using standard EEGLAB/MNE-Python pipelines.

### Week 2-4: Pursue Purdon dataset

Simultaneously contact MGH Anesthesia for Purdon 2013 data access. Use 2-3 week wait time to refine analysis pipeline on Chennu data and prepare analysis scripts for 64-channel dataset.

**Email:** Patrick Purdon (ppurdon@mgh.harvard.edu, verify on MGH website) and reference DOI 10.1073/pnas.1221180110. Use Template 1 above.

**If successful:** Purdon's gradual induction provides ideal test case. Sliding window analysis (30-second windows) across 2-hour recording enables fine-grained ΔC/Δt calculation. Test if complexity measure shows hysteresis (higher threshold at emergence than induction).

### Month 2: Large-scale validation

Download VitalDB after pipeline validation on high-quality datasets. Despite LOC/ROC limitations, test if population-level patterns match predictions:

- Do BIS threshold crossings correlate with predicted complexity changes?
- Does propofol versus sevoflurane show agent-specific thresholds?
- Do emergence patterns show hysteresis even with imprecise timing?

Use VitalDB's massive scale (5,566 cases) for robustness testing and outlier identification.

### Month 3: Multi-agent cross-validation

Contact TU München (Kreuzer group) and Michigan (Mashour group) for multi-agent datasets. If HIRM predictions hold for propofol and sevoflurane (VitalDB), test whether isoflurane (Michigan) and mixed-agent protocols (TU München) show universal thresholds or agent-specific patterns.

**Strategic value:** Universal thresholds across agents would support HIRM as fundamental consciousness mechanism. Agent-specific thresholds would indicate pharmacology modulates transition rather than determining it.

### Alternative if contact attempts fail

PhysioNet multitaper dataset (n=54) provides immediate restricted access. While frequency-domain only, test spectral versions of HIRM predictions:

- Spectral entropy calculations from 0-50 Hz power
- Alpha/delta ratio evolution as consciousness proxy
- Wideband versus narrowband information content

Submit parallel contact requests to all author groups to maximize probability of access within 2-month timeframe.

## Estimated data acquisition timeline

**Immediate (Day 1):** Cambridge Propofol Study, VitalDB, Zenodo ML dataset – start analysis immediately

**Week 1-2:** PhysioNet multitaper (after DUA), Harvard EEG DB (after credentialing) – credentialed access

**Week 2-4:** Purdon 2013, Michigan ReCCognition – reasonable request with established sharing culture

**Month 2-3:** Murphy 2011 Wisconsin, TU München multi-agent – contact required, success probability moderate

**Month 3-6:** Specialized datasets from literature search – longer contact chains, lower priority

**Contingency:** If high-priority contacts (Purdon, Michigan) don't respond within 4 weeks, prioritize PhysioNet multitaper and VitalDB large-scale analyses. Three datasets (Cambridge, VitalDB, PhysioNet) are definitely accessible within 2 weeks.

## Conclusion and strategic recommendations

The field offers sufficient data to begin comprehensive HIRM validation immediately. The Cambridge dataset provides publication-quality starting point with full documentation and proven reusability. VitalDB enables large-scale robustness testing despite temporal limitations. Purdon and Michigan datasets, while requiring contact, have high access probability given the open science culture of consciousness research groups.

**Key success factors:**

1. **Start immediately** with Cambridge data to validate analytical pipeline and generate preliminary results
2. **Parallel contact strategy:** Email all data request targets simultaneously to maximize response rate
3. **Flexible methodology:** Adapt analyses to dataset constraints (e.g., frequency-domain methods for PhysioNet spectra)
4. **Cross-validation emphasis:** Test predictions across multiple datasets to establish robustness

**Critical insight:** The absence of anesthesia EEG on OpenNeuro, despite its prominence for neuroimaging, highlights that consciousness researchers primarily use institutional repositories and direct sharing. Cambridge's exceptional data deposit sets the standard the field should follow.

**Most viable rapid validation path:** Cambridge (immediate) → Purdon (2-4 weeks) → VitalDB large-scale (parallel) → Michigan multi-agent (6-8 weeks). This sequence provides gradual sedation, rapid induction, real-world surgical data, and cross-agent validation within 2-3 months.

The research community has generated the necessary data. Access barriers are moderate and surmountable through standard contact protocols. Begin analysis immediately while pursuing additional datasets in parallel.