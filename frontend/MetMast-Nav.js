$(document).ready(function () {
    $('#menuToggle').click(function () {
        $(this).toggleClass('active');
        $('.mm-menu').slideToggle('show');
    });
    // GA link tracking
    $('span.wfs-downloadlink a').click(function (e) {
        e.preventDefault();
        var linkURL = this.href;

        // Per GA recommendations, adding timeout to ensure
        // link loads if GA doesn't load.
        setTimeout(navigateToLink, 1000);

        function navigateToLink() {
            document.location = linkURL;
        }

        ga('send', 'event', 'Wind for Schools', 'Download', this.href, 1, {
            transport: 'beacon',
            hitCallback: navigateToLink(),
        }); // End GA event.
    }); // End a click event.

    // Smooth scroll to anchors.
    $(document).on('click', '.anchor-smooth-scroll', function (e) {
        // Get anchor within span.
        var link = $(this).find('a').first();
        if (link.length > 0) {
            // Prevent default anchor click behavior.
            e.preventDefault();

            // Store hash
            var hash = link[0].hash;

            if (hash.length > 0) {
                $('html, body').animate({
                    scrollTop: $(hash).offset().top
                }, 500, function () {
                    // Add hash (#) to URL when done scrolling (default click behavior)
                    window.location.hash = hash;
                });
            }
        }
    }); // End smooth scroll to anchors.
}); // End document ready.

function getIconForResource(type, fileName) {
    //filemap
    var fileTypes = {
        'fa fa-file-word-o': ['doc', 'docx', 'docy'],
        'fa fa-file-excel-o': ['xls', 'xlsx', 'xlsy'],
        'fa fa-file-powerpoint-o': ['ppt', 'pptx', 'ppty'],
        'fa fa-file-pdf-o': ['pdf'],
        'fa fa-file-archive-o': ['zip', 'tar', 'gz'],
        'fa fa-file-image-o': ['bmp', 'jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff', 'svg', 'fig'],
        'fa fa-file-audio-o': ['wav', 'aiff', 'mp3', 'wma'],
        'fa fa-file-video-o': ['flv', 'avi', 'mov', 'qt', 'wmv', 'mp4', 'm4v'],
        'fa fa-file-text-o': ['txt', 'csv', 'mat', 'rdf', 'tab', 'dbf', 'dat', 'las', 'h5'], //data
        'fa fa-file-code-o': ['mlx', 'py', 'm', 'ipynb', 'xml']
    };

    //default
    var iconClasses = 'fa fa-file-o';
    if (type == "link") {
        iconClasses = "fa fa-link";
    } else if (type == "folder") {
        iconClasses = "fa fa-folder-o";
    } else if (type == "file") {
        iconClasses = 'fa fa-file-o';
        var regex = /(?:\.([^.]+))?$/;
        var fileExt = '' + regex.exec(fileName)[1];
        for (var key in fileTypes) {
            if (in_array(fileExt.toLowerCase(), fileTypes[key])) {
                iconClasses = key;
                break;
            }
        }
    }
    return '<i class="' + iconClasses + '" aria-hidden="true"></i>';
}

function in_array(needle, haystack, argStrict) {
    var key = '', strict = !!argStrict;
    if (strict) {
        for (key in haystack) {
            if (haystack[key] === needle) {
                return true;
            }
        }
    } else {
        for (key in haystack) {
            if (haystack[key] == needle) {
                return true;
            }
        }
    }
    return false;
}
