# import module
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import date, datetime

# create the application
app = Flask(__name__)

posts = [
    {'id': 0, 'usrname': '@luigi', 'usrimg': 'user.jpg', 'img': 'img1.jpg',
     'date': '1 giorno fa', 'post': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tristique lobortis molestie. Donec laoreet iaculis nibh sed viverra. Nunc condimentum tincidunt mollis. Curabitur gravida aliquam urna, ac vulputate felis condimentum at. Sed sapien lectus, aliquam ac ornare sed, dapibus pulvinar ligula. Ut ultrices a nibh eget eleifend. Nullam eleifend metus nec erat vestibulum venenatis ornare sed orci. Donec vel sapien sit amet felis cursus rutrum.'},
    {'id': 1, 'usrname': '@alberto', 'usrimg': 'user.jpg', 'img': 'img2.jpg',
     'date': '4 giorni fa', 'post': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tristique lobortis molestie. Donec laoreet iaculis nibh sed viverra. Nunc condimentum tincidunt mollis. Curabitur gravida aliquam urna, ac vulputate felis condimentum at. Sed sapien lectus, aliquam ac ornare sed, dapibus pulvinar ligula. Ut ultrices a nibh eget eleifend. Nullam eleifend metus nec erat vestibulum venenatis ornare sed orci. Donec vel sapien sit amet felis cursus rutrum.'},
    {'id': 2, 'usrname': '@juan', 'usrimg': 'user.jpg', 'img': 'img3.jpg',
     'date': '2 settimane fa', 'post': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tristique lobortis molestie. Donec laoreet iaculis nibh sed viverra. Nunc condimentum tincidunt mollis. Curabitur gravida aliquam urna, ac vulputate felis condimentum at. Sed sapien lectus, aliquam ac ornare sed, dapibus pulvinar ligula. Ut ultrices a nibh eget eleifend. Nullam eleifend metus nec erat vestibulum venenatis ornare sed orci. Donec vel sapien sit amet felis cursus rutrum.'}
]

# define the homepage

@app.route('/')
def home():
    users = [d['usrname'] for d in posts]
    return render_template('home.html', posts=posts, users=users)
        

# define the 'about' page

@app.route('/about')
def about():
    p_developers = [
        {'id': 1234, 'name': 'Luigi De Russis', 'devimg': 'user.jpg',
            'quote': 'A well-known quote, contained in a blockquote element', 'quoteAuthor': 'First quote author'},
        {'id': 5678, 'name': 'Alberto Monge Roffarello', 'devimg': 'user.jpg',
            'quote': 'A well-known quote, contained in a blockquote element', 'quoteAuthor': 'Second quote author'},
        {'id': 9012, 'name': 'Juan Pablo Sáenz', 'devimg': 'user.jpg',
            'quote': 'A well-known quote, contained in a blockquote element', 'quoteAuthor': 'Third quote author'}
    ]
    return render_template('about.html', developers=p_developers)


@app.route('/posts/<int:id>')
def single_post(id):
    post = posts[id]
    return render_template('post.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
            
            post = request.form.to_dict()

            if post['usrname'] not in [d['usrname'] for d in posts]:
                app.logger.error("Non esiste l'utente!")
                return redirect(url_for('home'))
            
            if post['post'] == '':
                app.logger.error('Il post non può essere vuoto!')
                return redirect(url_for('home'))

            if post['date'] == '':
                app.logger.error('Devi selezionare una data')
                return redirect(url_for('home'))

            if datetime.strptime(post['date'], '%Y-%m-%d').date() < date.today():
                app.logger.error('Data errata')
                return redirect(url_for('home'))


            post_image = request.files['image']
            if post_image:
                post_image.save('static/' + post_image.filename)
                post['img'] = post_image.filename
            
            post['id'] = posts[-1]['id'] + 1
            post['usrimg'] = [p['usrimg'] for p in posts if p['usrname'] == post['usrname']][0]

            posts.append(post)
            
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
