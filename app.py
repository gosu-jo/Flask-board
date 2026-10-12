from flask import Flask, render_template,request,redirect,flash
import json

FILENAME ="posts.json"
app = Flask(__name__)
app.secret_key = "dev-secret-key"


def load_posts():
    try:
        with open(FILENAME,"r",encoding="utf-8")as file:
            return json.load(file)
    except FileNotFoundError:
        return []





@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    try:
        with open(FILENAME,"r",encoding="utf-8")as file:
            posts = json.load(file)
    except FileNotFoundError:
        return redirect("/")
    if index < 0 or index >= len(posts):
        flash("게시글이 존재하지 않습니다.")
        return redirect("/")
    posts.pop(index)
    with open(FILENAME,"w",encoding="utf-8")as file:
        json.dump(posts,file,ensure_ascii=False,indent=4)
    flash("게시글이 삭제되었습니다.")
    return redirect("/")

@app.route("/detail/<int:index>")
def detail(index):
    try:
        with open(FILENAME,'r',encoding='utf-8')as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    if index < 0 or index >= len(posts):
        return "게시글이 없습니다."
    post = posts[index]
    return render_template("detail.html",post=post,index=index)



@app.route("/edit/<int:index>")
def edit(index):
    try:
        with open(FILENAME,"r",encoding='utf-8')as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    if index < 0 or index >= len(posts):
        return "게시글이 없습니다."
    post = posts[index]
    return render_template("edit.html",post=post,index=index)

@app.route("/update/<int:index>",methods=["POST"])
def update(index):
    title = request.form['title'].strip()
    author = request.form['author'].strip()
    content = request.form['content'].strip()
    if not (title and author and content):
        flash("제목,작성자,내용을입력해주세요.")
        return redirect("/")
    post = {
        'title' : title,
        'author' : author,
        'content' : content
    }
    try:
        with open(FILENAME,"r",encoding='utf-8')as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    if index < 0 or index >= len(posts):
        return "게시글이 없습니다."
    posts[index] = post
    with open(FILENAME,"w",encoding='utf-8')as file:
        json.dump(posts,file,ensure_ascii=False,indent=4)
    return redirect("/")
    






@app.route("/")
def home():
    try:
        with open(FILENAME,"r",encoding='utf-8')as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    return render_template("pratice4.html",posts=posts)

@app.route("/write",methods=["POST"])
def write():
    title = request.form['title'].strip()
    author = request.form['author'].strip()
    content = request.form['content'].strip()
    if not (title and author and content):
        flash("제목,작성자,내용을입력해주세요.")
        return redirect("/")
    try:
        with open(FILENAME,"r",encoding="utf-8")as file:
            posts = json.load(file)
    except FileNotFoundError:
        posts = []
    
    posts.append({
        "title" : title,
        "content" : content,
        "author" : author
    })
    with open(FILENAME,"w",encoding="utf-8")as file:
        json.dump(posts,file,ensure_ascii=False,indent=4)



    print("제목:", title)
    print("작성자", author)
    print("내용:", content)
    

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)