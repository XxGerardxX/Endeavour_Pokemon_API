from dataclasses import dataclass, field
from typing import List,Optional




@dataclass
class BerryFlavor:
    spicy: int = 0
    dry: int = 0
    sweet: int = 0
    bitter: int = 0
    sour: int = 0


@dataclass
class Berry:
    flavors: BerryFlavor
    id: int = 0
    name: str = ""
    growth_time: int = 0

@dataclass
class PokeStats:
    hp: int = 0
    hp_effort: int = 0
    attack: int = 0
    attack_effort: int = 0
    defense: int = 0
    defense_effort: int = 0
    speed: int = 0
    speed_effort: int = 0
    special_attack: int = 0
    special_attack_effort: int = 0
    special_defense: int = 0
    special_defense_effort: int = 0


@dataclass
class Pokemon:
    stats: Optional[PokeStats]
    name: str = ""
    poke_id: int = 0
    id: int = 0
    base_experience: int = 0
    weight: float = 0.0
    height: float = 0.0
    types: List[str] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    hidden_abilities: List[str] = field(default_factory=list)
    natural_moves: List[str] =field(default_factory=list)


