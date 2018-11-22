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

function decrypt(enmsg){
    // var msg = "hi this is yash\n" +
    //     "sdouaeusfgvbhjjeioaweADSKLssfavd'\n" +
    //     "\n" +
    //     "adfddschfvdgguyfewsdjckla\n" +
    //     "sdcajvgQWSDAYUAFUIEWDSPODVKDF\n" +
    //     "D2356278E3%$^%^&**uoi*&*^%$%^\n" +
    //     "k3E";
    enmsg = enmsg.split(/\s/).join('');
    var key = CryptoJS.enc.Hex.parse(document.getElementById("key").value);
    var iv = CryptoJS.enc.Hex.parse(document.getElementById("iv").value);
    console.log(CryptoJS.AES.encrypt(msg,key,{
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
    console.log(decrypted.toString(CryptoJS.enc.Utf8));
    // document.getElementById("decrypted").innerHTML = decrypted.toString(CryptoJS.enc.Utf8);
    return decrypted;
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
