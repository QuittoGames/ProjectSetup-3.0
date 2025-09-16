package Data;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

//Classe De Dados Globlais

public class Data {
    public final static HashMap<String , Path> TempletesDataPaths = new HashMap<>(
        Map.of(
            "Test", Paths.get("C:\\Users\\gustavoquitto-ieg\\OneDrive - Instituto J&F\\Área de Trabalho\\Projetcs\\Projects\\Java\\ProjectSetup-3.0\\src\\Templete\\data.ps3tlp")
    ));
}
