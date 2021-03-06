import os
import copy

class WrongValueException(Exception):
    pass

def loadThemes():
    allCss = {}
    basePath = os.path.join(os.path.dirname(__file__), "themes")
    templates = [os.path.join(basePath,o) for o in os.listdir(basePath)
                 if os.path.isdir(os.path.join(basePath,o))]
    for template in templates:
        themeName = os.path.basename(template)
        path = os.path.join(template, themeName + ".css")
        with open(path) as f:
            allCss[themeName] = "".join(f.readlines())
    return allCss

def loadBaseLayers():
    path = os.path.join(os.path.dirname(__file__), "baselayers", "baselayers.txt")
    with open(path) as f:
        text = "".join(f.readlines())
    return splitElements(text)

def loadBaseOverlays():
    path = os.path.join(os.path.dirname(__file__), "baselayers", "baseoverlays.txt")
    with open(path) as f:
        text = "".join(f.readlines())
    return splitElements(text)

def splitElements(s):
    lines = s.splitlines()
    css = {}
    element = None
    for line in lines:
        if line.strip().startswith("/*"):
            element = line.strip()[2:-2]
            css[element] = []
        elif element is not None:
            css[element].append(line)
    for element in css:
        css[element] = "\n".join(css[element])
    return css

def joinElements(els):
    s = ""
    for el, css in els.iteritems():
        s += "\n\n/*%s*/\n" % el
        s += css
    return s

baseLayers = loadBaseLayers()
baseOverlays = loadBaseOverlays()
themes = loadThemes()

defaultPanelContent = "<h1>Panel Title</h1>\n<p>This is the description of my web app</p>"

defaultWidgetsParams = {"About panel": {"content": defaultPanelContent,
                                        "isClosable": True,
                                        "showNavBarLink": True},
                        "Bookmarks": {"bookmarks": [],
                                      "format": 3,
                                      "interval": 3,
                                      "introText": "",
                                      "introTitle": "",
                                      "showIndicators": True},
                        "Chart tool": {"charts": {}},
                        "Overview map": {"collapsed":True},
                        "Scale bar": {"minWidth": 64,
                                      "units": ("metric", ("metric", "degrees", "imperial", "nautical", "us"))
                                      },
                        "Zoom controls": {"duration": 250, "zoomInLabel": "+", "zoomOutLabel": "-",
                                         "zoomInTipLabel": "Zoom in", "zoomOutTipLabel": "Zoom out", "delta": 1.2},
                        "Mouse position": {"coordinateFormat": "ol.coordinate.createStringXY(4)",
                                           "projection": "EPSG:4326", "undefinedHTML": "&nbsp;"},
                        "Layers list": {"tipLabel": "Layers",
                                        "showOpacity": False,
                                        "showZoomTo": False,
                                        "showDownload": False,
                                        "allowReordering": False,
                                        "showGroupContent":False},
                        "Selection tools": {"Select single feature": True,
                                            "Select by rectangle": True,
                                            "Select by polygon": True,
                                            "Select by point and radius": True,
                                            },
                        "Links": {"links":{}}
                        }


selectedFeaturesStyle = '''new ol.style.Style({
    fill: new ol.style.Fill({
        color: 'rgba(255, 100, 50, 0.3)'
    }),
    stroke: new ol.style.Stroke({
        width: 2,
        color: 'rgba(255, 100, 50, 0.8)'
    }),
    image: new ol.style.Circle({
        fill: new ol.style.Fill({
            color: 'rgba(255, 100, 50, 0.5)'
        }),
        stroke: new ol.style.Stroke({
            width: 2,
            color: 'rgba(255, 100, 50, 0.8)'
        }),
        radius: 7
    })
  })'''

highlightedFeaturesStyle = '''new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: '#f00',
      width: 1
    }),
    fill: new ol.style.Fill({
      color: 'rgba(255,0,0,0.1)'
    }),
    })'''

defaultAppSettings = {"Extent": ("Full globe extent", ("Full globe extent", 
                                "Clip to layers extent", "Move to layers extent")),
}


def initialize():
    global widgetsParams
    global currentCss
    global appSettings
    widgetsParams = copy.deepcopy(defaultWidgetsParams)
    currentTheme = "basic" if "basic" in themes else themes.keys()[0]
    currentCss =  themes[currentTheme]
    appSettings = copy.deepcopy(defaultAppSettings)

initialize()