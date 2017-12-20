import findlinks


def compare_str(line):
    compare_result = True
    with open("urls_old.txt", "r") as urls_old:
        for url_old in urls_old:
            url_old = url_old.strip("\n")
            # print "comparing : %s,%s"%(url_old,line)
            if url_old == line:
                # print "True"
                return True
        # print "False"
        return False

        
with open("urls.txt", "r") as lines:
    for line in lines:
        line = line.strip("\n")
        if compare_str(line):continue
        try:
            # print line
            findlinks.findlink(line,3)
            urls_old = open("urls_old.txt","a")
            urls_old.write("\n"+line)
            urls_old.close()
        except Exception:
            print line," : ",Exception
            pass