from pathlib import Path
from urllib.request import pathname2url
import os

# Writes out a menu list in HTML of the received tree
def writeMenu(htmlfile, tree, folderClass, accClass, fileClass, fileOpenClass, colapsibleClass, loadButtonClass):

    # Create base ul and in the first list write the current foldername.
    htmlfile.write("<ul class=\""+folderClass+"\" >\n<li class=\""+folderClass+"\">")
    # Create the button around the name to fold in the next children.
    htmlfile.write("<button class=\""+accClass+" "+folderClass+"\">")
    htmlfile.write(tree.name)
    htmlfile.write("</button>")

    # Find any HTML files that exist in the current folder
    # Then make a string list of them to add to the data in the load button
    htmlPages = ""
    for fileName in tree.filelist:

        # Splitting the file name
        fileSplit = fileName.split(".")
        if len(fileSplit) > 2:
            fileEnd = fileSplit[-1]
            fileTitle = fileSplit[0]
            for i in range(len(fileSplit) - 2):
                fileTitle = "." + fileSplit[i+1]
        else:
            [fileTitle, fileEnd] = fileSplit


        # If any file has the same name as the folder then add it to the data section
        if tree.name in fileTitle:
            if htmlPages == "":
                htmlPages = pathname2url(str(Path(tree.currentDir) / fileName))

            else:
                htmlPages = htmlPages + "," + pathname2url(str(Path(tree.currentDir) / fileName))


# ToCheck: Changed it to only display if there is something to display. Check if works.
    # Create the button next to the name to display the corresponding page on
    # the rhs
    if htmlPages != "":
        htmlfile.write("<button class=\""+loadButtonClass+"\" data-pages=\""+htmlPages+"\">")
        htmlfile.write("-->")
        htmlfile.write("</button>")
    # Create complete encapsulation of all children after the button.
    # Everything in this div will be hidden when the button is clicked.
    htmlfile.write("\n<div class=\""+colapsibleClass+"\">\n")

    # For each child recur the function to create a subtree for them.
    for wrchild in tree.children:
        writeMenu(htmlfile, wrchild, folderClass, accClass, fileClass, fileOpenClass, colapsibleClass, loadButtonClass)

#Todo Add option to open each file or file location when clicked.
    # For each file create file lists in their own
    if tree.filelist:
        htmlfile.write("<ul class=\"" + fileClass + "\">\n")
        for file in tree.filelist:
            fileSplit = file.split(".")
            htmldir = pathname2url(str(Path(tree.currentDir) / file))
            if tree.currentDir == ".":
                directory = os.getcwd()
            else:
                directory = os.getcwd() + "\\" + tree.currentDir
            if any(ext in fileSplit[-1] for ext in ["htm", "HTM", "pdf", "PDF", "jpg", "JPG", "png", "PNG"]):
                htmlfile.write("<li><button data-pages=\""+htmldir+"\" class=\"" + fileOpenClass + "\">"+file+"</button></li>\n")
            else:
                htmlfile.write("<li><button data-folder=\""+directory+"\" class=\"" + fileClass + "\">"+file+"</button></li>\n")
        htmlfile.write("</ul>\n")
    htmlfile.write("</div>\n")
    htmlfile.write("</li>\n")
    htmlfile.write("</ul>\n")

# Writes out a header with a link to the css file.
# The level is how far up the file-tree this file is, so it can find
# the css file without a problem.
def writeHeader(htmlfile, cssFileName, level):

    # Get base directory address
    baseDir = "../"*level

    # Write out header
    htmlfile.write("<head>\n")
    htmlfile.write("<link href=\"" + baseDir + cssFileName +
        "\" rel=\"stylesheet\" type=\"text/css\" media=\"screen\">\n")
    htmlfile.write("</head>\n")

# Write out two divs, one for the top menu, and another for the shown page.
def rhsDiv(htmlfile, dynamicPageTableID, topPageMenuID, loadPageDivID, pageNavButtonClass, pageNavClass, maxPages):

    # It will cover it in a table, so as to have the top cell be the menu
    # This is making the following:
    #+---------------+
    #| topPageMenuID |
    #+---------------+
    #| loadPageDivID |
    #+---------------+
    # While the dynamicPageTableID is the ID for the whole table

    # Writing the table container
    htmlfile.write("<table id=\""+dynamicPageTableID+"\">\n")

    # Writing the top menu container
    htmlfile.write("<tr><td>\n<div id=\""+topPageMenuID+"\" style=\"display: none;\">\n")

    if maxPages > 0:
        htmlfile.write("<ul class=\"" + pageNavClass + "\">\n")
        for i in range(maxPages):
            htmlfile.write("<li class=\"" + pageNavClass + "\">")
            htmlfile.write("<button class=\"" + pageNavButtonClass + "\" id=\"" + pageNavButtonClass + str(i + 1) + "\" style=\"display: none;\" >Page " + str(i+1) +"</button>")
            htmlfile.write("</li>\n")
        htmlfile.write("</ul>\n")

    # Ending top menu contianter
    htmlfile.write("</div>\n</td></tr>\n")

    # Todo: Add a for loop for the maximum pages if any, add a page 1, page 2
    # for each one. Then make each of their atributes "hidden" and then give
    # them each a seperate ID and all one class.

    # Writing the main page div container
    htmlfile.write("<tr><td>\n<div ID=\""+loadPageDivID+"\">\n")

    # Ending min page container
    htmlfile.write("</div>\n</td></tr>\n</table>\n")

# When a folder button is clicked, display any html pages with the same name as
# them in the RHS div.
# Also reveal and add functions to the top page navigation to select desired page.
def writePageLoadScript(htmlfile, loadButtonClass, dynamicPageTableID, topPageMenuID, loadPageDivID, pageNavButtonClass, fileOpenClass):

    htmlfile.write("""
<script src="PythonFiles/jquery-3.3.1.js"></script>
<script>
var loadButtons = document.querySelectorAll(".%s, .%s");
var topMenuLoadButtons = document.getElementsByClassName("%s")
var i;

for (i = 0; i < loadButtons.length; i++) {
    var pagesString = loadButtons[i].getAttribute("data-pages");
    console.log(pagesString);
    var pages = pagesString.split(",");
    console.log(pages);
    if (pages[0] !== "") {
        loadButtons[i].addEventListener("click", function() {
            var pgStr = this.getAttribute("data-pages");
            var pgs = pgStr.split(",");
            console.log("Pages: " + (pgs.length > 1));
            var topMenuDiv = document.getElementById("%s");
            if (pgs.length > 1) {
                console.log(topMenuDiv);
                topMenuDiv.style.display = "block";
            } else {
                topMenuDiv.style.display = "none";
            }
            console.log("Trying to load " + pgs[0]);
            var Wwidth = $( window ).width()*3/4;
            var Wheight = $( window ).height()
            $("#%s").html("<iframe src=\\""+pgs[0]+"\\" width=\\""+Wwidth+"\\" height=\\""+Wheight+"\\"></iframe>");
            console.log("Activating buttons");
            for (j = 0; j < topMenuLoadButtons.length; j++) {
                topMenuLoadButtons[j].style.display = "none";
                if (j < pgs.length) {
                    topMenuLoadButtons[j].dataset.page = pgs[j];
                    topMenuLoadButtons[j].addEventListener("click", function() {
                        var pg = this.getAttribute("data-page");
                        console.log("Trying to load " + pg);
                        $("#%s").html("<iframe src=\\""+pg+"\\" width=\\""+Wwidth+"\\" height=\\""+Wheight+"\\"></iframe>");
                    });
                    topMenuLoadButtons[j].style.display = "inline";
                }
            }

        });
    }
}
</script>
    """ % (loadButtonClass, fileOpenClass, pageNavButtonClass, topPageMenuID, loadPageDivID, loadPageDivID))

# When a file button is clicked, copy the filepath of it.
def writeCopyPathScript(htmlfile, fileClass, textAreaId):

    htmlfile.write("""
<script>
var fileButtons = document.getElementsByClassName("%s");
var i;

for (i = 0; i < fileButtons.length; i++) {
    var pages = fileButtons[i].getAttribute("data-folder");
    console.log("Pages: " + pages)
    if (pages !== "" && "BUTTON" == fileButtons[i].tagName ) {
        fileButtons[i].addEventListener("click", function() {
            console.log("Clicked filepath Button")
            var pgs = this.getAttribute("data-folder");
            console.log("Got path: "+ pgs)
            var textArea = document.getElementById("%s");
            textArea.value = pgs;
            textArea.select();
            document.execCommand("copy");
            alert("Coppied filepath")
        });
    }
}
</script>
    """ % (fileClass, textAreaId))


# This writes an accordion script into the HTML file for all elements with
# class AccClass.
def writeAccordionScript(htmlfile, AccClass, colapsibleClass):

    htmlfile.write("""
<script>
var acc = document.getElementsByClassName("%s");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    while (panel.className !== "%s") {
        panel = panel.nextElementSibling;
    }
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}
</script>
    """ % (AccClass, colapsibleClass))


# Writes the CSS file
def writeCSS(cssfile):
    cssfile.write("""
*	{ font-size:14px; font-weight:normal; }

h1			{
font-size: 24px;
font-style: italic;
text-align: center;
}
h2			{ font-size:18px; font-weight:bold; }
h3			{ font-size:16px; font-weight:bold; }

.colapsingDiv { display:none; }

.fileClass { font-weight:normal; }

.fileOpen { background-color:#ff9966; }
.loadRHSButton { background-color:#ff9966; }

.topPageButton { background-color:#aaa;
                    border:none;
                    cursor:pointer; }

.folderMenu { list-style-type:none;
                text-decoration:none;
                font-weight:bold; }

.dropButton { background-color:#aaa;
                border:none;
                cursor:pointer;}

.topPageNav { display:inline;
                list-style-type:none; }

.active, .dropButton:hover { background-color:#888;
                                transform: scale(1.1); }


a:link		{ color: #FFF; }
a:visited	{ color: #FFF; }
a:active	{ color: #FFF; }
a:hover		{ color: #666; background-color: #333 }
a:focus		{ color: #666; background-color: #333 }

button.fileMenu {}


#textbox	{ width:300px; height:600px;
            padding-left:20px;
            padding-right:20px;
            position:relative;
             }
    """)
