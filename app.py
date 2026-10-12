from flask import Flask, render_template,request,redirect,flash
import json

FILENAME ="posts.json"
app = Flask(__name__)
app.secret_key = "dev-secret-key"

def save_posts(posts):
    with open(FILENAME,"w",encoding="utf-8")as file:
        json.dump(posts,file,ensure_ascii=False,indent=4)


def load_posts():
    try:
        with open(FILENAME,"r",encoding="utf-8")as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def is_invalid_index(index,posts):
    return  index < 0 or index >= len(posts)

def get_valid_post_data():
    title = request.form['title'].strip()
    author = request.form['author'].strip()
    content = request.form['content'].strip()
    if not (title and author and content):
        return False
    return title,author,content



@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    posts = load_posts()

    is_invalid = is_invalid_index(index,posts)
    if is_invalid:
        flash("게시글이 존재하지 않습니다.")
        return redirect("/")
    posts.pop(index)
    save_posts(posts)
    flash("게시글이 삭제되었습니다.")
    return redirect("/")

@app.route("/detail/<int:index>")
def detail(index):
    posts = load_posts()
    is_invalid = is_invalid_index(index,posts)
    if is_invalid:
        flash("게시글이 존재하지 않습니다.")
        return redirect("/")
    post = posts[index]
    return render_template("detail.html",post=post,index=index)



@app.route("/edit/<int:index>")
def edit(index):
    posts = load_posts()

    is_invalid = is_invalid_index(index,posts)
    if is_invalid:
        flash("게시글이 존재하지 않습니다.")
        return redirect("/")
    post = posts[index]
    return render_template("edit.html",post=post,index=index)

@app.route("/update/<int:index>",methods=["POST"])
def update(index):
    post_data = get_valid_post_data()
    if not post_data:
        flash("제목,작성자,내용을입력해주세요.")
        return redirect("/")
    title,author,content = post_data
    post = {
        'title' : title,
        'author' : author,
        'content' : content
    }
    posts = load_posts()

    is_invalid = is_invalid_index(index,posts)
    if is_invalid:
        flash("게시글이 존재하지 않습니다.")
        return redirect("/")
    posts[index] = post
    save_posts(posts)
    return redirect("/")
    






@app.route("/")
def home():
    posts = load_posts()
    return render_template("pratice4.html",posts=posts)

@app.route("/write",methods=["POST"])
def write():
    post_data = get_valid_post_data()
    if not post_data:
        flash("제목,작성자,내용을입력해주세요.")
        return redirect("/")
    title,author,content = post_data

    posts = load_posts()
    
    posts.append({
        "title" : title,
        "content" : content,
        "author" : author
    })
    save_posts(posts)



    print("제목:", title)
    print("작성자", author)
    print("내용:", content)
    

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)