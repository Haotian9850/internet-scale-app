from pyspark import SparkContext 


def check_counts(counts, id):
    return counts.get(id, 0) >= 3


def make_recommendations(co_view_list, counts):
    result = dict()
    for co_views in co_view_list:
        for id in co_views:
            recommendations = set()
            for possible_recommendation in co_views:
                if check_counts(counts, possible_recommendation):
                    recommendations.add(possible_recommendation)
            if id in recommendations:
                recommendations.remove(id)
            result[id] = result.get(id, set()).union(recommendations)
    return result



if __name__ == "__main__":
    view_counts = dict()

    sc = SparkContext("spark://spark-master:7077", "PopularPets")
    data = sc.textFile("/tmp/data/pet_view_log.txt", 2)
    pairs = data.map(lambda line: line.split(":"))
    pages = pairs.map(lambda pair: (pair[1], 1))
    count = pages.reduceByKey(lambda x, y: int(x) + int(y))
    co_views = pairs.groupByKey()
    for pet_id, count in count.collect():
        print("pet_id: {}, views: {}".format(
            pet_id,
            count
        ))
        view_counts[pet_id] = view_counts.get(pet_id, 0) + count
    co_view_list = []
    for username, views in co_views.collect():
        co_view_list.append(set([pet_id for pet_id in views]))
           
    sc.stop()
    print(co_view_list)
    print(view_counts)
    print(make_recommendations(co_view_list, view_counts))

