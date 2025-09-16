package Config;
import java.util.Map;
import java.util.HashMap;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Config {
    // Array de Strings
    public static final String[] FILES_PROJECTS = {"index", "data", "tool"};

    // Map de arquivos web e suas extensões
    public static final Map<String, String> FILES_PROJECTS_WEB;
    static {
        FILES_PROJECTS_WEB = new HashMap<>();
        FILES_PROJECTS_WEB.put("index", ".html");
        FILES_PROJECTS_WEB.put("style", ".css");
        FILES_PROJECTS_WEB.put("js", ".js");
    }
    public static final Path DIRETORIO = Paths.get("C:\\Users\\gustavoquitto-ieg\\OneDrive - Instituto J&F\\Área de Trabalho\\Projetcs\\Projects");
    public static final Path DIRETORIO_WEB = Paths.get("C:\\Users\\gustavoquitto-ieg\\OneDrive - Instituto J&F\\Área de Trabalho\\Projetcs\\Tech\\Web\\DS1\\HTML");
    public static final String MESSAGE_SCRIPT = "#Project created successfully!";
}
