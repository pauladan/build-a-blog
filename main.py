from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(1000))

    def __init__(self, name, body):
        self.name = name
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():

    blog_id = request.args.get('id')

    if blog_id == None:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs, title = "Build a Blog")
    else:    
        blog = Blog.query.get(blog_id)
        return render_template('entry.html', blog=blog)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    
    if request.method == 'POST':
        blog_name = request.form['name']
        blog_body = request.form['body']
        blog_name_error = " "
        blog_body_error = " "

        if blog_name == "":
            blog_name_error = "Please enter a valid blog title"
        if blog_body == "":
            blog_body_error = "Please enter blog content"

        if blog_name_error == " " and blog_body_error == " ":
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            return render_template('entry.html', blog=new_blog)

        else:
            return render_template('new_post.html', blog_name= blog_name, blog_name_error= blog_name_error, blog_body = blog_body, blog_body_error=blog_body_error)    

    return render_template('new_post.html', title='New Post')





if __name__ == '__main__':
    app.run()