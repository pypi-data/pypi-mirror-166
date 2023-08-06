"""Implementation of the `Choice` type."""

from abc import ABCMeta
from typing import Any, Iterator, Type


class FrozenError(Exception):
    """Thrown when attempting to modify a frozen `Choice`."""


class Variant:
    """Representative object for a choice type variant."""

    def __init__(self, choice: Type["Choice"], name: str) -> None:
        self.choice = choice
        self.name = name

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.choice.__name__}, {repr(self.name)})"


class ChoiceMeta(ABCMeta):
    """Metaclass to assist in the construction of new `Choice` subtypes."""

    __variants__: set[str]

    def __new__(
        cls: type,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        frozen: bool = True,
        **kwargs: Any,
    ) -> Type["Choice"]:
        namespace.update({"__variants__": set(), "__frozen__": frozen})
        choice_class: Type[Choice] = super().__new__(cls, name, bases, namespace, **kwargs)  # type: ignore

        for base in reversed(choice_class.mro()):
            for attr_name in vars(base).get("__annotations__", {}):
                # Do not overwrite user-defined special methods
                if attr_name.startswith("__"):
                    continue

                # Variants are mutually exclusive: a choice type can only be
                # instantiated with exactly one of its variants. If default values are
                # specified for multiple variants, the behavior would be incorrect.
                #
                # In principle, it might be reasonable to define a default value for
                # exactly one of the variants. But that'll require some further thought.
                # For now, default values are simply disallowed entirely.
                if attr_name in namespace:
                    raise ValueError(
                        f"A default value was assigned to attribute '{attr_name}', but "
                        "this is not permitted for Choice types."
                    )

                choice_class.__variants__.add(attr_name)
                variant = Variant(choice=choice_class, name=attr_name)
                setattr(choice_class, attr_name, variant)

        return choice_class

    def __iter__(cls) -> Iterator[Variant]:
        for variant in sorted(cls.__variants__):
            yield getattr(cls, variant)

    def __len__(cls) -> int:
        return len(cls.__variants__)


class Choice(metaclass=ChoiceMeta):
    """Basic type for a value matching one of multiple variants."""

    __choice__: str
    __frozen__: bool
    __variants__: set[str]

    def __init__(self, **kwargs: Any) -> None:
        if len(kwargs) < 1:
            if len(self.__variants__) == 0:
                return
            raise ValueError("A variant value is required, but none were provided.")

        if len(kwargs) > 1:
            raise ValueError(
                "Multiple variant values were provided, but only one is permitted."
            )

        argument, value = kwargs.popitem()
        if argument not in self.__variants__:
            raise ValueError(
                f"Provided argument '{argument}' is not a valid variant for this type."
            )
        setattr(self, argument, value)

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in self.__variants__:
            super().__setattr__(name, value)

        elif not hasattr(self, "__choice__"):
            super().__setattr__("__choice__", name)
            super().__setattr__(name, value)

        elif self.__frozen__:
            raise FrozenError(
                "Cannot overwrite variants when 'frozen=True'. To enable mutability, "
                "pass 'frozen=False' to the class constructor. See the documentation "
                "for examples."
            )

        else:
            delattr(self, self.__choice__)
            delattr(self, "__choice__")
            setattr(self, name, value)

    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)

        # Do not allow access to the variant class attributes once this choice type has
        # been instantiated, otherwise match statements will not work correctly.
        if (
            name in super().__getattribute__("__variants__")
            and super().__getattribute__("__choice__") != name
        ):
            raise AttributeError(
                f"'{type(self).__name__}' instance has no attribute '{name}' because it"
                f" was defined with variant '{self.__choice__}' instead."
            )

        return value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return getattr(self, self.__choice__) == getattr(other, other.__choice__)  # type: ignore

        if isinstance(other, Variant):
            return other.choice is type(self) and other.name == self.__choice__

        raise NotImplementedError(
            f"Cannot compare choice type '{type(self).__name__}' with"
            f" '{type(other).__name__}'."
        )

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}({self.__choice__}={repr(getattr(self, self.__choice__))})"
        )
