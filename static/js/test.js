// var salt = "E612A048FE0BCE53";
var key = CryptoJS.enc.Base64.parse("2AE7B9111B2E116F2A15224BEF05BBCB17379E90261232DDDE2C898F08AD28DA");
var iv = CryptoJS.enc.Base64.parse("FE9AE37315E8B368E7BB5B5732E57645");
var message = "blah ko encrypt kiya lol";
var encrypted = CryptoJS.AES.encrypt(message, key, {iv: iv});
console.log(encrypted.toString());
var decrypted = CryptoJS.AES.decrypt(encrypted,key, {iv: iv});
console.log(decrypted.toString(CryptoJS.enc.Utf8));