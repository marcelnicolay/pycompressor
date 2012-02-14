PyCompressor
======================

PyCompressor collect all css and js references in html files, merge and compress then, puting all static files in an specific bucket, filtering all js,css and images references in html to apply your bucket url.

Installation
-----------------

Installing: `pip install compressor`

Usage
=======

    compressor -c compressor.yaml --color

compressor.yaml
-----------------

    # your files path
    path:
      template: template
      css: media/css
      js: media/js
     
    # compressor results path
    output:
      template: compressor/template
      css: compressor/media/css
      js: compressor/media/js

    # pattern to find tags in html code
    pattern:
      css: ../media/css
      js: ../media/js
      img: ../media/img

    # filter url tags
    filter:
      url: 
        css: http://demo.pycompressor.com/media/css
        js: http://demo.pycompressor.com/media/js
        img: http://demo.pycompressor.com/media/img

Issues
------

Please report any issues via [github issues](https://github.com/marcelnicolay/pycompressor/issues)