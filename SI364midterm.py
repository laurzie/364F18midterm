###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements

import requests
import json
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,SubmitField,ValidationError  # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy

## App setup code
app = Flask(__name__)
app.debug = True

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string for si364 midterm'

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/laurzieMidterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################

##################
##### MODELS #####
##################
class Episodes(db.Model):
    __tablename__ = "episodes"
    id = db.Column(db.Integer,primary_key=True)
    episode_number = db.Column(db.String(2))
    title = db.Column(db.String(180))
    season_id = db.Column(db.Integer,db.ForeignKey("seasons.id"))

    def __repr__(self):
        return "Episode Number: {}, Title: {}".format(self.episode_number, self.title)

class Seasons(db.Model):
    __tablename__ = "seasons"
    id = db.Column(db.Integer,primary_key=True)
    season_number = db.Column(db.Integer)
    winner_id = db.Column(db.Integer)
    episodes = db.relationship('Episodes',backref='Seasons')

    def __repr__(self):
        return " Season: {}, winner_id: {})".format(self.season_number, self.winner_id)

#This was code for a function that didnt end up working
# class Queens(db.Model):
#     __tablename__ = "queens"
#     id = db.Column(db.Integer,primary_key=True)
#     status = db.Column(db.String(5))
#     queen_id = db.Column(db.Integer)
#     queen_name = db.Column(db.String(100))
#     quote = db.Column(db.String(300))
#
#     def __repr__(self):
#         return "{} | ID: {} | {}" .format(self.queen_name, self.id, self.quote)

class Favorites(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer,primary_key=True)
    favorite_queen = db.Column(db.String(50))
    season = db.Column(db.Integer)
    quote = db.Column(db.String(300))

    def __repr__(self):
        return "{} | Season: {} | {}" .format(self.favorite_name, self.season, self.quote)

###################
###### FORMS ######
###################
class FavoritesForm(FlaskForm):
    fav_queen = StringField("Please enter the name of ypur favorite queen:", validators=[Required()])
    season = IntegerField("Please enter the number of the season your favorite queen was on:", validators=[Required()])
    fav_quote = StringField("Please your favorite quote by your favorite queen:", validators=[Required(), Length(1,280)])
    submit = SubmitField()

class SeasonForm(FlaskForm):
    season_number = IntegerField("Please enter the name of the Season(1-10) you want more information on:", validators=[Required()])
    submit = SubmitField()

    def validate_season_name(self, field):
        check_season = field.data.strip()
        list_of_seasons = [0,1,2,3,4,5,6,7,8,9,10]
        errors = None
        if check_season not in list_of_seasons:
            error = "The season number you entered is not valid. Please enter a valid season number"
            raise ValidationError(error)

#code that didn't end up working
# class QueenNameForm(FlaskForm):
#     queen_name = StringField("Please enter the name of a Drag Queen:", validators=[Required(), Length(1,280)])
#     submit = SubmitField()
#
#     def validate_queen_name(self, field):
#         check_name = field.data.lower().strip()
#         list_of_queens = ["bebezaharabenet","ninaflowers","rebeccaglasscock","shannel","ongina","jadesotomayor","akashia","tammiebrown","victoria'porkchop'parker",
#     "tyrasanchez","raven","jujubee","tatianna","pandoraboxx","jessicawild","saharadavenport","morganmcmichaels","sonique",
#     "mystiquesummersmadison","nicolepaigebrooks","shangela","raja","manilaluzon","alexismateo","yarasofia",
#     "carmencarrera","deltawork","stacylaynematthews","mariah","indiaferrah","mimiimfurst","phoenix","venusd-lite",
#     "sharonneedles","chadmichaels","phiphio'hara","latriceroyale","kenyamichaels","didaritz","willam",
#     "jigglycaliente","milan","madamelaqueer","theprincess","lashauwnbeyond","alisasummers","jinkxmonsoon","alaska",
#     "roxxxyandrews","detox","cocomontrese","alyssaedwards","ivywinters","jadejolie","lineyshasparx","viviennepinay",
#     "honeymahogany","monicabeverlyhillz","serenachacha","pennytration","biancadelrio","adoredelano","courtneyact","dariennelake","bendelacreme",
#     "joslynfox","trinityk.bonet","laganjaestranja","milk","giagunn","aprilcarrión","vivacious","magnoliacrawford","kellymantle",
#     "violetchachki","gingerminj","pearlliaison","kennedydavenport","katyazamolodchikova","trixiemattel","missfame","jaidynndiorefierce",
#     "max","kandyho","mrs.kashadavis","jasminemasters","sashabelle","tempestdujour","bobthedragqueen","kimchi","naomismalls","chichidevayne",
#     "derrickbarry","thorgythor","thorgythor","robbieturner","nayshalopez","cynthialeefontaine","daxexclamationpoint",
#     "lailamcqueen","sashavelour","peppermint","sheacouleé", "trinitytaylor","alexismichelle","ninabo'ninabrown","valentina",
#     "farrahmoan","aja","eurekao'hara","charliehides","kimorablac","jaymesmansfield","aquaria","eureka",
#     "kameronmichaels","asiao'hara","mizcracker","monétxchange","thevixen","moniqueheart",
#     "blairst.clair","mayhemmiller","dustyraybottoms","yuhuahamasaki","kaloriekarbdashianwilliams","vanessavanjiemateo"]
#         errors = None
#         if check_name not in list_of_queens:
#             error = "The Drag Queen name you entered is not valid. Please enter a valid name"
#             raise ValidationError(error)

#######################
###### VIEW FXNS ######
#######################


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SeasonForm()
    if form.validate_on_submit():
        season_number_form= form.season_number.data
        season = Seasons.query.filter_by(season_number=season_number_form).first()
        if season:
            flash("Season already entered that season")
        if not season:
            baseurl="http://www.nokeynoshade.party/api/seasons/{}".format(season_number_form)
            response = requests.get(baseurl)
            text = response.text
            python_obj = json.loads(text)
            season_number_api = python_obj["seasonNumber"]
            winner_id_api= python_obj["winnerId"]
            seasons = Seasons(season_number=season_number_api,winner_id = winner_id_api)
            db.session.add(seasons)
            db.session.commit()
            baseurl = "http://www.nokeynoshade.party/api/seasons/{}/episodes".format(season_number_form)
            response = requests.get(baseurl)
            text = response.text
            python_obj = json.loads(text)
            print("***************\n\n\n")
            print(python_obj)
            for item in python_obj:
                episode_title = item["title"]
                episode_number = item["episodeInSeason"]
                episodes = Episodes(episode_number=episode_number, title = episode_title, season_id = seasons.id )
                db.session.add(episodes)
                db.session.commit()
            flash("Season successfully saved!")

    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return render_template('index.html', form=form)




@app.route('/queens_form', methods=['GET', 'POST'])
def queens():
    form = FavoritesForm()
    if form.validate_on_submit():
        queen_fav_queen= form.fav_queen.data
        queen_season = form.season.data
        queen_fav_quote = form.fav_quote.data
        favorites =Favorites(favorite_queen = queen_fav_queen, season = queen_season, quote = queen_fav_quote)
        db.session.add(favorites)
        db.session.commit()
        return redirect(url_for('get_all_queens'))
        flash("Season successfully saved!")

    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return render_template('queens_form.html',form = form)

@app.route('/favorites')
def get_all_queens():
    favorites = Favorites.query.all()
    return render_template('queens_info.html',favorites = favorites)

@app.route('/episodes')
def get_all_episodes():
    episodes= Episodes.query.all()
    return render_template('episodes_by_season.html', episodes = episodes)

#code that didn't end up working
# @app.route('/queens_form', methods=['GET', 'POST'])
# def queens():
#     form = QueenNameForm()
#     queens = Queens.query.all()
#     num_queens= len(queens)
#     if form.validate_on_submit():
#         queen_name_entered = form.queen_name.data
#         print(queen_name_entered)
#         lower_queen_name = queen_name_entered.lower()
#         cap_queen_name = queen_name_entered.title()
#         search_queen_name = new_queen_name.replace(" ", "%20")
#         queens = Queens.query.filter_by(queen_name=cap_queen_name).first()
#         if queens:
#             flash("Season already entered that season")
#             # return redirect(url_for('see_all_queens'))
#         if not queens:
#             baseurl = "http://www.nokeynoshade.party/api/queens?"
#             params_diction = {}
#             params_diction['name'] = search_queen_name
#             response = requests.get(baseurl, params= params_diction)
#             text = response.text
#             print(text)
#             python_obj = json.loads(text)
#             queen_id = python_obj[0]["id"]
#             status = python_obj[0]["winner"]
#             queen_name_cap = python_obj[0]["name"]
#             queen_quote = python_obj[0]["quote"]
#             queen = Queens(status = status, queen_name=queen_name_cap,display_name = queen_qoute)
#             db.session.add(queen)
#             db.session.commit()
#             queens = Queens.query.filter_by(queen_name=cap_queen_name).first()
#             flash("Season successfully saved!")
#             return redirect(url_for('see_all_queens'))
#     errors = [v for v in form.errors.values()]
#     if len(errors) > 0:
#         flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
#     return render_template('queens_form.html',form = form)




## Code to run the application...

# Put the code to do so here!
if __name__ == '__main__':
    db.create_all()
    app.run(use_reloader=True,debug=True)
    # b.create_all()
    # app.run(use_reloader=True,debug=True)
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
