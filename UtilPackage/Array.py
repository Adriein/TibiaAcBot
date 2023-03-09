class Array:
    @staticmethod
    def reverse(arr: list) -> list[str]:
        return list(map(str, arr))[::-1]
