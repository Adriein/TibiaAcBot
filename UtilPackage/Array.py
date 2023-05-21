from typing import TypeVar

T = TypeVar('T')

class Array:
    @staticmethod
    def reverse(arr: list) -> list[str]:
        return list(map(str, arr))[::-1]

    @staticmethod
    def to_string(arr: list) -> list[str]:
        return list(map(str, arr))

    @staticmethod
    def is_array(arr: any) -> bool:
        return isinstance(arr, list)

    @staticmethod
    def chunk(arr: list[T], size) -> list[list[T]]:
        result = []
        for i in range(0, len(arr), size):
            result.append(arr[i:i + size])

        return result
