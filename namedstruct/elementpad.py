"""StarStruct element class."""

import struct
import re

from starstruct.element import register, Element
from starstruct.modes import Mode


@register
class ElementPad(Element):
    """
    The basic StarStruct element class.
    """

    def __init__(self, field, mode=Mode.Native, alignment=1):
        """Initialize a StarStruct element object."""

        # All of the type checks have already been performed by the class
        # factory

        # Pad elements effectively have no name
        self.name = None

        # The ref attribute is required for all elements, but the base element
        # type does not have one
        self.ref = None

        self._mode = mode

        # Strictly speaking, a non-byte aligned message probably wouldn't have
        # explicit padding fields, and if it does they probably wouldn't be
        # unaligned, but however rare that case might be we need to ensure that
        # this field is properly aligned also.
        self._alignment = alignment

        # Validate that the format specifiers are valid struct formats, this
        # doesn't have to be done now because the format will be checked when
        # any struct functions are called, but it's better to inform the user of
        # any errors earlier.
        # The easiest way to perform this check is to create a "Struct" class
        # instance, this will also increase the efficiency of all struct related
        # functions called.
        self.format = mode.value + field[1]
        self._struct = struct.Struct(self.format)

    @staticmethod
    def valid(field):
        """
        Validation function to determine if a field tuple represents a valid
        base element type.

        The basics have already been validated by the Element factory class,
        validate the specific struct format now.
        """
        return len(field) == 2 \
            and isinstance(field[1], str) \
            and re.match(r'\d*x', field[1])

    def validate(self, msg):
        """
        Ensure that the supplied message contains the required information for
        this element object to operate.

        The "padding" element requires no further validation.
        """
        pass

    def update(self, mode=None, alignment=None):
        """change the mode of the struct format"""
        if alignment:
            self._alignment = alignment

        if mode:
            self._mode = mode
            self.format = mode.value + self.format[1:]
            # recreate the struct with the new format
            self._struct = struct.Struct(self.format)

    def pack(self, msg):
        """Pack the provided values into the supplied buffer."""
        data = self._struct.pack()

        # If the data does not meet the alignment, add some padding
        missing_bytes = len(data) % self._alignment
        if missing_bytes:
            data += b'\x00' * missing_bytes
        return data

    def unpack(self, msg, buf):
        """Unpack data from the supplied buffer using the initialized format."""
        # Remember to remove any alignment-based padding
        extra_bytes = self._alignment - 1 - (struct.calcsize(self.format) %
                                             self._alignment)
        unused = buf[struct.calcsize(self.format) + extra_bytes:]
        return (None, unused)

    def make(self, msg):
        """This shouldn't be called, but if called it returns nothing."""
        return None
