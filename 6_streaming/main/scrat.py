def main():
    tweet = "hello [sami ]"
    print(((tweet.split("["))[1]).split("]")[0])

main()