# Groundwater modelling: geospatial preparation

Selected research notebooks from Badrinath Padmanabhan's groundwater modelling work at IIT Delhi.

This initial release covers representative-well selection and groundwater development feature integration at micro-watershed scale. It is a source snapshot of preparation stages, **not** a complete trained groundwater prediction system.

## Start here

`prepare_wells.py` extracts the useful well-selection stage from the exploratory mapping notebook into a runnable workflow:

```bash
python -m pip install -r requirements.txt
python prepare_wells.py --demo --output outputs/demo
```

The demo creates artificial well points and two rectangular watersheds. It demonstrates containment, continuity-based selection and unmatched boundary points. It uses no actual well locations or research data.

## Run with authorised geospatial data

```bash
python prepare_wells.py --wells data/wells.geojson \
  --watersheds data/watersheds.geojson --output outputs/well_mapping
```

Wells require unique `station_id` values, point geometries and a nonnegative integer `consecutive_non_nan_pairs` field calculated by the upstream observation-cleaning stage. Watersheds require unique `mws_id` values and polygon geometries. Both files must have a known CRS. The workflow reprojects well points to the watershed CRS; it never guesses or overwrites missing CRS metadata.

The workflow uses `within`, so points on polygon boundaries remain unmatched. Wells inside overlapping polygons trigger an error rather than an arbitrary assignment. It selects the highest continuity count within each watershed, breaking ties by station ID. Outputs are representative well points, unmatched well points and a summary. GeoJSON outputs use WGS84 longitude/latitude. No hardcoded geographic region, random sampling or trained model is involved.

This is a new portable refactor of the existing mapping stage, not a reconstruction of missing groundwater prediction code. The original exploratory notebooks are retained below for provenance and feature-integration context. Their study-specific filters and intermediate schemas differ from the explicit CLI contract.

## Included notebooks

| Notebook                                  | Purpose                                                                                                                                                |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `mapping_wells_with_microwatershed.ipynb` | Inspect geometries, associate monitoring wells with containing micro-watersheds and select representative wells using available observation continuity |
| `soge_data_adding_shallow.ipynb`          | Join groundwater assessment blocks to micro-watersheds and derive annual development-percentage features from assessment years                         |

The broader project also includes well cleaning, aquifer integration, terrain features and regression experiments. Those stages have not been included in this reviewed release. No datasets, coordinates of individual wells, generated maps, notebook outputs or trained models are distributed.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

Each notebook begins with portable path configuration. Inputs default to `data/` and generated files go to `outputs/` at the repository root. Set `RESEARCH_DATA_DIR` and `RESEARCH_OUTPUT_DIR` to override these locations.

Supply authorised copies of the following inputs:

| Notebook            | Required files                                                                                                                                      |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Well mapping        | `micro_watershed_gdf.pickle`, `cgwb_from_2001_preprocessed_data.pickle`                                                                             |
| Feature integration | `gwra2011.geojson`, `gwra2013.geojson`, `gwra2017.geojson`, `gwra2020.geojson`, `shallow_aquifers_csv_export.csv`, `Indian_states_boundary.geojson` |

The source assumes particular geometry, identifier and assessment fields, including micro-watershed IDs and `sgw_dev_pe`. Inspect those schemas and coordinate reference systems before running. Only load trusted pickle files. Historical geospatial pickles may require their original library versions.

## Research limits

These notebooks retain exploratory plotting and intermediate calculations. They require manual review rather than an unattended “Run all” workflow. Geographic filters, random samples, one-block-per-watershed choices, missing matches and overlapping geometries must be checked against the intended study region.

Interpolated or extrapolated annual features are derived values, not measurements for those years. The notebook's assumptions must be evaluated before using them in a model. This release does not establish prediction accuracy, causal effects or suitability for water-management decisions.

## Provenance and checks

The notebooks come from the existing research Drive project. Publication cleanup removed outputs, execution metadata, Colab mounting and package-install cells, and replaced private Drive paths. A stale intermediate reload was omitted so that the earlier join result remains available in memory. Scientific calculations and historical exploratory choices were otherwise retained.

Notebook structure, code-cell syntax and the release file allowlist have been checked. No original-data workflow, model training or geospatial benchmark was rerun. Full reproducibility is not claimed.

This is part of collaborative research, not a claim of sole ownership of the underlying data or wider project. No project-wide licence has been added. Obtain source data through its authorised providers and respect its redistribution terms.
