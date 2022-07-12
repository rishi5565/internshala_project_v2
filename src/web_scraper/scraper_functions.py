
def format_categories(category_list, wfh_status):
    final_params = []
    for category in category_list:
        category = category.strip().lower()
        category = category.replace(' ','-')
        final_params.append(category)
    final_params = ','.join(final_params)
    if wfh_status == True:
        final_params+='-internships'
    elif wfh_status == False:
        final_params+='-internship'
    return final_params


def format_locations(location_list):
    final_params = []
    for location in location_list:
        location = location.strip().lower()
        location = location.replace(' ','-')
        final_params.append(location)
    final_params = ','.join(final_params)
    final_params ='-in-'+final_params

    return final_params