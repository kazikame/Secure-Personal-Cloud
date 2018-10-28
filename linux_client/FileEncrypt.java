import java.io.*;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

import javax.crypto.*;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

//reference: https://javapapers.com/java/java-symmetric-aes-encryption-decryption-using-jce/
public class FileEncrypt {
    public static void main(String... args) throws IOException {
        /*
         *  args[0]: File Encryption Schema
         *  args[1]: "encrypt"/"decrypt"
         *  args[2]: decrypted key
         *  args[3]: file path of decrypted/encrypted file to encrypt/decrypt
         *  args[4]: file path to store encrypted/decrypted file
         */
        FileInputStream keyf = null;
        FileInputStream fin = null;
        FileOutputStream fos = null;
        try {
            keyf = new FileInputStream(new File(args[2]));
            fin = new FileInputStream(new File(args[3]));
            fos = new FileOutputStream(new File(args[4]));
        }
        catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        try {
            if (args[1].equals("encrypt")) {
                if (args[0].equals("AES")) {
                    AESEncrypt(keyf, fin, fos);
                }
                else if(args[0].equals("TripleDES")) {
                    DESedeEncrypt(keyf, fin, fos);
                }
                else if(args[0].equals("Blowfish")) {
                    BlowfishEncrypt(keyf, fin, fos);
                }
            }
            else if (args[1].equals("decrypt")) {
                if (args[0].equals("AES")) {
                    AESDecrypt(keyf, fin, fos);
                }
                else if(args[0].equals("TripleDES")) {
                    DESedeDecrypt(keyf, fin, fos);
                }
                else if(args[0].equals("Blowfish")) {
                    BlowfishDecrypt(keyf, fin, fos);
                }
            }
        }
        catch (NoSuchPaddingException | NoSuchAlgorithmException | BadPaddingException | IllegalBlockSizeException | InvalidKeyException e) {
            e.printStackTrace();
        }
    }

    private static void BlowfishEncrypt(FileInputStream keyFileInputStream, FileInputStream fileInputStream, FileOutputStream fileOutputStream) {

    }

    private static void BlowfishDecrypt(FileInputStream keyFileInputStream, FileInputStream fileInputStream, FileOutputStream fileOutputStream) {

    }

    private static void DESedeEncrypt(FileInputStream keyFileInputStream, FileInputStream fileInputStream, FileOutputStream fileOutputStream) throws IOException, NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance("DESede");
        byte[] key = new byte[24];
        keyFileInputStream.read(key);
        SecretKey secretKey = new SecretKeySpec(key, "DESede");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] plainTextByte = new byte[48];
        int bytesRead;
        while ((bytesRead = fileInputStream.read(plainTextByte)) != -1) {
            byte[] output = cipher.update(plainTextByte, 0, bytesRead);
            if (output != null) {
                fileOutputStream.write(output);
            }
        }
        byte[] output = cipher.doFinal();
        if (output != null)
            fileOutputStream.write(output);

        fileInputStream.close();
        fileOutputStream.flush();
        fileOutputStream.close();
        System.out.println("File encrypted.");
    }

    private static void DESedeDecrypt(FileInputStream keyFileInputStream, FileInputStream fileInputStream, FileOutputStream fileOutputStream) throws IOException, NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        byte[] fileByteArray = new byte[fileInputStream.available()];
        Cipher cipher = Cipher.getInstance("DESede");
        byte[] key = new byte[24];
        keyFileInputStream.read(key);
        SecretKey secretKey = new SecretKeySpec(key, "DESede");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] in = new byte[48];
        int read;
        while ((read = fileInputStream.read(in)) != -1) {
            byte[] output = cipher.update(in, 0, read);
            if (output != null)
                fileOutputStream.write(output);
        }

        byte[] output = cipher.doFinal();
        if (output != null)
            fileOutputStream.write(output);
        fileInputStream.close();
        fileOutputStream.flush();
        fileOutputStream.close();
        System.out.println("File decrypted.");
    }

    private static void AESEncrypt(FileInputStream keyFileInputStream, FileInputStream fileInputStream, FileOutputStream fileOutputStream) throws NoSuchPaddingException, NoSuchAlgorithmException, BadPaddingException, IllegalBlockSizeException, IOException, InvalidKeyException {
        Cipher cipher = Cipher.getInstance("AES");
        byte[] key = new byte[32];
        keyFileInputStream.read(key);
        SecretKey secretKey = new SecretKeySpec(key, "AES");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        byte[] plainTextByte = new byte[64];
        int bytesRead;
        while ((bytesRead = fileInputStream.read(plainTextByte)) != -1) {
            byte[] output = cipher.update(plainTextByte, 0, bytesRead);
            if (output != null) {
                fileOutputStream.write(output);
            }
        }
        byte[] output = cipher.doFinal();
        if (output != null)
            fileOutputStream.write(output);

        fileInputStream.close();
        fileOutputStream.flush();
        fileOutputStream.close();
//        System.out.println("File encrypted.");
    }
    private static void AESDecrypt(FileInputStream keyFileInputStream, FileInputStream fileInputStream, FileOutputStream fileOutputStream) throws NoSuchPaddingException, NoSuchAlgorithmException, IOException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance("AES");
        byte[] key = new byte[32];
        keyFileInputStream.read(key);
        SecretKey secretKey = new SecretKeySpec(key, "AES");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        byte[] in = new byte[64];
        int read;
        while ((read = fileInputStream.read(in)) != -1) {
            byte[] output = cipher.update(in, 0, read);
            if (output != null)
                fileOutputStream.write(output);
        }

        byte[] output = cipher.doFinal();
        if (output != null)
            fileOutputStream.write(output);
        fileInputStream.close();
        fileOutputStream.flush();
        fileOutputStream.close();
//        System.out.println("File Decrypted.");

    }
}
