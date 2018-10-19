import javax.crypto.*;
import java.io.*;
import java.nio.file.Files;
import java.security.*;
import java.security.spec.EncodedKeySpec;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.*;


public class Main {

    public static void main(String... args) {
        /*
        args[0] is RSA---
        args[1] is "encrypt" or "decrypt"
        encrypt - the next arguments are:
        [2]<public key der file path> [3]<file to encode> [4]<file path to store encoded file>
        decrypt - the next arguments are:
        [2]<private key path> [3]<file to decode> [4]<file path to decoded file>
         */
        try {
            if(args[0].equals("RSA")) {
                if(args[1].equals("encrypt"))
                    RSAEncrypt(args);
                else if(args[1].equals("decrypt"))
                    RSADecrypt(args);
            }
        }
        catch (IOException | InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException |
                InvalidKeySpecException | BadPaddingException | IllegalBlockSizeException e) {
            e.printStackTrace();
        }
    }

    private static void RSAEncrypt(String[] args) throws IOException, InvalidKeyException, NoSuchPaddingException,
            NoSuchAlgorithmException, InvalidKeySpecException, BadPaddingException, IllegalBlockSizeException {
        File pubfile = new File(args[2]);
//        File privfile = new File(args[2]);
        byte[] publicKeyBytes = Files.readAllBytes(pubfile.toPath());
//        byte[] privateKeyBytes = Files.readAllBytes(privfile.toPath());

        KeyFactory keyFactory = KeyFactory.getInstance(args[0]);

//        EncodedKeySpec privateKeySpec = new PKCS8EncodedKeySpec(privateKeyBytes);
//        PrivateKey privateKey = keyFactory.generatePrivate(privateKeySpec);

        EncodedKeySpec publicKeySpec = new X509EncodedKeySpec(publicKeyBytes);
        PublicKey publicKey = keyFactory.generatePublic(publicKeySpec);

        Cipher ciphere = Cipher.getInstance(args[0]);
//        Cipher cipherd = Cipher.getInstance(args[0]);
        ciphere.init(Cipher.ENCRYPT_MODE, publicKey);
//        cipherd.init(Cipher.DECRYPT_MODE, privateKey);
        File file = new File(args[3]);
        assert(file.exists());
        FileInputStream fin = new FileInputStream(file);
        FileOutputStream fos1 = new FileOutputStream(new File(args[4]));
//        FileOutputStream fos2 = new FileOutputStream(new File(args[5]));


        byte[] block = new byte[245];
        int i;
        while ((i = fin.read(block)) != -1) {
            byte[] encrypted= ciphere.doFinal(Arrays.copyOfRange(block,0,i));
//            byte[] decryted = cipherd.doFinal(encrypted);
            fos1.write(encrypted);
//            fos2.write(decryted);
        }
        fos1.close();
//        fos2.close();
    }
    private static void RSADecrypt(String[] args) throws IOException, InvalidKeyException, NoSuchPaddingException,
            NoSuchAlgorithmException, InvalidKeySpecException, BadPaddingException, IllegalBlockSizeException {
//        File pubfile = new File(args[1]);
        File privfile = new File(args[2]);
//        byte[] publicKeyBytes = Files.readAllBytes(pubfile.toPath());
        byte[] privateKeyBytes = Files.readAllBytes(privfile.toPath());

        KeyFactory keyFactory = KeyFactory.getInstance(args[0]);

        EncodedKeySpec privateKeySpec = new PKCS8EncodedKeySpec(privateKeyBytes);
        PrivateKey privateKey = keyFactory.generatePrivate(privateKeySpec);

//        EncodedKeySpec publicKeySpec = new X509EncodedKeySpec(publicKeyBytes);
//        PublicKey publicKey = keyFactory.generatePublic(publicKeySpec);

//        Cipher ciphere = Cipher.getInstance(args[0]);
        Cipher cipherd = Cipher.getInstance(args[0]);
//        ciphere.init(Cipher.ENCRYPT_MODE, publicKey);
        cipherd.init(Cipher.DECRYPT_MODE, privateKey);
        File file = new File(args[3]);
        assert(file.exists());
        FileInputStream fin = new FileInputStream(file);
        FileOutputStream fos1 = new FileOutputStream(new File(args[4]));
//        FileOutputStream fos2 = new FileOutputStream(new File(args[5]));


        byte[] block = new byte[245];
        int i;
        while ((i = fin.read(block))!= -1) {
            byte[] decrypted= cipherd.doFinal(Arrays.copyOfRange(block,0,i));
//            byte[] decryted = cipherd.doFinal(encrypted);
            fos1.write(decrypted);
//            fos2.write(decryted);
        }
        fos1.close();
//        fos2.close();
    }
}
