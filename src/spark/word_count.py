from pyspark import SparkContext, SparkConf

if __name__ == "__main__":
    conf = SparkConf().setAppName("word count").setMaster("local[3]")
    sc = SparkContext(conf=conf)

    lines = sc.textFile("../../data/word_count.txt")
    words = lines.flatMap(lambda line: line.split(" "))
    # s = sorted(sc.parallelize([1, 2, 1, 2, 2], 2).countByValue().items())
    # print(s)
    wordCounts = words.countByValue()

    for word, count in wordCounts.items():
        print("{} : {}".format(word, count))