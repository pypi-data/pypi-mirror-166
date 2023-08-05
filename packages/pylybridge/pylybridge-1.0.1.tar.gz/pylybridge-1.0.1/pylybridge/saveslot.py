"""
pylybridge.saveslot - Edit PB2 save slots in Python
"""
import io
import struct
from os.path import exists
from typing import Union

from PIL import Image

from pylybridge import datatypes, sandbox
from pylybridge import exceptions
from pylybridge import constants


class SaveSlot:
    """
    An object representing a save slot.
    You can initialize this object with a file path, file object, or buffer,
    or initialize with no parameters to create a new save slot.
    The `deserialize_on_init` parameter controls whether to deserialize the save slot
    on initialization or not. If this is False, you must call the internal _deserialize
    method to deserialize the slot.
    """
    def __init__(
            self,
            fp: Union[str, bytes, io.IOBase, io.BufferedIOBase, None] = None,
            deserialize_on_init: bool = True
    ):
        self.path: Union[str, None] = None
        
        if isinstance(fp, bytes):
            self._file = io.BytesIO(fp)
            self.path = None
        elif isinstance(fp, str):
            self._file = open(fp, "rb") if fp is not None else None
            self.path: str = fp if fp is not None else ""
        elif isinstance(fp, io.IOBase):
            self._file = fp
            self.path = None
        else:
            self._file = None
            self.path = None

        if isinstance(fp, str) and not exists(fp):
            raise FileNotFoundError("File " + fp + "does not exist.")

        self.version: int
        self.physics_version: int
        self.slot_id: int
        self.display_name: str
        self.file_name: str
        self.budget: int
        self.last_write_time: int
        self.bridge: datatypes.Bridge
        self.thumbnail: Image
        self.unlimited_materials: bool
        self.unlimited_budget: bool
        self.__new_slot = False
        self.__stream = io.BytesIO()
        if fp is None:
            self.__new_slot = True  # The user is creating a new save slot.

        if fp is not None and deserialize_on_init:
            self._deserialize()

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

    def __read_int64(self):
        return struct.unpack("<q", self.__read_bytes(8))[0]

    def __read_float(self) -> float:
        return struct.unpack("<f", self.__read_bytes(4))[0]

    def __read_string(self) -> str:
        num = self.__read_int8()
        if num < 0:
            return ""
        if num == 0:
            num2 = self.__read_int32()
            return self.__read_bytes(num2).decode("utf-8")
        if num == 1:
            num2 = self.__read_int32()
            num3 = num2 * 2
            return self.__read_bytes(num3).decode("utf-16")
        return ""

    def __read_vector3(self) -> datatypes.Vec3:
        x = self.__read_float()
        y = self.__read_float()
        z = self.__read_float()

        return datatypes.Vec3(x, y, z)

    def __read_vector2(self) -> datatypes.Vec2:
        return datatypes.Vec2(
            self.__read_float(),
            self.__read_float()
        )

    def __read_quat(self) -> datatypes.Quaternion:
        return datatypes.Quaternion(
            self.__read_float(),
            self.__read_float(),
            self.__read_float(),
            self.__read_float()
        )

    def __read_color(self) -> datatypes.Color:
        return datatypes.Color(
            self.__read_int8() / 255.0,
            self.__read_int8() / 255.0,
            self.__read_int8() / 255.0,
            1.0
        )

    @staticmethod
    def _assert_type(got: constants.BinaryEntryType, expected: constants.BinaryEntryType):
        if not got == expected:
            raise exceptions.UnexpectedTypeError(got, expected)

    @staticmethod
    def _assert_name(got: str, expected: str):
        if got != expected:
            raise exceptions.UnexpectedNameError(got, expected)

    @staticmethod
    def _assert_node_id(got: int, expected: int):
        if got != expected:
            raise exceptions.WrongNodeError(got, expected)

    def _read_entry_type(self, expect_name=None, expect_type=None) -> list:
        type_ = int.from_bytes(self.__read_byte(), byteorder="little", signed=False)
        tn = constants.BinaryEntryType(type_)
        if expect_type is not None:
            self._assert_type(tn, expect_type)
        name = None
        if "Named" in tn.name:
            name = self.__read_string()
            if expect_name is not None:
                self._assert_name(name, expect_name)

        return [tn, name]

    def _read_type_entry(self, expect_assembly=None, expect_typename=None) -> list[str, str]:
        num = int.from_bytes(self.__read_byte(), byteorder="little", signed=False)
        if num < 0:
            return []
        num = constants.BinaryEntryType(num)
        if num == constants.BinaryEntryType.TypeName:
            key = self.__read_int32()
            type_and_assembly = self.__read_string().split(", ")
            typename = type_and_assembly[0]
            assembly = type_and_assembly[1]

            if expect_assembly is not None:
                self._assert_name(assembly, expect_assembly)
            if expect_typename is not None:
                self._assert_name(typename, expect_typename)

            return [assembly, typename]
        elif num == constants.BinaryEntryType.TypeID:
            # we'll just assume there's an override built into the deserializer
            pass
        else:
            raise ValueError("Unexpected type entry: " + str(num))

    def _deserialize(self):
        self._read_entry_type(expect_type=constants.BinaryEntryType.UnnamedStartOfReferenceNode)  # Primary node
        # BridgeSaveSlotData type
        self._read_type_entry(
            expect_typename="BridgeSaveSlotData",
            expect_assembly="Assembly-CSharp"
        )
        # Node ID
        self._assert_node_id(self.__read_int32(), 0)

        # Version
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedInt, expect_name="m_Version")
        self.version = self.__read_int32()

        # Physics Version
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedInt, expect_name="m_PhysicsVersion")
        self.physics_version = self.__read_int32()

        # Slot ID
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedInt, expect_name="m_SlotID")
        self.slot_id = self.__read_int32()

        # Display Name
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedString, expect_name="m_DisplayName")
        self.display_name = self.__read_string()

        # File Name
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedString, expect_name="m_SlotFilename")
        self.file_name = self.__read_string()

        # Budget
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedInt, expect_name="m_Budget")
        self.budget = self.__read_int32()

        # Last write time in C# ticks
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedLong, expect_name="m_LastWriteTimeTicks")
        self.last_write_time = self.__read_int64()

        # Bridge
        self._read_entry_type(expect_type=constants.BinaryEntryType.NamedStartOfReferenceNode, expect_name="m_Bridge")
        self._read_type_entry(expect_assembly="mscorlib", expect_typename="System.Byte[]")
        self._assert_node_id(self.__read_int32(), 1)  # Node ID should be 1

        self._read_entry_type(expect_type=constants.BinaryEntryType.PrimitiveArray)
        num = self.__read_int32()
        num2 = self.__read_int32()
        num3 = num * num2
        _bridge = self.__read_bytes(num3)
        bridge_version = int.from_bytes(_bridge[0:4], byteorder="little", signed=False)
        _bridge = _bridge[4:]
        self.bridge = sandbox.Layout(_bridge, deserialize_on_init=False).deserialize_bridge(bridge_version)

        self._read_entry_type(constants.BinaryEntryType.EndOfNode)

        # Thumbnail
        tn = constants.BinaryEntryType(self.__read_int8())
        self._assert_name(self.__read_string(), "m_Thumb")
        if tn == constants.BinaryEntryType.NamedNull:
            # No thumbnail
            self.thumbnail = None
        elif tn == constants.BinaryEntryType.NamedStartOfReferenceNode:
            self._assert_type(constants.BinaryEntryType(self.__read_int8()), constants.BinaryEntryType.TypeID)
            self.__read_int32()  # we don't care about the type ID
            self._assert_node_id(self.__read_int32(), 2)

            self._read_entry_type(expect_type=constants.BinaryEntryType.PrimitiveArray)
            num = self.__read_int32()
            num2 = self.__read_int32()
            num3 = num * num2
            self.thumbnail = Image.open(io.BytesIO(self.__read_bytes(num3)))

            self._assert_type(constants.BinaryEntryType(self.__read_int8()), constants.BinaryEntryType.EndOfNode)
        else:
            raise exceptions.UnexpectedTypeError(tn, constants.BinaryEntryType.NamedStartOfReferenceNode)

        # Unlimited materials
        self._read_entry_type(
            expect_type=constants.BinaryEntryType.NamedBoolean,
            expect_name="m_UsingUnlimitedMaterials"
        )
        self.unlimited_materials = self.__read_bool()

        # Unlimited budget
        self._read_entry_type(
            expect_type=constants.BinaryEntryType.NamedBoolean,
            expect_name="m_UsingUnlimitedBudget"
        )
        self.unlimited_budget = self.__read_bool()

        # End of primary node
        self._assert_type(constants.BinaryEntryType(self.__read_int8()), constants.BinaryEntryType.EndOfNode)

    def __write_bytes(self, value):
        self.__stream.write(value)

    def __write_int8(self, value):
        self.__stream.write(value.to_bytes(1, byteorder="little"))

    def __write_bool(self, value):
        self.__stream.write(b"\x01" if value else b"\x00")

    def __write_int16(self, value):
        self.__stream.write(value.to_bytes(2, byteorder="little"))

    def __write_int32(self, value):
        self.__stream.write(value.to_bytes(4, byteorder="little"))

    def __write_int64(self, value):
        self.__stream.write(value.to_bytes(8, byteorder="little"))

    def __write_float(self, value):
        self.__stream.write(struct.pack("<f", value))

    def __write_string(self, value):
        self.__write_int8(0)
        self.__write_int32(len(value))
        self.__write_bytes(value.encode("utf-8"))

    def __write_vec2(self, value):
        self.__write_float(value.x)
        self.__write_float(value.y)

    def __write_vec3(self, value):
        self.__write_float(value.x)
        self.__write_float(value.y)
        self.__write_float(value.z)

    def __write_quat(self, value):
        self.__write_float(value.x)
        self.__write_float(value.y)
        self.__write_float(value.z)
        self.__write_float(value.w)

    def __write_color(self, value):
        self.__write_int8(value.r * 255)
        self.__write_int8(value.g * 255)
        self.__write_int8(value.b * 255)

    def _serialize(self):
        # Start of primary node
        self.__write_int8(constants.BinaryEntryType.UnnamedStartOfReferenceNode.value)
        # Type name byte
        self.__write_int8(constants.BinaryEntryType.TypeName.value)
        # Node ID
        self.__write_int32(0)
        # Type name
        self.__write_string("BridgeSaveSlotData, Assembly-CSharp")
        # no idea
        self.__write_int32(0)

        # Version
        self.__write_int8(constants.BinaryEntryType.NamedInt.value)
        self.__write_string("m_Version")
        self.__write_int32(constants.CURRENT_SLOT_VERSION)

        # Physics version
        self.__write_int8(constants.BinaryEntryType.NamedInt.value)
        self.__write_string("m_PhysicsVersion")
        self.__write_int32(constants.CURRENT_PHYSICS_VERSION)

        # Slot ID
        self.__write_int8(constants.BinaryEntryType.NamedInt.value)
        self.__write_string("m_SlotID")
        self.__write_int32(self.slot_id)

        # Display name
        self.__write_int8(constants.BinaryEntryType.NamedString.value)
        self.__write_string("m_DisplayName")
        self.__write_string(self.display_name)

        # Filename
        self.__write_int8(constants.BinaryEntryType.NamedString.value)
        self.__write_string("m_SlotFilename")
        self.__write_string(self.file_name)

        # Budget
        self.__write_int8(constants.BinaryEntryType.NamedInt.value)
        self.__write_string("m_Budget")
        self.__write_int32(self.budget)

        # Last write time
        self.__write_int8(constants.BinaryEntryType.NamedLong.value)
        self.__write_string("m_LastWriteTimeTicks")
        self.__write_int64(self.last_write_time)

        # Bridge
        self.__write_int8(constants.BinaryEntryType.NamedStartOfReferenceNode.value)
        self.__write_string("m_Bridge")
        self.__write_int8(constants.BinaryEntryType.TypeName.value)
        self.__write_int32(1)  # Type ID?
        self.__write_string("System.Byte[], mscorlib")
        self.__write_int32(1)  # Node ID
        self.__write_int8(constants.BinaryEntryType.PrimitiveArray.value)

        # Serialize bridge data
        sr = sandbox.Layout()
        sr.bridge = self.bridge
        sr.serialize_bridge()
        sr.output_stream.seek(0)
        bridge_data = sr.output_stream.read()
        self.__write_int32(len(bridge_data))
        self.__write_int32(1)
        self.__write_bytes(bridge_data)

        # End of bridge node
        self.__write_int8(constants.BinaryEntryType.EndOfNode.value)

        # Thumbnail
        if self.thumbnail is None:
            # No thumbnail
            self.__write_int8(constants.BinaryEntryType.NamedNull.value)
            self.__write_string("m_Thumb")
        else:
            # Thumbnail
            self.__write_int8(constants.BinaryEntryType.NamedStartOfReferenceNode.value)
            self.__write_string("m_Thumb")
            self.__write_int8(constants.BinaryEntryType.TypeID.value)
            self.__write_int32(1)
            self.__write_int32(2)

            thumb_data = io.BytesIO()
            self.thumbnail.save(thumb_data, format="PNG")
            thumb_data.seek(0)
            thumb_data = thumb_data.read()

            self.__write_int8(constants.BinaryEntryType.PrimitiveArray.value)
            self.__write_int32(len(thumb_data))
            self.__write_int32(1)
            self.__write_bytes(thumb_data)

            self.__write_int8(constants.BinaryEntryType.EndOfNode.value)

        # Using unlimited materials
        self.__write_int8(constants.BinaryEntryType.NamedBoolean.value)
        self.__write_string("m_UsingUnlimitedMaterials")
        self.__write_bool(self.unlimited_materials)

        # Using unlimited budget
        self.__write_int8(constants.BinaryEntryType.NamedBoolean.value)
        self.__write_string("m_UsingUnlimitedBudget")
        self.__write_bool(self.unlimited_budget)

        # End of primary node
        self.__write_int8(constants.BinaryEntryType.EndOfNode.value)

    def save(self, path: Union[str, None]):
        """
        Saves the slot to a file.
        :param path: The path to save to. Leave this to None
        """
        self._serialize()
        if path is None:
            path = self.path
            if path is None:
                raise ValueError("Path may not be none when saving a newly created slot.")

        with open(path, "wb") as f:
            self.__stream.seek(0)
            f.write(self.__stream.read())

    def serialize_to_bytes(self):
        """
        Serialize the slot to an io.BytesIO object.
        """
        self._serialize()
        self.__stream.seek(0)
        return self.__stream.read()
