class ValueUnit:
    def __init__(self, value: int, unit: str):
        self.value = value
        self.unit = unit

    @classmethod
    def from_dict(cls, volume_info: dict):
        value = volume_info.get("value")
        unit = volume_info.get("unit")
        return cls(value, unit)


##################


class MashTemperaure:
    def __init__(self, temp: ValueUnit, duration: int):
        self.temp = temp
        self.duration = duration

    @classmethod
    def from_dict(cls, mesh_temperature_info: dict):
        temp = ValueUnit.from_dict(mesh_temperature_info.get("temp"))
        duration = mesh_temperature_info.get("duration")
        return cls(temp, duration)


class Fermentation:
    def __init__(self, temp: ValueUnit):
        self.temp = temp

    @classmethod
    def from_dict(cls, fermentation_info: dict):
        temp = ValueUnit.from_dict(fermentation_info.get("temp"))

        return cls(temp)


class Method:
    def __init__(
        self, mash_temp: MashTemperaure, fermentation: Fermentation, twist: str
    ):
        self.mash_temp = mash_temp
        self.fermentation = fermentation
        self.twist = twist

    @classmethod
    def from_dict(cls, method_info: dict):
        mash_temp = MashTemperaure.from_dict(method_info.get("mash_temp")[0])
        fermentation = Fermentation.from_dict(method_info.get("fermentation"))
        twist = method_info.get("twist")
        return cls(mash_temp, fermentation, twist)


##################


class Ingredients:
    def __init__(self, malt, hops, yeast):
        self.malt = malt
        self.hops = hops
        self.yeast = yeast

    @classmethod
    def from_dict(cls, ingredients_info: dict):
        malt = ingredients_info.get("malt")
        hops = ingredients_info.get("hops")
        yeast = ingredients_info.get("yeast")
        return cls(malt, hops, yeast)


class Beer:
    def __init__(
        self,
        id: int,
        name: str,
        tagline: str,
        first_brewed: str,
        description: str,
        image_url: str,
        abv: float,
        ibu: int,
        target_fg: int,
        target_og: int,
        ebc: int,
        srm: int,
        ph: float,
        attenuation_level: int,
        volume: ValueUnit,
        boil_volume: ValueUnit,
        method: Method,
        ingredients: Ingredients,
        food_pairing: list,
        brewers_tips: str,
        contributed_by: str,
    ):
        self.id = id
        self.name = name
        self.tagline = tagline
        self.first_brewed = first_brewed
        self.description = description
        self.image_url = image_url
        self.abv = abv
        self.ibu = ibu
        self.target_fg = target_fg
        self.target_og = target_og
        self.ebc = ebc
        self.srm = srm
        self.ph = ph
        self.attenuation_level = attenuation_level
        self.volume = volume
        self.boil_volume = boil_volume
        self.method = method
        self.ingredients = ingredients  # doar primele 3 chei
        self.food_pairing = food_pairing  # nu face object
        self.brewers_tips = brewers_tips
        self.contributed_by = contributed_by

    def __repr__(self) -> str:
        return str(self.id)

    @classmethod
    def from_json(cls, beer_json):
        """Create a beer object from parsed data"""
        id = beer_json.get("id")
        name = beer_json.get("name")
        tagline = beer_json.get("tagline")
        first_brewed = beer_json.get("first_brewed")
        description = beer_json.get("description")
        image_url = beer_json.get("image_url")
        abv = beer_json.get("abv")
        ibu = beer_json.get("ibu")
        target_fg = beer_json.get("target_fg")
        target_og = beer_json.get("target_og")
        ebc = beer_json.get("ebc")
        srm = beer_json.get("srm")
        ph = beer_json.get("ph")
        attenuation_level = beer_json.get("attenuation_level")

        volume = ValueUnit.from_dict(beer_json.get("volume"))
        boil_volume = ValueUnit.from_dict(beer_json.get("boil_volume"))
        method = Method.from_dict(beer_json.get("method"))
        ingredients = Ingredients.from_dict(beer_json.get("ingredients"))

        food_pairing = beer_json.get("food_pairing")
        brewers_tips = beer_json.get("brewers_tips")
        contributed_by = beer_json.get("contributed_by")

        return cls(
            id,
            name,
            tagline,
            first_brewed,
            description,
            image_url,
            abv,
            ibu,
            target_fg,
            target_og,
            ebc,
            srm,
            ph,
            attenuation_level,
            volume,
            boil_volume,
            method,
            ingredients,
            food_pairing,
            brewers_tips,
            contributed_by,
        )
