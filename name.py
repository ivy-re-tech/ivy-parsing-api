import logging
import string
from collections import OrderedDict
from functools import reduce
from typing import List, Optional, Tuple

from fastapi import HTTPException
from probablepeople import parse, tag, RepeatedLabelError
from pydantic import BaseModel

logger = logging.getLogger("App")

# by no means complete -- we see "Smith Fam Lving Tr st" all the time
remove_list = ["tr", "trust", "living", "family", "revocable", "rev", "etal"]

CORP = "Corporation"
PERSON = "Person"
GIVEN = "GivenName"
MIDDLE = "Middle"
SURNAME = "Surname"
AND = "And"

expand = lambda x: x.expand()  # call expand on the SurnameGrouping class
extend = lambda x, y: x + y  # add two things... like lists in a reduce call


class Name(BaseModel):
    first_name: str = None
    middle_name: str = None
    last_name: str = None
    entity_name: str = None
    empty: bool = None
    arity: int = None

    def __init__(
        self,
        first_name: str = None,
        middle_name: str = None,
        last_name: str = None,
        entity_name: str = None,
        *args,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.entity_name = entity_name
        self.empty = self._empty
        self.arity = self._arity

    @property
    def _evals(self) -> List[bool]:
        return [
            self.first_name is None,
            self.last_name is None,
            self.middle_name is None,
            self.entity_name is None,
        ]

    @property
    def _empty(self) -> bool:
        return all(self._evals)

    @property
    def _arity(self) -> int:
        return sum([1 for e in self._evals if not e])

    def __str__(self):
        return self.entity_name or " ".join(
            [s for s in [self.first_name, self.middle_name, self.last_name] if s]
        )


class NameResponse(BaseModel):
    source: str = None
    names: List[Name] = None
    best: Name = None
    category: str = None
    error: str = None


class LabelPair:
    """a (<component_value>, <component_name>) pair"""

    TBL = str.maketrans("", "", string.punctuation)

    def __init__(self, item: Tuple[str, str]):
        self.value, self.label = item
        self._clean()

    def _clean(self):
        self.value = self.value.translate(self.TBL)

    def __iter__(self):
        yield self.value
        yield self.label


class NamePair:
    """first and middle name for a SurnameGrouping"""

    def __init__(self):
        self.first_name = None
        self.middle_name = None

    def add(self, item: LabelPair):
        if GIVEN in item.label:
            self.first_name = item.value
        elif MIDDLE in item.label:
            self._add_middle(item.value)

    def _add_middle(self, new_middle: str) -> None:
        nm = " ".join([self.middle_name or "", new_middle])
        self.middle_name = nm

    def __str__(self):
        return " ".join([self.first_name or "", self.middle_name])


class SurnameGrouping:
    def __init__(self, surname: str):
        self.surname: str = surname
        self.name_pairs: List[NamePair] = [NamePair()]

    @property
    def current(self) -> NamePair:
        return self.name_pairs[-1]

    def start_new(self, item: LabelPair) -> bool:
        """based on current label and NamePair, should we start a new NamePair?"""
        if self.current.first_name and (GIVEN in item.label or AND in item.label):
            return True
        return False

    def add(self, item: LabelPair):
        if not self.start_new(item):
            self.current.add(item)
        else:
            np = NamePair()
            np.add(item)
            self.name_pairs.append(np)

    def expand(self):
        return [
            Name(
                first_name=pair.first_name,
                middle_name=pair.middle_name,
                last_name=self.surname,
            )
            for pair in self.name_pairs
        ]

    def __str__(self):
        return f"{self.surname}, {len(self.name_pairs)}"


def parsed_name_retrieve(tag_list: List[Tuple[str, str]]) -> List[Name]:
    groupings: List[SurnameGrouping] = []
    pairs = [LabelPair(item) for item in tag_list]
    if pairs and SURNAME in pairs[0].label:  # "if pairs" is a guard for empty list
        pairs.reverse()

    pool = []
    # if it's not a surname, add it to the pool
    # when we hit a surname: construct the grouping, reset the pool
    for p in pairs:
        if not (SURNAME in p.label):
            pool.append(p)
        else:
            grp = SurnameGrouping(surname=p.value)
            for deferred in pool:
                grp.add(deferred)
            groupings.append(grp)
            pool = []

    names = reduce(extend, map(expand, groupings))
    return names


def tagged_name_retrieve(tagged: OrderedDict) -> List[Name]:
    """split an OrderedDict from probablepeople.tag into a list of dicts of
    name components

    This function relies (implicitly, sorry) on the ordering of tagged elements
    coming from probable people.

    This is optimized for names like "SMITH, JACK C & JILL Q"

    Names like "John and George Kershall" will return only viable name.
    """
    result = []
    current = Name()
    for k, v in tagged.items():
        if "GivenName" in k:
            current.first_name = v
        elif "MiddleName" in k:
            current.middle_name = v
        elif "Surname" in k:
            current.last_name = v
        elif "And" in k:
            result.append(current)
            current = Name()
    result.append(current)
    return result


def get_names(name_str: str) -> Tuple[List[Name], Optional[str]]:
    if not name_str:
        return [], None
    name_str = " ".join(
        [
            component.title()
            for component in name_str.split()
            if component.lower() not in remove_list
        ]
    )
    try:
        tagged, category = tag(name_str)
        if category == CORP:
            return [Name(entity_name=name_str)], category
        elif category == PERSON:
            return tagged_name_retrieve(tagged), PERSON
        else:  # Household (ie: multiple names) should be the only other option
            return parsed_name_retrieve(parse(name_str)), category
    except RepeatedLabelError as e:
        tag_list = e.parsed_string  # this is actually the same as parse(<name>)
        return parsed_name_retrieve(tag_list), None


def choose_name(names: List[Name]) -> Optional[Name]:
    # If we don't have any Name with something in it, return None
    if not [n for n in names if not n.empty]:
        return None

    current = None
    for name in names:
        if name.arity >= 3 and not name.entity_name:  # first, middle, last
            return name
        # absent that, something worthwhile
        if name.first_name and name.last_name:
            current = name
    # return our best option (or something, at least)
    return current or names[0]


def run_parse(fullname: str) -> dict:
    if not fullname:
        raise HTTPException(status_code=400, detail="No name parameter found")
    names, category = get_names(fullname)

    error = ""
    if category is None:
        category = "Crowded"
        error = "This name appears to represent many people."
    elif category == CORP:
        error = "The name appears to be from a corporation or other non-person entity."

    return {
        "source": fullname,
        "names": names,
        "best": choose_name(names),
        "category": category,
        "error": error,
    }
