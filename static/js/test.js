var salt = "E612A048FE0BCE53";
// var key = CryptoJS.enc.Hex.parse("2AE7B9111B2E116F2A15224BEF05BBCB17379E90261232DDDE2C898F08AD28DA");
// var iv = CryptoJS.enc.Hex.parse("FE9AE37315E8B368E7BB5B5732E57645");
// var message = "hi this is yash";
// var encrypted = CryptoJS.AES.encrypt(message, key, {iv: iv, mode: CryptoJS.mode.CTR});
var enmsg = "yM9NwHtZfCTEHxXYt3qpGA==";





// function encrypt(){
//     var encrypted = CryptoJS.AES.encrypt(document.getElementById("text").value, document.getElementById("pass").value);
//     document.getElementById("result").innerHTML = encrypted;
//     document.getElementById("decrypted").innerHTML = '';
// }

function decrypt(){
    var key = CryptoJS.enc.Hex.parse(document.getElementById("key").value);
    var iv = CryptoJS.enc.Hex.parse(document.getElementById("iv").value);
    var decrypted = CryptoJS.AES.decrypt(
        enmsg,
        key,
        {
            iv: iv,
            mode:CryptoJS.mode.CTR,
            padding: CryptoJS.pad.Pkcs7
        });
    console.log(decrypted.toString(CryptoJS.enc.Utf8));
    document.getElementById("decrypted").innerHTML = decrypted.toString(CryptoJS.enc.Utf8);
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
