# Groundwater modelling: geospatial preparation

Selected research notebooks from Badrinath Padmanabhan's groundwater modelling work at IIT Delhi.

This initial release covers representative-well selection and groundwater development feature integration at micro-watershed scale. It is a source snapshot of preparation stages, **not** a complete trained groundwater prediction system.

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
