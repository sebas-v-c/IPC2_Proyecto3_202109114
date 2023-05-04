import re
import string
import copy

from flask.scaffold import _matching_loader_thinks_module_is_package


class MessageStats:
    def __init__(
        self,
        username: str,
        date: str,
        time: str,
        message: str,
        profiles_list: list,
    ) -> None:
        self.username = username
        self.profiles = dict.fromkeys(profiles_list, 0)
        self.profile_list = profiles_list
        self.date = date
        self.time = time
        self.message = message
        self.word_list = []

    def remove_words(self, to_remove: list) -> None:
        text = re.sub(r"\s+", " ", self.message)
        regex = re.compile("[%s]" % re.escape(string.punctuation))
        text = regex.sub("", text)
        text = re.sub(r"\b\d+\b", "", text)
        words = text.lower().split()

        for word in to_remove:
            new_list = [item for item in words if item != word]
            words = new_list

        self.word_list = words

    def process_statistics(self, profile_list: list):
        total = len(self.word_list)
        for profile in profile_list:
            # using a dictionary is such an awful design, I should chage this later
            prof_name = profile["name"]
            keyword_list = profile["keywords"]
            word_list = copy.deepcopy(self.word_list)
            multi_word_list = list(
                filter(lambda x: True if len(x.split()) > 1 else False, keyword_list)
            )
            one_word_list = list(
                filter(lambda x: False if len(x.split()) > 1 else True, keyword_list)
            )
            profile_count = 0

            index = 0
            # print(prof_name)
            while index < len(self.word_list):
                sum = 1
                for keyword in multi_word_list:
                    matched_word = self._compare_word_at(index, keyword)
                    if matched_word:
                        # print(self.word_list[index : index + matched_word])
                        profile_count += matched_word
                        sum = matched_word
                        break

                if sum != 1:
                    index += sum
                    continue

                for keyword in one_word_list:
                    matched_word = self._compare_word_at(index, keyword)
                    if matched_word:
                        # print(self.word_list[index : index + matched_word])
                        profile_count += 1
                        break

                index += sum

            self.profiles[prof_name] = (profile_count * 100) / total
            # print(self.profiles[prof_name])

    def _compare_word_at(self, start: int, word: str) -> int:
        ranged_word = " ".join(self.word_list[start : start + len(word.split())])
        if ranged_word == word.lower():
            return len(ranged_word.split())

        return 0
