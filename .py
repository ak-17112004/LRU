from flask import Flask, request, jsonify, render_template
from collections import OrderedDict

app = Flask(__name__)

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: str):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1
    
    def put(self, key: str, value: str):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def display_cache(self):
        return list(self.cache.items())

cache = LRUCache(3)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/put', methods=['POST'])
def put_item():
    data = request.json
    key, value = data.get("key"), data.get("value")
    if key and value:
        cache.put(key, value)
        return jsonify({"message": "Item added", "cache": cache.display_cache()})
    return jsonify({"error": "Invalid input"}), 400

@app.route('/get/<key>', methods=['GET'])
def get_item(key):
    value = cache.get(key)
    if value != -1:
        return jsonify({"message": "Cache Hit", "value": value, "cache": cache.display_cache()})
    return jsonify({"message": "Cache Miss", "value": -1, "cache": cache.display_cache()})

@app.route('/display', methods=['GET'])
def display_cache():
    return jsonify({"cache": cache.display_cache()})

if __name__ == "__main__":
    app.run(debug=True)
