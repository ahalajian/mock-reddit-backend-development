import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    0: {
    "id": 0,
    "upvotes": 1,
    "title": "My cat is the cutest!",
    "link": "https://i.imgur.com/jseZqNK.jpg",
    "username": "alicia98",
    }, 
    1 : {
    "id": 1,
    "upvotes": 3,
    "title": "Cat loaf",
    "link": "https://i.imgur.com/TJ46wX4.jpg",
    "username": "alicia98",
    }
}

#the keys represent the posts, and the lists represent the comments associated with each post
post_comments = { 0: [0], 1: [1]}

comments = {
    0: {
    "id": 0,
    "upvotes": 8,
    "text": "Wow, my first Reddit gold!",
    "username": "alicia98",
    },
    1: {
    "id": 1,
    "upvotes": 20320,
    "text": "Yeehaw!",
    "username": "amonkey94",
    }
}

post_id_counter = 2
comment_id_counter = 2

@app.route("/")
def hello_world():
    return "Hello world!"

# your routes here
@app.route("/api/posts/")
def get_posts():
    """
    This route gets all posts.
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200

@app.route("/api/posts/", methods = ["POST"])
def create_post():
    """
    This route creates a post.
    """
    global post_id_counter
    body = json.loads(request.data)
    title = body.get("title")
    link = body.get("link")
    username = body.get("username")
    if not title or not link or not username:
        return json.dumps({"error": "missing a field"}), 400
    post = {"id": post_id_counter,
            "upvotes": 1,
            "title": title,
            "link": link,
            "username": username }
    posts[post_id_counter] = post
    post_comments[post_id_counter] = []
    post_id_counter += 1
    return json.dumps(post), 201

@app.route("/api/posts/<int:id>/")
def get_post(id):
    """
    This route gets a post.
    """
    post = posts.get(id)
    if not post:
        return json.dumps({"error": "post not found"}), 404
    return json.dumps(post), 200

@app.route("/api/posts/<int:id>/", methods = ["DELETE"])
def delete_post(id):
    """
    This route deletes a post.
    """
    post = posts.get(id)
    if not post:
        return json.dumps({"error": "post not found"}), 404
    del posts[id]
    return json.dumps(post), 200

@app.route("/api/posts/<int:id>/comments/")
def get_comments(id):
    """
    This route gets comments for a specific post.
    """
    post = posts.get(id)
    if not post:
        return json.dumps({"error": "post not found"}), 404
    lst = []
    for comment_id in post_comments[id]:
        lst.append(comments.get(comment_id))
    res = {"comments": lst}
    return json.dumps(res), 200

@app.route("/api/posts/<int:id>/comments/", methods = ["POST"])
def post_comment(id):
    """
    This route posts a comment for a specific post
    """
    global comment_id_counter
    post = posts.get(id)
    if not post:
        return json.dumps({"error": "post not found"}), 404
    body = json.loads(request.data)
    text = body.get("text")
    username = body.get("username")
    if not text or not username:
        return json.dumps({"error": "missing a field"}), 400
    comment = {"id" : comment_id_counter, "upvotes": 1, "text": text, "username": username}
    comments[comment_id_counter] = comment
    post_comments[id].append(comment_id_counter)
    comment_id_counter += 1
    return json.dumps(comment), 201

@app.route("/api/posts/<int:pid>/comments/<int:cid>/", methods = ["POST"])
def edit_comment(pid, cid):
    """
    This route edits a comment for a specific post
    """
    post = posts.get(pid)
    comment = comments.get(cid)
    if not post or not comment: 
        return json.dumps({"error": "post or comment not found"}), 404
    body = json.loads(request.data)
    text = body.get("text")
    if not text:
        return json.dumps({"error": "missing text"}), 400
    comments[cid]["text"] = text
    return json.dumps(comments[cid]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

