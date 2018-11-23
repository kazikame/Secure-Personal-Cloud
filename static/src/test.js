
function wordToByteArray(word, length) {
	var ba = [],
		i,
		xFF = 0xFF;
	if (length > 0)
		ba.push(word >>> 24);
	if (length > 1)
		ba.push((word >>> 16) & xFF);
	if (length > 2)
		ba.push((word >>> 8) & xFF);
	if (length > 3)
		ba.push(word & xFF);

	return ba;
}

function wordArrayToByteArray(wordArray, length) {
	if (wordArray.hasOwnProperty("sigBytes") && wordArray.hasOwnProperty("words")) {
		length = wordArray.sigBytes;
		wordArray = wordArray.words;
	}

	var result = [],
		bytes
		i = 0;
	while (length > 0) {
		bytes = wordToByteArray(wordArray[i], Math.min(4, length));
		length -= bytes.length;
		result.push(bytes);
		i++;
	}
	return [].concat.apply([], result);
}

function base64ToArrayBuffer(base64) {
    var binaryString = window.atob(base64);
    var binaryLen = binaryString.length;
    var bytes = new Uint8Array(binaryLen);
    for (var i = 0; i < binaryLen; i++) {
       var ascii = binaryString.charCodeAt(i);
       bytes[i] = ascii;
    }
    return bytes;
 }

function decrypt(enmsg, filename = ''){
    var scheme = document.getElementById("encryption_schema").value;
    var fileext = filename.split(".");
    fileext = fileext[fileext.length - 1];
    var finalStr = null;
    enmsg = enmsg.split(/\s/).join('');
    if(scheme === "AES") {
        finalStr = aesdecryption(enmsg);
    }
    else if(scheme === "TripleDES") {
        finalStr = tdesdecryption(enmsg);
    }
    else if(scheme === "RC4") {
        finalStr = rc4decryption(enmsg);
    }
    else {
        return;
    }
    var decrypted = CryptoJS.enc.Base64.parse(finalStr);

    if (!(['pdf', 'jpeg', 'jpg', 'mp4', 'txt'].includes(fileext)))
    {
        document.getElementById('error').innerHTML= "<h2>Sorry, the file format isn't currently supported for viewing online.</h2>";
        var blob = new Blob([base64ToArrayBuffer(finalStr)], {type: "application/octet-stream"});
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    }

    if (fileext == "txt" || fileext == "cpp")
    {
            document.getElementById("text_file").innerHTML = "<h2>" + filename + "</h2><br>" + "<pre>" + decrypted.toString(CryptoJS.enc.Utf8) + "</pre>";
    }
    if (fileext == "jpeg" || fileext == "jpg" || fileext == "png")
    {

        var objbuilder = ('<img src="data:image/png;base64,' + finalStr +'" alt="Red dot" />')
        var win = window.open("","_self","titlebar=yes");
        win.document.title = filename;
        win.document.write('<html><title>' + filename +  '</title><body style="background-color: #000000">');
        win.document.write(objbuilder);
        win.document.write('</body></html>');
    }

    else if (fileext == "pdf")
    {
          var objbuilder = '';
          objbuilder += ('<object width="100%" height="100%"      data="data:application/pdf;base64,');
            objbuilder += finalStr;
            objbuilder += ('" type="application/pdf" class="internal"');
            objbuilder += ('name="' + filename + '"');
            objbuilder += ('<embed src="data:application/pdf;base64,');
            objbuilder += finalStr;
            objbuilder += ('" type="application/pdf" />');
            objbuilder += ('</object>');
            var win = window.open("","_self","titlebar=yes");
        win.document.title = filename;
        win.document.write('<html><title>' + filename +  '</title><body>');
        win.document.write(objbuilder);
        win.document.write('</body></html>');
        layer = jQuery(win.document);
    }

    else if (fileext == "mp4")
    {
        var vidURL = URL.createObjectURL(b64toBlob(finalStr, 'video/mp4'));
        var objbuilder= "<video controls>\n" +
            "\t<source type=\"video/mp4\" src=\"data:video/mp4;base64," + finalStr + "\">\n" +
            "</video>"

        var win = window.open("","_self","titlebar=yes");
        win.document.title = filename;
        win.document.write('<html><title>' + filename +  '</title><body style="background-color: #000000">');
        win.document.write(objbuilder);
        win.document.write('</body></html>');
    }


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

    var blob = new Blob(byteArrays, {type: contentType});
    return blob;
}