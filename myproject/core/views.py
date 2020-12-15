# core/views.py
from flask import render_template, request, Blueprint
from projectKanpai.models import BlogPost
from projectKanpai.core.forms import SearchForm


core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page = page, per_page = 5)
    return render_template('index.html', blog_posts = blog_posts)

@core.route('/search', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        all_query = []
        key = form.key.data.split(" ")
        stopwords_array = {"i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"}
        tokens_without_sw = [word for word in key if not word in stopwords_array]
        print(tokens_without_sw)

        id = set()
        for word in tokens_without_sw:
            query1 = BlogPost.query.filter(BlogPost.title.contains(word)).all()
            print(query1)
            for ele in query1:
                if ele.id in id:
                    break
                else: 
                    id.add(ele.id) 
                all_query += [ele]
            query2 = BlogPost.query.filter(BlogPost.text.contains(word)).all()
            for ele in query2:
                print(type(ele), type(query1))
                if ele.id in id:
                    break
                else: 
                    id.add(ele.id) 
                all_query += [ele]
        print(all_query)
 
        return render_template('search.html', form = form, query = all_query)
    return render_template('search.html', form = form)

def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title,
                            date=blog_post.date, post=blog_post)

