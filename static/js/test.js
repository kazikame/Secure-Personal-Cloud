var salt = "E612A048FE0BCE53";
var key = CryptoJS.enc.Hex.parse("2AE7B9111B2E116F2A15224BEF05BBCB17379E90261232DDDE2C898F08AD28DA");
var iv = CryptoJS.enc.Hex.parse("FE9AE37315E8B368E7BB5B5732E57645");
var message = "blah ko encrypt kiya";
var encrypted = CryptoJS.AES.encrypt(message, key, {iv: iv});
console.log(encrypted.toString());
var decrypted = CryptoJS.AES.decrypt(encrypted,key, {iv: iv,padding: CryptoJS.pad.Pkcs7, mode: CryptoJS.mode.CBC});
console.log(decrypted.toString(CryptoJS.enc.Utf8));
encrypted = CryptoJS.enc.Base64.parse("iN42vonhIL+auH6OfxVGo8lwBVkdcogGXBoye2j3XWQ=");
console.log(encrypted.toString());
decrypted = CryptoJS.AES.decrypt(encrypted, key, {iv: iv,padding: CryptoJS.pad.Pkcs7, mode: CryptoJS.mode.CBC});
console.log(decrypted.toString(CryptoJS.enc.Utf8));

function encrypt(){
    var encrypted = CryptoJS.AES.encrypt(document.getElementById("text").value, document.getElementById("pass").value);
    document.getElementById("result").innerHTML = encrypted;
    document.getElementById("decrypted").innerHTML = '';
}

function decrypt(){
    var decrypted = CryptoJS.AES.decrypt(document.getElementById("result").innerHTML, document.getElementById("pass").value).toString(CryptoJS.enc.Utf8);
    document.getElementById("decrypted").innerHTML = decrypted;
    document.getElementById("result").innerHTML = '';
}
