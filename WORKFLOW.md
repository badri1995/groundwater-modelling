# CGWB workflow and source coverage

This release covers the code-bearing stages of the groundwater Drive project, plus the deep and shallow modelling notebooks that were stored separately in Colab Notebooks. There are 17 distinct notebooks. A near-identical Colab copy of `creating_aquifer_wise_training_data.ipynb` differed only by a blank line and is not duplicated.

## Workflow index

| Stage                | Notebook                                                                                                     | Main work                                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Ground truth archive | [cleaning_ground_truth](notebooks/project/cleaning_ground_truth.ipynb)                                       | Earlier combined exploration of observation continuity, geospatial joins, aquifers and thresholds                                |
| 1                    | [analyzing_CGWB_raw_data](notebooks/project/analyzing_CGWB_raw_data.ipynb)                                   | Clean and inspect monitoring-well time series and continuity                                                                     |
| 2                    | [combining_aquifer_types_based_on_ACWADAM](notebooks/project/combining_aquifer_types_based_on_ACWADAM.ipynb) | Regroup aquifer categories                                                                                                       |
| 3                    | [mapping_wells_with_microwatershed](notebooks/mapping_wells_with_microwatershed.ipynb)                       | Spatially match wells and select a representative by continuity                                                                  |
| 4                    | [mapping_microwatershed_with_aquifer](notebooks/project/mapping_microwatershed_with_aquifer.ipynb)           | Associate micro-watersheds with aquifer information                                                                              |
| 5                    | [thresholding_mws_data_aquifer_wise](notebooks/project/thresholding_mws_data_aquifer_wise.ipynb)             | Inspect aquifer-specific observation thresholds                                                                                  |
| 6                    | [adding_stream_order_terrain_info](notebooks/project/adding_stream_order_terrain_info.ipynb)                 | Integrate stream-order, terrain and landform covariates                                                                          |
| 7                    | [extracting_mws_ids_aquifer_wise](notebooks/project/extracting_mws_ids_aquifer_wise.ipynb)                   | Export grouped watershed IDs                                                                                                     |
| 8                    | [preprocessing_calculated_data](notebooks/project/preprocessing_calculated_data.ipynb)                       | Reshape calculated water-depth inputs                                                                                            |
| 9                    | [creating_aquifer_wise_training_data](notebooks/project/creating_aquifer_wise_training_data.ipynb)           | Assemble seasonal training tables, grouped splits and regression comparisons                                                     |
| 10                   | [checking_ABY_data](notebooks/project/checking_ABY_data.ipynb)                                               | Examine Atal Bhujal observations, missingness and spatial associations                                                           |
| 11                   | [soge_data_adding](notebooks/project/soge_data_adding.ipynb)                                                 | Join development-percentage assessment features for deep aquifers                                                                |
| 12                   | [soge_data_adding_shallow](notebooks/soge_data_adding_shallow.ipynb)                                         | Corresponding shallow-aquifer assessment features                                                                                |
| 13                   | [preprocessing_deep_aquifers_five_years](notebooks/project/preprocessing_deep_aquifers_five_years.ipynb)     | Five-year/lagged covariates, trend analysis, grouped splits, regression/classification experiments and cross-aquifer comparisons |
| 14                   | [preprocessing_shallow_five_years](notebooks/project/preprocessing_shallow_five_years.ipynb)                 | Shallow-aquifer counterpart, model comparisons and evaluation using saved deep models                                            |
| Earlier deep variant | [Copy_of_preprocessing_deep_aquifers](notebooks/project/Copy_of_preprocessing_deep_aquifers.ipynb)           | Earlier annual deep-aquifer preprocessing and regression experiments                                                             |
| Infiltration helper  | [CONVERTING_AQUIFER_INFILTRATION_RATE](notebooks/project/CONVERTING_AQUIFER_INFILTRATION_RATE.ipynb)         | Parse and convert infiltration-rate fields for deep/shallow inputs                                                               |

The stage 13/14 code subfolders were empty in the reviewed Drive layout; their substantive notebooks were recovered from Colab Notebooks. Data-only folders and checkpoint folders are intentionally not published.

## Private input workspace

The newly recovered notebooks under `notebooks/project/` use `CGWB_WORKSPACE`, defaulting to `data/cgwb/` at the repository root. The setup cell changes the notebook's working directory into that private workspace so relative generated files stay outside the source tree. Paths preserve the historical internal folder structure, with trailing spaces in folder components removed. Create the required input and output directories before running a stage.

Some historical source paths use older stage numbers. These are intentionally not silently rewritten because input schemas and cached results can differ:

| Historical path in the notebook                                         | Current source-stage label                                  |
| ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| `13. Checking ABY data`                                                 | 10, ABY checks                                              |
| `20. SOGE new data`                                                     | 11, SOGE deep                                               |
| `21. Soge shallow`                                                      | 12, SOGE shallow                                            |
| `22. Training_deep_five_years`                                          | 13, deep modelling                                          |
| `23. Training_shallow_five_years`                                       | 14, shallow modelling                                       |
| `18. preprocessing_shallow_aquifers`, `19. preprocessing_deep_aquifers` | Earlier preprocessing inputs referenced by the later models |

Either reproduce the historical layout inside the private workspace or explicitly adjust the input paths after checking each file's schema. Several stages expect cached upstream outputs in a stage's `input/` directory. This is not an automated dependency graph. The original combined ground-truth notebook uses `00. CGWB Ground Truth/` within the workspace.

The two previously published notebooks retain their portable `RESEARCH_DATA_DIR` and `RESEARCH_OUTPUT_DIR` configuration. Stage 3 needs `micro_watershed_gdf.pickle` and `cgwb_from_2001_preprocessed_data.pickle`; stage 12 needs the assessment-year GeoJSONs, `shallow_aquifers_csv_export.csv` and a state boundary file. The small CLI uses its own explicit `--wells`, `--watersheds` and `--output` arguments.

Broader source dependencies include CGWB/ABY time series, watershed and aquifer geometries, terrain and stream-order exports, groundwater development assessments, cropping and infiltration covariates, connectivity and catchment data, calculated hydrological variables and GRACE-related inputs. None are bundled. Inspect the file reads in the selected notebook for the exact schema and subset it expects. Only load trusted pickle/joblib files.

## Model experiments and caveats

The recovered source includes OLS/WLS, Ridge/Lasso/ElasticNet, nearest-neighbour and support-vector regression, tree ensembles, MLP and XGBoost comparisons. The five-year notebooks also include trend estimators, feature-collinearity work, sign/threshold classification experiments and deep/shallow transfer checks. These are existing exploratory branches, not a newly selected production model.

Outer splits in several branches use watershed IDs, but not every inner cross-validation routine is group-aware. Audit grouping, temporal overlap, preprocessing fit scope and repeated feature/model selection before reporting generalisation. Some exploratory normalisation is performed on a whole supplied frame. MAPE is unstable near zero change in water depth and should not be treated as a sufficient error summary. Interpolated development assessments and fitted trends are derived estimates, not new observations.

Duplicate definitions, manually selected covariates, notebook-state dependencies and saved-model requirements remain. Choose a coherent branch and rebuild its inputs before execution. Do not Run All through every exploratory alternative. No research model was trained or original scientific metric reproduced during this publication.

## Publication changes

Outputs, execution metadata, private Drive prefixes and environment-install/mount commands were removed. The ground-truth archive had a stray slash before one import; it was corrected. One accidentally indented top-level plotting loop in each five-year notebook was dedented. These mechanical repairs do not validate the experimental design.

The two existing portable adaptations and `prepare_wells.py` are retained. In the earlier well-mapping adaptation, a stale intermediate reload was already omitted. Source filenames, hashes and cell-level cleanup notes are recorded in [source_manifest.json](source_manifest.json). The originals remain unchanged in Drive.
