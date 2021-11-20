import unittest
from lss import longest_subsequence, _array_for_mask, _brute_force_is_subseq_of, _dynamic_is_subseq_of


class TestLongestSubsequence(unittest.TestCase):
#    @unittest.SkipTest
    def test_torture(self):
        longest_subsequence(
            """
            "It hit the ground right beside his heel and he was hit by sparks and felt a burning feeling - but luckily it only burned his sock.
            
            "He was more worried about whether his goal still counted."
            
            Fans realised the firework came from a nearby house and asked the owners to stop their display, he said.
            
            Mr Hughes-Mason said the referee stopped the match initially for 10 minutes and then decided to abandon the match as "there were still a fair few fireworks in the sky".
            
            Hashtag United were set up five years ago and moved into non-league football in 2018.
            
            Essex Police has been approached for comment.
            """, """
            Once we understand what the Python interpreter is doing, we can make better sense of the example at the beginning of this blog post, where we opened a file in the with statement: File objects expose their own __enter__ and __exit__ methods, and can therefore act as their own context managers. Specifically, the __exit__ method closes the file.
            Exception Handling
            
            Returning to the drawing example, what happens if an exception occurs within the nested code block? For example, suppose we mistakenly passed the wrong number of arguments to the rectangle call. In that case, the steps taken by the Python interpreter would be:
            
            The rectangle method raises a TypeError exception: “Context.rectangle() takes exactly 4 arguments.”
            The with statement catches this exception.
            The with statement calls __exit__ on the Saved object. It passes information about the exception in three arguments: (type, value, traceback) – the same values you’d get by calling sys.exc_info. This tells the __exit__ method everything it could possibly need to know about the exception that occurred.
            In this case, our __exit__ method does not particularly care. It calls restore on the cairo context anyway, and returns None. (In Python, when no return statement is specified, the function actually returns None.)
            The with statement checks to see whether this return value is true. Since it isn’t, the with statement re-raises the TypeError exception to be handled by someone else.
            """)

    def test_longest_subsequence(self):
        happy_paths = [
            ("abcde", "cdefg", 3),
            ("abcde", "fghij", 0),
            ("abcde", "abcde", 5),
            ("abcde", "", 0),
            ("abc", "a b c", 3),
            ("abc", "abcdefabc", 3),
            ("abcd", "abcaaaabcd", 4)
        ]

        for (a, b, longest) in happy_paths:
            with self.subTest(a=a, b=b, longest=longest):
                self.assertEqual(longest_subsequence(a, b), longest)
                self.assertEqual(longest_subsequence(b, a), longest)

    def test_array_for_mask(self):
        test_array = [1, 2, 3, 4, 5]
        happy_paths = [
            (0b00000, []),
            (0b00001, [1]),
            (0b00100, [3]),
            (0b00101, [1, 3]),
            (0b10000, [5]),
            (0b11111, test_array)
        ]

        for (mask, result_arr) in happy_paths:
            with self.subTest(mask=mask, result_arr=result_arr):
                self.assertEqual(_array_for_mask(test_array, mask), result_arr)

    def test_is_subseq_of(self):
        test_array = [1, 2, 3, 4, 5]
        happy_paths = [
            ([], True),
            ([1, 2], True),
            (test_array, True),
            ([1, 3, 5], True),
            ([1], True),
            ([5], True),
            ([2, 1], False),
            ([2, 6], False),
            ([2, 2], False),
            ([6], False),
            (test_array + test_array, False),
        ]

        for (subseq, result) in happy_paths:
            with self.subTest("Brute force subseq", subseq=subseq, result=result):
                self.assertEqual(_brute_force_is_subseq_of(subseq, test_array), result)
            with self.subTest("Dynamic subseq", subseq=subseq, result=result):
                self.assertEqual(_dynamic_is_subseq_of(subseq, 0, test_array) > -1, result)


if __name__ == "__main__":
    print("running main")
    unittest.main()
