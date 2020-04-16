#####################################################
#                  Liam Floyd
#                    CS461
#                   Program 4
#####################################################
import tensorflow as tf
import review
import count


def main():
    ratings_list = load_data()


def load_data():
    ratings = []
    major_brands = get_major_brand()
    top_vars = get_top_var()

    ratings_file = open("ramen-ratings.csv", "r", encoding="utf-8")
    for line in ratings_file:
        val = line.split(',')

        if len(val) < 3:
            continue

        # Check if the brand is a main brand or "Other"
        if val[1] not in major_brands:
            brand_name = "Other"
        else:
            brand_name = val[1]
        # Count only the top 100 varieties
        vars_list = val[2].split()
        valid_vars = []
        for item in vars_list:
            if item in top_vars:
                valid_vars.append(item)

        temp_review = review.Review(val[0], brand_name, valid_vars, val[3], val[4], val[5])
        ratings.append(temp_review)
        
    ratings_file.close()
    return ratings


def get_major_brand():
    """Count each instance of a brand and return a list of major brands"""
    in_file = open("ramen-ratings.csv", "r", encoding="utf-8")
    brand_count = []
    for line in in_file:
        val = line.split(',')
        # Handle invalid lines
        if len(val) < 3:
            continue

        # Add the first value if the list is empty
        if len(brand_count) == 0:
            temp_brand = count.Count(val[1])
            brand_count.append(temp_brand)
        else:
            for item in brand_count:
                # If the brand is already present, increase the count by 1
                if val[1] == item.name:
                    item.add_count()
                    break

            # If brand hasn't been accounted for, add it
            temp_brand = count.Count(val[1])
            brand_count.append(temp_brand)

    # Create list of Brands with more than 1 occurrence
    major_brands = []
    for brand_object in brand_count:
        if brand_object.count > 1:
            major_brands.append(str(brand_object))

    in_file.close()
    return major_brands


def get_top_var():
    """Find the top 100 variety keywords and return a list of strings"""
    in_file = open("ramen-ratings.csv", "r", encoding="utf-8")
    raw_vars = []
    for line in in_file:
        val = line.split(',')
        if len(val) < 3:
            continue

        varieties = val[2].split()

        for var in varieties:
            if len(raw_vars) == 0:
                temp_brand = count.Count(var)
                raw_vars.append(temp_brand)
            else:
                for item in raw_vars:
                    # If the var is already present, increase the count by 1
                    if var == item.name:
                        item.add_count()
                        break
                # If var hasn't been accounted for, add it
                temp_brand = count.Count(var)
                raw_vars.append(temp_brand)

    var_list = []
    for cnt in range(100):
        # Take the top 100 varieties and add them to the list
        temp_var = cnt_max(raw_vars)
        raw_vars.remove(temp_var)
        var_list.append(str(temp_var))

    in_file.close()
    return var_list


def cnt_max(in_list):
    """Returns a max from a list of count objects"""
    temp_max = count.Count("benchmark")
    for item in in_list:
        if item.count > temp_max.count:
            temp_max = item
    return temp_max


if __name__ == "__main__":
    main()