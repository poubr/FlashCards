import pandas

# creating cvs files to work with
# (words sourced from
# https://1000mostcommonwords.com/1000-most-common-finnish-words/
# and
# https://www.learnentry.com/english-finnish/1000-most-common-finnish-words/
# copied into files finnish_words_one.txt and finnish_words_two.txt)


def get_list():
    df1 = pandas.read_csv("finnish_words_one.txt", delimiter="\t", header=None)
    df1 = df1.iloc[:, 1:]   # removes numbered column
    df1.columns = ["Suomi", "English"]    # names columns
    df2 = pandas.read_csv("finnish_words_two.txt", delimiter="\t", header=None)
    df2 = df2.iloc[:, [1, 0]]   # switches columns to correspond to df1
    df2.columns = ["Suomi", "English"]    # names columns
    wordlist = pandas.concat([df1, df2], ignore_index=True)
    wordlist["Suomi"] = wordlist["Suomi"].str.lower()   # lowercase so that duplicates can be deleted
    wordlist["English"] = wordlist["English"].str.lower()
    wordlist = wordlist.drop_duplicates()   # deleting duplicate words
    wordlist.to_csv("wordlist.csv", index=False)  # and saving to file just in case

    return wordlist
