# game_logic.py

class ChineseWordGame:
    MAX_TRIES = 8

    def __init__(self, sentence, hint=""):
        """Initialize game with a Chinese sentence and optional hint"""
        self.sentence = sentence
        self.hint = hint
        self.guessed_chars = set()
        self.tries_remaining = self.MAX_TRIES
        self.game_over = False
        self._won = False

        # Remove spaces and punctuation for gameplay
        self.playing_chars = [char for char in self.sentence if char.strip() and not self._is_punctuation(char)]

    @staticmethod
    def _is_punctuation(char):
        """Check if a character is punctuation or space"""
        return char in "。，！？、．；：" "〝〞…—（）《》【】" or char.isspace()

    @classmethod
    def from_state(cls, state):
        """Recreate game instance from a saved state"""
        if not state or 'sentence' not in state:
            return None

        game = cls(state['sentence'], state.get('hint', ''))
        game.guessed_chars = set(state.get('guessed_chars', []))
        game.tries_remaining = state.get('tries_remaining', cls.MAX_TRIES)
        game.game_over = state.get('game_over', False)
        game._won = state.get('won', False)
        return game

    def make_guess(self, char):
        """
        Process a guess and return a tuple of (is_valid, is_correct, message)
        """
        if self.game_over:
            return False, False, "游戏结束！Game over!"

        # Validate input
        if not char or not isinstance(char, str):
            return False, False, "无效输入！Invalid input!"

        if len(char) != 1:
            return False, False, "请输入一个汉字！Please enter a Chinese character!"

        # Check if character was already guessed
        if char in self.guessed_chars:
            return False, False, f"你已经猜过 '{char}' 了！You've guessed '{char}'."

        # Process the guess
        self.guessed_chars.add(char)

        if char not in self.playing_chars:
            self.tries_remaining -= 1
            if self.tries_remaining == 0:
                self.game_over = True
                return True, False, f"'{char}'这个字不在句子中！游戏结束！The character '{char}' is not in the sentence. Game over!"
            return True, False, f"'{char}'这个字不在句子中！The character '{char}' is not in the sentence."

        # Check if won
        if self._is_sentence_complete():
            self.game_over = True
            self._won = True
            return True, True, "恭喜你猜对了！You got it right!"

        return True, True, f"正确！'{char}'这个字在句子中！The character '{char}' is in the sentence."

    def _is_sentence_complete(self):
        """Check if all characters in the sentence have been guessed"""
        return all(char in self.guessed_chars or self._is_punctuation(char)
                   for char in self.sentence)

    def get_display_sentence(self):
        """Return the sentence with unguessed characters hidden"""
        return ''.join(char if char in self.guessed_chars or self._is_punctuation(char)
                       else '_ ' for char in self.sentence)

    def get_game_state(self):
        """Return the current game state as a dictionary"""
        return {
            'sentence': self.sentence,
            'hint': self.hint,
            'display_sentence': self.get_display_sentence(),
            'guessed_chars': sorted(list(self.guessed_chars)),
            'tries_remaining': self.tries_remaining,
            'game_over': self.game_over,
            'won': self._won,
            'max_tries': self.MAX_TRIES
        }