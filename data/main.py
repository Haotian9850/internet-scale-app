from pyspark import SparkContext 
import requests
import json


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
    for id in result:
        result[id] = list(result[id])
    return result



def update_recommendations(recommendations):
    try:
        print(json.dumps(recommendations))
        res = requests.post(
            "http://entity:8000/api/v1/update_recommendations",
            data={
                "recommendations":json.dumps(recommendations)
            }
        )
    except requests.exceptions.Timeout:
        print("request timed out")
    except requests.exceptions.HTTPError as err:
        print("request failed with HTTPError {}".format(err.response.text))
    print(res.text)



if __name__ == "__main__":
    view_counts = dict()
    sc = SparkContext("spark://spark-master:7077", "PopularPets")
    data = sc.textFile("/tmp/data/log_dump.txt", 2)
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
    recommendations = make_recommendations(co_view_list, view_counts)
    print(recommendations)
    print("sending updated recommendations to entity...")
    update_recommendations(recommendations)

