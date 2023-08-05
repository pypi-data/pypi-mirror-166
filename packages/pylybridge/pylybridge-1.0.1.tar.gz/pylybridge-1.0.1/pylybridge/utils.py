from __future__ import annotations
from PIL import Image, ImageDraw
from pylybridge import datatypes, constants
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pylybridge.sandbox  # Fix circular imports


def find_joint_from_guid(bridge: datatypes.Bridge, uuid: str) -> datatypes.BridgeJoint:
    for joint in bridge.joints:
        if joint.guid == uuid:
            return joint
    for anchor in bridge.anchors:
        if anchor.guid == uuid:
            return anchor
    raise ValueError(f"Could not find joint with guid '{uuid}'")


def get_material_color(material: constants.BridgeMaterialType) -> tuple[int, int, int]:
    # TODO make this simpler
    if material == constants.BridgeMaterialType.ROAD:
        return 93, 67, 53
    elif material == constants.BridgeMaterialType.REINFORCED_ROAD:
        return 175, 98, 31
    elif material == constants.BridgeMaterialType.WOOD:
        return 227, 176, 110
    elif material == constants.BridgeMaterialType.STEEL:
        return 186, 93, 97
    elif material == constants.BridgeMaterialType.HYDRAULICS:
        return 9, 102, 214
    elif material == constants.BridgeMaterialType.ROPE:
        return 143, 96, 23
    elif material == constants.BridgeMaterialType.CABLE:
        return 47, 47, 52
    elif material == constants.BridgeMaterialType.BUNGEE_ROPE:
        return 227, 31, 217
    elif material == constants.BridgeMaterialType.SPRING:
        return 208, 175, 0
    else:
        raise ValueError(f"Unknown material type '{material}'")


def get_material_pixel_width(material: constants.BridgeMaterialType, scale: int) -> int:
    if material == constants.BridgeMaterialType.CABLE or material == constants.BridgeMaterialType.BUNGEE_ROPE:
        return scale // 32
    elif material == constants.BridgeMaterialType.SPRING:
        return scale // 16
    else:
        return scale // 8


def render_preview(
        layout: "pylybridge.sandbox.Layout",
        scale: int = 75,
        draw_grid: bool = False,
        antialias: bool = True
) -> Image.Image:
    """
    Render a thumbnail of the given layout.
    **This function does not currently function correctly.**
    Customizable.
    :param layout: The layout to render.
    :param scale: The scale of the preview. Default: 75.
    :param draw_grid: Whether to draw the grid. Default: True. Please note that this is quite slow,
    uses a lot of memory and CPU, and should only be used when necessary.
    :param antialias: Whether to use antialiasing. Default: True.
    """

    bg_col: datatypes.Color = datatypes.Color(43, 70, 104, 1)

    bg_col_t = bg_col.to_tuple()[:3]  # Remove alpha

    # Add padding and scale to size
    width, height = ((int(i) * ((scale * 4 * 4) if draw_grid else scale)) + 20 for i in layout.get_dimensions())

    print(width, height, scale * 4 * 4)

    rescale = (scale * 4 * 4) if draw_grid else scale

    im = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, width, height), fill=bg_col_t)

    # draw gridlines
    # unfortunately, we can't use rgba for this, so we have to use a darker color than the background
    # TODO: optimize this, it's really slow
    if draw_grid:
        for i in range(0, width, scale * 4 * 4):
            draw.rectangle((i, 0, i + 5, height), fill=(31, 51, 76))
            for j in range(0, i, scale * 4):
                draw.rectangle((j, 0, j + 2, height), fill=(31, 51, 76))
                for k in range(0, j, scale):
                    draw.rectangle((k, 0, k + 1, height), fill=(31, 51, 76))
        for i in range(0, height, scale * 4 * 4):
            draw.rectangle((0, i, width, i + 5), fill=(31, 51, 76))
            for j in range(0, i, scale * 4):
                draw.rectangle((0, j, width, j + 2), fill=(31, 51, 76))
                for k in range(0, j, scale):
                    draw.rectangle((0, k, width, k + 1), fill=(31, 51, 76))

    def realval(val: int | float) -> int:
        return int(val) * rescale // 2

    # draw terrain stretches
    for stretch in layout.terrain_stretches:
        # TODO: implement better
        # for now, we just draw a rectangle
        draw.rectangle(
            (
                realval(stretch.pos.x),
                realval(stretch.pos.y),
                realval(stretch.pos.x - 25.25),
                realval(stretch.pos.y - 5),
            ),
            outline=(255, 255, 255),
            width=10
        )

    # anchors
    for anchor in layout.anchors:
        draw.rectangle(
            (
                realval(anchor.pos.x),
                realval(anchor.pos.y),
                realval(anchor.pos.x) + (rescale // 10),
                realval(anchor.pos.y) + (rescale // 10)
            ),
            fill=(255, 0, 0),
            outline=(0, 0, 0)
        )

    # bridge
    # edges (aka pieces) represented by lines colored according to their material
    for edge in layout.bridge.edges:
        color = get_material_color(edge.material_type)
        start_pos = find_joint_from_guid(layout.bridge, edge.node_a_guid).pos
        end_pos = find_joint_from_guid(layout.bridge, edge.node_b_guid).pos
        draw.line(
            (
                realval(start_pos.x) + (rescale // 20),
                realval(start_pos.y) + (rescale // 20),
                realval(end_pos.x) + (rescale // 20),
                realval(end_pos.y) + (rescale // 20)
            ),
            fill=color,
            width=rescale // 32
        )

    # joints represented by yellow circles
    for joint in layout.bridge.joints:
        draw.ellipse(
            (
                realval(joint.pos.x),
                realval(joint.pos.y),
                realval(joint.pos.x) + (rescale // 10),
                realval(joint.pos.y) + (rescale // 10)
            ),
            fill=(255, 255, 0),
            outline=(0, 0, 0)
        )

    # custom shapes
    # sort by z position
    custom_shapes = sorted(layout.custom_shapes, key=lambda x: x.pos.z)
    for shape in custom_shapes:
        # draw based on points
        for i in range(len(shape.points_local_space)):
            point = shape.points_local_space[i]
            next_point = shape.points_local_space[(i + 1) % len(shape.points_local_space)]
            draw.line(
                (
                    realval(shape.pos.x + point.x),
                    realval(shape.pos.y + point.y),
                    realval(shape.pos.x + next_point.x),
                    realval(shape.pos.y + next_point.y)
                ),
                fill=(int(shape.color.r * 255), int(shape.color.g * 255), int(shape.color.b * 255)),
                width=2
            )

    # anti-aliasing and scaling
    im = im.resize(
        (im.size[0] // ((scale // 8) if draw_grid else 2), im.size[1] // ((scale // 8) if draw_grid else 2)),
        Image.ANTIALIAS if (antialias or draw_grid) else Image.NEAREST,
    )

    return im


def parse_budget(budget: str) -> int:
    """
    Parse a budget string into an integer.
    :param budget: The budget string. Example: "$1,000,000"
    :return: The budget integer.
    """

    if budget == "":
        return 0
    elif budget == "∞" or budget == "Unlimited":
        return 10000000
    else:
        try:
            return int(budget.replace(",", "").replace("$", ""))
        except ValueError:
            return 0


def parse_resources(resources: str) -> list[constants.BridgeMaterialType]:
    """
    Parse a string of resources into a list of BridgeMaterialType objects.
    :param resources: The resources string. Example: "Road, Wood, Steel"
    :return: The list of BridgeMaterialType.
    """

    if resources == "":
        return []
    else:
        try:
            return [constants.BridgeMaterialType[resource.strip().upper()] for resource in resources.split(",")]
        except KeyError:
            return []
