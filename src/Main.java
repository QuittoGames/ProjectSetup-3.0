import Config.Config;
import Data.Data;
import Tool.Tool;

public class Main {
    public static void main(String[] args) {
        Tool.readTemplete(Data.TempletesDataPaths.get("Test"));
    }
}