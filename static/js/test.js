// var key = CryptoJS.enc.Hex.parse("2AE7B9111B2E116F2A15224BEF05BBCB17379E90261232DDDE2C898F08AD28DA");
    // var iv = CryptoJS.enc.Hex.parse("FE9AE37315E8B368E7BB5B5732E57645");
var enmsg = "yM9NwHtZfCTEHxXYt3qpE3cXevdfDLpuzNAp6gyi/hGxyKqEQVKTlFu9gBXk9xSM\n" +
    "klxcMnnQ1IHQqqRNnxXzj1lqmOU/p+dqddovk/8M3R81+c1CSVrNNGw5OjWaTZBX\n" +
    "3W+HuXmN8vKAqZlurkVrcm3rofVqgDFUIx+pJ/orh4kU0/vJ7b1bBu2flcc=\n";
// enmsg = CryptoJS.enc.Base64.parse(enmsg);



// function encrypt(){
//     var encrypted = CryptoJS.AES.encrypt(document.getElementById("text").value, document.getElementById("pass").value);
//     document.getElementById("result").innerHTML = encrypted;
//     document.getElementById("decrypted").innerHTML = '';
// }


function decrypt(enmsg, filename = 'lol.jpeg'){
    // var msg = "hi this is yash\n" +
    //     "sdouaeusfgvbhjjeioaweADSKLssfavd'\n" +
    //     "\n" +
    //     "adfddschfvdgguyfewsdjckla\n" +
    //     "sdcajvgQWSDAYUAFUIEWDSPODVKDF\n" +
    //     "D2356278E3%$^%^&**uoi*&*^%$%^\n" +
    //     "k3E";
    enmsg = enmsg.split(/\s/).join('');
    var fileext = filename.split(".");
    fileext = fileext[fileext.length - 1];

    var key = CryptoJS.enc.Hex.parse(document.getElementById("key").value);
    var iv = CryptoJS.enc.Hex.parse(document.getElementById("iv").value);
    console.log(CryptoJS.AES.encrypt(enmsg,key,{
        iv: iv,
        mode: CryptoJS.mode.CTR,
        padding: CryptoJS.pad.NoPadding
    }).toString());
    var decrypted = CryptoJS.AES.decrypt(
        enmsg,
        key,
        {
            iv: iv,
            mode:CryptoJS.mode.CTR,
            padding: CryptoJS.pad.NoPadding
        });

    var finalStr = decrypted.toString(CryptoJS.enc.Base64);

    if (fileext == "jpeg")
    {
        // document.getElementById("iframe").src = 'data:image/jpg;base64,' + decrypted.toString(CryptoJS.enc.Base64)
        // document.getElementById("iframe").style.height = document.getElementById("iframe").contentWindow.document.body.scrollHeight + 'px';
        // document.body.appendChild(image);

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
    //document.getElementById("decrypted").innerHTML =

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

// encrypted = function(object, secret) {
//     var message = JSON.stringify(object);
//     return CryptoJS.TripleDES.encrypt(message, secret);
// };
//
// decrypt = function(encrypted, secret) {
//     var decrypted = CryptoJS.TripleDES.decrypt(encrypted, secret);
//     return JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
// };
