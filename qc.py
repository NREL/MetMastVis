def remove_colon_in_timezone(filename):
    csvin = open("example_data/" + filename, "r")
    csvout = open("example_data_qc/" + filename, "w")

    for line in csvin:
        fixed_line = line[:22] + line[23:]
        csvout.write(fixed_line)

    csvin.close()
    csvout.close()

if __name__=="__main__":
    files = [
        "2012_August.csv",
        "2012_December.csv",
        "2012_November.csv",
        "2012_October.csv",
        "2012_September.csv",
        "2013_April.csv",
        "2013_August.csv",
        "2013_December.csv",
        "2013_February.csv",
        "2013_January.csv",
        "2013_July.csv",
        "2013_June.csv",
        "2013_March.csv",
        "2013_May.csv",
        "2013_November.csv",
        "2013_October.csv",
        "2013_September.csv",
        "2014_April.csv",
        "2014_August.csv",
        "2014_December.csv",
        "2014_February.csv",
        "2014_January.csv",
        "2014_July.csv",
        "2014_June.csv",
        "2014_March.csv",
        "2014_May.csv",
        "2014_November.csv",
        "2014_October.csv",
        "2014_September.csv",
        "2015_April.csv",
        "2015_August.csv",
        "2015_December.csv",
        "2015_February.csv",
        "2015_January.csv",
        "2015_July.csv",
        "2015_June.csv",
        "2015_March.csv",
        "2015_May.csv",
        "2015_November.csv",
        "2015_October.csv",
        "2015_September.csv",
        "2016_April.csv",
        "2016_August.csv",
        "2016_December.csv",
        "2016_February.csv",
        "2016_January.csv",
        "2016_July.csv",
        "2016_June.csv",
        "2016_March.csv",
        "2016_May.csv",
        "2016_November.csv",
        "2016_October.csv",
        "2016_September.csv",
        "2017_April.csv",
        "2017_August.csv",
        "2017_December.csv",
        "2017_February.csv",
        "2017_January.csv",
        "2017_July.csv",
        "2017_June.csv",
        "2017_March.csv",
        "2017_May.csv",
        "2017_November.csv",
        "2017_October.csv",
        "2017_September.csv"
    ]

    for f in files:
        remove_colon_in_timezone(f)