$('#download-doc').on('click', function () {
  // Show confirmation dialog
  if (!confirm("Do you want to download this document?")) {
    return; // Exit if user cancels
  }

  // Get the content
  var content = document.getElementById('doc-content').innerHTML;

  // Wrap it in a full HTML document
  var preHtml = '<html xmlns:o="urn:schemas-microsoft-com:office:office" ' +
                'xmlns:w="urn:schemas-microsoft-com:office:word" ' +
                'xmlns="http://www.w3.org/TR/REC-html40">' +
                '<head><meta charset="utf-8"><title>Document</title></head><body>';
  var postHtml = '</body></html>';
  var html = preHtml + content + postHtml;

  // Create a Blob with Word-compatible MIME type
  var blob = new Blob(['\ufeff', html], {
    type: 'application/msword'
  });

  // Create download link
  var downloadLink = document.createElement("a");
  document.body.appendChild(downloadLink);
  downloadLink.href = URL.createObjectURL(blob);
  downloadLink.download = 'booking_info.doc';
  downloadLink.click();
  document.body.removeChild(downloadLink);
});
