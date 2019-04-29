from flask import Flask, render_template, redirect, url_for, request
from modules import convert_to_dict, make_ordinal

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import Required

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'VguhZssWgM'

# Flask-Bootstrap requires this line
Bootstrap(app)

# create a list of dicts
members_list = convert_to_dict("flask_rep_info.csv")
state_financial_list = convert_to_dict("state_financial_info.csv")
# with Flask-WTF, each web form is represented by a class
# "SearchForm" can change; "(FlaskForm)" cannot
class SearchForm(FlaskForm):
    # the choices are (option, string)
    state_choice = SelectField('Select from this list')
    submit = SubmitField('Search')


# first route

@app.route('/', methods=['GET', 'POST'] )
def index():
    # make three empty lists
    state_list = []
    second_state_list = []
    pairs_list = []
    # fill one list with the number of each presidency and
    # fill the other with the name of each president=
    for state in state_financial_list:
        state_list.append(state['state'])
        second_state_list.append(state['state'])
        # zip() is a built-in function that combines lists
        # creating a new list of tuples
    pairs_list = zip(state_list, second_state_list)

    # this is from the class above; form will go to the template
    form = SearchForm()
    # this is how we auto-populate a select menu in a form
    form.state_choice.choices = [ (m[0], m[1]) for m in pairs_list ]

    # if page opened by form submission, redirect to detail page
    if request.method == "POST":
        # get the input from the form
        state_choice = request.form.get("state_choice")
        return redirect( url_for('state_page', state_id=state_choice ) )
    # no else - just do this by default
    return render_template('search.html', form=form)
# second route

@app.route('/member/<num>')
def detail(num):
    for member in members_list:
        if member['id'] == num:
            member_dict = member
            break
    return render_template('member.html', mem=member_dict, the_title=member_dict['name'])

@app.route('/state/<state_id>')
def state_page(state_id):
    for state in state_financial_list:
        if state['state'] == state_id:
            s = state
            members = select_where_state_is(state_id)
            break
            
    return render_template('state.html', s=s, the_title=state_id, members=members)

def select_where_state_is(state):
    selected_members = []
    for member in members_list:
        if member[' state'] == state:
            selected_members.append(member)

    return selected_members

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)