from svgwrite.base import BaseElement

from chalk.types import Diagram, Primitive, Empty

def to_svg(diagram: Diagram) -> BaseElement:
    if isinstance(diagram, Primitive):
        pass
    elif isinstance(diagram, Emtpy):
        pass
    else:
        assert False
