class String:
    @staticmethod
    def snake_to_camel_case(word: str):
        words = word.split('_')
        return words[0].capitalize() + ''.join(word.capitalize() for word in words[1:])