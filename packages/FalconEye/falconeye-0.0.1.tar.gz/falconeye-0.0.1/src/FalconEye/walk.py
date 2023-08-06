class Walk:
    def __init__(self, obj):
        self.obj = obj
        self.current_items = []
        self.queue = []
        def runtime(obj=obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if isinstance(value, dict) or isinstance(value, list):
                        self.queue.append(value)
                    else:
                        self.current_items.append(value)
            elif isinstance(obj, list):
                for value in obj:
                    if isinstance(value, dict) or isinstance(value, list):
                        self.queue.append(value)
                    else:
                        self.current_items.append(value)
            if self.queue:
                next_item = self.queue.pop()
                runtime(next_item)
        runtime()

