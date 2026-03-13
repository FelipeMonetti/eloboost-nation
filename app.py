from flask import Flask, render_template, request
import os

# --- Inicialización de la aplicación Flask ---
app = Flask(__name__)

# --- Constantes del sistema (Ligas, Divisiones y Precios base) ---
LIGAS = ["Hierro", "Bronce", "Plata", "Oro", "Platino", "Esmeralda", "Diamante", "Master", "Grandmaster"]
DIVISIONES = ["IV", "III", "II", "I"]

# Precios base para las ligas normales
PRECIOS_ARS = {"Hierro": 2000, "Bronce": 3000, "Plata": 4000, "Oro": 5000, "Platino": 6000, "Esmeralda": 8000}
PRECIOS_USD = {"Hierro": 2, "Bronce": 2.5, "Plata": 3.5, "Oro": 4, "Platino": 5.5, "Esmeralda": 7.5}

# NUEVO: Precios escalonados específicos para Diamante
# 0 = de IV a III | 1 = de III a II | 2 = de II a I
PRECIOS_DIAMANTE_ARS = {0: 10000, 1: 12000, 2: 15000, 3: 15000} 
PRECIOS_DIAMANTE_USD = {0: 10, 1: 12, 2: 15, 3: 15}

# --- Diccionario de Textos y Traducciones (Español, Inglés, Portugués) ---
TEXTOS = {
    "es": {
        "hero_title": "Jugá en la liga que realmente merecés",
        "hero_subtitle": "Esquivá a los trolls y a los AFKs. Contratá a un profesional y asegurá tu rango sin estrés ni dolores de cabeza.",
        "titulo": "Subí de división hoy mismo. Calculá tu presupuesto.",
        "calc_titulo": "CALCULÁ TU BOOST", "lbl_actual": "Liga Actual", "lbl_deseada": "Liga Deseada",
        "lbl_extras": "Opciones Extra", "check_rol": "Rol Específico (+30%)", "check_champ": "Campeón Específico (+50%)",
        "check_flash": "Flash en D", "check_express": "Entrega Express (+20%)", "check_duoboost": "DuoBoost", 
        "tt_rol": "Elegís exactamente qué línea va a jugar el booster.",
        "tt_champ": "El booster jugará solo con los campeones que vos le pidas.",
        "tt_flash": "Acomodamos la tecla del Flash para que coincida con tu costumbre.",
        "tt_express": "Tu pedido salta al primer lugar de la cola. Asignación inmediata.",
        "tt_duoboost": "Jugás en tu propia cuenta en duo con uno de nuestros boosters.",
        "btn_cotizar": "COTIZAR AHORA",
        "res_presupuesto": "Presupuesto:", "btn_elegir": "ELEGIR BOOSTER", "res_subtext": "Elegí el mejor",
        "boosters_titulo": "Seleccioná a tu Profesional", "btn_contratar": "CONTRATAR", "champ_pool": "CHAMP POOL:",
        "liga_Hierro": "Hierro", "liga_Bronce": "Bronce", "liga_Plata": "Plata", "liga_Oro": "Oro",
        "liga_Platino": "Platino", "liga_Esmeralda": "Esmeralda", "liga_Diamante": "Diamante",
        "liga_Master": "Master", "liga_Grandmaster": "Grandmaster",
        "txt_amedida": "A MEDIDA", "btn_consultar_wsp": "CONSULTAR POR WSP",
        
        "txt_promo_1": "🔥 PROMO: 10% OFF en 1 Liga Completa",
        "txt_promo_2": "🔥 PROMO: 15% OFF en 2+ Ligas Completas",
        "msg_descuento_1": "¡{desc}% OFF APLICADO (1 LIGA COMPLETA)!",
        "msg_descuento_2": "¡{desc}% OFF APLICADO (2+ LIGAS COMPLETAS)!",
        
        "tit_servicios": "NUESTROS SERVICIOS",
        "btn_consultar": "CONSULTAR",
        
        "srv_1_tit": "PLACEMENTS", 
        "srv_1_desc": "Asegurá el mejor comienzo de temporada. Jugamos tus 5 primeras partidas para garantizarte el elo más alto posible.",
        "srv_1_bullets": ["Winrate garantizado superior al 80%.", "Evitá el 'Elo Hell' desde el día 1.", "Disponible para todas las ligas.", "Privacidad absoluta de la cuenta."],
        "srv_1_wsp": "Hola!%20Vengo%20de%20la%20web,%20estoy%20interesado%20en%20el%20servicio%20de%20*Placements*.",

        "srv_2_tit": "FIX MMR (Limpieza)", 
        "srv_2_desc": "¿Ganás 15 LP y perdés 30? Tu MMR está roto. Jugamos hasta normalizar tus ganancias de puntos para que vuelvas a subir rápido.",
        "srv_2_bullets": ["Estabilización de ganancias de LP.", "Mejora del emparejamiento de la cuenta.", "Ideal para cuentas 'stuck' (atascadas).", "Resultados 100% garantizados."],
        "srv_2_wsp": "Hola!%20Vengo%20de%20la%20web,%20estoy%20interesado%20en%20el%20servicio%20de%20*Fix%20MMR*.",

        "srv_3_tit": "COACHING PERSONALIZADO", 
        "srv_3_desc": "Convertite en el carry de tus partidas. Sesiones individuales con jugadores High Elo para pulir tus errores.",
        "srv_3_bullets": ["Análisis de Replays (VOD Review).", "Optimización de Pool de campeones y builds.", "Guía de Wave Management y Macro.", "Atención 1 a 1 directa en Discord."],
        "srv_3_wsp": "Hola!%20Vengo%20de%20la%20web,%20estoy%20interesado%20en%20el%20servicio%20de%20*Coaching*.",

        "tit_garantia": "🛡️ GARANTÍA NATION",
        "gar_off_tit": "🔌 MODO OFFLINE", "gar_off_desc": "Jugamos en modo desconectado. Nadie sabrá que estás jugando.",
        "gar_prot_tit": "🔐 PROTECCIÓN DE CUENTA", "gar_prot_desc": "No tocamos tu RP, Esencia Azul ni Artesanía.",
        "gar_tox_tit": "🤐 CERO TOXICIDAD", "gar_tox_desc": "Chat restringido por protocolo. Cuidamos tu honor al 100%.",
        
        "chat_faq": "FAQ",
        "chat_desc": "¡Hola! Resolvé tus dudas rápido o escribinos al WhatsApp.",
        "faq_1_q": "¿Quién va a jugar en mi cuenta?",
        "faq_1_a": "Tu cuenta será asignada a un jugador verificado de nuestro equipo con elo Grandmaster o Challenger.",
        "faq_2_q": "¿Hay riesgo de baneo?",
        "faq_2_a": "Cero riesgo. Jugamos en Modo Offline (nadie te ve conectado) y usamos VPN dedicada para proteger tu cuenta.",
        "faq_3_q": "¿Usan algún tipo de hack o script?",
        "faq_3_a": "Absolutamente no. Todos nuestros boosters juegan 100% de forma manual. Cero tolerancia a programas de terceros.",
        "faq_4_q": "¿Cuánto tiempo tardan?",
        "faq_4_a": "Promediamos 1 división por día. El tiempo exacto depende de tu MMR y la liga a la que quieras llegar.",
        "faq_5_q": "¿Puedo usar mi cuenta?",
        "faq_5_a": "¡Sí! Nos coordinamos por WhatsApp para no entrar al mismo tiempo. Podés jugar normales sin problema.",
        "faq_6_q": "¿Qué pasa si el booster pierde partidas?",
        "faq_6_a": "No te preocupes, vos pagás por el resultado final (la división deseada). Si el booster pierde, él mismo se encarga de recuperar los puntos sin ningún costo extra para vos.",
        "faq_7_q": "¿Qué pasa si no pueden llegar a la liga que pagué?",
        "faq_7_a": "Si por algún motivo extremo no podemos completar el pedido, te devolvemos el dinero proporcional a las divisiones que faltaron subir.",
        "chat_btn": "Hablar por WhatsApp"
    },
    "en": {
        "hero_title": "Play in the rank you truly deserve",
        "hero_subtitle": "Dodge the trolls and AFKs. Hire a professional and secure your rank without stress or headaches.",
        "titulo": "Rank up today. Calculate your budget.",
        "calc_titulo": "CALCULATE YOUR BOOST", "lbl_actual": "Current Rank", "lbl_deseada": "Desired Rank",
        "lbl_extras": "Extra Options", "check_rol": "Specific Role (+30%)", "check_champ": "Specific Champ (+50%)",
        "check_flash": "Flash on D", "check_express": "Express Delivery (+20%)", "check_duoboost": "DuoBoost",
        "tt_rol": "Choose exactly which lane the booster will play.",
        "tt_champ": "The booster will only play with the champions you request.",
        "tt_flash": "We set the Flash key to match your preference.",
        "tt_express": "Your order jumps to the front of the queue. Immediate assignment.",
        "tt_duoboost": "Play on your own account in duo with one of our boosters.",
        "btn_cotizar": "QUOTE NOW",
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
        "gar_tox_tit": "🤐 ZERO TOXICITY", "gar_tox_desc": "Chat restricted by protocol. 100% honor protection.",
        
        "chat_faq": "FAQ",
        "chat_desc": "Hello! Solve your doubts quickly or message us on WhatsApp.",
        "faq_1_q": "Who will play on my account?",
        "faq_1_a": "Your account will be assigned to a verified player from our team with Grandmaster or Challenger elo.",
        "faq_2_q": "Is there any ban risk?",
        "faq_2_a": "Zero risk. We play in Offline Mode (no one sees you online) and use a dedicated VPN to protect your account.",
        "faq_3_q": "Do you use any hacks or scripts?",
        "faq_3_a": "Absolutely not. All our boosters play 100% manually. Zero tolerance for third-party programs.",
        "faq_4_q": "How long does it take?",
        "faq_4_a": "We average 1 division per day. The exact time depends on your MMR and your desired rank.",
        "faq_5_q": "Can I use my account?",
        "faq_5_a": "Yes! We coordinate via WhatsApp to avoid logging in at the same time. You can play normal games without any issues.",
        "faq_6_q": "What happens if the booster loses games?",
        "faq_6_a": "Don't worry, you pay for the final result (the desired division). If the booster loses, they will recover the points at no extra cost to you.",
        "faq_7_q": "What if you can't reach the rank I paid for?",
        "faq_7_a": "It's very rare, but if for some extreme reason we can't complete the order, we will refund the money proportional to the uncompleted divisions.",
        "chat_btn": "Chat on WhatsApp"
    },
    "pt": {
        "hero_title": "Jogue na liga que você realmente merece",
        "hero_subtitle": "Evite os trolls e AFKs. Contrate um profissional e garanta seu elo sem estresse ou dores de cabeça.",
        "titulo": "Suba de divisão hoje mesmo. Calcule seu orçamento.",
        "calc_titulo": "CALCULE SEU BOOST", "lbl_actual": "Liga Atual", "lbl_deseada": "Liga Desejada",
        "lbl_extras": "Opções Extras", "check_rol": "Rota Específica (+30%)", "check_champ": "Campeão Específico (+50%)",
        "check_flash": "Flash no D", "check_express": "Entrega Express (+20%)", "check_duoboost": "DuoBoost",
        "tt_rol": "Escolha exatamente qual rota o booster vai jogar.",
        "tt_champ": "O booster jogará apenas com os campeões que você pedir.",
        "tt_flash": "Ajustamos a tecla do Flash para combinar com o seu costume.",
        "tt_express": "Seu pedido vai para o topo da fila. Atribuição imediata.",
        "tt_duoboost": "Jogue em sua própria conta em duo com um de nossos boosters.",
        "btn_cotizar": "ORÇAR AGORA",
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
        "gar_tox_tit": "🤐 ZERO TOXICIDADE", "gar_tox_desc": "Chat restrito por protocolo. Cuidamos do seu nivel de honra.",
        
        "chat_faq": "FAQ",
        "chat_desc": "Olá! Tire suas dúvidas rapidamente ou nos chame no WhatsApp.",
        "faq_1_q": "Quem vai jogar na minha conta?",
        "faq_1_a": "Sua conta será atribuída a um jogador verificado da nossa equipe com elo Grandmaster ou Challenger.",
        "faq_2_q": "Existe risco de banimento?",
        "faq_2_a": "Zero risco. Jogamos em Modo Offline (ninguém te vê online) e usamos uma VPN dedicada para proteger sua conta.",
        "faq_3_q": "Vocês usam algum tipo de hack ou script?",
        "faq_3_a": "Absolutamente não. Todos os nossos boosters jogam 100% manualmente. Tolerância zero para programas de terceiros.",
        "faq_4_q": "Quanto tempo demora?",
        "faq_4_a": "A média é de 1 divisão por dia. O tempo exato depende do seu MMR e do elo que você deseja alcançar.",
        "faq_5_q": "Posso usar minha conta?",
        "faq_5_a": "Sim! Coordenamos pelo WhatsApp para não entrarmos ao mesmo tempo. Você pode jogar partidas normais sem problemas.",
        "faq_6_q": "O que acontece se o booster perder partidas?",
        "faq_6_a": "Não se preocupe, você paga pelo resultado final (a divisão desejada). Se o booster perder, ele mesmo recupera os pontos sem custo extra.",
        "faq_7_q": "O que acontece se não conseguirem chegar à liga que paguei?",
        "faq_7_a": "É muito raro, mas se por algum motivo extremo não conseguirmos completar o pedido, devolveremos o dinheiro proporcional às divisões não alcançadas.",
        "chat_btn": "Falar no WhatsApp"
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
        "extraRol": False, "extraChamp": False, "extraFlash": False, "extraExpress": False, "extraDuoboost": False,
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
        extra_express = request.form.get("extraExpress") == "on"
        extra_duoboost = request.form.get("extraDuoboost") == "on"

        # Seguridad Backend: Si DuoBoost está activo, forzamos a apagar el resto de extras
        if extra_duoboost:
            extra_rol = False
            extra_champ = False
            extra_flash = False
            extra_express = False

        # Mantener los valores elegidos en pantalla
        context.update({
            "selLigaActual": liga_actual, "selDivActual": div_actual,
            "selLigaDeseada": liga_deseada, "selDivDeseada": div_deseada,
            "extraRol": extra_rol, "extraChamp": extra_champ, 
            "extraFlash": extra_flash, "extraExpress": extra_express, "extraDuoboost": extra_duoboost,
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
                    
                    div_diff = end - start

                    # --- LÓGICA DE PRECIOS ACTUALIZADA ---
                    precios_normales = PRECIOS_USD if currency == "USD" else PRECIOS_ARS
                    precios_diamante = PRECIOS_DIAMANTE_USD if currency == "USD" else PRECIOS_DIAMANTE_ARS
                    
                    precio_base = 0
                    for i in range(start, end):
                        liga_del_salto = LIGAS[i // 4]
                        division_del_salto = i % 4 # 0=IV, 1=III, 2=II, 3=I
                        
                        if liga_del_salto == "Diamante":
                            # Si está en Diamante, usa los precios escalonados
                            precio_base += precios_diamante[division_del_salto]
                        else:
                            # Si es otra liga, usa el precio base de siempre
                            precio_base += precios_normales[liga_del_salto]

                    # --- LÓGICA DE DESCUENTOS POR LIGA COMPLETA ---
                    descuento_pct = 0
                    msg_key = ""
                    if div_diff >= 8:      # 2 ligas completas o más
                        descuento_pct = 15
                        msg_key = "msg_descuento_2"
                    elif div_diff >= 4:    # 1 liga completa
                        descuento_pct = 10
                        msg_key = "msg_descuento_1"
                    
                    if descuento_pct > 0:
                        precio_base = precio_base * (1 - (descuento_pct / 100.0))
                        msg_base = TEXTOS.get(lang, TEXTOS["es"]).get(msg_key, "¡{desc}% OFF!")
                        context["texto_descuento"] = msg_base.format(desc=descuento_pct)

                    # Aplicación de extras
                    precio_final = float(precio_base)
                    extras_texto = []

                    if extra_duoboost: precio_final += (precio_base * 0.50); extras_texto.append("DuoBoost")
                    if extra_rol: precio_final += (precio_base * 0.30); extras_texto.append("Rol")
                    if extra_champ: precio_final += (precio_base * 0.50); extras_texto.append("OTP Champ")
                    if extra_express: precio_final += (precio_base * 0.20); extras_texto.append("Express")
                    if extra_flash: extras_texto.append("Flash D")

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
    # Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)