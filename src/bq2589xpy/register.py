import collections


class BitField:
    def __init__(
        self,
        width: int = 1,
        default: int | None = None,
    ) -> None:
        self.width = width
        self.offset = 0
        self.mask = (1 << self.width) - 1
        self.default = default

    def __get__(self, obj, _):
        if obj is None:
            # instance attribute accessed on class, return self
            return self
        return (obj._value >> self.offset) & self.mask

    def __set__(self, obj, value):
        obj._value &= ~(self.mask << self.offset)
        obj._value |= (value & self.mask) << self.offset


class RegisterMeta(type):
    """For setting bit offset based on fields order"""

    @classmethod
    def __prepare__(metacls, name, bases):
        # for older python versions, where dict order wasn't guaranteed
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace):
        offset = 0
        fields = []
        for field_name, value in namespace.items():
            if isinstance(value, BitField):
                fields.append(field_name)
                value.offset = offset
                offset += value.width

        new_cls = super().__new__(cls, name, bases, namespace)
        new_cls.size = offset
        new_cls._fields_ = tuple(fields)
        return new_cls


class Register(metaclass=RegisterMeta):
    _fields_: tuple[str] = ()
    size: int = 0

    def __init__(self, value: int = 0) -> None:
        self._value = value

    def __repr__(self) -> str:
        bits = " ".join(f"{f}:0b{getattr(self, f):b}" for f in self._fields_)
        return f"<{type(self).__name__} value=0x{self._value:02X}, 0b{self._value:b}>: {bits}"

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        self._value = val

    def address() -> int:
        raise NotImplementedError


if __name__ == "__main__":

    class Reg0(Register):
        # Fields declared in the desired order.
        FLAG = BitField(1)
        SOME_SETTING = BitField(5)
        AND_ONE_MORE = BitField(1)

    r0 = Reg0(0b101010)
    print(r0)
    r0.FLAG = 1
    r0.SOME_SETTING = 0b11101

    assert r0.value == 0b0111011
