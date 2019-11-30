from pyspark import SparkContext 


if __name__ == "__main__":
    sc = SparkContext("spark://spark-master:7077", "PopularPets")
    data = sc.textFile("/tmp/data/pet_view_log.txt", 2)
    pairs = data.map(lambda line: line.split(":"))
    pages = pairs.map(lambda pair: (pair[0], 1))
    count = pages.reduceByKey(lambda x, y: int(x) + int(y))
    output = count.collect()
    for pet_id, count in output:
        print("pet_id: {}, views: {}".format(
            pet_id,
            count
        ))
    sc.stop()

