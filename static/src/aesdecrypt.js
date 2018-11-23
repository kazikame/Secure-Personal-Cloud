function aesdecryption(enmsg) {
    var key = CryptoJS.enc.Hex.parse(document.getElementById("key").value);
    var iv = CryptoJS.enc.Hex.parse(document.getElementById("iv").value);

    var decrypted = CryptoJS.AES.decrypt(
        enmsg,
        key,
        {
            iv: iv,
            mode:CryptoJS.mode.CTR,
            padding: CryptoJS.pad.NoPadding
        });

    return decrypted.toString(CryptoJS.enc.Base64);
}