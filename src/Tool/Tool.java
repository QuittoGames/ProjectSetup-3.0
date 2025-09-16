package Tool;

import java.io.File;
import java.nio.file.Path;
import java.util.Scanner;

public class Tool {
    public static String readTemplete(Path path) {
        File file = path.toFile();
        try(Scanner sc = new Scanner(file)) {
            sc.useDelimiter("\\Z");
            String returnCode = sc.next();
            return returnCode;
        }catch (Exception e) {
            System.out.println("[ERROR] Erro Al Ler Templete , Erro: " + e.getMessage());
        }
        return "";
    }
}
