import os,shutil

from markdowntohtml import extract_title, markdown_to_html_node

def clean_and_copy(old_folder, new_folder):
    if os.path.exists(new_folder):
        print(f"Deleting existing folder {new_folder}")
        shutil.rmtree(new_folder)
    recursivecopy(old_folder,new_folder)

def recursivecopy(old_folder,new_folder):
    os.mkdir(new_folder)
    dir_contents = os.listdir(old_folder)
    for c in dir_contents:
        oldfile = os.path.join(old_folder,c)
        newfile = os.path.join(new_folder,c)
        if os.path.isfile(oldfile):
            print(f"copying file {oldfile} to {newfile}")
            shutil.copy(oldfile,newfile)
        elif os.path.isdir(oldfile):
            print(f"recursively copying directory: {oldfile} to {newfile}")
            recursivecopy(oldfile,newfile)
        else:
            print(f"unexpected entry: {oldfile}")

def generate_site(old_folder,new_folder):
    dir_contents = os.listdir(old_folder)
    for c in dir_contents:
        oldfile = os.path.join(old_folder,c)
        newfile = os.path.join(new_folder,c)
        if os.path.isfile(oldfile):
            print(f"generating from {oldfile} to {newfile}")
            #shutil.copy(oldfile,newfile)
            generate_page(oldfile, "template.html", newfile[:-2] + "html")
        elif os.path.isdir(oldfile):
            print(f"recursively copying directory: {oldfile} to {newfile}")
            generate_site(oldfile,newfile)
        else:
            print(f"unexpected entry: {oldfile}")


# Create a generate_page(from_path, template_path, dest_path) function. It should:

#     Print a message like "Generating page from from_path to dest_path using template_path".
#     Read the markdown file at from_path and store the contents in a variable.
#     Read the template file at template_path and store the contents in a variable.
#     Use your markdown_to_html_node function and .to_html() method to convert the markdown file to an HTML string.
#     Use the extract_title function to grab the title of the page.
#     Replace the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
#     Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don't exist.

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    md_file = f.read()
    f.close()
    f = open(template_path)
    template = f.read()
    f.close()
    node = markdown_to_html_node(md_file)
    html = node.to_html()
    title = extract_title(md_file)
    webpage_text = template.replace("{{ Content }}",html)
    webpage_text = webpage_text.replace("{{ Title }}",title)
    
    dirname = os.path.dirname(dest_path)
    os.makedirs(dirname,exist_ok=True)
    f = open(dest_path,mode = "w")
    f.write(webpage_text)
    f.close()

