from pydantic import BaseModel, Field


class RegisterField(BaseModel):
    """Represents a field within a register."""

    name: str = Field(description="The name of the field within the register")
    bit_offset: int = Field(description="The bit offset of the field within the register")
    bit_width: int = Field(description="The width of the field in bits")
    description: None | str = Field(default=None, description="A description of the field's purpose or functionality")
    access: str = Field(
        default="RW",
        description="The access type of the field: RW (read-write), RO (read-only), WO (write-only)",
    )
    default: None | int = Field(default=None, description="The default value of the field, if applicable")


class Register(BaseModel):
    """Represents a register in the datasheet."""

    name: str = Field(description="The name of the register")
    address: int = Field(description="The address of the register")
    description: None | str = Field(
        default=None, description="A description of the register's purpose or functionality"
    )
    fields: list[RegisterField] = Field(description="A list of fields contained within the register")


class DriverModel(BaseModel):
    """Represents the entire driver model."""

    name: str = Field(description="The name of the driver")
    description: None | str = Field(default=None, description="A description of the driver")
    registers: list[Register] = Field(description="A list of registers defined in the driver")
