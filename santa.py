from flask import Flask, request, render_template
import os
from pymongo import MongoClient


app = Flask(__name__)
uri = os.environ.get('MONGOLAB_URI', 'mongodb://localhost')
client = MongoClient(uri)
db = client.heroku_app32469592
collection = db.santa


@app.route('/', methods=['GET'])
def main_page():
    print db
    return render_template('form.html')


@app.route('/form', methods=['POST'])
def add_to_database():
    fname = request.form['firstname']
    lname = request.form['lastname']
    email = request.form['email']
    info = request.form['info']
    if (db.santa.find({"email": email}).count() == 0):
        f = open('storage.txt', 'a')
        f.write(fname + "|" + lname + "|" + email + "|" + info + "\n")
        f.close()

        db.santa.insert({'fname':fname, 'lname':lname, 'email':email, 'info':info})

    else:
        return render_template('invalid.html')

    return render_template('worked.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
