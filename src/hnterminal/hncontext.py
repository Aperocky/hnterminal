from .hnclient import HNClient


class HNContext:

    def __init__(self):
        self.client = HNClient()
        self.current_pointers = {}
        self.story_list = []
        self.loaded_items = {}
        self.loaded_stories = {}
        self.loaded_comments = {}
        self.call_count = 0

    def get_story_list(self, story_type="TOP"):
        self.story_list = self.client.get_stories(story_type=story_type)

    def store_item(self, item_id):
        if item_id in self.loaded_items:
            return
        item = self.client.get_item(item_id)
        self.loaded_items[item_id] = item

    def store_pointer(self, index, item_id):
        self.current_pointers[index] = item_id

    def clear_pointers(self):
        self.current_pointers = {}

