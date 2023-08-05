"""
Poly Bridge 2-related enumerators.
"""

import enum


class BridgeMaterialType(enum.Enum):
    """
    Enum for the different types of materials that can be used in a bridge.

    .. note::
        Bungee rope is not actually used in the game, and has no texture or physics.
    """
    INVALID = 0
    ROAD = 1
    REINFORCED_ROAD = 2
    WOOD = 3
    STEEL = 4
    HYDRAULICS = 5
    ROPE = 6
    CABLE = 7
    BUNGEE_ROPE = 8
    SPRING = 9


class SplitJointPart(enum.Enum):
    """
    Enum for the different parts of a split joint.

    .. note::
        :class:`SplitJointPart.C` does not have an effect if the joint is not a 3-way split joint.
    """
    A = 0
    B = 1
    C = 2


class SplitJointState(enum.Enum):
    ALL_SPLIT = 0
    NONE_SPLIT = 1
    A_SPLIT_ONLY = 2
    B_SPLIT_ONLY = 3
    C_SPLIT_ONLY = 4


class StrengthMethod(enum.Enum):
    Acceleration = 0
    MaxSlope = 1
    TorquePerWheel = 2


class TerrainIslandType(enum.Enum):
    Bookend = 0
    Middle = 1


class SplineType(enum.Enum):
    Hermite = 0
    BSpline = 1
    Bezier = 2
    Linear = 3


class Theme(enum.Enum):
    PineMountains = "PineMountains"
    GlowingGorge = "Volcano"
    TranquilOasis = "Savanna"
    SanguineGulch = "Western"
    SerenityValley = "ZenGardens"
    Steamtown = "Steampunk"


class VehicleType(enum.Enum):
    Vespa = "Vespa"
    Chopper = "Chopper"
    CompactCar = "CompactCar"
    DuneBuggy = "DuneBuggy"
    SportsCar = "SportsCar"
    Taxi = "Taxi"
    ModelT = "ModelT"
    PickupTruck = "PickupTruck"
    Limo = "Limo"
    Van = "Van"
    TowTruck = "TowTruck"
    SteamCar = "SteamCar"
    Truck = "Truck"
    MonsterTruck = "MonsterTruck"
    Ambulance = "Ambulance"
    SchoolBus = "SchoolBus"
    FireTruck = "FireTruck"
    Bulldozer = "Bulldozer"
    FlatBedTruck = "TruckWithFlatbed"
    DumpTruck = "DumpTruck"
    ArticulatedBus = "ArticulatedBus"
    TankerTruck = "TruckWithLiquid"
    ContainerTruck = "TruckWithContainer"


DefaultVehicleSettings = {
    "Vespa": {
        "acceleration": 1.0,
        "braking_force_multiplier": 4.0,
        "horsepower": 3.0,
        "max_slope": 0.0,
        "mass": 6.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "Chopper": {
        "acceleration": 2.0,
        "braking_force_multiplier": 1.5,
        "horsepower": 4.0,
        "max_slope": 0.0,
        "mass": 8.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 6.0,
    },
    "CompactCar": {
        "acceleration": 1.0,
        "braking_force_multiplier": 2.5,
        "horsepower": 5.0,
        "max_slope": 0.0,
        "mass": 14.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 5.0,
    },
    "DuneBuggy": {
        "acceleration": 10.0,
        "braking_force_multiplier": 2.5,
        "horsepower": 10.0,
        "max_slope": 0.0,
        "mass": 14.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 0.5,
        "target_speed": 15.0,
    },
    "SportsCar": {
        "acceleration": 4.0,
        "braking_force_multiplier": 4.0,
        "horsepower": 7.0,
        "max_slope": 0.0,
        "mass": 16.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 12.0,
    },
    "Taxi": {
        "acceleration": 2.0,
        "braking_force_multiplier": 1.5,
        "horsepower": 5.0,
        "max_slope": 0.0,
        "mass": 16.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 5.0,
    },
    "ModelT": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 4.0,
        "max_slope": 0.0,
        "mass": 18.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "PickupTruck": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 8.5,
        "max_slope": 0.0,
        "mass": 20.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "Limo": {
        "acceleration": 1.0,
        "braking_force_multiplier": 1.5,
        "horsepower": 5.0,
        "max_slope": 0.0,
        "mass": 20.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 2.5,
    },
    "Van": {
        "acceleration": 1.5,
        "braking_force_multiplier": 1.5,
        "horsepower": 5.0,
        "max_slope": 0.0,
        "mass": 24.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 4.0,
    },
    "TowTruck": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 9.0,
        "max_slope": 0.0,
        "mass": 26.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.5,
    },
    "SteamCar": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 5.0,
        "max_slope": 0.0,
        "mass": 26.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 4.0,
    },
    "Truck": {
        "acceleration": 1.0,
        "braking_force_multiplier": 1.5,
        "horsepower": 12.0,
        "max_slope": 0.0,
        "mass": 28.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "MonsterTruck": {
        "acceleration": 1.0,
        "braking_force_multiplier": 1.5,
        "horsepower": 20.0,
        "max_slope": 0.0,
        "mass": 32.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "Ambulance": {
        "acceleration": 1.5,
        "braking_force_multiplier": 1.5,
        "horsepower": 4.5,
        "max_slope": 0.0,
        "mass": 36.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 5.0,
    },
    "SchoolBus": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 6.0,
        "max_slope": 0.0,
        "mass": 40.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "FireTruck": {
        "acceleration": 1.5,
        "braking_force_multiplier": 1.5,
        "horsepower": 5.0,
        "max_slope": 0.0,
        "mass": 40.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 5.0,
    },
    "Bulldozer": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 30.0,
        "max_slope": 0.0,
        "mass": 44.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 1.5,
    },
    "TruckWithFlatbed": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 12.0,
        "max_slope": 0.0,
        "mass": 56.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "DumpTruck": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 15.0,
        "max_slope": 0.0,
        "mass": 56.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 2.0,
    },
    "ArticulatedBus": {
        "acceleration": 0.8,
        "braking_force_multiplier": 1.5,
        "horsepower": 6.0,
        "max_slope": 0.0,
        "mass": 56.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "TruckWithLiquid": {
        "acceleration": 0.6,
        "braking_force_multiplier": 1.5,
        "horsepower": 12.0,
        "max_slope": 0.0,
        "mass": 84.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    },
    "TruckWithContainer": {
        "acceleration": 0.6,
        "braking_force_multiplier": 1.5,
        "horsepower": 12.0,
        "max_slope": 0.0,
        "mass": 84.0,
        "rotation_degrees": 0.0,
        "shocks_multiplier": 1.0,
        "target_speed": 3.0,
    }
}


class BinaryEntryType(enum.Enum):
    Invalid = 0
    NamedStartOfReferenceNode = 1
    UnnamedStartOfReferenceNode = 2
    NamedStartOfStructNode = 3
    UnnamedStartOfStructNode = 4
    EndOfNode = 5
    StartOfArray = 6
    EndOfArray = 7
    PrimitiveArray = 8
    NamedInternalReference = 9
    UnnamedInternalReference = 10
    NamedExternalReferenceByIndex = 11
    UnnamedExternalReferenceByIndex = 12
    NamedExternalReferenceByGuid = 13
    UnnamedExternalReferenceByGuid = 14
    NamedSByte = 15
    UnnamedSByte = 16
    NamedByte = 17
    UnnamedByte = 18
    NamedShort = 19
    UnnamedShort = 20
    NamedUShort = 21
    UnnamedUShort = 22
    NamedInt = 23
    UnnamedInt = 24
    NamedUInt = 25
    UnnamedUInt = 26
    NamedLong = 27
    UnnamedLong = 28
    NamedULong = 29
    UnnamedULong = 30
    NamedFloat = 31
    UnnamedFloat = 32
    NamedDouble = 33
    UnnamedDouble = 34
    NamedDecimal = 35
    UnnamedDecimal = 36
    NamedChar = 37
    UnnamedChar = 38
    NamedString = 39
    UnnamedString = 40
    NamedGuid = 41
    UnnamedGuid = 42
    NamedBoolean = 43
    UnnamedBoolean = 44
    NamedNull = 45
    UnnamedNull = 46
    TypeName = 47
    TypeID = 48
    EndOfStream = 49
    NamedExternalReferenceByString = 50
    UnnamedExternalReferenceByString = 51


PB1ToPB2Vehicles = [
    VehicleType.CompactCar,
    VehicleType.Limo,
    VehicleType.Van,
    VehicleType.SchoolBus,
    VehicleType.MonsterTruck,
    VehicleType.DumpTruck,
    VehicleType.Vespa,
    VehicleType.ModelT,
    VehicleType.CompactCar,
    VehicleType.ModelT,
    VehicleType.FlatBedTruck,
    VehicleType.ArticulatedBus,
    VehicleType.Taxi,
    VehicleType.Taxi,
    VehicleType.SportsCar,
    VehicleType.PickupTruck,
    VehicleType.CompactCar,
    VehicleType.TowTruck,
    VehicleType.Chopper,
    VehicleType.Chopper,
    VehicleType.Van
]

PB1ToPB2Ships = [
    "Steamboat",
    "Hydrofoil",
    "CruiseShip",
    "SpeedBoat",
    "CruiseShip",
    "Sailboat"
]

PB1ToPB2Planes = [
    "BiPlane",
    "ShowJet",
    "Blimp"
]

CURRENT_LAYOUT_VERSION = 26
CURRENT_BRIDGE_VERSION = 11
CURRENT_SLOT_VERSION = 3
CURRENT_PHYSICS_VERSION = 1


CUSTOM_SHAPE_DEFAULT_COLOR = (193, 160, 159, 1)
CUSTOM_SHAPE_DEFAULT_MASS = 40.0
CUSTOM_SHAPE_DEFAULT_BOUNCINESS = 0.5

PTF_STRING_SEPARATOR = "\u058D"

THEME_STUB_KEYS = ["PineMountains", "Volcano", "Savanna", "Western", "ZenGardens", "Steampunk"]
