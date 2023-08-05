# Standard Packages
import re
import time
import pickle
import logging

# External Packages
import torch

# Internal Packages
from src.utils.helpers import LRU, resolve_absolute_path
from src.utils.config import SearchType


logger = logging.getLogger(__name__)


class ExplicitFilter:
    # Filter Regex
    required_regex = r'\+"(\w+)" ?'
    blocked_regex = r'\-"(\w+)" ?'

    def __init__(self, filter_directory, search_type: SearchType, entry_key='raw'):
        self.filter_file = resolve_absolute_path(filter_directory / f"{search_type.name.lower()}_explicit_filter_entry_word_sets.pkl")
        self.entry_key = entry_key
        self.search_type = search_type
        self.word_to_entry_index = dict()
        self.cache = LRU()


    def load(self, entries, regenerate=False):
        if self.filter_file.exists() and not regenerate:
            start = time.time()
            with self.filter_file.open('rb') as f:
                self.word_to_entry_index = pickle.load(f)
            end = time.time()
            logger.debug(f"Load {self.search_type} entries by word set from file: {end - start} seconds")
        else:
            start = time.time()
            self.cache = {}  # Clear cache on (re-)generating entries_by_word_set
            entry_splitter = r',|\.| |\]|\[\(|\)|\{|\}|\t|\n|\:'
            # Create map of words to entries they exist in
            for entry_index, entry in enumerate(entries):
                for word in re.split(entry_splitter, entry[self.entry_key].lower()):
                    if word == '':
                        continue
                    if word not in self.word_to_entry_index:
                        self.word_to_entry_index[word] = set()
                    self.word_to_entry_index[word].add(entry_index)

            with self.filter_file.open('wb') as f:
                pickle.dump(self.word_to_entry_index, f)
            end = time.time()
            logger.debug(f"Convert all {self.search_type} entries to word sets: {end - start} seconds")

        return self.word_to_entry_index


    def can_filter(self, raw_query):
        "Check if query contains explicit filters"
        # Extract explicit query portion with required, blocked words to filter from natural query
        required_words = re.findall(self.required_regex, raw_query)
        blocked_words = re.findall(self.blocked_regex, raw_query)

        return len(required_words) != 0 or len(blocked_words) != 0


    def apply(self, raw_query, raw_entries, raw_embeddings):
        "Find entries containing required and not blocked words specified in query"
        # Separate natural query from explicit required, blocked words filters
        start = time.time()

        required_words = set([word.lower() for word in re.findall(self.required_regex, raw_query)])
        blocked_words = set([word.lower() for word in re.findall(self.blocked_regex, raw_query)])
        query = re.sub(self.blocked_regex, '', re.sub(self.required_regex, '', raw_query)).strip()

        end = time.time()
        logger.debug(f"Extract required, blocked filters from query: {end - start} seconds")

        if len(required_words) == 0 and len(blocked_words) == 0:
            return query, raw_entries, raw_embeddings

        # Return item from cache if exists
        cache_key = tuple(sorted(required_words)), tuple(sorted(blocked_words))
        if cache_key in self.cache:
            logger.info(f"Explicit filter results from cache")
            entries, embeddings = self.cache[cache_key]
            return query, entries, embeddings

        if not self.word_to_entry_index:
            self.load(raw_entries, regenerate=False)

        start = time.time()

        # mark entries that contain all required_words for inclusion
        entries_with_all_required_words = set(range(len(raw_entries)))
        if len(required_words) > 0:
            entries_with_all_required_words = set.intersection(*[self.word_to_entry_index.get(word, set()) for word in required_words])

        # mark entries that contain any blocked_words for exclusion
        entries_with_any_blocked_words = set()
        if len(blocked_words) > 0:
            entries_with_any_blocked_words = set.union(*[self.word_to_entry_index.get(word, set()) for word in blocked_words])

        end = time.time()
        logger.debug(f"Mark entries satisfying filter: {end - start} seconds")

        # get entries (and their embeddings) satisfying inclusion and exclusion filters
        start = time.time()

        included_entry_indices = entries_with_all_required_words - entries_with_any_blocked_words
        entries = [entry for id, entry in enumerate(raw_entries) if id in included_entry_indices]
        embeddings = torch.index_select(raw_embeddings, 0, torch.tensor(list(included_entry_indices)))

        end = time.time()
        logger.debug(f"Keep entries satisfying filter: {end - start} seconds")

        # Cache results
        self.cache[cache_key] = entries, embeddings

        return query, entries, embeddings
