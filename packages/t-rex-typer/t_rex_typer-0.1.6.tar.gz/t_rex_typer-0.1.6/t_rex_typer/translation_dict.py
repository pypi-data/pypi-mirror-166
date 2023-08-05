import re
import json


# single quotes are used in two ways. First, as apostrophes in the
# middle of a string of characters. Second at the boundary of a unit
# as a quote or as an abbreviation.  Exclude single quotes and parse
# these out later.
UNIT_REGEX = r"[\w']+|[{}()\[\]~`!@#$%^&*-_+=|\/.,:;\"]"


class TranslationDict:
    """Python dict-like storage for Plover dictionaries.

    Parameters
    ----------

    plover_dicts : iterable

      Iterable of paths to Plover dictionaries.

    """

    #############
    # Internals #
    #############
    # TranslationDict is not actually a dict.  The dict implementation
    # prevents it from working well with inheritance[1].  The
    # TranslationDict emulates a dict using the API given in the
    # Python documentation "(python) Emulating container types".
    #
    # INTERNAL API IMPLEMENTATION SHOULD USE 'self._data'.
    # EXTERNAL API IMPLEMENTATION SHOULD USE 'self'.
    #
    # [1] https://web.archive.org/web/20220313103021/https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/

    def __init__(self, plover_dicts=None):
        self._data = {}

        if plover_dicts:
            self._data = self.load_(plover_dicts)

    def __repr__(self):
        return self._data.__repr__()

    
    ##################################
    # Internals: container emulation #
    ##################################

    # The following functions are part of the Python API for dict-like
    # behavior. Details can be found in the Python documentation
    # "(python) Emulating container types".

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def get(self, key, default=None):
        try:
            return self._data[key]
        except KeyError:
            return default

    def pop(self, key, default=None):
        return self._data.pop(key, default)

    def __iter__(self):
        return self._data.__iter__()

    def keys(self):
        if not self._data:
            raise KeyError("No dictionary loaded.")
        return self._data.keys()

    def values(self):
        # get_strokes fails on IndexError when getting first element
        # when no dictionary loaded.
        if not self._data:
            raise ValueError("No dictionary loaded.")
        return self._data.values()

    def items(self):
        if not self._data:
            raise ValueError("No dictionary loaded.")
        return self._data.items()

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    
    #############
    # Externals #
    #############

    @staticmethod
    def load_(dictionary_list):
        """Convert Plover json dictionaries to Python dictionary.

        Parameters
        ----------

        dictionary_list : iterable

          Iterable (e.g. list or tuple) of Plover dictionary file
          paths in json format.

        Returns
        -------

        Python dict mapping strokes to phrases.


        """

        # TODO handle different dictionary types

        temp = {}
        for path in dictionary_list:
            with open(path, 'r') as f:
                contents = f.read()
                loaded = json.loads(contents)

            temp = {**temp, **loaded}

        return temp

    def load(self, dictionary_list):
        """Import Python dictionary from Plover json dictionaries.

        Parameters
        ----------

        dictionary_list : iterable

          Iterable (e.g. list or tuple) of Plover dictionary file
          paths in json format.

        """

        self._data = self.load_(dictionary_list)

    def _get_stroke_indices(self, unit):
        """Find indices of all strokes matching a unit.

        Parameters
        ----------
        unit : str

          A unit is the output of a stroke, such as–but not limited
          to–a word or phrase.

        Returns
        -------

        List of indices corresponding to strokes in the Plover
        dictionary.

        """

        # TODO fails to find some words and punctuation.  This may be
        # because of the direct comparison.  A unit may map to
        # something like '{~|"^}' (i.e. double quote, KW-GS).

        return [i for i, u in enumerate(list(self.values()))
                if u == unit.strip()]

    def get_strokes(self, unit, sorted=True):
        """Find strokes in the dictionary corresponding to the unit.

        Parameters
        ----------

        unit : str

          A unit is the output of a stroke, such as–but not limited
          to–a word or phrase.

        sorted : bool, optional

          When True, return the list of strokes ordered from shortest
          to longest.  Default is True.

        Returns
        -------

        List of strokes corresponding to the given unit.

        """

        # TODO performance?
        indices = self._get_stroke_indices(unit)
        strokes = [list(self.keys())[i] for i in indices]
        if sorted:
            strokes.sort(key=len)
        return strokes

    @staticmethod
    def split_into_strokable_units(text):
        """Split text into strokable units.

        NOTE: TODO: This is not likely accurate! It is assumed that
        text split on spaces and symbols will match a key in the
        Plover dictionary.  That assumption may not be true.  However,
        it should be good enough to get the application in a useable
        state.

        Parameters
        ----------
        text : str

          Text to be split.

        Returns
        -------

          List of strokable units (e.g. words and symbols)

        """

        # Symbols need to be strokable units except that single quote
        # shouldn't be a stroke unit if it appears inside a unit.  The
        # following works. TODO Is there a better way to express this?

        # split into words
        _split_with_single_quotes = re.findall(UNIT_REGEX, text)

        # split apostrophes at the beginning and end of a unit
        text_split = []
        for stroke_unit in _split_with_single_quotes:
            if stroke_unit[0] == "\'" or stroke_unit[-1] == "\'":
                for u in stroke_unit.split("\'"):
                    if u:
                        text_split.append(u)
                    else:
                        # split removes separator and returns empty
                        # string
                        text_split.append("'")
            else:
                text_split.append(stroke_unit)

        return text_split

    def translate(self, text):
        """Translate to steno strokes.

        Units are defined by the UNIT_REGEX and are translated
        one-to-one.  Each unit corresponds to a stroke.  For example,
        the unit "as well as" returns three strokes even if a brief
        exists to do it in one stroke.

        Parameters
        ----------

        text : str

          Corpus to be translated.

        Returns
        -------

        List of strokes corresponding to each unit in the text.

        """

        # TODO There may be optimizations here. Aside from the lookup
        # being slow, there's the issue of getting the correct
        # translation.  For example, "went" will be translated as
        # 'WEBLT' instead of 'WEPBT' since the strings have the same
        # length and B < P.
        split = self.split_into_strokable_units(text)
        translation = [self.get_strokes(u)[0] for u in split]
        return translation
