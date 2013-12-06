import re
from flask import Flask, render_template, redirect, url_for, request
import xmlController as xc
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html',
                           title='Home',
                           hm_active='active')


@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html',
                           title='Welcome',
                           w_active='active')


@app.route('/all_bands.html')
def all_bands():
    valid = xc.xmlIsValid('static/bands.xml',
                          'static/bandSchema.xsd')
    bands = xc.getAllBands()
    return render_template('all_bands.html',
                           title='All the Bands!',
                           valid=valid,
                           bands=bands,
                           ab_active='active'), 200


@app.route('/<band>_albums')
def discography(band):
    bandElement = xc.getBand(band)
    return render_template('discog.html',
                           band=band,
                           bandElement=bandElement)


@app.route('/band_list.html')
def band_list():
    valid = xc.xmlIsValid('static/bands.xml',
                          'static/bandSchema.xsd')
    print "XML IS VALID :)" if valid else "XML IS INVALID!"
    bands = xc.getAllBands()
    title = 'All the bands'

    if len(request.args) > 0 :
        query = request.args['search']
        regex = re.compile('.*(%s).*'%query)
        title = 'Results for "%s"' % query
        ab_active=''
        bands = [band for band in bands if band.get('name').lower().find(query.lower()) != -1]
    else:
        ab_active='active'
    return render_template('band_list.html',
                           title=title,
                           valid=valid,
                           bands=bands,
                           ab_active=ab_active)


@app.route('/<band>_page')
def band_page(band):
    print 'rendering'
    valid = xc.xmlIsValid('static/bands.xml',
                          'static/bandSchema.xsd')
    bandElement = xc.getBand(band)
    return render_template('discog.html',
                           title=band,
                           bandElement=bandElement,
                           valid = valid)


@app.route('/post', methods=['POST'])
def handlePost():
    member =  request.form['value']
    print member
    message = xc.addmember(member)
    return json.dumps({"html":str.format("<tr><td>{}</td><td>{}</td><td>{}</td><tr>","John Smith","djskfhsk","jhdsgfjhsd")})


@app.route('/delete', methods=['POST'])
def delete():
    print "delete"
    performerno = request.form['performerno']
    band = request.form['band']
    result = xc.deletePerformer(band, performerno)
    return "",result


@app.route('/addperformer', methods=['POST'])
def addperformer():
    print "adding"
    fullname = request.form['fullname']
    joindate = request.form['joindate']
    instrument = request.form['instrument']
    band = request.form['band']
    message = xc.addmember(band, instrument, fullname, joindate)
    return "mike smells",200


@app.route('/infomodify', methods=['POST'])
def infomodify():
    print request.form
    band = request.form['pk']
    value = request.form['value']
    name = request.form['name']
    print name,", ", band, ", ", value

    ## hacky switch case
    if name == 'city':
        print "in the switch"
        xc.update_city(band, value)
    elif name == 'province':
        xc.update_province(band, value)
    elif name == 'country':
        xc.update_country(band, value)
    elif name == 'genre':
        xc.update_genre(band, value)
    else: # label
        xc.update_label(band, value)
    return "",200


@app.route('/deletesong', methods=['POST'])
def delete_song():
    print "delete song"
    print request.form
    songno = request.form['songno']
    band = request.form['band']
    album = request.form['album']
    result = xc.deleteSong(band, album, songno)
    return "",result


@app.route('/addsong', methods=['POST'])
def add_song():
    xc.add_song(songtitle=request.form['songtitle'],
                band=request.form['band'],
                duration=request.form['duration'],
                album=request.form['album'])
    return "", 200


@app.route('/addalbum', methods=['POST'])
def add_album():
    xc.add_album(band = request.form['band'],
                 title = request.form['title'],
                 date = request.form['date'])
    band = xc.getBand(request.form['band'])
    print band
    print band[0]
    html = render_template('blankAlbum.html',
                           album = band[0].find('Album'))
    return html, 200


@app.route('/deleteAlbum', methods=['POST'])
def delete_album():
    print 'deleting album'
    xc.delete_album(band = request.form['band'],
                    title = request.form['title'])
    return '', 200


@app.route('/addBand', methods=['POST'])
def add_band():
    print 'adding band', request.form['band']
    xc.add_band(band = request.form['band'])
    return band_page(band = request.form['band'])


@app.route('/deleteBand', methods=['POST'])
def delete_band():
    print 'deleting band', request.form['band']
    xc.delete_band(band = request.form['band'])
    return band_list()

if __name__ == '__main__':
    app.run()