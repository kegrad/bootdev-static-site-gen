from textnode import TextType,TextNode

def main():
    o = TextNode('Some text', TextType.LINK_TEXT, "https://www.google.com")
    print(o)


if __name__ == "__main__":
    main()