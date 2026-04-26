from textnode import TextType,TextNode
from filestuff import clean_and_copy,generate_site
import sys

def main():
    #o = TextNode('Some text', TextType.LINK, "https://www.google.com")
    #print(o)
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = ""
    if basepath == "":
        basepath = "/"
    print("basepath->" + basepath + "<-")
    clean_and_copy("static", "docs")
    generate_site("content", "docs", basepath)




if __name__ == "__main__":
    main()