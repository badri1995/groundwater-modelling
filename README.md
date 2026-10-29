# CGWB groundwater modelling

Research source from Badrinath Padmanabhan's groundwater work at IIT Delhi, covering monitoring-well observations, aquifer and terrain integration, and deep/shallow groundwater-depth modelling.

The expanded release contains **17 distinct notebooks**, not just the two preparation examples in the first publication. It includes the original deep and shallow five-year modelling notebooks recovered from Colab, earlier regression work, the infiltration helper, and the code-bearing stages of the main Drive project.

## Read the project in order

Start with the [workflow and source coverage map](WORKFLOW.md). It links each notebook to its stage and explains the historical folder names, dependencies and known limitations.

| Area                                 | Included work                                                                                                                                               |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Observations and spatial preparation | Ground-truth cleaning, continuity, representative wells, micro-watershed/aquifer joins and thresholds                                                       |
| Covariates                           | Stream order, terrain, calculated water depth, ABY observations, SOGE assessments, cropping, catchment/connectivity and infiltration inputs                 |
| Deep and shallow modelling           | Five-year/lagged features, trend analysis, grouped splits, OLS/WLS and machine-learning comparisons, threshold classification and cross-aquifer experiments |
| Earlier experiments                  | Combined ground-truth archive, seasonal training-table models and the earlier deep-aquifer preprocessing notebook                                           |

These are authentic exploratory source notebooks. They retain alternative branches, repeated definitions and study-specific assumptions. Their presence is not a claim that every notebook runs from top to bottom or that scientific results have been reproduced.

## Small runnable entry point

`prepare_wells.py` is the earlier portable refactor of the representative-well selection stage. It is intentionally smaller than the research archive.

```bash
python -m pip install -r requirements.txt
python prepare_wells.py --demo --output outputs/demo
```

The demo uses artificial points and two rectangular watersheds. It tests geometry handling and selection logic, not groundwater prediction.

For authorised data:

```bash
python prepare_wells.py --wells data/wells.geojson \
  --watersheds data/watersheds.geojson --output outputs/well_mapping
```

Wells need unique `station_id`, point geometries and nonnegative integer `consecutive_non_nan_pairs`. Watersheds need unique `mws_id` and polygon geometries. Both inputs need a known CRS. The workflow reprojects well points, uses strict `within` containment and rejects ambiguous overlapping-polygon assignments. Boundary points remain unmatched. Selection favours the highest continuity count, then station ID for ties. GeoJSON exports use WGS84.

## Research notebook setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-research.txt
export CGWB_WORKSPACE=/absolute/path/to/private/cgwb_workspace
jupyter lab
```

`requirements-research.txt` is an inventory of the broader source dependencies, not a recreated historical lockfile. Some older APIs and geospatial pickles may require the original environment. Install only the dependencies needed for the branch being inspected.

Newly recovered notebooks live in `notebooks/project/` and use `CGWB_WORKSPACE`. Existing well-mapping and shallow-SOGE adaptations remain directly under `notebooks/` with their earlier `RESEARCH_DATA_DIR` / `RESEARCH_OUTPUT_DIR` configuration. [WORKFLOW.md](WORKFLOW.md) explains both layouts and the older stage numbers still referenced by the source. Supply authorised inputs and create the relevant output folders before execution. Only deserialize trusted pickle/joblib files.

## Research limits

Spatial and temporal dependence, feature selection, inner validation and preprocessing scope require a fresh audit before reporting accuracy. Some branches use grouped outer splits without consistently grouped inner validation. Several metrics include MAPE, which is problematic for near-zero depth changes. Development-percentage interpolation and trend-derived features are estimates, not observations.

The archive includes model-fitting code but no trained weights, reproduced benchmark or deployment claim. It is not validated for operational water-management decisions.

## Provenance and privacy

The originals remain unchanged in Drive. Publication removes notebook outputs, execution metadata, installation/mount commands and private paths. Two obvious syntax defects were mechanically repaired as documented in the workflow. The previous small CLI and portable notebook adaptations are retained. [source_manifest.json](source_manifest.json) records original filenames, private-source hashes and cleanup notes.

Notebook structure, code-cell syntax and the code-only release boundary are checked. The portable synthetic demo is checked separately; original-data training and full geospatial workflows have not been rerun.

No datasets, individual well locations, generated maps, medical data, credentials or model weights are distributed. This is collaborative research source, not a claim of sole ownership of the underlying data or wider project. No project-wide licence is added.
