#! /usr/bin/python
import requests
import json
import os
import argparse
import re
import random
from platform import system
from uuid import uuid4 as rand_name
from lastfm.api import LastAPI
from subprocess import Popen, PIPE
from sys import stderr, stdout
from math import ceil
from time import sleep

#global constants
lastapi = None
class const:
    LINUX = 'LINUX'
    WINDOWS = 'WINDOWS'
    OSX = 'OSX'
    RANDOMSOURCE = 'randomsource'
    RANDOMART = 'randomart'
    TOPALBUMS = 'topalbums'
    TOPARTISTS = 'topartists'
    TOPTRACKS = 'toptracks'
    LOVEDTRACKS = 'lovedtracks'
    ARTISTART = 'artistart'
    ALBUMART = 'albumart'
    BADIMAGESIZE = 654

    #global variables
    _PLATFORM = None
    _SOURCE_PRIORITY = RANDOMSOURCE
    _ART_PRIORITY = RANDOMART
    _ROUND_DOWN_TILE_SIZE = False
    _USE_ALBUM_ART = True
    _USE_ARTIST_ART = True
    _IMAGE_DIR = 'pics'
    _OUTPUT_DARKNESS = 0
    _OUTPUT_DESATURATION = 0
    #montage -background black -bordercolor black ./pics/* output.jpg



#look at this for the image stitcher
#http://www.imagemagick.org/script/command-line-options.php?ImageMagick=8fg7b7mbhs8tfjg3pr27ti49a2#geometry
#http://www.imagemagick.org/download/python/ (up to date!)

#Final output command for 1920x1080
#montage -tile 32x9  -geometry 120x120+1+1 -background black -bordercolor black * dual_output.jpg
#Have to add a 'image-size' command, possibly save bandwidth by getting the smaller images.
#>>>Maybe derive from resolution, so resolution & tile-size (default 120x120) >yeilds final geometry

def run(args):
    #Setup global args
    set_args(args)
    set_platform()
    
    #Setup API
    apikey = args['api_key']
    username = args['user_name']
    global lastapi
    lastapi = LastAPI(username, apikey)
    
    #Setup image and tile geometry
    tile_size = args['target_tile_size']
    round_pref = args['round_down_tile_size']
    image_size = args['image_size']
    output_darkness = args['output_darkness']
    output_desaturation = args['output_desaturation']
    width = None
    height = None
    
    if image_size is not None:
        width, height = parse_resolution(image_size)
    else:
        width, height = get_resolution()
    width = int(width)
    height = int(height)

    tile_geometry = generate_tile_geometry(width, height, tile_size,
                                           round_tilesize_down=round_pref)
    tiles_x, tiles_y, tilesize, total_tiles = tile_geometry

    #Generate Image
    rc = args['rearrange_current']
    aset = args['auto_set']
    generate_image(width, height, tiles_x, tiles_y, tilesize, total_tiles,
                   output_darkness, output_desaturation, rearrange_current = rc,
                   autoset = aset)
    
#def get_loved_track_images(user, apikey):
#    r = requests.get(url, params=params)
#    data = json.loads(r.content)
#    return data['lovedtracks']['track']

def generate_image(image_x, image_y, tiles_x, tiles_y, tilesize, total_tiles,
                   output_darkness, output_desaturation, autoset=False,
                   rearrange_current=False):

    localpath = const._IMAGE_DIR+'/albumart'
    if rearrange_current == True:
        artpath = os.path.abspath(localpath+'/')
        [os.rename(os.path.join(artpath, f), os.path.join(artpath, str(rand_name()))) for f in os.listdir(artpath)]
    else:
        albums = lastapi.user.getTopAlbums(limit=(total_tiles*2))
        urls = []
        for a in albums:
            a.images.select_largest()
            urls.append(a.images.get_selected_image_url())

        urls = list(set(urls))
        random.shuffle(urls)
        content = dict()
        for url in urls:
            update_download_status('Downloading {0} of {1} images'.format(len(content), total_tiles))
            image = download_selected_image(url)
            if image:
                content[image] = rand_name()
            if len(content) >= total_tiles:
                break

        write_quick_and_dirty_dict(localpath, content)

    #GENERATE IMAGE
    output_name = str(rand_name())+'.jpg'
    grey_output_name = 'grey_'+str(output_name)
    composite_output_name = 'composite_'+str(output_name)
    final_output_name = 'final_'+str(output_name)
    
    output_name = const._IMAGE_DIR + '/' + output_name
    grey_output_name = const._IMAGE_DIR + '/' + grey_output_name
    composite_output_name = const._IMAGE_DIR + '/' + composite_output_name
    canvas_output_name = const._IMAGE_DIR + '/canvas.jpg'
    canvas_color = 'black'
    final_output_name = const._IMAGE_DIR + '/final.jpg'
    
    #Create montage
    CMD = 'montage -tile %sx%s  -geometry %sx%s+0+0 -background black -bordercolor black %s/* %s'%\
    (str(tiles_x), str(tiles_y), str(tilesize), str(tilesize), str(localpath), str(output_name))
    _exec_cmd(CMD)
    
    #Create grey-scale version
    CMD = 'convert %s -colorspace Gray %s' % (output_name, grey_output_name)
    _exec_cmd(CMD)    
    
    #composite both together to desaturate
    CMD = 'composite %s -blend 20x80 %s %s' % (output_name, grey_output_name,
                                               composite_output_name)
    _exec_cmd(CMD)
    
    #create black canvas for darkening
    CMD = 'convert -size %sx%s xc:%s %s' % (image_x, image_y, canvas_color,
                                            canvas_output_name)
    _exec_cmd(CMD)
    
    #composite both together to desaturate
    CMD = 'composite %s -blend 20x80 %s %s' % (composite_output_name,
                                               canvas_output_name,
                                               final_output_name)
    _exec_cmd(CMD)
    
    CMD = 'rm %s %s %s %s' % (output_name, grey_output_name,
                              composite_output_name, canvas_output_name)
    _exec_cmd(CMD)
    
    full_path = os.path.abspath(final_output_name)

    print full_path
    if autoset == True:
        CMD = 'gsettings set org.gnome.desktop.background picture-uri file://%s' % full_path
        _exec_cmd(CMD)        

def update_download_status(msg):
    stdout.write(str(msg) + '\r')
    stdout.flush()
    
def _exec_cmd(cmd):
    out, err = Popen(cmd, bufsize=1, stderr=PIPE, shell=True).communicate()

    if (out != None) and (err != None):
        print cmd
        print '\n'
        print err
        print 'Problem generating montage'
        
def download_selected_image(url):
        s = url.split('/')
        url_name = s[len(s) - 1]

        r = requests.get(url)
        r.raw.decode_content = True

        if not r.ok or url_name == 'default_album_medium.png':
            return ""
        return r.content

def write_quick_and_dirty_dict(localpath, teh_dict):
    for data, name in teh_dict.items():
        try:
            os.mkdir(localpath)
        except:
            pass
        loc = "{0}/{1}".format(localpath, name)
        f = open(loc, 'wb')
        f.write(data)
        f.close()


def set_args(args):
    global const
    #global _SOURCE_PRIORITY
    #global _ART_PRIORITY
    #global _ROUND_DOWN_TILE_SIZE
    #global _TARGET_TILE_SIZE
    #global _IMAGE_HEIGHT
    #global _IMAGE_WIDTH
    #global _USER_CONFIG
    #global _USE_ARTIST_ART
    #global _USE_ALBUM_ART
    #global _IMAGE_DIR


    const._IMAGE_DIR = args['image_dir']
    const._USE_ARTIST_ART = args['use_album_art']
    const._USE_ALBUM_ART = args['use_artist_art']
    
    const._SOURCE_PRIORITY = const.TOPALBUMS if args['top_albums_first'] else\
                       const.TOPARTISTS if args['top_artists_first'] else\
                       const.TOPTRACKS if args['top_tracks_first'] else\
                       const.LOVEDTRACKS  if args['loved_tracks_first'] else\
                       const.RANDOMSOURCE
    
    const._ART_PRIORITY = const.ARTISTART if args['artist_art_first'] else\
                    const.ALBUMART if args['album_art_first'] else\
                    const.RANDOMART


def generate_tile_geometry(width, height, tilesize, round_tilesize_down=False):
    portrait_mode = False
    if height > width:
        t = height
        height = width
        width = t
        portrait_mode = True

    ratio = float(width) / float(height)
    multiplier = 10.0
    if ((ratio*multiplier) % 1) > 0:
        multiplier = 9.0

    numerator = ratio * multiplier
    gcd = __gcd(numerator, multiplier)    
    aspect_x = numerator / gcd
    aspect_y = multiplier / gcd
    
    #Set default tile sizes 'native'
    tile_size = width / aspect_x
    tiles_x = aspect_x
    tiles_y = aspect_y
    
    if tilesize != 0:
        tile_size = tilesize
        if round_tilesize_down:
            tiles_x = int(float(width) / float(tile_size))
            tiles_y = int(float(height) / float(tile_size))
        else:
            tiles_x = ceil(float(width) / float(tile_size))
            tiles_y = ceil(float(height) / float(tile_size))
    
    if portrait_mode:
        t = tiles_x
        tiles_x = tiles_y
        tiles_y = t
        
    total_tiles = tiles_x * tiles_y
    
    #May need to return these for images that are larger than specified size
    #final_x = tiles_x * tile_size
    #final_y = tiles_y * tile_size

    return (int(tiles_x), int(tiles_y), int(tile_size), int(total_tiles))

def __gcd(a, b):
    a = int(a)
    b = int(b)
    while b:
        a,b = b,a%b
    return a    

def set_platform():
    global PLATFORM
    pinfo = system()
    if re.search('linux', pinfo, re.IGNORECASE):
        PLATFORM = const.LINUX
    elif re.search('darwin', pinfo, re.IGNORECASE):
        PLATFORM = const.OSX
    elif re.search('windows', pinfo, re.IGNORECASE):
        PLATFORM =const.WINDOWS
    elif re.search('microsoft', pinfo, re.IGNORECASE):
        PLATFORM = const.WINDOWS
    else:
        PLATFORM = const.LINUX       

def get_resolution():
    try:
        if PLATFORM == const.LINUX:    
            out,err = Popen("xrandr | grep '*'", bufsize=0, stdout=PIPE,
                                  stderr=PIPE,shell=True).communicate()
            if err:
                raise 'Error autodetecting resolution'
            return parse_resolution(out)

        else:
            from Tkinter import Tk
            r = Tk()
            return (r.winfo_screenwidth(), r.winfo_screenheight())

    except Exception as e:
        print e
        stderr.write('Unable to auto-detect resolution. '
                     + 'Please re-run with -is \'width\'x\'height\' to'
                     + 'explicitly define output image resolution')            
    
def parse_resolution(res):
    match = re.findall('([0-9]+)x([0-9]+)', res)
    return match[0]    


if __name__ == '__main__':
    desc = 'Scrobbled Art Background Maker.'\
           + '\nGet API Key at http://www.last.fm/api/account.'\
           + '\nDefault output image size is 1920x1080'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-k', '--api-key', help="LAST.FM Public API Key", required=True)
    parser.add_argument('-u', '--user-name', help="LAST.FM user account", required=True)
    parser.add_argument('-i', '--image-dir', help="Directory to hold downloaded images.", default='./pics')
    parser.add_argument('-is', '--image-size', help="['<width>x<height>': Absolute widthxheight of the background image.  By default, autop-detects image size based on current monitor resolution.")
    parser.add_argument('-rc', '--rearrange-current', action='store_true', default='False', help="Rearrange current background")
    parser.add_argument('-as', '--auto-set', action='store_true', default='False', help="Automatically set image as background.")
    parser.add_argument('--target-tile-size', default=0, help='Try and make each tile roughly this size square.  Default is to automatically chose a tilesize that fills up the image size.')
    parser.add_argument('--round-down-tile-size', action='store_true', default=False, help='Makes the image smaller than the given image size if art would otherwise be cut-off at the edges.')
    parser.add_argument('--output-darkness', default=0, help='As a percent. Default 0.  Bring the total brightness of the image down by the specified percent.')
    parser.add_argument('--output-desaturation', default=0, help='As a percent. Default 0. Desaturate final image by specified percent')
    
    
    parser.add_argument('--use-album-art', action='store_true', default=True, help='Use album art in output.')
    parser.add_argument('--use-artist-art', action='store_true', default=True, help='Use artist art in output.')
    parser.add_argument('--use-top-albums', action='store_true', default=True, help='Use Top Albums before other sources')
    parser.add_argument('--use-top-artists', action='store_true', default=False, help='Use Top Artists before other sources')
    parser.add_argument('--use-top-tracks', action='store_true', default=True, help='Use Top Tracks before other sources')
    parser.add_argument('--use-loved-tracks', action='store_true', default=True, help='Use Loved Tracks before other sources')    
    
    aagroup = parser.add_mutually_exclusive_group()
    aagroup.add_argument('--artist-art-first', action='store_true', help='Use available artist art before using any album art.')
    aagroup.add_argument('--album-art-first', action='store_true', help='Use available album art before using any album art.')
    
    upgroup = parser.add_mutually_exclusive_group()
    upgroup.add_argument('--top-albums-first', action='store_true', help='Use Top Albums before other sources')
    upgroup.add_argument('--top-artists-first', action='store_true', help='Use Top Artists before other sources')
    upgroup.add_argument('--top-tracks-first', action='store_true', help='Use Top Tracks before other sources')
    upgroup.add_argument('--loved-tracks-first', action='store_true', help='Use Loved Tracks before other sources')
    args = vars(parser.parse_args())

    run(args)
