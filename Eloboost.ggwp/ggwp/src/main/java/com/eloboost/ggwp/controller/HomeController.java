package com.eloboost.ggwp.controller;

import com.eloboost.ggwp.model.Booster;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
public class HomeController {

    private static final List<String> LIGAS = Arrays.asList("Hierro", "Bronce", "Plata", "Oro", "Platino", "Esmeralda", "Diamante");
    private static final List<String> DIVISIONES = Arrays.asList("IV", "III", "II", "I");
    
    private Map<String, Integer> preciosARS = new HashMap<>();
    private Map<String, Integer> preciosUSD = new HashMap<>();
    private Map<String, Map<String, String>> diccionario = new HashMap<>();

    public HomeController() {
        cargarPrecios();
        cargarTraducciones();
    }

    // --- TUS BOOSTERS ACTUALIZADOS (Skins Tryhard) ---
    private List<Booster> getBoostersPorIdioma(String lang) {
        List<Booster> lista = new ArrayList<>();
        
        if ("en".equals(lang)) {
            // INGLES
            lista.add(new Booster("1", "Junior", "Master", "MID", "ARG", "Katarina, Akali", 
                "OTP Katarina. I end games in 20 mins. 80% Winrate.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Katarina_10.jpg")); // Death Sworn
                
            lista.add(new Booster("2", "Guido", "Grandmaster", "JUNGLE", "ARG", "Lee Sin, Viego", 
                "Total objective control. I guarantee the 4 dragons.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/LeeSin_4.jpg")); // Muay Thai
                
            lista.add(new Booster("3", "Thomas", "Challenger", "MID/TOP", "CHI", "Akali, Sylas", 
                "Mechanical god. Impossible to gank. I delete the ADC.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Akali_15.jpg")); // Star Guardian

        } else if ("pt".equals(lang)) {
            // PORTUGUES
            lista.add(new Booster("1", "Junior", "Master", "MID", "ARG", "Katarina, Akali", 
                "OTP Katarina. Termino partidas em 20 min. Winrate 80%.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Katarina_10.jpg"));
                
            lista.add(new Booster("2", "Guido", "Grandmaster", "JUNGLE", "ARG", "Lee Sin, Viego", 
                "Controle total de objetivos. Garanto os 4 dragões.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/LeeSin_4.jpg"));
                
            lista.add(new Booster("3", "Thomas", "Challenger", "MID/TOP", "CHI", "Akali, Sylas", 
                "Deus mecânico. Impossível de gankar. Eu deleto o ADC.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Akali_15.jpg"));

        } else {
            // ESPAÑOL
            lista.add(new Booster("1", "Junior", "Master", "MID", "ARG", "Katarina", 
                "OTP Katarina. Termino las partidas en 20 minutos. Winrate 80%.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Katarina_10.jpg")); // Muerte Anunciada
                
            lista.add(new Booster("2", "Guido", "Grandmaster", "JUNGLE", "ARG", "Lee Sin, Jayce", 
                "Control total de objetivos. Te aseguro los 4 dragones.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/LeeSin_4.jpg")); // Muay Thai
                
            lista.add(new Booster("3", "Thomas", "Challenger", "MID/TOP", "CHI", "Akali, Sylas", 
                "Mecánicas perfectas. Imposible de gankear. Borro al ADC.", 
                "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Akali_15.jpg")); // Star Guardian
        }
        return lista;
    }

    @GetMapping("/")
    public String home(
        @RequestParam(defaultValue = "es") String lang, 
        @RequestParam(defaultValue = "ARS") String currency,
        Model model
    ) {
        configurarModeloBasico(model, lang, currency);
        model.addAttribute("txt_titulo", "ELOBOOST NATION"); 
        
        model.addAttribute("selLigaActual", "Plata");
        model.addAttribute("selDivActual", "IV");
        model.addAttribute("selLigaDeseada", "Oro");
        model.addAttribute("selDivDeseada", "IV");

        model.addAttribute("extraRol", false);
        model.addAttribute("extraChamp", false);
        model.addAttribute("extraFlash", false);
        model.addAttribute("extraOffline", false);

        model.addAttribute("imgActual", "https://opgg-static.akamaized.net/images/medals_new/silver.png");
        model.addAttribute("imgDeseada", "https://opgg-static.akamaized.net/images/medals_new/gold.png");
        
        return "index";
    }

    @PostMapping("/calcular-presupuesto")
    public String calcular(
            @RequestParam String ligaActual, 
            @RequestParam String divActual,
            @RequestParam String ligaDeseada, 
            @RequestParam String divDeseada,
            @RequestParam(defaultValue = "false") boolean extraRol,
            @RequestParam(defaultValue = "false") boolean extraChamp,
            @RequestParam(defaultValue = "false") boolean extraFlash,
            @RequestParam(defaultValue = "false") boolean extraOffline,
            @RequestParam(defaultValue = "es") String lang,
            @RequestParam(defaultValue = "ARS") String currency,
            Model model
    ) {
        configurarModeloBasico(model, lang, currency);
        model.addAttribute("txt_titulo", "ELOBOOST NATION");

        try {
            int start = (LIGAS.indexOf(ligaActual) * 4) + DIVISIONES.indexOf(divActual);
            int end = (LIGAS.indexOf(ligaDeseada) * 4) + DIVISIONES.indexOf(divDeseada);

            if (start >= end) {
                String errorMsg = lang.equals("en") ? "Target must be higher than current." : 
                                  lang.equals("pt") ? "A meta deve ser maior que a atual." : 
                                  "La meta debe ser mayor a la liga actual.";
                model.addAttribute("error", errorMsg);
            } else {
                Map<String, Integer> preciosUsados = currency.equals("USD") ? preciosUSD : preciosARS;
                int precioBase = 0;
                for (int i = start; i < end; i++) {
                    precioBase += preciosUsados.get(LIGAS.get(i / 4));
                }

                double precioFinal = precioBase;
                List<String> extrasTexto = new ArrayList<>(); 

                if (extraRol) { precioFinal += (precioBase * 0.15); extrasTexto.add("Rol"); }
                if (extraChamp) { precioFinal += (precioBase * 0.35); extrasTexto.add("OTP Champ"); }
                if (extraOffline) { precioFinal += (precioBase * 0.10); extrasTexto.add("Offline"); }
                if (extraFlash) { extrasTexto.add("Flash D"); }

                int total = (int) precioFinal;
                String simbolo = currency.equals("USD") ? "US$ " : "$ ";
                
                String lActualTrad = diccionario.get(lang).get("liga_" + ligaActual);
                String lDeseadaTrad = diccionario.get(lang).get("liga_" + ligaDeseada);

                String resumenTxt = lActualTrad + " " + divActual + " -> " + lDeseadaTrad + " " + divDeseada;
                if (!extrasTexto.isEmpty()) {
                    resumenTxt += " (+ " + String.join(", ", extrasTexto) + ")";
                }

                model.addAttribute("resultadoPrecio", total);
                model.addAttribute("simboloMoneda", simbolo);
                model.addAttribute("resumen", resumenTxt);
                model.addAttribute("boosters", getBoostersPorIdioma(lang));
            }
        } catch (Exception e) {
            model.addAttribute("error", "Error.");
        }

        model.addAttribute("imgActual", generarUrlImagen(ligaActual));
        model.addAttribute("imgDeseada", generarUrlImagen(ligaDeseada));
        model.addAttribute("selLigaActual", ligaActual);
        model.addAttribute("selDivActual", divActual);
        model.addAttribute("selLigaDeseada", ligaDeseada);
        model.addAttribute("selDivDeseada", divDeseada);
        model.addAttribute("extraRol", extraRol);
        model.addAttribute("extraChamp", extraChamp);
        model.addAttribute("extraFlash", extraFlash);
        model.addAttribute("extraOffline", extraOffline);

        return "index";
    }

    private void configurarModeloBasico(Model model, String lang, String currency) {
        if (!diccionario.containsKey(lang)) lang = "es";
        Map<String, String> textos = diccionario.get(lang);
        for (Map.Entry<String, String> entry : textos.entrySet()) {
            model.addAttribute("txt_" + entry.getKey(), entry.getValue());
        }
        model.addAttribute("lang", lang);
        model.addAttribute("currency", currency);
    }

    private String generarUrlImagen(String nombreLiga) {
        String englishName = "provisional";
        switch (nombreLiga) {
            case "Hierro": englishName = "iron"; break;
            case "Bronce": englishName = "bronze"; break;
            case "Plata": englishName = "silver"; break;
            case "Oro": englishName = "gold"; break;
            case "Platino": englishName = "platinum"; break;
            case "Esmeralda": englishName = "emerald"; break;
            case "Diamante": englishName = "diamond"; break;
        }
        return "https://opgg-static.akamaized.net/images/medals_new/" + englishName + ".png";
    }

    private void cargarPrecios() {
        // ACTUALIZADO CON TUS PRECIOS (Promedio por división según docx)
        preciosARS.put("Hierro", 2500); 
        preciosARS.put("Bronce", 3750); 
        preciosARS.put("Plata", 5000);
        preciosARS.put("Oro", 7500); 
        preciosARS.put("Platino", 9500); 
        preciosARS.put("Esmeralda", 12250);
        preciosARS.put("Diamante", 17250);

        // Precios USD (Estimados estándar internacional)
        preciosUSD.put("Hierro", 5); preciosUSD.put("Bronce", 7); preciosUSD.put("Plata", 9);
        preciosUSD.put("Oro", 12); preciosUSD.put("Platino", 18); preciosUSD.put("Esmeralda", 25);
        preciosUSD.put("Diamante", 40);
    }

    private void cargarTraducciones() {
        Map<String, String> es = new HashMap<>();
        es.put("titulo", "Subí de división hoy mismo. Calculá tu presupuesto."); 
        es.put("calc_titulo", "CALCULÁ TU BOOST A MEDIDA 💪");
        es.put("lbl_actual", "Liga Actual"); es.put("lbl_deseada", "Liga Deseada");
        es.put("lbl_extras", "Opciones Extra (Personalizá tu pedido)");
        es.put("check_rol", "Rol Específico (+15%)"); es.put("check_champ", "Campeón Específico (+35%)");
        es.put("check_flash", "Flash en D (Gratis)"); es.put("check_offline", "Jugar Offline (+10%)");
        es.put("btn_cotizar", "COTIZAR AHORA"); es.put("res_presupuesto", "Presupuesto:");
        es.put("btn_elegir", "👇 ELEGIR BOOSTER PARA ESTE TRABAJO");
        es.put("res_subtext", "Elegí el que mejor se adapte a tus requerimientos");
        es.put("boosters_titulo", "Seleccioná a tu Profesional"); es.put("btn_contratar", "CONTRATAR");
        es.put("champ_pool", "CHAMP POOL:");
        es.put("liga_Hierro", "Hierro"); es.put("liga_Bronce", "Bronce"); es.put("liga_Plata", "Plata");
        es.put("liga_Oro", "Oro"); es.put("liga_Platino", "Platino"); es.put("liga_Esmeralda", "Esmeralda"); es.put("liga_Diamante", "Diamante");
        diccionario.put("es", es);

        Map<String, String> en = new HashMap<>();
        en.put("titulo", "Rank up today. Calculate your budget.");
        en.put("calc_titulo", "CUSTOMIZE YOUR BOOST 💪");
        en.put("lbl_actual", "Current League"); en.put("lbl_deseada", "Desired League");
        en.put("lbl_extras", "Extra Options (Customize Order)");
        en.put("check_rol", "Specific Role (+15%)"); en.put("check_champ", "Specific Champion (+35%)");
        en.put("check_flash", "Flash on D (Free)"); en.put("check_offline", "Offline Mode (+10%)");
        en.put("btn_cotizar", "CALCULATE NOW"); en.put("res_presupuesto", "Budget:");
        en.put("btn_elegir", "👇 CHOOSE BOOSTER FOR THIS JOB");
        en.put("res_subtext", "Choose the one that best fits your needs");
        en.put("boosters_titulo", "Select your Pro Player"); en.put("btn_contratar", "HIRE");
        en.put("champ_pool", "CHAMP POOL:");
        en.put("liga_Hierro", "Iron"); en.put("liga_Bronce", "Bronze"); en.put("liga_Plata", "Silver");
        en.put("liga_Oro", "Gold"); en.put("liga_Platino", "Platinum"); en.put("liga_Esmeralda", "Emerald"); en.put("liga_Diamante", "Diamond");
        diccionario.put("en", en);

        Map<String, String> pt = new HashMap<>();
        pt.put("titulo", "Suba de elo hoje. Calcule seu orçamento.");
        pt.put("calc_titulo", "CALCULE SEU BOOST 💪");
        pt.put("lbl_actual", "Liga Atual"); pt.put("lbl_deseada", "Liga Desejada");
        pt.put("lbl_extras", "Opções Extras (Personalize)");
        pt.put("check_rol", "Role Específica (+15%)"); pt.put("check_champ", "Campeão Específico (+35%)");
        pt.put("check_flash", "Flash no D (Grátis)"); pt.put("check_offline", "Modo Offline (+10%)");
        pt.put("btn_cotizar", "COTAR AGORA"); pt.put("res_presupuesto", "Orçamento:");
        pt.put("btn_elegir", "👇 ESCOLHER BOOSTER");
        pt.put("res_subtext", "Escolha o que melhor se adapta a você");
        pt.put("boosters_titulo", "Selecione seu Profissional"); pt.put("btn_contratar", "CONTRATAR");
        pt.put("champ_pool", "CHAMP POOL:");
        pt.put("liga_Hierro", "Ferro"); pt.put("liga_Bronce", "Bronze"); pt.put("liga_Plata", "Prata");
        pt.put("liga_Oro", "Ouro"); pt.put("liga_Platino", "Platina"); pt.put("liga_Esmeralda", "Esmeralda"); pt.put("liga_Diamante", "Diamante");
        diccionario.put("pt", pt);
    }
}