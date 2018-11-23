function tdesdecryption(enmsg) {
    var key = CryptoJS.enc.Hex.parse(document.getElementById("key").value);
    var iv = CryptoJS.enc.Hex.parse(document.getElementById("iv").value);

    var decrypted = CryptoJS.TripleDES.decrypt(
        enmsg,
        key,
        {
            iv: iv,
            mode:CryptoJS.mode.CFB
        });

    return decrypted.toString(CryptoJS.enc.Base64);
}