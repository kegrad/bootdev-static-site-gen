from textnode import TextType,TextNode
from filestuff import clean_and_copy,generate_page

def main():
    o = TextNode('Some text', TextType.LINK, "https://www.google.com")
    print(o)
    clean_and_copy("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")




if __name__ == "__main__":
    main()