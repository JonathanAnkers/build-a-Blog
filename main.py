import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):

        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        
        self.write(self.render_str(template, **kw))

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    author = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 5;")
        self.render("front.html", blogs=blogs)





class Newpost(Handler):
    def get(self):
        self.render("newpost.html")

    def render_newpost(self, title="", art="", author="", error=""):
        self.render("newpost.html", title=title, art=art, author=author, error=error)

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        author = self.request.get("author")
        if title and art and author:
            a = Art(title = title, art = art, author = author)
            a.put()

            self.redirect("/")
        else:
            error = "I will need all feilds filled!"
            self.render_newpost(title, art, author, error)

class ViewPostHandler(Handler):
    def get(self, id):
        
        sblog = Art.get_by_id(int(id))

        
        self.render("sblog.html", sblog=sblog)

    


app = webapp2.WSGIApplication([('/', Blog),
                               ('/newpost', Newpost),
                  webapp2.Route('/<id:\d+>', ViewPostHandler),
                               ],
                              debug=True)
