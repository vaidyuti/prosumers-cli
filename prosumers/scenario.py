from dataclasses import dataclass
import yaml
import csv

TimeSeriesProfile = list[float]


@dataclass
class PeerGeneration:
    _path: str
    category: str
    profile: TimeSeriesProfile


@dataclass
class PeerStorage:
    _path: str
    category: str
    total_energy: float
    usable_energy: float
    max_charge: float
    max_grid_charge: float
    max_discharge: float
    round_trip_efficiency: float


@dataclass
class Peer:
    id: str
    location: tuple[float, float]
    generations: list[PeerGeneration]
    consumptions: list[PeerGeneration]
    storage: list[PeerStorage]


@dataclass
class Scenario:
    _path: str
    version: str
    peers: list[Peer]


def read_storage(path: str):
    with open(path, "r") as stream:
        source = yaml.safe_load(stream)
    return PeerStorage(path, **source)


def parse_generation(source: dict):
    with open(source["profile"], "r") as stream:
        csv_reader = csv.reader(stream)
        profile = list(map(float, [r for r in csv_reader][0]))
    return PeerGeneration(
        source["profile"],
        category=source["category"],
        profile=profile,
    )


def parse_peer(source: dict):
    return Peer(
        id=source["id"],
        location=tuple(map(lambda x: float(x.strip()), source["location"].split(","))),
        generations=list(map(parse_generation, source.get("generations", []))),
        consumptions=list(map(parse_generation, source.get("consumptions", []))),
        storage=list(map(read_storage, source.get("storage", []))),
    )


def read_scenario(path: str):
    with open(path, "r") as stream:
        source = yaml.safe_load(stream)
    return Scenario(
        path,
        version=source.get("version", "unknown"),
        peers=list(map(parse_peer, source["peers"])),
    )
