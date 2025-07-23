from enum import Enum

class PropertyType(str, Enum):
    ONE_BHK = "1BHK"
    TWO_BHK = "2BHK"
    THREE_BHK = "3BHK"
    FOUR_BHK = "4BHK"
    FIVE_BHK = "5BHK"
    PG = "pg"
    VILLA = "villa"

class ListingType(str, Enum):
    TENANT = "tenant"  # Looking for a tenant
    FLATMATE = "flatmate"  # Looking for a flatmate

class PreferenceType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    ANY = "any"

class FoodPreferenceType(str, Enum):
    VEG = "veg"
    NON_VEG = "non-veg"
    ANY = "any"