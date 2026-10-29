"""Associate wells with watersheds and select by observation continuity."""

import argparse
import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point, box


def select_representative_wells(wells, watersheds):
    well_columns = {"station_id", "consecutive_non_nan_pairs"}
    if not well_columns.issubset(wells.columns) or "mws_id" not in watersheds.columns:
        raise ValueError("Wells need station_id and consecutive_non_nan_pairs; watersheds need mws_id.")
    if wells.empty or watersheds.empty:
        raise ValueError("Both geometry tables must be nonempty.")
    for name, frame, identifier, geometry_types in (
        ("wells", wells, "station_id", {"Point"}),
        ("watersheds", watersheds, "mws_id", {"Polygon", "MultiPolygon"}),
    ):
        if frame.crs is None:
            raise ValueError(f"{name} has no CRS; establish it from the data source before running.")
        if frame[identifier].isna().any():
            raise ValueError(f"{name} identifiers must not be missing.")
        identifiers = frame[identifier].astype(str).str.strip()
        if identifiers.eq("").any() or identifiers.duplicated().any():
            raise ValueError(f"{name} identifiers must be nonempty and unique.")
        if frame.geometry.isna().any() or frame.geometry.is_empty.any() or not frame.geometry.is_valid.all():
            raise ValueError(f"{name} contains missing, empty or invalid geometries.")
        if not frame.geometry.geom_type.isin(geometry_types).all():
            raise ValueError(f"Unexpected geometry type in {name}.")
    continuity = pd.to_numeric(wells["consecutive_non_nan_pairs"], errors="raise")
    if not np.isfinite(continuity).all() or (continuity < 0).any() or (continuity % 1 != 0).any():
        raise ValueError("Continuity counts must be finite nonnegative integers.")
    points = gpd.GeoDataFrame({
        "station_id": wells["station_id"].astype(str).str.strip().to_numpy(),
        "consecutive_non_nan_pairs": continuity.to_numpy(),
    }, geometry=list(wells.geometry), crs=wells.crs).to_crs(watersheds.crs)
    areas = gpd.GeoDataFrame({"mws_id": watersheds["mws_id"].astype(str).str.strip().to_numpy()}, geometry=list(watersheds.geometry), crs=watersheds.crs)
    joined = gpd.sjoin(points, areas, how="left", predicate="within")
    if joined["station_id"].duplicated().any():
        raise ValueError("A well lies inside multiple watersheds; resolve overlapping boundaries first.")
    unmatched = joined[joined["mws_id"].isna()][["station_id", "geometry"]].copy()
    matched = joined[joined["mws_id"].notna()].copy()
    selected = matched.sort_values(
        ["mws_id", "consecutive_non_nan_pairs", "station_id"],
        ascending=[True, False, True], kind="stable",
    ).drop_duplicates("mws_id")
    selected = selected[["mws_id", "station_id", "consecutive_non_nan_pairs", "geometry"]].reset_index(drop=True)
    summary = {
        "wells": len(wells), "watersheds": len(watersheds),
        "matched_wells": len(matched), "unmatched_wells": len(unmatched),
        "represented_watersheds": len(selected),
        "predicate": "within; boundary points are unmatched",
        "tie_break": "lexicographically smallest station_id",
        "output_geometry": "representative well point, not watershed polygon",
    }
    return selected, unmatched, summary


def synthetic_data():
    watersheds = gpd.GeoDataFrame({"mws_id": ["demo_a", "demo_b"]}, geometry=[box(0, 0, 10, 10), box(20, 0, 30, 10)], crs="EPSG:3857")
    wells = gpd.GeoDataFrame({
        "station_id": ["demo_1", "demo_2", "demo_3", "demo_boundary"],
        "consecutive_non_nan_pairs": [2, 5, 4, 9],
    }, geometry=[Point(2, 2), Point(3, 3), Point(22, 2), Point(0, 5)], crs=watersheds.crs)
    return wells, watersheds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--wells", type=Path)
    parser.add_argument("--watersheds", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs/well_mapping"))
    args = parser.parse_args()
    if args.demo:
        if args.wells or args.watersheds:
            parser.error("--demo cannot be combined with input files")
        wells, watersheds = synthetic_data()
    else:
        if not args.wells or not args.watersheds:
            parser.error("supply --wells and --watersheds, or use --demo")
        wells, watersheds = gpd.read_file(args.wells), gpd.read_file(args.watersheds)
    selected, unmatched, summary = select_representative_wells(wells, watersheds)
    summary["mode"] = "synthetic geometry demonstration, not research results" if args.demo else "user supplied data"
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, frame in (("representative_wells.geojson", selected), ("unmatched_wells.geojson", unmatched)):
        (args.output / filename).write_text(frame.to_crs("EPSG:4326").to_json(drop_id=True) + "\n")
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
