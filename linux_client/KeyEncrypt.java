import javax.crypto.*;
import javax.crypto.spec.PBEKeySpec;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.math.BigInteger;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.Arrays;
import java.util.Random;


public class KeyEncrypt {
    private class mySecureRandom extends SecureRandom {
        //reference: https://stackoverflow.com/a/11600910
        mySecureRandom() {
            SecureRandom s = new SecureRandom(null,null){};
        }
    }
    public static void main(String... args) throws GeneralSecurityException {
        /*
         *args[0] is the password
         *args[1] is "encrypt" or "decrypt"
         *encrypt - the next arguments are:
         *[1]<key file to encode> [3]<key file path to store encoded file>
         *decrypt - the next arguments are:
         *[2]<file to decode> [3]<file path to decoded file>
         */
        try {
            if(args[1].equals("encrypt"))
                RSAEncrypt(args);
            else if(args[1].equals("decrypt"))
                RSADecrypt(args);
        }
        catch (IOException | InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException |
                InvalidKeySpecException | BadPaddingException | IllegalBlockSizeException e) {
            e.printStackTrace();
        }
//        String password = "password";

    }


    private static void RSAEncrypt(String[] args) throws IOException, GeneralSecurityException {
        int keyLength = 2048;
        String password = args[0];
        byte[] salt = new byte[8];
        new Random(42).nextBytes(salt);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 8192, keyLength);
        SecretKey key = factory.generateSecret(spec);
        SecureRandom keyGenRand = mySecureRandom.getInstance("SHA1PRNG");
        keyGenRand.setSeed(key.getEncoded());
        KeyPairGenerator gen = KeyPairGenerator.getInstance("RSA");
        gen.initialize(keyLength, keyGenRand);
        java.security.KeyPair p = gen.generateKeyPair();
        PublicKey publicKey = p.getPublic();
        Cipher ciphere = Cipher.getInstance("RSA");
        ciphere.init(Cipher.ENCRYPT_MODE, publicKey);
        File file = new File(args[2]);
        assert(file.exists());
        FileInputStream fin = new FileInputStream(file);
        FileOutputStream fos1 = new FileOutputStream(new File(args[3]));


        byte[] block = new byte[245];
        int i;
        while ((i = fin.read(block)) != -1) {
            byte[] encrypted= ciphere.doFinal(Arrays.copyOfRange(block,0,i));
            fos1.write(encrypted);
        }
        fos1.close();
    }
    private static void RSADecrypt(String[] args) throws IOException, InvalidKeyException, NoSuchPaddingException,
            NoSuchAlgorithmException, InvalidKeySpecException, BadPaddingException, IllegalBlockSizeException {
//        File privfile = new File(args[2]);
//        byte[] privateKeyBytes = Files.readAllBytes(privfile.toPath());
        int keyLength = 2048;
        String password = args[0];
        byte[] salt = new byte[8];
        new Random(42).nextBytes(salt);
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 8192, keyLength);
        SecretKey key = factory.generateSecret(spec);
        SecureRandom keyGenRand = mySecureRandom.getInstance("SHA1PRNG");
        keyGenRand.setSeed(key.getEncoded());
        KeyPairGenerator gen = KeyPairGenerator.getInstance("RSA");
        gen.initialize(keyLength, keyGenRand);
        java.security.KeyPair p = gen.generateKeyPair();
        PrivateKey privateKey = p.getPrivate();
        Cipher cipherd = Cipher.getInstance("RSA");
        cipherd.init(Cipher.DECRYPT_MODE, privateKey);
        File file = new File(args[2]);
        assert(file.exists());
        FileInputStream fin = new FileInputStream(file);
        FileOutputStream fos1 = new FileOutputStream(new File(args[3]));


        byte[] block = new byte[256];
        int i;
        while ((i = fin.read(block))!= -1) {
            byte[] decrypted= cipherd.doFinal(Arrays.copyOfRange(block,0,i));
            fos1.write(decrypted);
        }
        fos1.close();
    }
    //reference: https://howtodoinjava.com
    private static String generateStrongPasswordHash(String password) throws NoSuchAlgorithmException, InvalidKeySpecException
    {
        int iterations = 1000;
        char[] chars = password.toCharArray();
        byte[] salt = getSalt();

        PBEKeySpec spec = new PBEKeySpec(chars, salt, iterations, 64 * 8);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
        byte[] hash = skf.generateSecret(spec).getEncoded();
        return iterations + ":" + toHex(salt) + ":" + toHex(hash);
    }

    private static byte[] getSalt() throws NoSuchAlgorithmException
    {
        SecureRandom sr = SecureRandom.getInstance("SHA1PRNG");
        byte[] salt = new byte[16];
        sr.nextBytes(salt);
        return salt;
    }

    private static String toHex(byte[] array) throws NoSuchAlgorithmException
    {
        BigInteger bi = new BigInteger(1, array);
        String hex = bi.toString(16);
        int paddingLength = (array.length * 2) - hex.length();
        if(paddingLength > 0)
        {
            return String.format("%0"  +paddingLength + "d", 0) + hex;
        }else{
            return hex;
        }
    }
}
