import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;

public class GenerateKey {
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
        keyGenerator.init(128);
        SecretKey secretKey = keyGenerator.generateKey();
        byte[] key = secretKey.getEncoded();
        fileOutputStream.write(key);
    }
    private static void GenerateDESede(FileOutputStream fileOutputStream) throws NoSuchAlgorithmException, IOException {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("Desede");
        keyGenerator.init(168);
        SecretKey secretKey = keyGenerator.generateKey();
        byte[] key = secretKey.getEncoded();
        fileOutputStream.write(key);
    }
}
