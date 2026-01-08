from dataclasses import dataclass

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