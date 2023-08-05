"""
Data structures of PB2 objects.
"""
from __future__ import annotations

from dataclasses import dataclass
from pylybridge import constants


@dataclass
class Vec3:
    """A 3-dimensional vector."""
    x: float
    y: float
    z: float


@dataclass
class Vec2:
    """A 2-dimensional vector."""
    x: float
    y: float


@dataclass
class Quaternion:
    """A quaternion."""
    x: float
    y: float
    z: float
    w: float


@dataclass
class Color:
    """A RGBA color."""
    r: float
    g: float
    b: float
    a: float

    def to_tuple(self) -> tuple[float, float, float, float]:
        """Converts the color to a tuple of (r, g, b, a)."""
        return self.r, self.g, self.b, self.a


@dataclass
class BridgeJoint:
    """A bridge joint."""
    pos: Vec3
    is_anchor: bool
    is_split: bool
    guid: str


Anchor = BridgeJoint  # alias for BridgeJoint, for convenience


@dataclass
class BridgeEdge:
    """A bridge edge (what connects two joints)."""
    material_type: constants.BridgeMaterialType
    node_a_guid: str
    node_b_guid: str
    joint_a_part: constants.SplitJointPart
    joint_b_part: constants.SplitJointPart
    guid: str


@dataclass
class BridgeSpring:
    """A spring."""
    normalized_value: float
    node_a_guid: str
    node_b_guid: str
    guid: str


@dataclass
class BridgeSplitJoint:
    """A split joint."""
    guid: str
    state: constants.SplitJointState


@dataclass
class Piston:
    """A piston (hydraulic)."""
    normalized_value: float
    node_a_guid: str
    node_b_guid: str
    guid: str


@dataclass
class HydraulicPhase:
    """A hydraulic phase."""
    time_delay: float
    guid: str


@dataclass
class ZAxisVehicle:
    """A zed-axis vehicle, e.g. a boat, plane, etc."""
    pos: Vec2
    prefab_name: str
    guid: str
    time_delay: float
    speed: float
    rot: Quaternion
    rotation_degrees: float


@dataclass
class Vehicle:
    """A vehicle."""
    display_name: str
    pos: Vec2
    rot: Quaternion
    prefab_name: str
    target_speed: float
    mass: float
    braking_force_multiplier: float
    strength_method: constants.StrengthMethod
    horsepower: float
    max_slope: float
    acceleration: float
    shocks_multiplier: float
    rotation_degrees: float
    time_delay: float
    idle_on_downhill: bool
    flipped: bool
    ordered_checkpoints: bool
    guid: str
    checkpoint_guids: list[str]


@dataclass
class VehicleStopTrigger:
    """A stop trigger for a vehicle."""
    pos: Vec2
    rot: Quaternion
    height: float
    rotation_degrees: float
    flipped: bool
    prefab_name: str
    stop_vehicle_guid: str


@dataclass
class ThemeObject:
    """A theme object. These are deprecated and shouldn't be used."""
    pos: Vec2
    prefab_name: str
    unknown_1: bool


@dataclass
class EventUnit:
    """An event unit."""
    guid: str


@dataclass
class EventStage:
    """A stage in a timeline."""
    units: list[EventUnit]


@dataclass
class EventTimeline:
    """A timeline of events."""
    checkpoint_guid: str
    stages: list[EventStage]


@dataclass
class Checkpoint:
    """A checkpoint."""
    pos: Vec2
    prefab_name: str
    vehicle_guid: str
    vehicle_restart_phase_guid: str
    trigger_timeline: bool
    stop_vehicle: bool
    reverse_vehicle_on_restart: bool
    guid: str


@dataclass
class Platform:
    """A platform."""
    pos: Vec2
    width: float
    height: float
    flipped: bool
    solid: bool


@dataclass
class HydraulicsControllerPhase:
    """A hydraulic phase."""
    hydraulics_phase_guid: str
    piston_guids: list[str]
    bridge_split_joints: list[BridgeSplitJoint]
    disable_new_additions: bool


@dataclass
class TerrainIsland:
    """A terrain island (stretch)."""
    pos: Vec3
    prefab_name: str
    height_added: float
    right_edge_water_height: float
    terrain_island_type: constants.TerrainIslandType
    variant_index: int
    flipped: bool
    lock_position: bool


@dataclass
class Ramp:
    """A ramp."""
    pos: Vec2
    control_points: list[Vec2]
    height: float
    num_segments: int
    spline_type: constants.SplineType
    flipped_vertical: bool
    flipped_horizontal: bool
    hide_legs: bool
    flipped_legs: bool
    line_points: list[Vec2]


@dataclass
class VehicleRestartPhase:
    """A vehicle restart phase."""
    time_delay: float
    guid: str
    vehicle_guid: str


@dataclass
class FlyingObject:
    """A flying object (hot air balloon)."""
    pos: Vec3
    scale: Vec3
    prefab_name: str


@dataclass
class Rock:
    """A rock."""
    pos: Vec3
    scale: Vec3
    prefab_name: str
    flipped: bool


@dataclass
class WaterBlock:
    """A water block."""
    pos: Vec3
    width: float
    height: float
    lock_position: bool


@dataclass
class Bridge:
    """The bridge in a layout or save slot."""
    version: int
    joints: list[BridgeJoint]
    edges: list[BridgeEdge]
    springs: list[BridgeSpring]
    pistons: list[Piston]
    anchors: list[BridgeJoint]
    phases: list[HydraulicsControllerPhase]


@dataclass
class Budget:
    """The budget for a layout."""
    cash: int
    road: int
    wood: int
    steel: int
    hydraulics: int
    rope: int
    cable: int
    bungee_rope: int
    spring: int
    allow_wood: bool
    allow_steel: bool
    allow_hydraulics: bool
    allow_rope: bool
    allow_cable: bool
    allow_spring: bool
    allow_reinforced_road: bool


@dataclass
class Settings:
    """A layout's settings."""
    hydraulics_controller_enabled: bool
    unbreakable: bool


@dataclass
class CustomShape:
    """A custom shape."""
    pos: Vec3
    rot: Quaternion
    scale: Vec3
    flipped: bool
    dynamic: bool
    collides_with_road: bool
    collides_with_nodes: bool
    collides_with_split_nodes: bool
    rotation_degrees: float
    color: Color
    mass: float
    bounciness: float
    pin_motor_strength: float
    pin_target_velocity: float
    points_local_space: list[Vec2]
    static_pins: list[Vec3]
    dynamic_anchor_guids: list[str]


@dataclass
class Workshop:
    """The workshop metadata of a layout."""
    id: str
    leaderboard_id: str
    title: str
    description: str
    autoplay: bool
    tags: list[str]


@dataclass
class SupportPillar:
    """A support pillars. These do not seem to be used in-game."""
    pos: Vec3
    scale: Vec3
    prefab_name: str


@dataclass
class Pillar:
    """A pillar."""
    pos: Vec3
    height: float
    prefab_name: str


# PTF support
@dataclass
class Mod:
    """A PolyTechFramework mod."""
    name: str
    version: str
    settings: str


@dataclass
class ModSaveData:
    """The save data for a mod."""
    name: str
    version: str
    data: bytes


# Better Coloured Edges support
@dataclass
class ColoredEdge:
    """A colored edge (Better Coloured Edges mod)."""
    joint_a_guid: str
    joint_b_guid: str
    material_type: constants.BridgeMaterialType
    color: Color
