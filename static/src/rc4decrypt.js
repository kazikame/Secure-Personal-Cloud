function rc4decryption(enmsg) {
    var key = CryptoJS.enc.Hex.parse(document.getElementById("key").value);

    var decrypted = CryptoJS.RC4.decrypt(
        enmsg,
        key,
        {
            mode: CryptoJS.mode.ECB
        });

    return decrypted.toString(CryptoJS.enc.Base64);
}