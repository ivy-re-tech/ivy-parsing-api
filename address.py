import re
from postal.parser import parse_address
import logging
from typing import List, Tuple

from pydantic import BaseModel
from usaddress import parse, tag, RepeatedLabelError, LABELS

logger = logging.getLogger("App")
first_cap_re = re.compile("(.)([A-Z][a-z]+)")
all_cap_re = re.compile("([a-z0-9])([A-Z])")


def convert(name):
    s1 = first_cap_re.sub(r"\1_\2", name)
    return all_cap_re.sub(r"\1_\2", s1).lower()


# relevant usaddress tags:
tag_map = {convert(label): label for label in LABELS}

libpostal_tag_map = {
    "postcode": "zip_code",
    "state": "state_name",
    "city": "place_name"
}


class Address(BaseModel):
    address_number_prefix: str = None
    address_number: str = None
    address_number_suffix: str = None
    street_name_pre_modifier: str = None
    street_name_pre_directional: str = None
    street_name_pre_type: str = None
    street_name: str = None
    street_name_post_type: str = None
    street_name_post_directional: str = None
    subaddress_type: str = None
    subaddress_identifier: str = None
    building_name: str = None
    occupancy_type: str = None
    occupancy_identifier: str = None
    corner_of: str = None
    landmark_name: str = None
    place_name: str = None
    state_name: str = None
    zip_code: str = None
    usps_box_type: str = None
    usps_box_id: str = None
    usps_box_group_type: str = None
    usps_box_group_id: str = None
    intersection_separator: str = None
    recipient: str = None
    not_address: str = None
    street_address: str = None

    @property
    def _all(self) -> List[str]:
        return [
            self.address_number_prefix,
            self.address_number,
            self.address_number_suffix,
            self.street_name_pre_modifier,
            self.street_name_pre_directional,
            self.street_name_pre_type,
            self.street_name,
            self.street_name_post_type,
            self.street_name_post_directional,
            self.subaddress_type,
            self.subaddress_identifier,
            self.building_name,
            self.occupancy_type,
            self.occupancy_identifier,
            self.corner_of,
            self.landmark_name,
            self.place_name,
            self.state_name,
            self.zip_code,
            self.usps_box_type,
            self.usps_box_id,
            self.usps_box_group_type,
            self.usps_box_group_id,
            self.intersection_separator,
            self.recipient,
            self.not_address,
        ]

    @property
    def _evals(self) -> List[bool]:
        return [x is None for x in self._all]

    @property
    def empty(self) -> bool:
        return all(self._evals)

    @property
    def arity(self) -> int:
        return sum([1 for e in self._evals if not e])

    def __str__(self):
        return " ".join([s for s in self._all if s])


def get_from_tags(parsed: List[Tuple[str, str]]) -> dict:
    """assemble a best-guess StreetAddress-compatible dictionary from parse"""
    base = dict(Address())
    seen = []
    for item in parsed:
        val, t = item
        if t in seen:
            # parsed is ordered, so we can detect the other address
            return base
        base.update({t: val})
        seen.append(t)
    return base


def clean_string(any_str: str):
    """remove commas and periods and other unwanted characters"""
    if not isinstance(any_str, str):
        return any_str
    unwanted = ",."
    for c in unwanted:
        return re.sub(c, "", any_str)


def multiparse(address: str) -> dict:
    """return a StreetAddress-compatible dictionary from either tag or parse"""
    base = dict(Address())
    parsed = {el[1]: el[0] for el in parse_address(address)}
    logger.info(parsed)
    street = format_street(parsed)

    try:
        out, input_type = tag(street)
    except RepeatedLabelError as e:
        parsed = parse(street)
        out = get_from_tags(parsed)
        input_type = "Ambiguous"

    base.update({"input_type": input_type})
    base.update({"street_address": street})
    base.update({k: out.get(v) for k, v in tag_map.items()})
    base.update({libpostal_tag_map.get(k, ""): v for k, v in parsed.items() if len(libpostal_tag_map.get(k, "")) > 0})
    return {k: clean_string(v) for k, v in base.items()}


def get_street_tags() -> List[str]:
    """These are the libpostal tags we're interested in"""
    return ["house_number", "po_box", "road", "unit"]


def format_street(components: dict) -> str:
    """Builds a street address from the parsed components from libpostal
    Supports P.O. Boxes as well as normal street addresses
    """
    return " ".join([components.get(el, "").title() for el in get_street_tags() if len(components.get(el, "")) > 0])

