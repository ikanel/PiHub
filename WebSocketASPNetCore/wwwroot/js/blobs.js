
function getBase64(file, callback) {
    var result;
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function () {
        result = reader.result;
    };
    reader.onerror = function (error) {
        console.log("Error: ", error);
    };
    return result;
}

function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;

    var byteCharacters = atob(b64Data);
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    var blob = new Blob(byteArrays, { type: contentType });
    return blob;
}

function saveFromBlob(placeholder, blob) {
    var contentType = "application/octet-stream";
    var myBlob = b64toBlob(blob.content, contentType);
    var blobUrl = URL.createObjectURL(myBlob);
    var link = document.createElement("a"); // Or maybe get it from the current document
    link.href = blobUrl;
    link.download = blob.name;
    link.innerHTML = blob.name;
    placeholder.innerHTML = '';
    placeholder.appendChild(link);
}
