package proyecto;

import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.List;

// ═══════════════════════════════════════════════════════════════════
//  APUNAB – Sistema de Puntos Académicos UNAB
//  Autor: Keiner Steve Sereno García
// ═══════════════════════════════════════════════════════════════════
public class APUNAB extends JFrame {

    // ── Paleta UNAB ───────────────────────────────────────────────
    public static final Color CAFE_OSCURO  = new Color(74,  44,  16);
    public static final Color CAFE_MEDIO   = new Color(111, 68,  28);
    public static final Color CAFE_CLARO   = new Color(160, 105, 50);
    public static final Color CREMA        = new Color(245, 235, 215);
    public static final Color CREMA_OSCURO = new Color(220, 200, 170);
    public static final Color DORADO       = new Color(212, 160, 40);
    public static final Color VERDE        = new Color(60,  140, 60);
    public static final Color ROJO         = new Color(180, 40,  40);
    public static final Color TEXTO_OSCURO = new Color(40,  20,  5);
    public static final Color TEXTO_CLARO  = new Color(255, 248, 235);

    // ── Persistencia ──────────────────────────────────────────────
    public static final String DATA_DIR   = System.getProperty("user.home") + File.separator + "APUNAB_Data";
    public static final String USERS_FILE = DATA_DIR + File.separator + "usuarios.csv";
    public static final String BETS_FILE  = DATA_DIR + File.separator + "apuestas.csv";

    // ── Estado global ─────────────────────────────────────────────
    public static List<Usuario> usuarios      = new ArrayList<>();
    public static List<Apuesta> apuestas      = new ArrayList<>();
    public static Usuario       usuarioActual = null;

    // ── Navegación ────────────────────────────────────────────────
    JPanel     panelRaiz;
    CardLayout cardLayout;

    public APUNAB() {
        setTitle("APUNAB – Sistema de Puntos Académicos");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1000, 660);
        setLocationRelativeTo(null);
        setResizable(false);

        Persistencia.cargarDatos();
        Persistencia.inicializarPlantillas();

        cardLayout = new CardLayout();
        panelRaiz  = new JPanel(cardLayout);

        panelRaiz.add(new PantallaLogin(this),     "login");
        panelRaiz.add(new PantallaRegistro(this),  "registro");
        panelRaiz.add(new JPanel(),                "principal"); // placeholder

        setContentPane(panelRaiz);
        cardLayout.show(panelRaiz, "login");
    }

    public void mostrar(String pantalla) {
        if (pantalla.equals("principal")) {
            // Reemplazar el panel principal para refrescar datos
            int count = panelRaiz.getComponentCount();
            if (count >= 3) panelRaiz.remove(2);
            panelRaiz.add(new PantallaPrincipal(this), "principal");
        }
        cardLayout.show(panelRaiz, pantalla);
        revalidate();
        repaint();
    }

    // ── MAIN ──────────────────────────────────────────────────────
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try { UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName()); }
            catch (Exception ignored) {}
            new APUNAB().setVisible(true);
        });
    }
}
