import unittest
import itertools
from snap import Card, Deck, Matcher, ExactMatcher, SuiteMatcher, ValueMatcher, Suite, Value

import snap

exact_match = Card(Suite.CLUBS, Value.ONE), Card(Suite.CLUBS, Value.ONE)
value_match = Card(Suite.CLUBS, Value.ONE), Card(Suite.HEARTS, Value.ONE)
suite_match = Card(Suite.CLUBS, Value.ONE), Card(Suite.CLUBS, Value.TWO)
no_match = Card(Suite.CLUBS, Value.ONE), Card(Suite.DIAMONDS, Value.TWO)


class CardTest(unittest.TestCase):
    def testEquality(self):
        self.assertEqual(*exact_match)
        self.assertNotEqual(*value_match)
        self.assertNotEqual(*suite_match)

    def testHash(self):
        self.assertEqual(*[hash(x) for x in exact_match])
        self.assertNotEqual(*[hash(x) for x in value_match])
        self.assertNotEqual(*[hash(x) for x in suite_match])
        self.assertNotEqual(*[hash(x) for x in no_match])


class MatcherTest(unittest.TestCase):
    def testExactMatcher(self):
        self.matcherTest(ExactMatcher(), (True, False, False), (exact_match, value_match, suite_match))

    def testValueMatcher(self):
        self.matcherTest(ValueMatcher(), (True, True, False), (value_match, exact_match, suite_match))

    def testSuiteMatcher(self):
        self.matcherTest(SuiteMatcher(), (True, True, False), (suite_match, exact_match, value_match))

    def matcherTest(self, matcher, expected, tests):
        for (i, test) in zip(expected, tests):
            self.assertEqual(i, matcher.match(*test))


class DeckTest(unittest.TestCase):
    def testDeckCreation(self):
        deck = Deck(1)
        self.assertEqual(len(deck.cards), 52)
        card_set = set()
        for card in deck:
            card_set.add(card)
        self.assertEqual(len(card_set), 52)

    def testShuffle(self):
        pass

class CardPlayTest(unittest.TestCase):
    def testCardPlay(self):
        deck = Deck(1);
        # Pretty much checking it doesn't crash; Given it's written to return a random winner,
        # it's kinda hard to check it's working correctly!
        snap.play_cards(deck, ExactMatcher())

if __name__ == "__main__":
    unittest.main()