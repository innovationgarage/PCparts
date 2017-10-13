# PCguts
preparing an annotated dataset of PC pieces to use with YOLO

1- Scrape the web for images of interesting parts/pieces in as many conditions and from as many angles as possible (especially including in an assembled machine)

2- Annotate the images with the tool of choice. I used [ImageNet-Utils](https://github.com/tzutalin/ImageNet_Utils) because it's simple and fast and easily gives you XML annotations (I have not tried the txt files). It is, however, missing a magic wand tool for object selection.
  * some of the other tools I found interesting along the way:
    - [VGG](http://www.robots.ox.ac.uk/~vgg/software/via/)
    - [LabelD](https://sweppner.github.io/labeld/)
    - [Sloth](https://cvhci.anthropomatik.kit.edu/~baeuml/projects/a-universal-labeling-tool-for-computer-vision-sloth/)
    - [Annotorious](http://annotorious.github.io/)
  * In real life we might want to spend some money and outsource it using , for example, [Amazon's mechanical turk](http://labelme2.csail.mit.edu/Release3.0/browserTools/php/mechanical_turk.php)

3- I used [this project](https://github.com/SsaRu/voc-annotation-to-yolo-format) -with some modificatios- to convert my XML files into the txt labels needed by [Darknet](https://github.com/pjreddie/darknet)
  * Later, I found out that there is a [script](https://github.com/Guanghan/darknet/blob/master/scripts/voc_label.py) on darknet github to do so. But for now, I'm just keeping it here in case somehting goes wrong.
