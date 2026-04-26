from textnode import TextType,TextNode
from filestuff import clean_and_copy,generate_site

def main():
    o = TextNode('Some text', TextType.LINK, "https://www.google.com")
    print(o)
    clean_and_copy("static", "public")
    generate_site("content", "public")




if __name__ == "__main__":
    main()