var salt = "E612A048FE0BCE53";
var key = CryptoJS.enc.Hex.parse("2AE7B9111B2E116F2A15224BEF05BBCB17379E90261232DDDE2C898F08AD28DA");
var iv = CryptoJS.enc.Hex.parse("FE9AE37315E8B368E7BB5B5732E57645");
var message = "hi this is yash";
// var encrypted = CryptoJS.AES.encrypt(message, key, {iv: iv, mode: CryptoJS.mode.CTR});
// console.log(encrypted.toString());
var enmsg = "yM9NwHtZfCTEHxXYt3qpGA==";
var decrypted = CryptoJS.AES.decrypt(
    enmsg,
    key,
    {
        iv: iv,
        mode:CryptoJS.mode.CTR,
        padding: CryptoJS.pad.Pkcs7
    });
console.log(decrypted.toString(CryptoJS.enc.Utf8));

