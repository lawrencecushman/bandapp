from lxml import etree
from lxml.etree import XMLSyntaxError


def xmlIsValid(filepath, schemapath):
    try:
        with open(schemapath, 'r') as f:
            schema_root = etree.XML(f.read())
        schema = etree.XMLSchema(schema_root)
        xmlparser = etree.XMLParser(schema=schema)
        with open(filepath, 'r') as f:
            etree.fromstring(f.read(), xmlparser)
        return [True,'The xml is valid']
    except XMLSyntaxError, e:
        print e.message
        return [False,e]
    except IOError, e:
        print e.message
        print "FILE: ", filepath
        print "SCHEMA: ", schemapath
        return [False,e]
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
        return [False,message]


def getAllBands():
    try:
        tree = etree.parse('static/bands.xml')
        bands = tree.getroot() #returns 'Bands' element, which is a list-like object
        return bands
    # Catch a general exception.
    except Exception, e:
        print "Error:", type(e), ": ",e.message
        return e.message


def getBand(band):
    try:
        tree = etree.parse('static/bands.xml')
        bands = tree.getroot() #returns 'Bands' element, which is a list-like object
        bandElement =  bands.xpath(str.format('Band[@name="{}"]',band)) #get specific band
        return bandElement
    # Catch a general exception.
    except Exception, e:
        print "Error:", type(e), ": ",e.message
        return e.message


def createBand(band):
    try:
        tree = etree.parse('static/bands.xml')
        bands = tree.getroot() #returns 'Bands' element, which is a list-like object
        bandElement =  bands.xpath(str.format('Band[@name="{}"]',band)) #get specific band
        return bandElement
    # Catch a general exception.
    except Exception, e:
        print "Error:", type(e), ": ",e.message
        return e.message


def addmember(band, instrument, fullname, joindate):
    try:
        parser  = etree.XMLParser(remove_blank_text=True)  # deals with whitespace

        # parse into a tree
        tree = etree.parse(source='static/bands.xml',parser=parser)

        # The band to insert the performer into
        bandEmt = tree.find(str.format('/Band[@name="{}"]',band))

        # build the new Performer
        a = {'instrument': instrument, 'join-date': joindate}  # create attributes
        element = etree.Element('Performer', attrib=a)
        element.text = fullname

        # calculate insertion point. After all Genres and Performers
        insertionPoint = len(bandEmt.findall('Performer')) + len(bandEmt.findall('Genre'))
        bandEmt.insert(insertionPoint, element)
        tree.write('static/bands.xml', pretty_print=True)
        print etree.tostring(tree, pretty_print=True)
        return "looking good"
    except Exception, e:
        print "Error:", type(e), ": ",e.message
        return e.message


#todo: Refactor using this
def getTree() :
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse('static/bands.xml')
        return tree
    except Exception, e:
        print "Error:", type(e), ": ",e.message
        return e


def writeTree(tree) :
    tree.write('static/bands.xml', pretty_print=True)
    print etree.tostring(tree, pretty_print=True)
    return 200

def lxmlFindBand(band, tree):
    bandEmt = tree.find(str.format('/Band[@name="{}"]',band))
    return bandEmt


def deletePerformer(band, performerno):
    # Get the DOM and band
    tree = getTree()
    if type(tree) is Exception:
        return 400
    bandEmt = lxmlFindBand(band, tree)

    # Find the performer
    performer = bandEmt.find(str.format("Performer[{}]",performerno))
    bandEmt.remove(performer)
    writeTree(tree)
    return 200


def update_city(band, value):
    print 'update_City'
    # Get the DOM and band
    tree = getTree()
    if type(tree) is Exception:
        return 400
    bandEmt = lxmlFindBand(band, tree)
    bandEmt.find('Hometown/City').text = value
    writeTree(tree)
    return 200


def update_province(band, value):
    print 'update_province'
    tree = getTree()
    if type(tree) is Exception:
        return 400
    bandEmt = lxmlFindBand(band, tree)
    bandEmt.find('Hometown/StateOrProvince').text = value
    writeTree(tree)
    return 200


def update_country(band, value):
    print 'update_country'
    tree = getTree()
    if type(tree) is Exception:
        return 400
    bandEmt = lxmlFindBand(band, tree)
    bandEmt.find('Hometown/Country').text = value
    writeTree(tree)
    return 200


def update_genre(band, value):
    print 'update_genre'
    tree = getTree()
    if type(tree) is Exception:
        return 400
    bandEmt = lxmlFindBand(band, tree)
    bandEmt.find('Genre').text = value
    writeTree(tree)
    return 200


def update_label(band, value):
    print 'update_label'
    tree = getTree()
    if type(tree) is Exception:
        return 400
    bandEmt = lxmlFindBand(band, tree)
    bandEmt.set("label", value)
    writeTree(tree)
    return 200


def deleteSong(band, album, songno):
    # Get the DOM and band
    tree = getTree()
    if type(tree) is Exception:
        return 400
    bandEmt = lxmlFindBand(band, tree)

    #find the album
    albumEmt = bandEmt.find(str.format('Album[@title="{}"]',album))
    print 'AE: ', album,'?=', albumEmt

    # Find the song
    song = albumEmt.find(str.format("Song[{}]",songno))
    albumEmt.remove(song)
    writeTree(tree)
    return 200


def add_song(band, album, songtitle, duration):
    tree = getTree()
    if type(tree) == Exception:
        return 400

    # get the album element
    bandEmt = lxmlFindBand(band, tree)
    albumEmt = bandEmt.find(str.format('Album[@title="{}"]',album))

    #build the song element
    songID = 's999999'
    a = {'songID':songID, 'title': songtitle, 'length': duration}
    songEmt = etree.Element('Song',a)

    print songEmt
    albumEmt.append(songEmt)

    writeTree(tree)
    return 200