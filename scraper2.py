import wikirepo
from wikirepo.data import wd_utils
from datetime import date

ents_dict = wd_utils.EntitiesDict()
# Strings must match their Wikidata English page names
countries = ["Germany", "United States of America", "People's Republic of China"]
# countries = ["Q183", "Q30", "Q148"] # we could also pass QIDs
# data.incl_lctn_lbls(lctn_lvls='country') # or all countries`