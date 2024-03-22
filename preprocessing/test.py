import pycountry_convert as pc


def get_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    continent_name = pc.convert_continent_code_to_continent_name(continent_code)
    return continent_name


# Example: Get the continent of Australia
print(get_continent("France"))
