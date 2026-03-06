from flask import Flask, render_template, request

# --- Inicialización de la aplicación Flask ---
app = Flask(__name__)

# --- Constantes del sistema (Ligas, Divisiones y Precios base) ---
# AGREGADAS Master y Grandmaster
LIGAS = ["Hierro", "Bronce", "Plata", "Oro", "Platino", "Esmeralda", "Diamante", "Master", "Grandmaster"]
DIVISIONES = ["IV", "III", "II", "I"]

PRECIOS_ARS = {"Hierro": 2000, "Bronce": 3000, "Plata": 4000, "Oro": 5000, "Platino": 6000, "Esmeralda": 8000, "Diamante": 10000}
PRECIOS_USD = {"Hierro": 2, "Bronce": 2.5, "Plata": 3.5, "Oro": 4, "Platino": 5.5, "Esmeralda": 7.5, "Diamante": 10}

# --- Diccionario de Textos y Traducciones (Español, Inglés, Portugués) ---
TEXTOS = {
    "es": {
        "titulo": "Subí de división hoy mismo. Calculá tu presupuesto.",
        "calc_titulo": "CALCULÁ TU BOOST", "lbl_actual": "Liga Actual", "lbl_deseada": "Liga Deseada",
        "lbl_extras": "Opciones Extra", "check_rol": "Rol Específico (+15%)", "check_champ": "Campeón Específico (+35%)",
        "check_flash": "Flash en D (Gratis)", "check_offline": "Modo Offline (+10%)", "btn_cotizar": "COTIZAR AHORA",
        "res_presupuesto": "Presupuesto:", "btn_elegir": "ELEGIR BOOSTER", "res_subtext": "Elegí el mejor",
        "boosters_titulo": "Seleccioná a tu Profesional", "btn_contratar": "CONTRATAR", "champ_pool": "CHAMP POOL:",
        "liga_Hierro": "Hierro", "liga_Bronce": "Bronce", "liga_Plata": "Plata", "liga_Oro": "Oro",
        "liga_Platino": "Platino", "liga_Esmeralda": "Esmeralda", "liga_Diamante": "Diamante",
        "liga_Master": "Master", "liga_Grandmaster": "Grandmaster",
        "txt_amedida": "A MEDIDA", "btn_consultar_wsp": "CONSULTAR POR WSP",
        
        # TEXTOS NUEVOS DE LA PROMO SEPARADOS
        "txt_promo_1": "🔥 PROMO: 10% OFF en 1 Liga Completa",
        "txt_promo_2": "🔥 PROMO: 15% OFF en 2+ Ligas Completas",
        "msg_descuento_1": "¡{desc}% OFF APLICADO (1 LIGA COMPLETA)!",
        "msg_descuento_2": "¡{desc}% OFF APLICADO (2+ LIGAS COMPLETAS)!",
        
        "tit_servicios": "NUESTROS SERVICIOS",
        "btn_consultar": "CONSULTAR",
        
        # SERVICIO 1: Placements
        "srv_1_tit": "PLACEMENTS", 
        "srv_1_desc": "Asegurá el mejor comienzo de temporada. Jugamos tus 5 primeras partidas para garantizarte el elo más alto posible.",
        "srv_1_bullets": ["Winrate garantizado superior al 80%.", "Evitá el 'Elo Hell' desde el día 1.", "Disponible para todas las ligas.", "Privacidad absoluta de la cuenta."],
        "srv_1_wsp": "Hola!%20Vengo%20de%20la%20web,%20estoy%20interesado%20en%20el%20servicio%20de%20*Placements*.",

        # SERVICIO 2: Fix MMR
        "srv_2_tit": "FIX MMR (Limpieza)", 
        "srv_2_desc": "¿Ganás 15 LP y perdés 30? Tu MMR está roto. Jugamos hasta normalizar tus ganancias de puntos para que vuelvas a subir rápido.",
        "srv_2_bullets": ["Estabilización de ganancias de LP.", "Mejora del emparejamiento de la cuenta.", "Ideal para cuentas 'stuck' (atascadas).", "Resultados 100% garantizados."],
        "srv_2_wsp": "Hola!%20Vengo%20de%20la%20web,%20estoy%20interesado%20en%20el%20servicio%20de%20*Fix%20MMR*.",

        # SERVICIO 3: Coaching
        "srv_3_tit": "COACHING PERSONALIZADO", 
        "srv_3_desc": "Convertite en el carry de tus partidas. Sesiones individuales con jugadores High Elo para pulir tus errores.",
        "srv_3_bullets": ["Análisis de Replays (VOD Review).", "Optimización de Pool de campeones y builds.", "Guía de Wave Management y Macro.", "Atención 1 a 1 directa en Discord."],
        "srv_3_wsp": "Hola!%20Vengo%20de%20la%20web,%20estoy%20interesado%20en%20el%20servicio%20de%20*Coaching*.",

        "tit_garantia": "🛡️ GARANTÍA NATION",
        "gar_off_tit": "🔌 MODO OFFLINE", "gar_off_desc": "Jugamos en modo desconectado. Nadie sabrá que estás jugando.",
        "gar_prot_tit": "🔐 PROTECCIÓN DE CUENTA", "gar_prot_desc": "No tocamos tu RP, Esencia Azul ni Artesanía.",
        "gar_tox_tit": "🤐 CERO TOXICIDAD", "gar_tox_desc": "Chat restringido por protocolo. Cuidamos tu honor al 100%."
    },
    "en": {
        "titulo": "Rank up today. Calculate your budget.",
        "calc_titulo": "CALCULATE YOUR BOOST", "lbl_actual": "Current Rank", "lbl_deseada": "Desired Rank",
        "lbl_extras": "Extra Options", "check_rol": "Specific Role (+15%)", "check_champ": "Specific Champ (+35%)",
        "check_flash": "Flash on D (Free)", "check_offline": "Offline Mode (+10%)", "btn_cotizar": "QUOTE NOW",
        "res_presupuesto": "Estimated Budget:", "btn_elegir": "CHOOSE BOOSTER", "res_subtext": "Pick the best one",
        "boosters_titulo": "Select your Professional", "btn_contratar": "HIRE NOW", "champ_pool": "CHAMP POOL:",
        "liga_Hierro": "Iron", "liga_Bronce": "Bronze", "liga_Plata": "Silver", "liga_Oro": "Gold",
        "liga_Platino": "Platinum", "liga_Esmeralda": "Emerald", "liga_Diamante": "Diamond",
        "liga_Master": "Master", "liga_Grandmaster": "Grandmaster",
        "txt_amedida": "CUSTOM", "btn_consultar_wsp": "INQUIRE ON WSP",
        
        "txt_promo_1": "🔥 PROMO: 10% OFF for 1 Full League",
        "txt_promo_2": "🔥 PROMO: 15% OFF for 2+ Full Leagues",
        "msg_descuento_1": "¡{desc}% OFF APPLIED (1 FULL LEAGUE)!",
        "msg_descuento_2": "¡{desc}% OFF APPLIED (2+ FULL LEAGUES)!",
        
        "tit_servicios": "OUR SERVICES",
        "btn_consultar": "INQUIRE",
        
        "srv_1_tit": "PLACEMENTS", 
        "srv_1_desc": "Secure the best season start. We play your first 5 games to guarantee the highest possible elo.",
        "srv_1_bullets": ["Guaranteed winrate over 80%.", "Avoid 'Elo Hell' from day 1.", "Available for all ranks.", "Absolute account privacy."],
        "srv_1_wsp": "Hi!%20I%20come%20from%20the%20website,%20I'm%20interested%20in%20the%20*Placements*%20service.",

        "srv_2_tit": "FIX MMR", 
        "srv_2_desc": "Winning 15 LP and losing 30? Your MMR is broken. We play until your LP gains normalize.",
        "srv_2_bullets": ["LP gain stabilization.", "Matchmaking improvement.", "Ideal for 'stuck' accounts.", "100% guaranteed results."],
        "srv_2_wsp": "Hi!%20I%20come%20from%20the%20website,%20I'm%20interested%20in%20the%20*Fix%20MMR*%20service.",

        "srv_3_tit": "CUSTOM COACHING", 
        "srv_3_desc": "Become the carry of your games. 1-on-1 sessions with High Elo players to fix your mistakes.",
        "srv_3_bullets": ["VOD Review Analysis.", "Champion pool & build optimization.", "Wave Management and Macro guide.", "Direct 1-on-1 Discord attention."],
        "srv_3_wsp": "Hi!%20I%20come%20from%20the%20website,%20I'm%20interested%20in%20the%20*Coaching*%20service.",

        "tit_garantia": "🛡️ NATION GUARANTEE",
        "gar_off_tit": "🔌 OFFLINE MODE", "gar_off_desc": "We play in offline mode. No one will know you're playing.",
        "gar_prot_tit": "🔐 ACCOUNT PROTECTION", "gar_prot_desc": "We don't touch your RP, Blue Essence, or Loot.",
        "gar_tox_tit": "🤐 ZERO TOXICITY", "gar_tox_desc": "Chat restricted by protocol. 100% honor protection."
    },
    "pt": {
        "titulo": "Suba de divisão hoje mesmo. Calcule seu orçamento.",
        "calc_titulo": "CALCULE SEU BOOST", "lbl_actual": "Liga Atual", "lbl_deseada": "Liga Desejada",
        "lbl_extras": "Opções Extras", "check_rol": "Rota Específica (+15%)", "check_champ": "Campeão Específico (+35%)",
        "check_flash": "Flash no D (Grátis)", "check_offline": "Modo Offline (+10%)", "btn_cotizar": "ORÇAR AGORA",
        "res_presupuesto": "Orçamento:", "btn_elegir": "ESCOLHER BOOSTER", "res_subtext": "Escolha o melhor",
        "boosters_titulo": "Selecione seu Profissional", "btn_contratar": "CONTRATAR", "champ_pool": "CHAMP POOL:",
        "liga_Hierro": "Ferro", "liga_Bronce": "Bronze", "liga_Plata": "Prata", "liga_Oro": "Ouro",
        "liga_Platino": "Platina", "liga_Esmeralda": "Esmeralda", "liga_Diamante": "Diamante",
        "liga_Master": "Master", "liga_Grandmaster": "Grandmaster",
        "txt_amedida": "SOB MEDIDA", "btn_consultar_wsp": "CONSULTAR NO WSP",
        
        "txt_promo_1": "🔥 PROMO: 10% OFF por 1 Liga Completa",
        "txt_promo_2": "🔥 PROMO: 15% OFF por 2+ Ligas Completas",
        "msg_descuento_1": "¡{desc}% OFF APLICADO (1 LIGA COMPLETA)!",
        "msg_descuento_2": "¡{desc}% OFF APLICADO (2+ LIGAS COMPLETAS)!",
        
        "tit_servicios": "NOSSOS SERVIÇOS",
        "btn_consultar": "CONSULTAR",
        
        "srv_1_tit": "PLACEMENTS", 
        "srv_1_desc": "Garanta o melhor início de temporada. Jogamos suas 5 primeiras partidas para garantir o maior elo possível.",
        "srv_1_bullets": ["Winrate garantido superior a 80%.", "Evite o 'Elo Hell' desde o dia 1.", "Disponível para todas as ligas.", "Privacidade absoluta da conta."],
        "srv_1_wsp": "Olá!%20Venho%20do%20site,%20estou%20interessado%20no%20serviço%20de%20*Placements*.",

        "srv_2_tit": "FIX MMR", 
        "srv_2_desc": "Ganhando 15 LP e perdendo 30? Seu MMR está quebrado. Jogamos até normalizar seus ganhos de pontos.",
        "srv_2_bullets": ["Estabilização de ganhos de LP.", "Melhoria do matchmaking da conta.", "Ideal para contas 'stuck' (presas).", "Resultados 100% garantidos."],
        "srv_2_wsp": "Olá!%20Venho%20do%20site,%20estou%20interessado%20no%20serviço%20de%20*Fix%20MMR*.",

        "srv_3_tit": "COACHING", 
        "srv_3_desc": "Torne-se o carry das suas partidas. Sessões individuais com jogadores High Elo para corrigir seus erros.",
        "srv_3_bullets": ["Análise de Replays (VOD Review).", "Otimização de Champion Pool e builds.", "Guia de Wave Management e Macro.", "Atenção 1 a 1 direta no Discord."],
        "srv_3_wsp": "Olá!%20Venho%20do%20site,%20estou%20interessado%20no%20serviço%20de%20*Coaching*.",

        "tit_garantia": "🛡️ GARANTIA NATION",
        "gar_off_tit": "🔌 MODO OFFLINE", "gar_off_desc": "Jogamos em modo desconectado. Ninguém saberá que você está jogando.",
        "gar_prot_tit": "🔐 PROTEÇÃO DE CONTA", "gar_prot_desc": "Não tocamos no seu RP, Essência Azul ou Espólios.",
        "gar_tox_tit": "🤐 ZERO TOXICIDADE", "gar_tox_desc": "Chat restrito por protocolo. Cuidamos do seu nível de honra."
    }
}

# --- Funciones Auxiliares ---
def get_boosters():
    """Devuelve la lista de profesionales disponibles con sus datos y fotos."""
    return [
        {"nickname": "Junior", "rango": "Master", "carril": "MID", "nacionalidad": "ARG", "champPool": "Katarina, Akali", "descripcion": "OTP Katarina. Termino las partidas en 20 minutos. Winrate 80%.", "fotoUrl": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Katarina_10.jpg"},
        {"nickname": "Guido", "rango": "Grandmaster", "carril": "JUNGLE", "nacionalidad": "ARG", "champPool": "Lee Sin, Viego", "descripcion": "Control total de objetivos. Te aseguro los 4 dragones.", "fotoUrl": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/LeeSin_4.jpg"},
        {"nickname": "Thomas", "rango": "Challenger", "carril": "MID/TOP", "nacionalidad": "CHI", "champPool": "Akali, Sylas", "descripcion": "Mecánicas perfectas. Imposible de gankear. Borro al ADC.", "fotoUrl": "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Akali_15.jpg"}
    ]

def get_imagen_liga(liga):
    """Traduce el nombre de la liga en español al nombre del archivo de imagen correspondiente."""
    mapa = {"Hierro": "iron", "Bronce": "bronze", "Plata": "silver", "Oro": "gold", "Platino": "platinum", "Esmeralda": "emerald", "Diamante": "diamond", "Master": "master", "Grandmaster": "grandmaster"}
    return f"https://opgg-static.akamaized.net/images/medals_new/{mapa.get(liga, 'provisional')}.png"


# --- Ruta Principal de la Aplicación ---
@app.route("/", methods=["GET", "POST"])
def home():
    
    # 1. Configuración de idioma y moneda (Por URL o por POST oculto)
    lang = request.args.get("lang", "es")
    currency = request.args.get("currency", "ARS")
    
    if request.method == "POST":
        lang = request.form.get("lang", "es")
        currency = request.form.get("currency", "ARS")
        
    # 2. Variables de contexto enviadas al HTML por defecto
    context = {
        "lang": lang, "currency": currency, **TEXTOS.get(lang, TEXTOS["es"]),
        "selLigaActual": "Plata", "selDivActual": "IV",
        "selLigaDeseada": "Oro", "selDivDeseada": "IV",
        "extraRol": False, "extraChamp": False, "extraFlash": False, "extraOffline": False,
        "imgActual": get_imagen_liga("Plata"), "imgDeseada": get_imagen_liga("Oro"),
        "resultadoPrecio": None, "error": None, "es_high_elo": False, "texto_descuento": None
    }

    # 3. Lógica de cálculo (Ejecutada al hacer click en "Cotizar")
    if request.method == "POST":
        
        # Obtener valores seleccionados
        liga_actual = request.form.get("ligaActual")
        div_actual = request.form.get("divActual")
        liga_deseada = request.form.get("ligaDeseada")
        div_deseada = request.form.get("divDeseada")
        
        # Obtener checkboxes
        extra_rol = request.form.get("extraRol") == "on"
        extra_champ = request.form.get("extraChamp") == "on"
        extra_flash = request.form.get("extraFlash") == "on"
        extra_offline = request.form.get("extraOffline") == "on"

        # Mantener los valores elegidos en pantalla
        context.update({
            "selLigaActual": liga_actual, "selDivActual": div_actual,
            "selLigaDeseada": liga_deseada, "selDivDeseada": div_deseada,
            "extraRol": extra_rol, "extraChamp": extra_champ, 
            "extraFlash": extra_flash, "extraOffline": extra_offline,
            "imgActual": get_imagen_liga(liga_actual), "imgDeseada": get_imagen_liga(liga_deseada)
        })

        try:
            # Control para Master y Grandmaster (Ligas sin precio fijo)
            is_high_elo = liga_actual in ["Master", "Grandmaster"] or liga_deseada in ["Master", "Grandmaster"]
            
            start_idx = LIGAS.index(liga_actual)
            end_idx = LIGAS.index(liga_deseada)

            # Validar que no vaya para atrás
            if start_idx > end_idx:
                context["error"] = "La meta debe ser mayor a la liga actual."
            elif start_idx == end_idx and not is_high_elo:
                if DIVISIONES.index(div_actual) >= DIVISIONES.index(div_deseada):
                    context["error"] = "La meta debe ser mayor a la división actual."
            
            # Si no hay errores y es High Elo, preparamos el botón especial
            if not context.get("error"):
                if is_high_elo:
                    context["es_high_elo"] = True
                    context["resumen"] = f"{liga_actual} -> {liga_deseada}"
                    context["wsp_high_elo"] = f"Hola!%20Vengo%20de%20la%20web,%20necesito%20presupuesto%20para%20High%20Elo:%20{liga_actual}%20a%20{liga_deseada}."
                else:
                    # Cálculo de distancia y precio normal
                    start = (start_idx * 4) + DIVISIONES.index(div_actual)
                    end = (end_idx * 4) + DIVISIONES.index(div_deseada)
                    
                    # Verificamos la cantidad de divisiones para aplicar descuento
                    div_diff = end - start

                    precios = PRECIOS_USD if currency == "USD" else PRECIOS_ARS
                    precio_base = 0
                    for i in range(start, end):
                        precio_base += precios[LIGAS[i // 4]]

                    # --- LÓGICA DE DESCUENTOS POR LIGA COMPLETA ACTUALIZADA ---
                    descuento_pct = 0
                    msg_key = ""
                    if div_diff >= 8:      # 2 ligas completas o más
                        descuento_pct = 15
                        msg_key = "msg_descuento_2"
                    elif div_diff >= 4:    # 1 liga completa
                        descuento_pct = 10
                        msg_key = "msg_descuento_1"
                    
                    if descuento_pct > 0:
                        # Aplicamos el descuento al precio base
                        precio_base = precio_base * (1 - (descuento_pct / 100.0))
                        # Preparamos el cartelito de descuento dinámico para el HTML
                        msg_base = TEXTOS.get(lang, TEXTOS["es"]).get(msg_key, "¡{desc}% OFF!")
                        context["texto_descuento"] = msg_base.format(desc=descuento_pct)

                    # Aplicación de extras (se calculan en base al precio ya descontado)
                    precio_final = float(precio_base)
                    extras_texto = []

                    if extra_rol: precio_final += (precio_base * 0.15); extras_texto.append("Rol")
                    if extra_champ: precio_final += (precio_base * 0.35); extras_texto.append("OTP Champ")
                    if extra_offline: precio_final += (precio_base * 0.10); extras_texto.append("Offline")
                    if extra_flash: extras_texto.append("Flash D")

                    # Inyección de resultados al contexto final
                    context["resultadoPrecio"] = int(precio_final)
                    context["simboloMoneda"] = "US$ " if currency == "USD" else "$ "
                    
                    resumen = f"{liga_actual} {div_actual} -> {liga_deseada} {div_deseada}"
                    if extras_texto: resumen += f" (+ {', '.join(extras_texto)})"
                    
                    context["resumen"] = resumen
                    
                # Cargamos los boosters (aunque estén ocultos en el HTML)
                context["boosters"] = get_boosters()

        except Exception as e:
            context["error"] = "Error al calcular."

    return render_template("index.html", **context)


# --- Arranque del Servidor ---
if __name__ == "__main__":
    app.run(debug=True)