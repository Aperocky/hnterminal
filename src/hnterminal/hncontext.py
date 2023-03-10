import argparse
from .hnclient import HNClient
from replbuilder import ReplCommand


class HNContext:

    def __init__(self):
        self.client = HNClient()
        self.current_pointers = {}
        self.story_list = []
        self.loaded_items = {}
        self.call_count = 0

    def get_story_list(self, story_type="TOP"):
        self.call_count += 1
        self.story_list = self.client.get_stories(story_type=story_type)

    def store_item(self, item_id):
        if item_id in self.loaded_items:
            return
        self.call_count += 1
        item = self.client.get_item(item_id)
        if item is None:
            raise ValueError("Provided id does not exist")
        self.loaded_items[item_id] = item

    def get_author_info(self, author_name):
        return self.client.get_author(author_name)

    def store_pointer(self, index, item_id):
        self.current_pointers[index] = item_id

    def clear_pointers(self):
        self.current_pointers = {}

    def get_cache(self, args):
        print("LOADED ITEMS COUNT : {}".format(len(self.loaded_items)))
        print("TOTAL HN API CALLS : {}".format(self.call_count))
        print("POINTERS COUNT     : {}".format(len(self.current_pointers)))

    def clear_cache(self, args):
        self.loaded_items = {}
        self.call_count = 0
        self.current_pointers = {}

    def get_context_commands(self):
        return [
            ReplCommand("get_cache", argparse.ArgumentParser(), self.get_cache, "See stored item count and call count"),
            ReplCommand("clear_cache", argparse.ArgumentParser(), self.clear_cache, "Remove all cache"),
        ]
