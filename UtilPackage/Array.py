import collections.abc


class Array:
    @staticmethod
    def reverse(arr: list) -> list[str]:
        return list(map(str, arr))[::-1]

    @staticmethod
    def to_string(arr: list) -> list[str]:
        return list(map(str, arr))

    @staticmethod
    def is_array(arr: any) -> bool:
        return isinstance(arr, collections.abc.Sequence)
