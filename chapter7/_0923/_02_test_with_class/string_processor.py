class StringProcessor:

    def reverse(self, text):
        """문자열을 반전합니다"""
        return text[::-1]

    def count_vowels(self, text):
        """모음(a, e, i, o, u) 개수를 셉니다"""
        return sum(1 for char in text.lower() if char in 'aeiou')

    def is_palindrome(self, text):
        """회문인지 확인합니다 (공백/대소문자 무시)"""
        cleaned = text.replace(" ", "").lower()
        return cleaned == cleaned[::-1]
