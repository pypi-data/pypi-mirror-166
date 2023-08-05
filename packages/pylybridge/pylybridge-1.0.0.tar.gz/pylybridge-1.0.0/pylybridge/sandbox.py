"""
pylybridge.sandbox - Edit PB2 sandbox layouts in Python
"""
from __future__ import annotations

import json
import random
import uuid
from typing import Union
from os.path import exists
import io
import logging
import pylybridge.constants as constants
import pylybridge.datatypes as datatypes
import struct


class Layout:
    """
    An object representing a layout.
    """
    def __init__(
            self,
            data: Union[str, bytes, io.IOBase, io.BufferedIOBase, None] = None,
            check_width_height: bool = True,
            deserialize_on_init: bool = True,
            is_pb1: bool = False
    ):
        """
        Initialize a new Layout object.

        :param data: The path to the layout file, or binary data.
                     If you want to use bytes, you can use :class:`io.BytesIO` or simply provide bytes.
        :param check_width_height: Whether to check the width and height of the layout on deserialization or not.
        :param deserialize_on_init: If the deserializer should try to deserialize the layout on initialization.
        :param is_pb1: If the layout is a Poly Bridge 1 layout. This will be auto-detected at
                       initialization if not defined by user.

        :raises ValueError: If the path is not a valid file.
        """

        self.path: Union[str, None] = None

        if isinstance(data, bytes):
            self._file = io.BytesIO(data)
            self.path = None
        elif isinstance(data, str):
            self._file = open(data, "rb") if data is not None else None
            self.path: str = data if data is not None else ""
        elif isinstance(data, io.IOBase):
            self._file = data
            self.path = None
        else:
            self._file = None
            self.path = None

        if isinstance(data, str) and not exists(data):
            raise FileNotFoundError("File " + data + "does not exist.")

        self.output_stream: io.BytesIO = io.BytesIO()
        self.version: int = constants.CURRENT_LAYOUT_VERSION
        self.stub_key: str = random.choice(constants.THEME_STUB_KEYS)
        # default anchors, guids are random
        self.anchors: list[datatypes.BridgeJoint] = [
            datatypes.BridgeJoint(
                pos=datatypes.Vec3(x=0.0, y=5.0, z=0.0),
                is_anchor=True,
                is_split=False,
                guid='dd84bd58-a5f2-4461-80c1-a07e91a67524'
            ),
            datatypes.BridgeJoint(
                pos=datatypes.Vec3(x=12.0, y=5.0, z=0.0),
                is_anchor=True,
                is_split=False,
                guid='dc72e01d-5335-4716-92e3-6b5778f904c0'
            )
        ]
        self.phases: list[datatypes.HydraulicPhase] = []
        self.bridge: datatypes.Bridge = datatypes.Bridge(9, [], [], [], [], [
            # same as above, not sure why this is needed
            datatypes.BridgeJoint(
                pos=datatypes.Vec3(x=0.0, y=5.0, z=0.0),
                is_anchor=True,
                is_split=False,
                guid='dd84bd58-a5f2-4461-80c1-a07e91a67524'
            ),
            datatypes.BridgeJoint(
                pos=datatypes.Vec3(x=12.0, y=5.0, z=0.0),
                is_anchor=True,
                is_split=False,
                guid='dc72e01d-5335-4716-92e3-6b5778f904c0'
            )
        ], [])
        self.z_axis_vehicles: list[datatypes.ZAxisVehicle] = []
        self.vehicles: list[datatypes.Vehicle] = []
        self.vehicle_stop_triggers: list[datatypes.VehicleStopTrigger] = []
        self.theme_objects: list[datatypes.ThemeObject] = []
        self.event_timelines: list[datatypes.EventTimeline] = []
        self.checkpoints: list[datatypes.Checkpoint] = []
        self.platforms: list[datatypes.Platform] = []
        # default terrain stretches
        self.terrain_stretches: list[datatypes.TerrainIsland] = [
            datatypes.TerrainIsland(
                pos=datatypes.Vec3(x=0.0, y=0.0, z=0.0),
                prefab_name='Terrain_BookEndA',
                height_added=0.0,
                right_edge_water_height=3.0,
                terrain_island_type=constants.TerrainIslandType.Bookend,
                variant_index=0,
                flipped=False,
                lock_position=False
            ),
            datatypes.TerrainIsland(
                pos=datatypes.Vec3(x=12.0, y=0.0, z=0.0),
                prefab_name='Terrain_BookEndB',
                height_added=0.0,
                right_edge_water_height=0.0,
                terrain_island_type=constants.TerrainIslandType.Bookend,
                variant_index=1,
                flipped=True,
                lock_position=False
            )
        ]
        self.ramps: list[datatypes.Ramp] = []
        self.vehicle_restart_phases: list[datatypes.VehicleRestartPhase] = []
        self.flying_objects: list[datatypes.FlyingObject] = []
        self.rocks: list[datatypes.Rock] = []
        # default water blocks (floating point errors corrected)
        self.water_blocks: list[datatypes.WaterBlock] = [
            datatypes.WaterBlock(
                pos=datatypes.Vec3(x=6.0, y=1.5, z=0.0),
                width=12.0,
                height=3.0,
                lock_position=False
            )
        ]
        self.budget: datatypes.Budget = datatypes.Budget(
            10000000, 100, 100, 100, 100, 100, 100, 100, 100, True, True, True, True, True, True, True
        )
        self.settings: datatypes.Settings = datatypes.Settings(False, False)
        self.custom_shapes: list[datatypes.CustomShape] = []
        self.workshop: datatypes.Workshop = datatypes.Workshop("", "", "", "", False, [])
        self.support_pillars: list[datatypes.SupportPillar] = []
        self.pillars: list[datatypes.Pillar] = []
        self.is_modded: bool = False
        self.mods: list[datatypes.Mod] = []
        self.mod_save_data: dict[str, datatypes.ModSaveData] = {}

        self.ground_height = 5.11  # for convenience

        self.check_width_height = check_width_height

        self._min_x = 0.0
        self._max_x = 0.0

        self._min_y = 0.0
        self._max_y = 0.0

        # PB1 support
        self.__pb1_layout = is_pb1 or (self.path.endswith(".pbl") if self.path else False)

        # keep track of all guids
        # We use a set for this to avoid duplicates, since sometimes objects will have guids pointing to an object that
        # has already been deserialized.
        self._guids: set[str] = set()

        # if the path is set, we can deserialize the layout.
        # otherwise, it means that we're creating a new layout.
        if data is not None and deserialize_on_init:
            if self.__pb1_layout:
                self._parse_pb1_layout()
            else:
                self._deserialize()

    # =========================== #
    #      DESERIALIZER CODE      #
    # =========================== #

    def __read_byte(self) -> bytes:
        return self._file.read(1)

    def __read_bytes(self, length: int) -> bytes:
        return self._file.read(length)

    def __read_int8(self) -> int:
        return struct.unpack("<b", self.__read_bytes(1))[0]

    def __read_bool(self) -> bool:
        return struct.unpack("<?", self.__read_byte())[0]

    def __read_int16(self) -> int:
        return struct.unpack("<h", self.__read_bytes(2))[0]

    def __read_uint16(self) -> int:
        return struct.unpack("<H", self.__read_bytes(2))[0]

    def __read_int32(self) -> int:
        return struct.unpack("<i", self.__read_bytes(4))[0]

    def __read_float(self) -> float:
        return struct.unpack("<f", self.__read_bytes(4))[0]

    def __read_string(self) -> str:
        length = self.__read_int16()
        return self.__read_bytes(length).decode("utf-8")

    def __read_vector3(self) -> datatypes.Vec3:
        x = self.__read_float()
        y = self.__read_float()
        z = self.__read_float()

        if self.check_width_height:
            if self._max_x < x:
                self._max_x = x
            elif self._min_x > x:
                self._min_x = x

            if self._max_y < y:
                self._max_y = y
            elif self._min_y > y:
                self._min_y = y

        return datatypes.Vec3(x, y, z)

    def __read_vector2(self) -> datatypes.Vec2:
        return datatypes.Vec2(
            self.__read_float(),
            self.__read_float()
        )

    def __read_quaternion(self) -> datatypes.Quaternion:
        return datatypes.Quaternion(
            self.__read_float(),
            self.__read_float(),
            self.__read_float(),
            self.__read_float()
        )

    def __read_color(self) -> datatypes.Color:
        # r, g, and b are 1 byte each.
        # there is no alpha channel in the _file, but it's added here for convenience and never saved.
        return datatypes.Color(
            self.__read_int8() / 255.0,
            self.__read_int8() / 255.0,
            self.__read_int8() / 255.0,
            1.0
        )

    @staticmethod
    def __clamp01(value: float) -> float:
        if value < 0.0:
            return 0.0
        elif value > 1.0:
            return 1.0
        else:
            return value

    @staticmethod
    def __lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    def __fix_piston_value(self, value: float) -> float:
        if value < 0.25:
            return self.__lerp(1.0, 0.5, self.__clamp01(value / 0.25))
        if value > 0.75:
            return self.__lerp(0.5, 1.0, self.__clamp01((value - 0.75) / 0.25))
        return self.__lerp(0.0, 0.5, self.__clamp01(abs(value - 0.5) / 0.25))

    def deserialize_bridge(self, bridge_version) -> datatypes.Bridge | None:
        """
        This is only public because the slot deserializer uses it. Use at your own risk!
        """

        # Before v2, there was no bridge data.
        if bridge_version < 2:
            return

        # Next, joints
        count = self.__read_int32()
        joints = []
        for _ in range(count):
            pos = self.__read_vector3()
            is_anchor = self.__read_bool()
            is_split = self.__read_bool()
            guid = self.__read_string()
            self._guids.add(guid)
            joint = datatypes.BridgeJoint(
                pos,
                is_anchor,
                is_split,
                guid
            )
            joints.append(joint)

        # Next, edges
        count = self.__read_int32()
        edges = []
        for _ in range(count):
            material_type = constants.BridgeMaterialType(self.__read_int32())
            node_a_guid = self.__read_string()
            node_b_guid = self.__read_string()
            joint_a_part = constants.SplitJointPart(self.__read_int32())
            joint_b_part = constants.SplitJointPart(self.__read_int32())
            self._guids.add(node_a_guid)
            self._guids.add(node_b_guid)

            guid = self._unique_guid()
            if self.bridge.version >= 11:
                guid = self.__read_string()
                self._guids.add(guid)

            edge = datatypes.BridgeEdge(
                material_type,
                node_a_guid,
                node_b_guid,
                joint_a_part,
                joint_b_part,
                guid
            )
            edges.append(edge)

        # In bridge_version 7+, springs
        springs = []
        if bridge_version >= 7:
            count = self.__read_int32()
            for _ in range(count):
                normalized_value = self.__read_float()
                node_a_guid = self.__read_string()
                node_b_guid = self.__read_string()
                guid = self.__read_string()
                self._guids.add(guid)
                self._guids.add(node_a_guid)
                self._guids.add(node_b_guid)
                spring = datatypes.BridgeSpring(
                    normalized_value,
                    node_a_guid,
                    node_b_guid,
                    guid
                )
                springs.append(spring)

        # Pistons
        count = self.__read_int32()
        pistons = []
        for _ in range(count):
            normalized_value = self.__read_float()
            node_a_guid = self.__read_string()
            node_b_guid = self.__read_string()
            guid = self.__read_string()
            self._guids.add(guid)

            # in v7-, the piston value has to be normalized
            if bridge_version < 8:
                normalized_value = self.__fix_piston_value(normalized_value)

            piston = datatypes.Piston(
                normalized_value,
                node_a_guid,
                node_b_guid,
                guid
            )
            pistons.append(piston)

        # Hydraulic phases
        count = self.__read_int32()
        hydraulic_phases = []
        for _ in range(count):
            phase_guid = self.__read_string()
            self._guids.add(phase_guid)

            count = self.__read_int32()
            piston_guids = []
            for _ in range(count):
                piston_guid = self.__read_string()
                self._guids.add(piston_guid)
                piston_guids.append(piston_guid)

            # Split joints
            if bridge_version > 2:
                count = self.__read_int32()
                split_joints = []
                for _ in range(count):
                    guid = self.__read_string()
                    state = constants.SplitJointState(self.__read_int32())
                    self._guids.add(guid)
                    split_joint = datatypes.BridgeSplitJoint(
                        guid,
                        state
                    )
                    split_joints.append(split_joint)
            else:
                # garbage data in v2-
                count = self.__read_int32()
                for _ in range(count):
                    self.__read_string()
                split_joints = []

            if bridge_version > 9:
                disable_new_additions = self.__read_bool()
            else:
                disable_new_additions = False

            phase2 = datatypes.HydraulicsControllerPhase(
                phase_guid,
                piston_guids,
                split_joints,
                disable_new_additions
            )

            hydraulic_phases.append(phase2)

        # in v5, there's some garbage data
        if bridge_version == 5:
            count = self.__read_int32()
            for _ in range(count):
                self.__read_string()

        # in v6+, we deserialize anchors
        anchors = []
        if bridge_version >= 6:
            count = self.__read_int32()
            for _ in range(count):
                pos = self.__read_vector3()
                is_anchor = self.__read_bool()
                is_split = self.__read_bool()
                guid = self.__read_string()
                self._guids.add(guid)
                anchor = datatypes.BridgeJoint(
                    pos,
                    is_anchor,
                    is_split,
                    guid
                )
                anchors.append(anchor)

        # lastly, in v4 to v8, there's a random boolean
        if 4 <= bridge_version < 9:
            self.__read_bool()

        return datatypes.Bridge(
            bridge_version,
            joints,
            edges,
            springs,
            pistons,
            anchors,
            hydraulic_phases
        )

    def _deserialize(self) -> None:

        if self._file is None:
            raise Exception(
                "Cannot deserialize a newly created layout."
                "If you want to create a layout from a file, use the constructor with the `path` parameter."
            )

        # First, we need to get the bridge_version of the layout.
        self.version = self.__read_int32()
        # If the version is negative, that means it's a modded layout.
        if self.version < 0:
            self.is_modded = True
            self.version *= -1

        # Next, we need to get the stub key.
        self.stub_key = self.__read_string()

        # If the version is 19+, deserialize anchors.
        if self.version >= 19:
            count = self.__read_int32()
            for _ in range(count):
                pos = self.__read_vector3()
                is_anchor = self.__read_bool()
                is_split = self.__read_bool()
                guid = self.__read_string()
                self._guids.add(guid)
                anchor = datatypes.BridgeJoint(
                    pos,
                    is_anchor,
                    is_split,
                    guid
                )
                self.anchors.append(anchor)

        # If the version is 5+, deserialize phases.
        if self.version >= 5:
            count = self.__read_int32()
            for _ in range(count):
                time_delay = self.__read_float()
                guid = self.__read_string()
                self._guids.add(guid)
                phase = datatypes.HydraulicPhase(
                    time_delay,
                    guid
                )
                self.phases.append(phase)

        # If the version is 4+, deserialize the bridge the normal way.
        if self.version >= 4:
            # Bridges are fairly complicated.
            bridge_version = self.__read_int32()
            self.bridge = self.deserialize_bridge(bridge_version)
        else:
            # If the versions is 4 or less, we need to deserialize the bridge the old way.

            # Joints
            count = self.__read_int32()
            joints = []
            for _ in range(count):
                pos = self.__read_vector3()
                is_anchor = self.__read_bool()
                is_split = self.__read_bool()
                guid = self.__read_string()
                self._guids.add(guid)
                joint = datatypes.BridgeJoint(
                    pos,
                    is_anchor,
                    is_split,
                    guid
                )
                joints.append(joint)

            # Edges
            count = self.__read_int32()
            edges = []
            for _ in range(count):
                material_type = constants.BridgeMaterialType(self.__read_int32())
                node_a_guid = self.__read_string()
                node_b_guid = self.__read_string()
                joint_a_part = constants.SplitJointPart(self.__read_int32())
                joint_b_part = constants.SplitJointPart(self.__read_int32())
                self._guids.add(node_a_guid)
                self._guids.add(node_b_guid)
                edge = datatypes.BridgeEdge(
                    material_type,
                    node_a_guid,
                    node_b_guid,
                    joint_a_part,
                    joint_b_part,
                    self._unique_guid()
                )
                edges.append(edge)

            # Pistons
            count = self.__read_int32()
            pistons = []
            for _ in range(count):
                normalized_value = self.__read_float()
                node_a_guid = self.__read_string()
                node_b_guid = self.__read_string()
                guid = self.__read_string()
                self._guids.add(guid)

                if self.bridge.version < 8:
                    normalized_value = self.__fix_piston_value(normalized_value)

                piston = datatypes.Piston(
                    normalized_value,
                    node_a_guid,
                    node_b_guid,
                    guid
                )
                pistons.append(piston)

            self.bridge = datatypes.Bridge(
                self.bridge.version,
                joints,
                edges,
                [],
                pistons,
                [],
                []
            )

        # v7+ Z-Axis vehicles
        if self.version >= 7:
            speed = 1.0
            count = self.__read_int32()
            self.z_axis_vehicles = []
            for _ in range(count):
                pos = self.__read_vector2()
                prefab_name = self.__read_string()
                guid = self.__read_string()
                time_delay = self.__read_float()
                self._guids.add(guid)

                if self.version >= 8:
                    speed = self.__read_float()

                rot = datatypes.Quaternion(0.0, 0.0, 0.0, 1.0)
                rotation_degrees = 0.0
                if self.version >= 26:
                    rot = self.__read_quaternion()
                    rotation_degrees = self.__read_float()

                vehicle = datatypes.ZAxisVehicle(
                    pos,
                    prefab_name,
                    guid,
                    time_delay,
                    speed,
                    rot,
                    rotation_degrees
                )
                self.z_axis_vehicles.append(vehicle)

        # Vehicles
        count = self.__read_int32()
        for _ in range(count):
            display_name = self.__read_string()
            pos = self.__read_vector2()
            rot = self.__read_quaternion()
            prefab_name = self.__read_string()
            target_speed = self.__read_float()
            mass = self.__read_float()
            braking_force_multiplier = self.__read_float()
            strength_method = constants.StrengthMethod(self.__read_int32())
            acceleration = self.__read_float()
            max_slope = self.__read_float()
            desired_acceleration = self.__read_float()
            shocks_multiplier = self.__read_float()
            rotation_degrees = self.__read_float()
            time_delay = self.__read_float()
            idle_on_downhill = self.__read_bool()
            flipped = self.__read_bool()
            ordered_checkpoints = self.__read_bool()
            guid = self.__read_string()
            self._guids.add(guid)

            # deserialize checkpoint guids
            checkpoint_guids = []
            count = self.__read_int32()
            for _ in range(count):
                checkpoint_guid = self.__read_string()
                self._guids.add(checkpoint_guid)
                checkpoint_guids.append(checkpoint_guid)

            vehicle2 = datatypes.Vehicle(
                display_name,
                pos,
                rot,
                prefab_name,
                target_speed,
                mass,
                braking_force_multiplier,
                strength_method,
                acceleration,
                max_slope,
                desired_acceleration,
                shocks_multiplier,
                rotation_degrees,
                time_delay,
                idle_on_downhill,
                flipped,
                ordered_checkpoints,
                guid,
                checkpoint_guids
            )
            self.vehicles.append(vehicle2)

        # vehicle stop triggers
        count = self.__read_int32()
        for _ in range(count):
            pos = self.__read_vector2()
            rot = self.__read_quaternion()
            height = self.__read_float()
            rotation_degrees = self.__read_float()
            flipped = self.__read_bool()
            prefab_name = self.__read_string()
            stop_vehicle_guid = self.__read_string()
            self._guids.add(stop_vehicle_guid)
            trigger = datatypes.VehicleStopTrigger(
                pos,
                rot,
                height,
                rotation_degrees,
                flipped,
                prefab_name,
                stop_vehicle_guid
            )
            self.vehicle_stop_triggers.append(trigger)

        # Obsolete theme objects
        if self.version < 20:
            count = self.__read_int32()
            for _ in range(count):
                obj = datatypes.ThemeObject(
                    self.__read_vector2(),  # pos
                    self.__read_string(),  # prefab_name
                    self.__read_bool()  # ??
                )
                self.theme_objects.append(obj)

        # Event timelines
        count = self.__read_int32()
        for _ in range(count):
            checkpoint_guid = self.__read_string()
            self._guids.add(checkpoint_guid)

            count = self.__read_int32()
            events_stages = []
            for _ in range(count):
                count = self.__read_int32()
                event_units = []
                for _ in range(count):
                    # kind of looks like somebody messed up version compatibility
                    # and only realized after 3 versions that this was an issue
                    guid = ""
                    if self.version >= 7:
                        guid = self.__read_string()
                        event_units.append(datatypes.EventUnit(guid))
                        continue
                    text = self.__read_string()
                    if text != "":
                        guid = text

                    text = self.__read_string()
                    if text != "":
                        guid = text

                    self._guids.add(guid)

                    event_units.append(datatypes.EventUnit(guid))

                events_stages.append(datatypes.EventStage(event_units))

            self.event_timelines.append(datatypes.EventTimeline(checkpoint_guid, events_stages))

        # Checkpoints
        count = self.__read_int32()
        for _ in range(count):
            pos = self.__read_vector2()
            prefab_name = self.__read_string()
            vehicle_guid = self.__read_string()
            vehicle_restart_phase_guid = self.__read_string()
            trigger_timeline = self.__read_bool()
            stop_vehicle = self.__read_bool()
            reverse_vehicle_on_restart = self.__read_bool()
            guid = self.__read_string()

            self._guids.add(guid)
            self._guids.add(vehicle_guid)
            self._guids.add(vehicle_restart_phase_guid)

            self.checkpoints.append(datatypes.Checkpoint(
                pos,
                prefab_name,
                vehicle_guid,
                vehicle_restart_phase_guid,
                trigger_timeline,
                stop_vehicle,
                reverse_vehicle_on_restart,
                guid
            ))

        # Terrain islands
        count = self.__read_int32()
        for _ in range(count):
            self.terrain_stretches.append(datatypes.TerrainIsland(
                self.__read_vector3(),  # pos
                self.__read_string(),  # prefab_name
                self.__read_float(),  # height_added
                self.__read_float(),  # right_edge_water_height
                constants.TerrainIslandType(self.__read_int32()),  # terrain_island_type
                self.__read_int32(),  # variant_index
                self.__read_bool(),  # flipped
                self.__read_bool() if self.version >= 6 else False  # lock_position
            ))

        # Platforms
        count = self.__read_int32()
        for _ in range(count):
            pos = self.__read_vector2()
            width = self.__read_float()
            height = self.__read_float()
            flipped = self.__read_bool()

            if self.version >= 22:
                solid = self.__read_bool()
                self.platforms.append(datatypes.Platform(pos, width, height, flipped, solid))
                continue

            # int at the end of earlier versions
            self.__read_int32()
            self.platforms.append(datatypes.Platform(pos, width, height, flipped, False))

        # Ramps
        count = self.__read_int32()
        for _ in range(count):
            pos = self.__read_vector2()

            # control points
            count = self.__read_int32()
            control_points = []
            for _ in range(count):
                control_points.append(self.__read_vector2())

            height = self.__read_float()
            num_segments = self.__read_int32()
            spline_type = constants.SplineType(self.__read_int32())
            flipped_vertical = self.__read_bool()
            flipped_horizontal = self.__read_bool()
            hide_legs = (self.version >= 23 and self.__read_bool())

            flipped_legs = False
            if self.version >= 25:
                flipped_legs = self.__read_bool()
            elif self.version >= 22:
                self.__read_bool()
            else:
                self.__read_int32()

            line_points = []
            if self.version >= 13:
                # line points
                count = self.__read_int32()
                for _ in range(count):
                    line_points.append(self.__read_vector2())

            self.ramps.append(datatypes.Ramp(
                pos,
                control_points,
                height,
                num_segments,
                spline_type,
                flipped_vertical,
                flipped_horizontal,
                hide_legs,
                flipped_legs,
                line_points
            ))

        # phases are here if the version is under 5
        if self.version < 5:
            count = self.__read_int32()
            for _ in range(count):
                time_delay = self.__read_float()
                guid = self.__read_string()

                self._guids.add(guid)

                self.phases.append(datatypes.HydraulicPhase(
                    time_delay,
                    guid
                ))

        # Vehicle restart phases
        count = self.__read_int32()
        for _ in range(count):
            time_delay = self.__read_float()
            guid = self.__read_string()
            vehicle_guid = self.__read_string()

            self._guids.add(guid)
            self._guids.add(vehicle_guid)

            self.vehicle_restart_phases.append(datatypes.VehicleRestartPhase(
                time_delay,
                guid,
                vehicle_guid
            ))

        # Flying objects
        count = self.__read_int32()
        for _ in range(count):
            self.flying_objects.append(datatypes.FlyingObject(
                self.__read_vector3(),  # pos
                self.__read_vector3(),  # scale
                self.__read_string()  # prefab_name
            ))

        # Rocks
        count = self.__read_int32()
        for _ in range(count):
            self.rocks.append(datatypes.Rock(
                self.__read_vector3(),  # pos
                self.__read_vector3(),  # scale
                self.__read_string(),  # prefab_name
                self.__read_bool()  # flipped
            ))

        # Water blocks
        count = self.__read_int32()
        for _ in range(count):
            self.water_blocks.append(datatypes.WaterBlock(
                self.__read_vector3(),  # pos
                self.__read_float(),  # width
                self.__read_float(),  # height
                self.__read_bool() if self.version >= 12 else False  # lock_position
            ))

        # v5- garbage
        if self.version < 5:
            count = self.__read_int32()
            for _ in range(count):
                self.__read_string()
                count2 = self.__read_int32()
                for _ in range(count2):
                    self.__read_string()

        # Budget
        self.budget = datatypes.Budget(
            self.__read_int32(),  # cash
            self.__read_int32(),  # road
            self.__read_int32(),  # wood
            self.__read_int32(),  # steel
            self.__read_int32(),  # hydraulics
            self.__read_int32(),  # rope
            self.__read_int32(),  # cable
            self.__read_int32(),  # spring
            self.__read_int32(),  # bungee_rope
            self.__read_bool(),  # allow_wood
            self.__read_bool(),  # allow_steel
            self.__read_bool(),  # allow_hydraulics
            self.__read_bool(),  # allow_rope
            self.__read_bool(),  # allow_cable
            self.__read_bool(),  # allow_spring
            self.__read_bool()  # allow_reinforced_road
        )

        # Settings
        self.settings = datatypes.Settings(
            self.__read_bool(),  # hydraulics_controller_enabled
            self.__read_bool()  # unbreakable
        )

        # Custom shapes in v9+
        if self.version >= 9:
            count = self.__read_int32()
            for _ in range(count):
                pos2 = self.__read_vector3()
                rot = self.__read_quaternion()
                scale = self.__read_vector3()
                flipped = self.__read_bool()
                dynamic = self.__read_bool()
                collides_with_road = self.__read_bool()
                collides_with_nodes = self.__read_bool()

                if self.version >= 25:
                    collides_with_split_nodes = self.__read_bool()
                else:
                    collides_with_split_nodes = False

                rotation_degrees = self.__read_float()

                if self.version >= 10:
                    color = self.__read_color()
                else:
                    self.__read_int32()
                    color = datatypes.Color(*constants.CUSTOM_SHAPE_DEFAULT_COLOR)

                if self.version >= 11:
                    mass = self.__read_float()
                else:
                    self.__read_float()
                    mass = constants.CUSTOM_SHAPE_DEFAULT_MASS

                if self.version >= 14:
                    bounciness = self.__read_float()
                else:
                    bounciness = constants.CUSTOM_SHAPE_DEFAULT_BOUNCINESS

                if self.version >= 24:
                    pin_motor_strength = self.__read_float()
                    pin_target_velocity = self.__read_float()
                else:
                    pin_motor_strength = 0.0
                    pin_target_velocity = 0.0

                # Shape points
                count2 = self.__read_int32()
                points_local_space = []
                for _ in range(count2):
                    points_local_space.append(self.__read_vector2())

                # Static pins
                count2 = self.__read_int32()
                static_pins = []
                for _ in range(count2):
                    _pos = self.__read_vector3()
                    _pos.z = -1.348  # some fix, probably a bug in the game
                    static_pins.append(_pos)

                # Dynamic anchors
                count2 = self.__read_int32()
                dynamic_anchor_guids = []
                for _ in range(count2):
                    dynamic_anchor_guids.append(self.__read_string())

                self.custom_shapes.append(datatypes.CustomShape(
                    pos2,
                    rot,
                    scale,
                    flipped,
                    dynamic,
                    collides_with_road,
                    collides_with_nodes,
                    collides_with_split_nodes,
                    rotation_degrees,
                    color,
                    mass,
                    bounciness,
                    pin_motor_strength,
                    pin_target_velocity,
                    points_local_space,
                    static_pins,
                    dynamic_anchor_guids
                ))

        # v15+ workshop
        if self.version >= 15:
            self.workshop = datatypes.Workshop(
                self.__read_string(),  # id
                self.__read_string() if self.version >= 16 else "",  # leaderboard_id
                self.__read_string(),  # title
                self.__read_string(),  # description
                self.__read_bool(),  # autoplay
                [self.__read_string() for _ in range(self.__read_int32())]  # tags
            )

        # v17+ support pillars
        if self.version >= 17:
            count = self.__read_int32()
            for _ in range(count):
                self.support_pillars.append(datatypes.SupportPillar(
                    self.__read_vector3(),  # pos
                    self.__read_vector3(),  # scale
                    self.__read_string()  # prefab_name
                ))

        # v18+ pillars
        if self.version >= 18:
            count = self.__read_int32()
            for _ in range(count):
                self.pillars.append(datatypes.Pillar(
                    self.__read_vector3(),  # pos
                    self.__read_float(),  # height
                    self.__read_string()  # prefab_name
                ))

        # remove blank guid
        if "" in self._guids:
            self._guids.remove("")

        # if the layout is vanilla, make sure we're at the end of the file

        # store the current position
        current_pos = self._file.tell()
        if not self.is_modded and self.__read_byte() != b"":
            logging.warning("File is not at end, may indicate a deserialization error")

        # if the file is vanilla, stop here
        if not self.is_modded:
            self._file.close()
            return

        # restore the position
        self._file.seek(current_pos)

        # if the layout is marked as modded, but doesn't have mod data, stop here
        if self.is_modded and self.__read_byte() == b"":
            self._file.close()
            return

        # restore the position
        self._file.seek(current_pos)

        # ----------------- #
#       |    MOD SUPPORT    |
        # ----------------- #

        # First, mod metadata
        count = self.__read_uint16()
        for _ in range(count):
            # ptf uses a separator and strings for the name, version, and settings
            parts = self.__read_string().split(constants.PTF_STRING_SEPARATOR)
            name = parts[0] if len(parts) >= 1 else ""
            version = parts[1] if len(parts) >= 2 else ""
            settings = parts[2] if len(parts) >= 3 else ""
            self.mods.append(datatypes.Mod(name, version, settings))

        # Then, mod data
        offset = self._file.tell()
        if offset == len(self._file.read()):
            self._file.close()
            return  # no mod data

        # restore the position
        self._file.seek(offset)

        save_data_count = self.__read_int32()
        if save_data_count == 0:
            self._file.close()
            return  # no mod save data
        for _ in range(save_data_count):
            # There's a bug in PTF where the count may be incorrect, so we need to check if this throws an exception
            try:
                mod_identifier = self.__read_string()

                # deserialize byte array
                size = self.__read_int32()
                if size > 0:
                    data = self.__read_bytes(size)
                else:
                    data = b""

                parts = mod_identifier.split(constants.PTF_STRING_SEPARATOR)
                name = parts[0] if len(parts) >= 1 else ""
                version = parts[1] if len(parts) >= 2 else ""

                self.mod_save_data[name] = datatypes.ModSaveData(name, version, data)
            except struct.error:
                self._file.close()
                return

        # make sure to close the file
        self._file.close()

    # ========================= #
    #      SERIALIZER CODE      #
    # ========================= #
    def __write_int32(self, value: int) -> None:
        self.output_stream.write(struct.pack("<i", value))

    def __write_int16(self, value: int) -> None:
        self.output_stream.write(struct.pack("<h", value))

    def __write_uint16(self, value: int) -> None:
        self.output_stream.write(struct.pack("<H", value))

    def __write_string(self, value: str) -> None:
        self.__write_int16(len(value))
        self.output_stream.write(value.encode("utf-8"))

    def __write_float(self, value: float) -> None:
        self.output_stream.write(struct.pack("<f", value))

    def __write_bool(self, value: bool) -> None:
        self.output_stream.write(struct.pack("<?", value))

    def __write_byte(self, value: bytes) -> None:
        self.output_stream.write(struct.pack("<b", value))

    def __write_vector3(self, value: datatypes.Vec3) -> None:
        self.__write_float(value.x)
        self.__write_float(value.y)
        self.__write_float(value.z)

    def __write_vector2(self, value: datatypes.Vec2) -> None:
        self.__write_float(value.x)
        self.__write_float(value.y)

    def __write_quaternion(self, value: datatypes.Quaternion) -> None:
        self.__write_float(value.x)
        self.__write_float(value.y)
        self.__write_float(value.z)
        self.__write_float(value.w)

    def __write_bytes(self, value: bytes) -> None:
        self.output_stream.write(value)

    def __write_color(self, value: datatypes.Color) -> None:
        self.output_stream.write(struct.pack("<B", int(value.r) * 255))
        self.output_stream.write(struct.pack("<B", int(value.g) * 255))
        self.output_stream.write(struct.pack("<B", int(value.b) * 255))

    def serialize_bridge(self):
        """
        Serializes the bridge data of the layout.
        Please note this is only public for use in the save slot serializer.
        Use at your own risk.
        """
        b = self.bridge  # for convenience
        self.__write_int32(constants.CURRENT_BRIDGE_VERSION)

        # Joints
        self.__write_int32(len(b.joints))
        for joint in b.joints:
            self.__write_vector3(joint.pos)
            self.__write_bool(joint.is_anchor)
            self.__write_bool(joint.is_split)
            self.__write_string(joint.guid)

        # Edges
        self.__write_int32(len(b.edges))
        for edge in b.edges:
            self.__write_int32(edge.material_type.value)
            self.__write_string(edge.node_a_guid)
            self.__write_string(edge.node_b_guid)
            self.__write_int32(edge.joint_a_part.value)
            self.__write_int32(edge.joint_b_part.value)
            self.__write_string(edge.guid)

        # Springs
        self.__write_int32(len(b.springs))
        for spring in b.springs:
            self.__write_float(spring.normalized_value)
            self.__write_string(spring.node_a_guid)
            self.__write_string(spring.node_b_guid)
            self.__write_string(spring.guid)

        # Pistons
        self.__write_int32(len(b.pistons))
        for piston in b.pistons:
            self.__write_float(piston.normalized_value)
            self.__write_string(piston.node_a_guid)
            self.__write_string(piston.node_b_guid)
            self.__write_string(piston.guid)

        # Hydraulics phases
        self.__write_int32(len(b.phases))
        for phase2 in b.phases:
            self.__write_string(phase2.hydraulics_phase_guid)

            # Piston GUIDs
            self.__write_int32(len(phase2.piston_guids))
            for piston_guid in phase2.piston_guids:
                self.__write_string(piston_guid)

            # Bridge split joints
            self.__write_int32(len(phase2.bridge_split_joints))
            for bridge_split_joint in phase2.bridge_split_joints:
                self.__write_string(bridge_split_joint.guid)
                self.__write_int32(bridge_split_joint.state.value)

            # Disable New Additions
            self.__write_bool(phase2.disable_new_additions)

        # Anchors
        self.__write_int32(len(b.anchors))
        for anchor in b.anchors:
            self.__write_vector3(anchor.pos)
            self.__write_bool(anchor.is_anchor)
            self.__write_bool(anchor.is_split)
            self.__write_string(anchor.guid)

    def _serialize(self) -> Union[io.BytesIO, None]:
        # make sure the buffer is empty
        self.output_stream.seek(0)
        self.output_stream.truncate(0)

        # ----------------------- #
#       |    PRE BRIDGE BINARY    |
        # ----------------------- #

        # Write the version, make sure to invert it back if the layout is modded
        # TODO: uncomment this line and comment the next one when mod reserialization is implemented
        # self.__write_int32(self.version if not self.is_modded else (self.version * -1))
        self.__write_int32(constants.CURRENT_LAYOUT_VERSION)

        # Write the stub key
        self.__write_string(self.stub_key)

        # Anchors
        self.__write_int32(len(self.anchors))
        for anchor in self.anchors:
            self.__write_vector3(anchor.pos)
            self.__write_bool(anchor.is_anchor)
            self.__write_bool(anchor.is_split)
            self.__write_string(anchor.guid)

        # Hydraulic phases
        self.__write_int32(len(self.phases))
        for phase in self.phases:
            self.__write_float(phase.time_delay)
            self.__write_string(phase.guid)

        # ------------------- #
#       |    BRIDGE BINARY    |
        # ------------------- #

        self.serialize_bridge()

        # ------------------------ #
#       |    POST BRIDGE BINARY    |
        # ------------------------ #

        # Z-Axis Vehicles
        self.__write_int32(len(self.z_axis_vehicles))
        for z_axis_vehicle in self.z_axis_vehicles:
            self.__write_vector2(z_axis_vehicle.pos)
            self.__write_string(z_axis_vehicle.prefab_name)
            self.__write_string(z_axis_vehicle.guid)
            self.__write_float(z_axis_vehicle.time_delay)
            self.__write_float(z_axis_vehicle.speed)
            self.__write_quaternion(z_axis_vehicle.rot)
            self.__write_float(z_axis_vehicle.rotation_degrees)

        # Vehicles
        self.__write_int32(len(self.vehicles))
        for v in self.vehicles:
            self.__write_string(v.display_name)
            self.__write_vector2(v.pos)
            self.__write_quaternion(v.rot)
            self.__write_string(v.prefab_name)
            self.__write_float(v.target_speed)
            self.__write_float(v.mass)
            self.__write_float(v.braking_force_multiplier)
            self.__write_int32(v.strength_method.value)
            self.__write_float(v.horsepower)
            self.__write_float(v.max_slope)
            self.__write_float(v.acceleration)
            self.__write_float(v.shocks_multiplier)
            self.__write_float(v.rotation_degrees)
            self.__write_float(v.time_delay)
            self.__write_bool(v.idle_on_downhill)
            self.__write_bool(v.flipped)
            self.__write_bool(v.ordered_checkpoints)
            self.__write_string(v.guid)

            # Checkpoint GUIDs
            self.__write_int32(len(v.checkpoint_guids))
            for checkpoint in v.checkpoint_guids:
                self.__write_string(checkpoint)

        # Vehicle stop triggers
        self.__write_int32(len(self.vehicle_stop_triggers))
        for st in self.vehicle_stop_triggers:
            self.__write_vector2(st.pos)
            self.__write_quaternion(st.rot)
            self.__write_float(st.height)
            self.__write_float(st.rotation_degrees)
            self.__write_bool(st.flipped)
            self.__write_string(st.prefab_name)
            self.__write_string(st.stop_vehicle_guid)

        # Timelines
        self.__write_int32(len(self.event_timelines))
        for timeline in self.event_timelines:
            self.__write_string(timeline.checkpoint_guid)

            self.__write_int32(len(timeline.stages))
            for stage in timeline.stages:
                self.__write_int32(len(stage.units))
                for unit in stage.units:
                    self.__write_string(unit.guid)

        # Checkpoints
        self.__write_int32(len(self.checkpoints))
        for ch in self.checkpoints:
            self.__write_vector2(ch.pos)
            self.__write_string(ch.prefab_name)
            self.__write_string(ch.vehicle_guid)
            self.__write_string(ch.vehicle_restart_phase_guid)
            self.__write_bool(ch.trigger_timeline)
            self.__write_bool(ch.stop_vehicle)
            self.__write_bool(ch.reverse_vehicle_on_restart)
            self.__write_string(ch.guid)

        # Terrain stretches
        self.__write_int32(len(self.terrain_stretches))
        for stretch in self.terrain_stretches:
            self.__write_vector3(stretch.pos)
            self.__write_string(stretch.prefab_name)
            self.__write_float(stretch.height_added)
            self.__write_float(stretch.right_edge_water_height)
            self.__write_int32(stretch.terrain_island_type.value)
            self.__write_int32(stretch.variant_index)
            self.__write_bool(stretch.flipped)
            self.__write_bool(stretch.lock_position)

        # Platforms
        self.__write_int32(len(self.platforms))
        for pf in self.platforms:
            self.__write_vector2(pf.pos)
            self.__write_float(pf.width)
            self.__write_float(pf.height)
            self.__write_bool(pf.flipped)
            self.__write_bool(pf.solid)

        # Ramps
        self.__write_int32(len(self.ramps))
        for ramp in self.ramps:
            self.__write_vector2(ramp.pos)

            # Control points
            self.__write_int32(len(ramp.control_points))
            for point in ramp.control_points:
                self.__write_vector2(point)

            self.__write_float(ramp.height)
            self.__write_int32(ramp.num_segments)
            self.__write_int32(ramp.spline_type.value)
            self.__write_bool(ramp.flipped_vertical)
            self.__write_bool(ramp.flipped_horizontal)
            self.__write_bool(ramp.hide_legs)
            self.__write_bool(ramp.flipped_legs)

        # Vehicle restart phases
        self.__write_int32(len(self.vehicle_restart_phases))
        for phase3 in self.vehicle_restart_phases:
            self.__write_float(phase3.time_delay)
            self.__write_string(phase3.guid)
            self.__write_string(phase3.vehicle_guid)

        # Flying objects
        self.__write_int32(len(self.flying_objects))
        for obj in self.flying_objects:
            self.__write_vector3(obj.pos)
            self.__write_vector3(obj.scale)
            self.__write_string(obj.prefab_name)

        # Rocks
        self.__write_int32(len(self.rocks))
        for rock in self.rocks:
            self.__write_vector3(rock.pos)
            self.__write_vector3(rock.scale)
            self.__write_string(rock.prefab_name)
            self.__write_bool(rock.flipped)

        # Water blocks
        self.__write_int32(len(self.water_blocks))
        for wb in self.water_blocks:
            self.__write_vector3(wb.pos)
            self.__write_float(wb.width)
            self.__write_float(wb.height)
            self.__write_bool(wb.lock_position)

        # Budget
        self.__write_int32(self.budget.cash)
        self.__write_int32(self.budget.road)
        self.__write_int32(self.budget.wood)
        self.__write_int32(self.budget.steel)
        self.__write_int32(self.budget.hydraulics)
        self.__write_int32(self.budget.rope)
        self.__write_int32(self.budget.cable)
        self.__write_int32(self.budget.spring)
        self.__write_int32(self.budget.bungee_rope)

        self.__write_bool(self.budget.allow_wood)
        self.__write_bool(self.budget.allow_steel)
        self.__write_bool(self.budget.allow_hydraulics)
        self.__write_bool(self.budget.allow_rope)
        self.__write_bool(self.budget.allow_cable)
        self.__write_bool(self.budget.allow_spring)
        self.__write_bool(self.budget.allow_reinforced_road)

        # Settings
        self.__write_bool(self.settings.hydraulics_controller_enabled)
        self.__write_bool(self.settings.unbreakable)

        # Custom shapes
        self.__write_int32(len(self.custom_shapes))
        for cs in self.custom_shapes:
            self.__write_vector3(cs.pos)
            self.__write_quaternion(cs.rot)
            self.__write_vector3(cs.scale)
            self.__write_bool(cs.flipped)
            self.__write_bool(cs.dynamic)
            self.__write_bool(cs.collides_with_road)
            self.__write_bool(cs.collides_with_nodes)
            self.__write_bool(cs.collides_with_split_nodes)
            self.__write_float(cs.rotation_degrees)
            self.__write_color(cs.color)
            self.__write_float(cs.mass)
            self.__write_float(cs.bounciness)
            self.__write_float(cs.pin_motor_strength)
            self.__write_float(cs.pin_target_velocity)

            # Points
            self.__write_int32(len(cs.points_local_space))
            for p in cs.points_local_space:
                self.__write_vector2(p)

            # Static pins
            self.__write_int32(len(cs.static_pins))
            for sp in cs.static_pins:
                self.__write_vector3(sp)

            # Dynamic anchor GUIDs
            self.__write_int32(len(cs.dynamic_anchor_guids))
            for da in cs.dynamic_anchor_guids:
                self.__write_string(da)

        # Workshop
        self.__write_string(self.workshop.id)
        self.__write_string(self.workshop.leaderboard_id)
        self.__write_string(self.workshop.title)
        self.__write_string(self.workshop.description)
        self.__write_bool(self.workshop.autoplay)
        # Tags
        self.__write_int32(len(self.workshop.tags))
        for tag in self.workshop.tags:
            self.__write_string(tag)

        # Support pillars
        self.__write_int32(len(self.support_pillars))
        for support_pillar in self.support_pillars:
            self.__write_vector3(support_pillar.pos)
            self.__write_vector3(support_pillar.scale)
            self.__write_string(support_pillar.prefab_name)

        # Pillars
        self.__write_int32(len(self.pillars))
        for pl in self.pillars:
            self.__write_vector3(pl.pos)
            self.__write_float(pl.height)
            self.__write_string(pl.prefab_name)

        # -------------- #
#       |    MOD DATA    |
        # -------------- #

        # TODO: mod support, as the below code does not work for some reason
        return self.output_stream

        # If the layout is vanilla, we don't need to write any mod data
        # if not self.is_modded:
        #     return
        #
        # # Mod metadata
        # self.__write_uint16(len(self.mods))
        # print(len(self.mods))
        # for mod in self.mods:
        #     combined_info = mod.name + constants.PTF_STRING_SEPARATOR + \
        #                     mod.version + constants.PTF_STRING_SEPARATOR + \
        #                     mod.settings
        #
        #     self.__write_string(combined_info)
        #
        # print("s_pos:", self.output_stream.tell())
        #
        # # Mod save data
        # self.__write_int32(len(self.mod_save_data))
        # print(len(self.mod_save_data))
        # mod_data: {str: datatypes.ModSaveData}
        # for mod_data in self.mod_save_data.values():
        #     combined = mod_data.name + constants.PTF_STRING_SEPARATOR + mod_data.version
        #     self.__write_string(combined)
        #
        #     self.__write_int32(len(mod_data.data))
        #     self.__write_bytes(mod_data.data)

    # =============== #
    #    UTILITIES    #
    # =============== #

    def save(self, path: Union[str, None] = None) -> None:
        """
        Saves the layout to a file.
        :param path: The path to save the layout to. If None, the layout will save to the path it was loaded from.
        :return: None
        """
        self._serialize()
        if path is None:
            path = self.path
            if path is None:
                raise ValueError("Path may not be none when saving a newly created layout.")

        with open(path, "wb") as file:
            self.output_stream.seek(0)
            file.write(self.output_stream.read())

    def serialize_to_bytes(self) -> bytes:
        """
        Serializes the layout to a bytes object.
        :return: The serialized bytes object.
        """
        self._serialize()
        self.output_stream.seek(0)
        return self.output_stream.read()

    def format_materials(self) -> str:
        """
        Formats the materials into a string.

        :return: A string like "Road, Wood, Steel"
        """
        materials = []
        materials.append("Wood") if self.budget.allow_wood else None
        materials.append("Steel") if self.budget.allow_steel else None
        materials.append("Hydraulics") if self.budget.allow_hydraulics else None
        materials.append("Rope") if self.budget.allow_rope else None
        materials.append("Cable") if self.budget.allow_cable else None
        materials.append("Spring") if self.budget.allow_spring else None
        materials.append("Reinforced Road") if self.budget.allow_reinforced_road else None
        materials = ", ".join(materials)
        return materials

    def get_dimensions(self) -> tuple[float, float]:
        """
        Returns the dimensions of the layout.

        :return: A tuple (width, height) of the layout.
        """
        return self._max_x - self._min_x, self._max_y - self._min_y

    def _unique_guid(self) -> str:
        """
        Generates a unique GUID.
        :return: A GUID that has not been used yet in the layout.
        """
        u = str(uuid.uuid4())
        while u in self._guids:
            u = str(uuid.uuid4())
        self._guids.add(u)
        return u

    # ==================== #
    #    USER INTERFACE    #
    # ==================== #

    def set_theme(self, theme: constants.Theme) -> None:
        """
        Sets the theme of the layout.
        :param theme: The theme to set.
        :return: None
        """
        self.stub_key = theme.value

    def add_anchor(self, pos: tuple[float, float, float], is_split: bool) -> datatypes.Anchor:
        """
        Adds an anchor to the layout.

        :param pos: The position of the anchor. Represented by a tuple of (x, y, z).
        :param is_split: Whether the anchor is a split anchor.
        :return: The anchor that was added.
        """
        g = self._unique_guid()
        anchor = datatypes.Anchor(
            datatypes.Vec3(*pos),
            True,
            is_split,
            g
        )
        self.anchors.append(anchor)
        self.bridge.anchors.append(anchor)
        return anchor

    def remove_anchor(self, anchor_guid: Union[str, datatypes.Anchor]) -> None:
        """
        Removes an anchor from the bridge.

        :param anchor_guid: The GUID of the anchor to remove. This can also be an Anchor object.
        """

        if isinstance(anchor_guid, datatypes.Anchor):
            anchor_guid = anchor_guid.guid

        if anchor_guid not in self._guids:
            return

        self._guids.remove(anchor_guid)
        for anchor in self.anchors:
            if anchor.guid == anchor_guid:
                self.anchors.remove(anchor)
                self.bridge.anchors.remove(anchor)
                return

    def add_vehicle(
            self,
            pos: tuple[float, float],
            rot: tuple[float, float, float, float] = (0, 0, 0, 1),
            vehicle_type: Union[constants.VehicleType, str] = constants.VehicleType.CompactCar,
            display_name: str = "",
            target_speed: float = None,
            mass: float = None,
            braking_intensity: float = None,
            acceleration: float = None,
            horsepower: float = None,
            shocks_multiplier: float = None,
            rotation_degrees: float = None,
            time_delay: float = 0.0,
            idle_on_downhill: bool = True,
            flipped: bool = False,
            ordered_checkpoints: bool = False,
            victory_flag_pos: tuple[float, float] = (17, 5.11),
            victory_flag_rot: tuple[float, float, float, float] = (0, 0, 0, 1),
            victory_flag_height: float = 1.75,
            victory_flag_rotation_degrees: float = 0.0,
            victory_flag_flipped: bool = False,
            event_timeline: int = 0
    ) -> datatypes.Vehicle:
        """
        Adds a vehicle to the layout.

        :param pos: The position of the vehicle. Represented by a tuple of (x, y).
        :param rot: The rotation of the vehicle. Represented by a tuple of (x, y, z, w).
        :param vehicle_type: The type of vehicle to add This can be a fuzzy string or a VehicleType enum.
        :param display_name: The display name of the vehicle.
        :param target_speed: The target speed of the vehicle.
        :param mass: The mass of the vehicle.
        :param braking_intensity: The braking intensity of the vehicle.
        :param acceleration: The acceleration of the vehicle.
        :param horsepower: The horsepower of the vehicle.
        :param shocks_multiplier: The shocks multiplier of the vehicle.
        :param rotation_degrees: The rotation degrees of the vehicle.
        :param time_delay: The time delay of the vehicle.
        :param idle_on_downhill: Whether the vehicle should idle on downhill.
        :param flipped: Whether the vehicle should be flipped.
        :param ordered_checkpoints: Whether the vehicle should use ordered checkpoints.
        :param victory_flag_pos: The position of the victory flag. Represented by a tuple of (x, y).
        :param victory_flag_rot: The rotation of the victory flag. Represented by a tuple of (x, y, z, w).
        :param victory_flag_height: The height of the victory flag.
        :param victory_flag_rotation_degrees: The rotation degrees of the victory flag.
        :param victory_flag_flipped: Whether the victory flag should be flipped.
        :param event_timeline: The event timeline of the vehicle. Generally, this is 0.

        :return: The vehicle that was added.
        """
        guid = self._unique_guid()

        # allow using strings for vehicle_type
        if isinstance(vehicle_type, str):
            vehicle_type = constants.VehicleType["".join([word.capitalize() for word in vehicle_type.split(" ")])].value
        elif isinstance(vehicle_type, constants.VehicleType):
            vehicle_type = vehicle_type.value

        # Set default values for optional parameters
        default_settings = constants.DefaultVehicleSettings[vehicle_type]
        if mass is None:
            mass = default_settings["mass"]
        else:
            mass = mass * 4.0  # Convert from polygrams
        if braking_intensity is None:
            braking_intensity = default_settings["braking_force_multiplier"]
        if acceleration is None:
            acceleration = default_settings["acceleration"]
        if horsepower is None:
            horsepower = default_settings["horsepower"]
        if shocks_multiplier is None:
            shocks_multiplier = default_settings["shocks_multiplier"]
        if rotation_degrees is None:
            rotation_degrees = default_settings["rotation_degrees"]
        if target_speed is None:
            target_speed = default_settings["target_speed"]

        vehicle = datatypes.Vehicle(
            display_name,
            datatypes.Vec2(*pos),
            datatypes.Quaternion(*rot),
            vehicle_type,
            target_speed,
            mass,
            braking_intensity,
            constants.StrengthMethod.Acceleration,
            horsepower,
            0.0,
            acceleration,
            shocks_multiplier,
            rotation_degrees,
            time_delay,
            idle_on_downhill,
            flipped,
            ordered_checkpoints,
            guid,
            []
        )

        self.vehicles.append(vehicle)

        # Make sure to add a stop trigger (victory flag) or else the vehicle will never start and have no letter name!
        self.vehicle_stop_triggers.append(
            datatypes.VehicleStopTrigger(
                datatypes.Vec2(*victory_flag_pos),
                datatypes.Quaternion(*victory_flag_rot),
                victory_flag_height,
                victory_flag_rotation_degrees,
                victory_flag_flipped,
                "VictoryFlag",
                guid
            )
        )

        # ...and an event timeline
        # make sure to create it if it doesn't exist
        if len(self.event_timelines) == 0:
            self.event_timelines.append(datatypes.EventTimeline("", []))

        self.event_timelines[event_timeline].stages.append(datatypes.EventStage([datatypes.EventUnit(guid)]))

        return vehicle

    def remove_vehicle(self, vehicle_guid: Union[str, datatypes.Vehicle]) -> None:
        """
        Removes a vehicle from the layout.

        :param vehicle_guid: The GUID of the vehicle. Can also be a Vehicle object.
        """

        if isinstance(vehicle_guid, datatypes.Vehicle):
            vehicle_guid = vehicle_guid.guid

        if vehicle_guid not in self._guids:
            return

        self._guids.remove(vehicle_guid)
        for vehicle in self.vehicles:
            if vehicle.guid == vehicle_guid:
                self.vehicles.remove(vehicle)
                return

        # remove the stop trigger
        for trigger in self.vehicle_stop_triggers:
            if trigger.stop_vehicle_guid == vehicle_guid:
                self.vehicle_stop_triggers.remove(trigger)
                return

        # remove the event unit
        for timeline in self.event_timelines:
            for stage in timeline.stages:
                for unit in stage.units:
                    if unit.guid == vehicle_guid:
                        stage.units.remove(unit)
                        return

    def add_hydraulic_phase(
            self,
            time_delay: float,
            pistons: list[Union[datatypes.Piston, str]],
            split_joints: list[datatypes.BridgeSplitJoint],
            disable_new_additions: bool = False
    ) -> datatypes.HydraulicsControllerPhase:
        """
        Adds a hydraulic phase to the layout.

        :param time_delay: The time delay of the phase, in seconds.
        :param pistons: The pistons of the phase. Can be a list of Piston objects or GUIDs.
        :param split_joints: The split joints that activate during this phase.
        :param disable_new_additions: If new additions to the phase should be disabled automatically.

        :return: The hydraulic phase that was added.
        """
        guid = self._unique_guid()
        self._guids.add(guid)

        self.phases.append(datatypes.HydraulicPhase(time_delay, guid))

        _pistons = []
        for piston in pistons:
            if isinstance(piston, datatypes.Piston):
                _pistons.append(piston.guid)
            else:
                _pistons.append(piston)

        _split_joints = []
        for split_joint in split_joints:
            if isinstance(split_joint, datatypes.BridgeSplitJoint):
                _split_joints.append(split_joint.guid)
            else:
                _split_joints.append(split_joint)

        self.bridge.phases.append(
            datatypes.HydraulicsControllerPhase(
                guid,
                _pistons,
                _split_joints,
                disable_new_additions
            )
        )

        return self.bridge.phases[-1]

    def remove_hydraulic_phase(self, phase: Union[str, datatypes.HydraulicsControllerPhase]) -> None:
        """
        Removes a hydraulic phase from the layout.

        :param phase: The GUID of the phase. Can also be a HydraulicsControllerPhase object.
        """

        if isinstance(phase, datatypes.HydraulicsControllerPhase):
            phase = phase.hydraulics_phase_guid

        if phase not in self._guids:
            return

        self._guids.remove(phase)
        for phase in self.bridge.phases:
            if phase.hydraulics_phase_guid == phase:
                self.bridge.phases.remove(phase)
                return

        for phase in self.phases:
            if phase.guid == phase:
                self.phases.remove(phase)
                return

    def add_terrain_island(self, pos, ) -> datatypes.TerrainIsland:
        """Adds a new terrain island to the layout."""
        pass

    # ================= #
    #    PB1 SUPPORT    #
    # ================= #

    def _parse_pb1_layout(self):
        if not self.__pb1_layout:
            return

        layout = json.loads(self._file.read())

        # start with the easy things
        self.settings.unbreakable = layout["unbreakable"]
        self.settings.hydraulics_controller_enabled = layout["hydroController"]

        def n1to100(val):
            return 100 if val == -1 else val

        self.budget.cash = 10000000 if layout["resources"]["budget"] == 0 else layout["resources"]["budget"]
        self.budget.road = n1to100(layout["resources"]["numRoads"])
        self.budget.wood = n1to100(layout["resources"]["numSegments"])
        self.budget.steel = n1to100(layout["resources"]["numSegmentsStrong"])
        self.budget.hydraulics = n1to100(layout["resources"]["numPistons"])
        self.budget.rope = n1to100(layout["resources"]["numRopes"])
        self.budget.cable = n1to100(layout["resources"]["numCablesStrong"])

        # Anchors (bridge and layout anchors were combined)
        # we add 5 to fix the ground level being 0 in PB1
        self.anchors = []
        self.bridge.anchors = []
        for anchor in layout["anchors"]:
            # Generate a new GUID for it
            new_guid = self._unique_guid()
            self.anchors.append(
                datatypes.BridgeJoint(
                    pos=datatypes.Vec3(anchor["pos"]["x"], anchor["pos"]["y"] + 5, 0),
                    is_anchor=True,
                    is_split=False,
                    guid=new_guid
                )
            )
            self.bridge.anchors.append(
                datatypes.BridgeJoint(
                    pos=datatypes.Vec3(anchor["pos"]["x"], anchor["pos"]["y"] + 5, 0),
                    is_anchor=True,
                    is_split=False,
                    guid=new_guid
                )
            )

        # Terrain
        self.terrain_stretches = []
        for terrain in layout["terrains"]:
            if terrain["terrainType"] in (0, 1):
                # Indexes have changed anyway, so let's just randomize it
                prefab_name = random.choice([
                    "Terrain_BookEndA",
                    "Terrain_BookEndB",
                    "Terrain_BookEndC",
                    "Terrain_BookEndD",
                ])
                terrain_island_type = constants.TerrainIslandType.Bookend
            else:
                prefab_name = random.choice([
                    "Terrain_MiddleA",
                    "Terrain_MiddleB",
                    "Terrain_MiddleC",
                    "Terrain_MiddleD",
                ])
                terrain_island_type = constants.TerrainIslandType.Middle
            self.terrain_stretches.append(
                datatypes.TerrainIsland(
                    pos=datatypes.Vec3(terrain["pos"]["x"], terrain["pos"]["y"], 0),
                    prefab_name=prefab_name,
                    height_added=0,
                    right_edge_water_height=3.0 if terrain["terrainType"] == 0 else 0.0,
                    terrain_island_type=terrain_island_type,
                    variant_index=random.randint(0, 4),  # whatever
                    flipped=True if terrain["terrainType"] == 1 else False,
                    lock_position=False
                )
            )

        # Vehicles
        for vehicle in layout["vehicleEvents"]:
            real_type = constants.PB1ToPB2Vehicles[vehicle["vehicleType"]]
            defaults = constants.DefaultVehicleSettings[real_type.value]
            new_guid = self._unique_guid()
            self.vehicles.append(
                datatypes.Vehicle(
                    "",
                    datatypes.Vec2(vehicle["pos"]["x"], vehicle["pos"]["y"] + 5),
                    datatypes.Quaternion(0.0, 0.0, 0.0, 1.0),
                    real_type.value,
                    defaults["target_speed"] * vehicle["speedMultiplier"],
                    defaults["mass"] * vehicle["weightMultiplier"],
                    defaults["braking_force_multiplier"],
                    constants.StrengthMethod.Acceleration,
                    defaults["horsepower"],
                    defaults["max_slope"],
                    defaults["acceleration"],
                    defaults["shocks_multiplier"],
                    0.0,
                    vehicle["delay"],
                    False,
                    False,
                    vehicle["orderCheckpoints"],
                    new_guid,
                    []
                )
            )

        # Ships
        for ship in layout["shipEvents"]:
            self.z_axis_vehicles.append(
                datatypes.ZAxisVehicle(
                    datatypes.Vec2(ship["pos"]["x"], ship["pos"]["y"]),
                    constants.PB1ToPB2Ships[ship["shipType"]],
                    self._unique_guid(),
                    ship["delay"],
                    1.0,
                    datatypes.Quaternion(0.0, 0.0, 0.0, 1.0),
                    0.0
                )
            )

        # Planes
        for plane in layout["airplaneEvents"]:
            self.z_axis_vehicles.append(
                datatypes.ZAxisVehicle(
                    datatypes.Vec2(plane["pos"]["x"], plane["pos"]["y"] + 5),
                    constants.PB1ToPB2Planes[plane["planeType"]],
                    self._unique_guid(),
                    plane["delay"],
                    1.0,
                    datatypes.Quaternion(0.0, 0.0, 0.0, 1.0),
                    0.0
                )
            )

    # ==================== #
    #    DUNDER METHODS    #
    # ==================== #

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__  # There's no good way to compare two layouts, so we have to use __dict__

    def __gt__(self, other):
        return self.version > other.version and self.bridge.version > other.bridge.version

    def __lt__(self, other):
        return self.version < other.version and self.bridge.version < other.bridge.version

    def __repr__(self) -> str:
        return f"<Layout (v{self.version}, bridge v{self.bridge.version}, {'modded' if self.is_modded else 'vanilla'})>"
