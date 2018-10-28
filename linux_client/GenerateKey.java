import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.util.Random;

public class GenerateKey {
    //aes key length = 256
    //tdes key length = 192 (although the real thing will be 168 inside due to padding)
    public static void main(String... args) {
        /*
         * args[0] : encryption schema
         * args[1] : file path to store (temporarily, hopefully)
         */
        FileOutputStream fos = null;
        try {
            fos = new FileOutputStream(new File(args[1]));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        assert fos != null;
        try {
            if(args[0].equals("AES")) {
                GenerateAES(fos);
            }
            else if(args[0].equals("TripleDES")) {
                GenerateDESede(fos);
            }
        }
        catch (NoSuchAlgorithmException | IOException e) {
            e.printStackTrace();
        }
    }
    private static void GenerateAES(FileOutputStream fileOutputStream) throws NoSuchAlgorithmException, IOException {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(256);
        SecretKey secretKey = keyGenerator.generateKey();
        byte[] key = secretKey.getEncoded();
//        System.out.println(key.length);
        fileOutputStream.write(key);
    }
    private static void GenerateDESede(FileOutputStream fileOutputStream) throws NoSuchAlgorithmException, IOException {
//        KeyGenerator keyGenerator = KeyGenerator.getInstance("Desede");
//        keyGenerator.init(192);
//        SecretKey secretKey = keyGenerator.generateKey();
//        byte[] key = secretKey.getEncoded();
//        fileOutputStream.write(key);
        /*
        reference: https://hamzakc.wordpress.com/2006/12/29/create-triple-des-secretkey-in-java/
        although i don't know why not the above commented out code, weird.
         */

        byte[] randomBytes = new byte[24];
        new Random().nextBytes(randomBytes);
        SecretKey secretKey = new SecretKeySpec(randomBytes, "DESede");
        byte[] key = secretKey.getEncoded();
        fileOutputStream.write(key);
    }
}
