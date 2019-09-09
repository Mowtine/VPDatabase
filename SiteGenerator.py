import os
from DirTree import DirTree
from ConstructTree import constructTree
import WritingFunctions as WF

# for server
import http.server
import socketserver

PORT = 8000 # port of the server

def main():

    os.chdir("../")
    # Create filetree of the current folder.
    fileTree = constructTree("Main menu",".")


    # Debugging Can coment this out on final
    #fileTree.printAll()

    # Specify
    cssFileName = "Styles.css"
    menuFileName = "index.html"

    # Create the HTML files!

    # TODO:
    # 1. Change all links to local links
    # 2. Change the div into a iframe
    # 3. When clicking on files make them load into the iframe
    # 4. Advanced: When a file is loaded in the Iframe, open the menu at that file location


    # Write the CSS
    with open(cssFileName,'w') as styles:
        WF.writeCSS(styles)

    with open(menuFileName,'w') as mainhtml:

        # HTML starts here
        mainhtml.write("<html>\n")

        WF.writeHeader(mainhtml, cssFileName, 0)

        # Body starts here
        mainhtml.write("<body>\n")

        # Enclose the menu in a table
        mainhtml.write("<table>\n<tr><td style=\"vertical-align: top\">\n")

        # Create class names for each class in the main page
        folderClass = "folderMenu"
        accordionClass = "dropButton"
        fileClass = "fileMenu"
        fileOpenClass = "fileOpen"
        colapsibleClass = "colapsingDiv"
        loadButtonClass = "loadRHSButton"
        pageNavButtonClass = "topPageButton"
        pageNavClass = "topPageNav"
        # ID's for the sepperator
        dynamicPageTableID = "dynamicPageTable"
        topPageMenuID = "topPageMenu"
        loadPageDivID = "loadPageDiv"
        textAreaId= "textAreaId"

        # Write the menu
        WF.writeMenu(mainhtml, fileTree, folderClass, accordionClass, fileClass, fileOpenClass, colapsibleClass, loadButtonClass)

        # Adding the right image display table cell.
        mainhtml.write("</td><td style=\"vertical-align: top\">\n")

        # Get the maximum pages in any single folder
        maxPages = fileTree.getMaxPages()

        # This will be the RHS page and menu above it. It is just two divs the
        # top one being the page navigation which is hidden and the second
        # being empty which will load the pages into with javascript later
        WF.rhsDiv(mainhtml, dynamicPageTableID, topPageMenuID, loadPageDivID, pageNavButtonClass, pageNavClass, maxPages)

        # End the table container
        mainhtml.write("</td></tr></table>\n")

        # Add script for the Accordion menu
        WF.writeAccordionScript(mainhtml, accordionClass, colapsibleClass)

        # Add script for coppying filepath of files and opening them
        WF.writeCopyPathScript(mainhtml, fileClass, textAreaId)

        # Add script for loading pages on RHS. Ignore top div for now
        WF.writePageLoadScript(mainhtml, loadButtonClass, dynamicPageTableID, topPageMenuID, loadPageDivID, pageNavButtonClass, fileOpenClass)

        # Add a text area for coppying
        mainhtml.write("<textarea id = \""+ textAreaId +"\"></textarea>")

        # Body ends here
        mainhtml.write("</body>\n")

        # HTML ends here
        mainhtml.write("</html>\n")

        # Start serving
        Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()



if __name__ == "__main__":
    main()
