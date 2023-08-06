from os import listdir as LD
from typing import List, Any

class render(object):
    def __load_all_file__(path) -> dict:
        re = {}
        for i in LD(path):
            re[i] = open(path + "/" + i, 'rb').read().decode()
        return re

    def __init__(self, PHtml : str | None = None, PCss : str | None = None, PJs : str | None = None) -> None:
        '''
        \r R = render(PHtml, PCss, PJs) -> render constructed.
        \r PHtml    : Main path to all the files that is html file
        \r PCss     : Main path to all the files that is css file
        \r PJs      : Main path to all the files that is js file
        '''
        self.__phtml__ = PHtml
        self.__pcss__ = PCss
        self.__pjs__ = PJs
        self.__dhtml__ = render.__load_all_file__(PHtml)
        self.__dcss__ = render.__load_all_file__(PCss)
        self.__djs__ = render.__load_all_file__(PJs)
    
    def __create_newtab__(tagname: str = "", tagvalue : Any | str = "", **tagattributes):
        att = " ".join([f'{i}={tagattributes[i]}' for i in tagattributes.keys()])
        return f'\r<{tagname} {att}>{tagvalue}</{tagname}>\n'
        

    def render(self, key_html : str, lkey_css : List[str] | None = None, lkey_js : List[str] | None = None):
        stl = None
        scc = None
        if lkey_css is not None:
            css = '\n'.join([self.__dcss__[i] for i in lkey_css])
            stl = render.__create_newtab__('style', css)
        if lkey_js is not None:
            js = '\n'.join([self.__dcss__[i] for i in lkey_js])
            scc = render.__create_newtab__('script', js)
        try:
            html = self.__dhtml__[key_html] 
            if stl:
                loc = html.find('</head>')
                html = html[:loc] + stl + html[loc:]
            if scc:
                loc = html.find('</body>')
                html = html[:loc] + scc + html[loc:]
            return html
        except:
            raise Exception()
    @property
    def dhtml(self) -> dict:
        return self.__dhtml__

    @dhtml.setter
    def dhtml(self, value : dict) -> None:
        self.__dhtml__ = value
    
    @property
    def dcss(self) -> dict:
        return self.__dcss__
    @dcss.setter
    def dcss(self, value: dict) -> None:
        self.__dcss__ = value

    @property
    def djs(self) -> dict:
        return self.__djs__
    @djs.setter
    def djs(self, value: dict) -> None:
        self.__djs__ = value