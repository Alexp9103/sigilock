"""Genera la versión en inglés del sitio (/en/...) a partir de las páginas en español.
Uso: python tools/i18n.py   (correr cada vez que cambie una página en español)
Cada frase en español tiene su traducción aquí; si una frase cambia en el español,
el script avisa cuál no encontró para actualizar la traducción."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://sigilock.com"
PAGES = [("index.html", "/", "en/index.html", "/en/"),
         ("gta6-pc/index.html", "/gta6-pc/", "en/gta6-pc/index.html", "/en/gta6-pc/"),
         ("tienda/index.html", "/tienda/", "en/store/index.html", "/en/store/")]

LANG_CSS = ".links a.lang{display:inline-block!important;font-weight:600;text-decoration:none;border-bottom:3px solid var(--lime)}@media(max-width:520px){nav{gap:12px}.links{gap:12px}.links .btn-o{padding:10px 12px;font-size:14px;white-space:nowrap}nav .logo{font-size:21px}}"

COMMON = [
    ('<html lang="es">', '<html lang="en">'),
    ('<span class="tag">Desconfía primero. Verifica siempre.</span>', '<span class="tag">Distrust first. Always verify.</span>'),
    ('href="/tienda/"', 'href="/en/store/"'), ('href="/gta6-pc/"', 'href="/en/gta6-pc/"'),
    ('class="logo" href="/"', 'class="logo" href="/en/"'), ('<a href="/">Inicio</a>', '<a href="/en/">Home</a>'),
    ('"img/', '"/img/'), ('"../img/', '"/img/'),
]

T = {
"index.html": [
    ("<title>Sigilock · IA y ciberseguridad para empresas</title>", "<title>Sigilock · AI and cybersecurity for businesses</title>"),
    ('content="Automatizo con IA el trabajo repetitivo de tu negocio y cierro las puertas por donde entran las estafas digitales. Empieza con un diagnóstico de una semana."',
     'content="I automate the repetitive work in your business with AI and close the doors that digital scams come through. It starts with a one-week assessment."'),
    ('content="Sigilock · IA y ciberseguridad para empresas"', 'content="Sigilock · AI and cybersecurity for businesses"'),
    ('content="Automatizaciones con IA y protección contra estafas para negocios. Empieza con un diagnóstico de una semana."',
     'content="AI automations and scam protection for businesses. It starts with a one-week assessment."'),
    ('<a href="#servicios">Servicios</a>\n', '<a href="#servicios">Services</a>\n'),
    ('<a href="#caso">Caso real</a>\n', '<a href="#caso">Case study</a>\n'),
    ('<a href="#proceso">Cómo trabajo</a>\n', '<a href="#proceso">How I work</a>\n'),
    ('<a href="#recursos">Guías gratis</a>', '<a href="#recursos">Free guides</a>'),
    ('>Pedir diagnóstico</a>', '>Book an assessment</a>'),
    ("<h1>Menos horas perdidas. Menos huecos por donde te estafen.</h1>", "<h1>Fewer wasted hours. Fewer gaps for scammers to get in.</h1>"),
    ("<p>Automatizo con IA el trabajo repetitivo de tu negocio y cierro las puertas por donde entran las estafas digitales. Todo empieza con un diagnóstico de una semana.</p>",
     "<p>I automate the repetitive work in your business with AI and close the doors that digital scams come through. It all starts with a one-week assessment.</p>"),
    (">Pedir un diagnóstico</a>", ">Book an assessment</a>"),
    ('aria-label="Herramientas que conecto"', 'aria-label="Tools I connect"'),
    ('<span class="tag">Servicios</span><p>Nada de venderte software que no necesitas. Primero entiendo tu negocio, después construyo.</p>',
     "<span class=\"tag\">Services</span><p>No selling you software you don't need. First I understand your business, then I build.</p>"),
    ("<h3><span>Diagnóstico</span><br><span>de IA · 7 días</span></h3>", "<h3><span>AI assessment</span><br><span>7 days</span></h3>"),
    ("<li>Conversación de 45 minutos sobre cómo trabaja tu equipo</li><li>Mapa de las tareas que se repiten y cuánto tiempo comen</li><li>Informe con las 3 automatizaciones que más horas te devuelven</li>",
     "<li>A 45-minute conversation about how your team works</li><li>A map of the repetitive tasks and how much time they eat</li><li>A report with the 3 automations that give you back the most hours</li>"),
    ("<h3><span>Asistentes</span><br><span>que responden</span></h3>", "<h3><span>Assistants</span><br><span>that answer</span></h3>"),
    ("<li>Contestan a tus clientes por WhatsApp o Instagram con tus datos</li><li>Agendan, cotizan y pasan a una persona cuando hace falta</li>",
     "<li>They answer your customers on WhatsApp or Instagram using your data</li><li>They book, quote, and hand off to a person when needed</li>"),
    ("<h3><span>Reportes</span><br><span>que se arman solos</span></h3>", "<h3><span>Reports</span><br><span>that build themselves</span></h3>"),
    ("<li>Paneles conectados a tus hojas de cálculo y tus ventas</li><li>El resumen de la semana te llega sin que nadie lo haga</li>",
     "<li>Dashboards connected to your spreadsheets and your sales</li><li>The weekly summary arrives without anyone making it</li>"),
    ("<h3><span>Flujos</span><br><span>conectados</span></h3>", "<h3><span>Connected</span><br><span>workflows</span></h3>"),
    ("<li>WhatsApp, correo y hojas de cálculo hablando entre sí</li><li>Cada pieza probada como si alguien quisiera romperla</li>",
     "<li>WhatsApp, email and spreadsheets talking to each other</li><li>Every piece tested as if someone were trying to break it</li>"),
    ("<h3><span>Seguridad</span><br><span>contra estafas</span></h3>", "<h3><span>Protection</span><br><span>against scams</span></h3>"),
    ("<li>Revisión de tus canales: dónde podrían copiarte o engañar a tus clientes</li><li>Alertas de las estafas nuevas que afectan a tu sector</li>",
     "<li>A review of your channels: where someone could copy you or trick your customers</li><li>Alerts about new scams hitting your industry</li>"),
    ("<h3><span>Acompañamiento</span><br><span>mensual</span></h3>", "<h3><span>Monthly</span><br><span>support</span></h3>"),
    ("<li>Ajustes cuando tu negocio cambia</li><li>Monitoreo de que todo siga funcionando</li>",
     "<li>Adjustments when your business changes</li><li>Monitoring that everything keeps working</li>"),
    ("<h2>¿Qué tarea te gustaría no volver a hacer?</h2>", "<h2>Which task would you like to never do again?</h2>"),
    ("<p>Cuéntamela por Instagram. Te respondo yo, en menos de 24 horas, y te digo si la IA puede encargarse.</p>",
     "<p>Tell me on Instagram. I reply myself, within 24 hours, and tell you whether AI can take care of it.</p>"),
    (">Escribirme</a>", ">Message me</a>"),
    ('<span class="tag">Caso real</span><p>Lo que construyo funciona con datos reales.</p>', '<span class="tag">Case study</span><p>What I build works with real data.</p>'),
    ("<p>señales de compra de res acertaron en la prueba con datos históricos 2022–2026.</p>", "<p>beef buying signals were right in the backtest on 2022–2026 historical data.</p>"),
    ("<p><b>Meat Signal.</b> Una plataforma que analiza precios de carne y le dice al comprador cuándo conviene comprar. La desarrollé de punta a punta para un cliente del sector.</p>",
     "<p><b>Meat Signal.</b> A platform that analyzes meat prices and tells the buyer when it's a good time to buy. I built it end to end for a client in the industry.</p>"),
    ("<p><b>Qué hice:</b> datos, modelo de señales y la aplicación web, para un cliente que compra res en volumen.</p><a href=\"https://meatsignal.com\">Ver meatsignal.com ↗</a><p class=\"note\">El proyecto y la marca son del cliente; yo lo desarrollé.</p>",
     "<p><b>What I did:</b> the data, the signal model and the web app, for a client who buys beef in volume.</p><a href=\"https://meatsignal.com\">See meatsignal.com ↗</a><p class=\"note\">The project and brand belong to the client; I built it.</p>"),
    ('<span class="tag">Cómo trabajo</span><p>Tres pasos, sin letra pequeña.</p>', '<span class="tag">How I work</span><p>Three steps, no fine print.</p>'),
    ("<b>01</b>Me escribes<i></i></summary><p>Por Instagram o correo. Me cuentas qué te quita tiempo o qué te preocupa. Te respondo yo, no un bot.</p>",
     "<b>01</b>You message me<i></i></summary><p>On Instagram or by email. Tell me what eats your time or what worries you. I reply myself, not a bot.</p>"),
    ("<b>02</b>Diagnóstico de una semana<i></i></summary><p>Hablamos 45 minutos sobre cómo trabaja tu equipo. En siete días te entrego el mapa de horas perdidas, los riesgos de tus canales y las tres automatizaciones que más tiempo te devuelven.</p>",
     "<b>02</b>One-week assessment<i></i></summary><p>We talk for 45 minutes about how your team works. Within seven days I deliver the map of wasted hours, the risks in your channels and the three automations that give you back the most time.</p>"),
    ("<b>03</b>Tú decides<i></i></summary><p>Si quieres, lo construimos juntos y después te acompaño cada mes. Si no, te quedas con el informe y lo usas como quieras.</p>",
     "<b>03</b>You decide<i></i></summary><p>If you want, we build it together and I support you every month after. If not, you keep the report and use it however you like.</p>"),
    ('<span class="tag">Sobre mí</span><p>La persona detrás de Sigilock.</p>', '<span class="tag">About me</span><p>The person behind Sigilock.</p>'),
    ('<p class="role">IA y ciberseguridad · República Dominicana</p>', '<p class="role">AI and cybersecurity · Dominican Republic</p>'),
    ("<p>Construyo aplicaciones, automatizaciones y agentes de IA para negocios.</p><p>Cada semana explico en <a href=\"https://www.instagram.com/sigilock/\">@sigilock</a> las noticias de IA y las estafas que te afectan. Esa es la parte pública de lo que hago para mis clientes.</p>",
     "<p>I build apps, automations and AI agents for businesses.</p><p>Every week on <a href=\"https://www.instagram.com/sigilock/\">@sigilock</a> I break down the AI news and the scams that affect you. That's the public side of what I do for my clients.</p>"),
    ('<span class="tag">Guías gratis</span><p>Lo que publico en reels, en pasos concretos que puedes seguir hoy.</p>',
     '<span class="tag">Free guides</span><p>What I post in reels, as concrete steps you can follow today.</p>'),
    ("<small>Para dueños de tienda</small><h3>Que no estafen a tus clientes con tu nombre</h3><span>Leer la guía ↗</span>",
     "<small>For store owners</small><h3>Stop scammers from using your name on your customers</h3><span>Read the guide ↗</span>"),
    ("<small>Para jugadores</small><h3>Cómo saber si un GTA 6 para PC es falso</h3><span>Leer la guía ↗</span>",
     "<small>For gamers</small><h3>How to tell if a GTA 6 for PC is fake</h3><span>Read the guide ↗</span>"),
    ("<h2>Cuéntame qué te quita tiempo.</h2>", "<h2>Tell me what eats your time.</h2>"),
    ("<p>Te digo en menos de 24 horas si la IA puede encargarse. Sin compromiso.</p>", "<p>Within 24 hours I'll tell you whether AI can take care of it. No strings attached.</p>"),
    (">Escribir por Instagram</a>", ">Message on Instagram</a>"),
    ('<div class="flinks"><a href="#servicios">Servicios</a><a href="#caso">Caso real</a><a href="#proceso">Cómo trabajo</a><a href="#recursos">Guías</a></div>',
     '<div class="flinks"><a href="#servicios">Services</a><a href="#caso">Case study</a><a href="#proceso">How I work</a><a href="#recursos">Guides</a></div>'),
],
"gta6-pc/index.html": [
    ("<title>Cómo saber si un GTA 6 para PC es falso · Sigilock</title>", "<title>How to tell if a GTA 6 for PC is fake · Sigilock</title>"),
    ('content="Los proyectos reales para correr GTA 6 en PC, las señales de una copia falsa y qué hacer si ya bajaste algo."',
     'content="The real projects trying to run GTA 6 on PC, the signs of a fake copy, and what to do if you already downloaded something."'),
    ('content="Cómo saber si un GTA 6 para PC es falso"', 'content="How to tell if a GTA 6 for PC is fake"'),
    ('content="Los proyectos reales, las señales de una copia falsa y qué hacer si ya bajaste algo."', 'content="The real projects, the signs of a fake copy, and what to do if you already downloaded something."'),
    ('<a href="#reales">Los reales</a><a href="#senales">Señales</a><a href="#ya-baje">Si ya bajaste algo</a>',
     '<a href="#reales">The real ones</a><a href="#senales">Red flags</a><a href="#ya-baje">If you downloaded something</a>'),
    (">Seguir el reporte</a>", ">Follow the report</a>"),
    (">Guía para jugadores · Actualizada 24 nov 2026</span>", ">Gamer guide · Updated Nov 24, 2026</span>"),
    (">Cómo saber si un GTA 6 para PC es falso.</h1>", ">How to tell if a GTA 6 for PC is fake.</h1>"),
    ("<p>El 23 de noviembre se filtró el ejecutable de Xbox y ya hay unos treinta proyectos intentando correrlo en PC. Ninguno es jugable todavía. <b>Cualquier cosa que te ofrezcan para bajar y jugar hoy es falsa.</b></p>",
     "<p>On November 23 the Xbox executable leaked, and about thirty projects are already trying to run it on PC. None of them is playable yet. <b>Anything offered to you to download and play today is fake.</b></p>"),
    ("<div><small>Jugable hoy</small><b>No</b></div><div><small>Más avanzado</small><b>4 fps</b></div><div><small>Para revisar</small><b>10 s</b></div>",
     "<div><small>Playable today</small><b>No</b></div><div><small>Furthest along</small><b>4 fps</b></div><div><small>To check</small><b>10 s</b></div>"),
    ('<span class="tag">Los reales</span><p>Ninguno tiene un instalador ni un juego para bajar. En sus páginas solo hay código para programadores, y piden que pongas tu propia copia del juego. Si alguien te manda un “GTA 6 PC listo” en nombre de cualquiera de estos proyectos, es mentira.</p>',
     '<span class="tag">The real ones</span><p>None of them has an installer or a game to download. Their pages only have code for developers, and they ask you to bring your own copy of the game. If someone sends you a “ready GTA 6 PC” in the name of any of these projects, it\'s a lie.</p>'),
    ("<th>Proyecto</th><th>Dónde va</th><th>Página oficial</th>", "<th>Project</th><th>Where it stands</th><th>Official page</th>"),
    ("<td>Dentro del juego, a unos 4 fps y sin luces</td><td>Privado. No tiene nada público.</td>", "<td>In-game, at about 4 fps and with no lighting</td><td>Private. Nothing public.</td>"),
    ("<td>Menú a 30 fps, según el propio proyecto</td>", "<td>Menu at 30 fps, according to the project itself</td>"),
    ("<td>Llega al mundo, se queda cargando</td>", "<td>Reaches the open world, gets stuck loading</td>"),
    ("<td>Primera imagen, inestable</td>", "<td>First image, unstable</td>"),
    ("<td>Primera pantalla, sobre todo en Linux</td>", "<td>First screen, mainly on Linux</td>"),
    ('<p class="src">Fuente: el tablero de <a href="https://portwatch-vi.xyz/">PortWatch VI</a>, que sigue todos los proyectos. Rockstar no ha anunciado versión de PC y no tiene relación con ninguno de ellos.</p>',
     '<p class="src">Source: the <a href="https://portwatch-vi.xyz/">PortWatch VI</a> tracker, which follows every project. Rockstar has not announced a PC version and has no connection to any of them.</p>'),
    ('<span class="tag">Señales de un falso</span><p>Con una sola de estas, ciérralo.</p>', '<span class="tag">Signs of a fake</span><p>If you see even one of these, close it.</p>'),
    ("<b>Hay un .exe o un “instalador” para bajar.</b>Los proyectos reales no tienen eso.", "<b>There's an .exe or an “installer” to download.</b>The real projects don't have that."),
    ("<b>Te piden dinero, cripto o “donación”.</b>Ya hay gente usando el nombre de los proyectos para vender monedas.", "<b>They ask for money, crypto or a “donation”.</b>People are already using the projects' names to sell coins."),
    ("<b>Te mandan a Telegram o a un link acortado.</b>El original está en GitHub.", "<b>They send you to Telegram or a shortened link.</b>The originals are on GitHub."),
    ("<b>El nombre es casi igual al real.</b>Una letra cambiada, o “oficial”, “full” o “crack” añadido.", "<b>The name is almost the same as the real one.</b>One letter changed, or “official”, “full” or “crack” added."),
    ("<b>Miles de estrellas, cero cambios.</b>Cuenta nueva sin cambios reales en el código: las estrellas se compran.", "<b>Thousands of stars, zero changes.</b>A new account with no real code changes: stars can be bought."),
    ("<b>Te pide apagar el antivirus.</b>O “ejecutar como administrador” para funcionar.", "<b>It asks you to turn off your antivirus.</b>Or to “run as administrator” to work."),
    ('<span class="tag">Si ya bajaste algo</span><p>Qué hacer ahora mismo, en este orden.</p>', '<span class="tag">If you downloaded something</span><p>What to do right now, in this order.</p>'),
    ("<b>01</b>No lo abras otra vez<i></i></summary><p>Si ya lo abriste, desconecta la PC de internet.</p>", "<b>01</b>Don't open it again<i></i></summary><p>If you already opened it, disconnect the PC from the internet.</p>"),
    ('<b>02</b>Revísalo en VirusTotal<i></i></summary><p>Súbelo a <a href="https://www.virustotal.com/">virustotal.com</a>. Si una sola alarma salta, bórralo y vacía la papelera.</p>',
     '<b>02</b>Check it on VirusTotal<i></i></summary><p>Upload it to <a href="https://www.virustotal.com/">virustotal.com</a>. If even one engine flags it, delete it and empty the Recycle Bin.</p>'),
    ("<b>03</b>Escanea con Windows<i></i></summary><p>Seguridad de Windows, Protección antivirus, Opciones de examen, “Examen de Microsoft Defender sin conexión”.</p>",
     "<b>03</b>Scan with Windows<i></i></summary><p>Windows Security, Virus &amp; threat protection, Scan options, “Microsoft Defender Offline scan”.</p>"),
    ("<b>04</b>Cambia tus contraseñas<i></i></summary><p>Desde otro dispositivo, no desde esa PC: correo, Steam, Rockstar, Discord y banco.</p>",
     "<b>04</b>Change your passwords<i></i></summary><p>From another device, not that PC: email, Steam, Rockstar, Discord and your bank.</p>"),
    ("<b>05</b>Cierra sesiones abiertas<i></i></summary><p>En cada cuenta (en Google: Seguridad, Tus dispositivos) y activa la verificación en dos pasos.</p>",
     "<b>05</b>Sign out of open sessions<i></i></summary><p>On every account (in Google: Security, Your devices) and turn on two-step verification.</p>"),
    ("<b>Si quieres probar algo sí o sí:</b> ábrelo dentro del Sandbox de Windows (Windows 10/11 Pro, se activa en “Características de Windows”). Todo lo que pase ahí se borra al cerrarlo.",
     "<b>If you absolutely want to try something:</b> open it inside Windows Sandbox (Windows 10/11 Pro, turn it on under “Windows Features”). Everything that happens there is wiped when you close it."),
    ("<h2>Te aviso el día que sea jugable.</h2>", "<h2>I'll let you know the day it's playable.</h2>"),
    ("<p>Sigo la carrera todos los días y subo el reporte en mis historias y reels. Esta página se actualiza con cada cambio.</p>",
     "<p>I follow the race every day and post the report in my stories and reels. This page is updated with every change.</p>"),
    ('>Seguir a @sigilock</a><span>Nunca te voy a mandar un link para bajar GTA 6.</span>', ">Follow @sigilock</a><span>I will never send you a link to download GTA 6.</span>"),
    ('<a href="/en/store/">Guía para tiendas</a>', '<a href="/en/store/">Store owner guide</a>'),
],
"tienda/index.html": [
    ("<title>Que no estafen a tus clientes con tu nombre · Sigilock</title>", "<title>Stop scammers from using your name on your customers · Sigilock</title>"),
    ('content="Boletín de seguridad para dueños de tienda: cómo avisar a tus clientes de los links falsos que usan tu marca este Black Friday. Plantillas listas para copiar."',
     'content="Security bulletin for store owners: how to warn your customers about fake links using your brand this Black Friday. Ready-to-copy templates."'),
    ('content="Que no estafen a tus clientes con tu nombre"', 'content="Stop scammers from using your name on your customers"'),
    ('content="Boletín de seguridad para dueños de tienda. Cuatro pasos, veinte minutos."', 'content="Security bulletin for store owners. Four steps, twenty minutes."'),
    ('<a href="#avisa">Avisa</a><a href="#verifica">Verifica</a><a href="#reporta">Reporta</a><a href="#clientes">Tus clientes</a>',
     '<a href="#avisa">Warn</a><a href="#verifica">Verify</a><a href="#reporta">Report</a><a href="#clientes">Your customers</a>'),
    (">Pedir revisión</a>", ">Request a review</a>"),
    (">Guía para dueños de tienda · Black Friday 2026</span>", ">Store owner guide · Black Friday 2026</span>"),
    (">Que no estafen a tus clientes con tu nombre.</h1>", ">Stop scammers from using your name on your customers.</h1>"),
    ("<p>Esta semana circulan por WhatsApp links falsos que copian tiendas reales: mismo logo, mismas fotos, precios imposibles. Tu cliente paga, no le llega nada, y <b>el reclamo te llega a ti.</b></p>",
     "<p>This week, fake links copying real stores are spreading on WhatsApp: same logo, same photos, impossible prices. Your customer pays, nothing arrives, and <b>the complaint lands on you.</b></p>"),
    ("<div><small>Pasos</small><b>4</b></div><div><small>Tiempo</small><b>20 min</b></div><div><small>Costo</small><b>0</b></div>",
     "<div><small>Steps</small><b>4</b></div><div><small>Time</small><b>20 min</b></div><div><small>Cost</small><b>0</b></div>"),
    ('<span class="when">Hoy</span>', '<span class="when">Today</span>'),
    ("<h2>Avisa antes de que les llegue el link falso.</h2>", "<h2>Warn them before the fake link reaches them.</h2>"),
    ("<p class=\"lead\">No puedes evitar que copien tu marca. Sí puedes lograr que tus clientes reconozcan la copia antes de pagar. Copia el mensaje, cambia lo resaltado y envíalo.</p>",
     "<p class=\"lead\">You can't stop people from copying your brand. You can make sure your customers recognize the copy before they pay. Copy the message, change the highlighted parts and send it.</p>"),
    ("<span>Lista de difusión · WhatsApp</span>", "<span>Broadcast list · WhatsApp</span>"),
    ("""Hola. Esta semana están circulando links falsos que usan el nombre de <var>[tu tienda]</var> con precios que no son reales.

Nuestros únicos canales oficiales son:
Web: <var>[tusitio.com]</var>
WhatsApp: <var>[este número]</var>
Instagram: <var>[@tuinstagram]</var>

Nunca te vamos a pedir pago por transferencia a cuentas personales ni con tarjetas de regalo. Si te llega una oferta demasiado buena, escríbenos aquí antes de pagar y te confirmamos en minutos.""",
     """Hi. This week fake links are going around using the name <var>[your store]</var> with prices that aren't real.

Our only official channels are:
Website: <var>[yoursite.com]</var>
WhatsApp: <var>[this number]</var>
Instagram: <var>[@yourinstagram]</var>

We will never ask you to pay by transfer to a personal account or with gift cards. If you get a deal that looks too good, message us here before paying and we'll confirm within minutes."""),
    ("<span>Historia de Instagram · 3 pantallas</span>", "<span>Instagram story · 3 screens</span>"),
    ("<b>Hay links falsos usando nuestro nombre.</b><span>Aviso</span>", "<b>There are fake links using our name.</b><span>Warning</span>"),
    ("<b>Solo vendemos en nuestra web, este WhatsApp y esta cuenta.</b><span>Canales oficiales</span>", "<b>We only sell on our website, this WhatsApp and this account.</b><span>Official channels</span>"),
    ("<b>¿Te llegó una oferta rara? Mándanos captura.</b><span>Te confirmamos en minutos</span>", "<b>Got a strange offer? Send us a screenshot.</b><span>We'll confirm within minutes</span>"),
    ("Guárdala en una historia destacada llamada “Oficial”.", "Save it to a story highlight called “Official”."),
    ("<span>Correo o banner de tu web</span>", "<span>Email or website banner</span>"),
    ("Este Black Friday solo vendemos en <var>[tusitio.com]</var>. Si ves ofertas nuestras en otro link, no pagues y escríbenos.",
     "This Black Friday we only sell on <var>[yoursite.com]</var>. If you see our deals on any other link, don't pay and message us."),
    ('<span class="when">Esta semana</span>', '<span class="when">This week</span>'),
    ("<h2>Que tu cliente pueda verificarte en diez segundos.</h2>", "<h2>Let your customer verify you in ten seconds.</h2>"),
    ("<li><span><b>Un solo link oficial</b>, el mismo en la bio de Instagram, Facebook y WhatsApp.</span></li>",
     "<li><span><b>One single official link</b>, the same in your Instagram, Facebook and WhatsApp bio.</span></li>"),
    ("<li><span><b>WhatsApp Business completo:</b> nombre, logo, dirección, web y horario.</span></li>",
     "<li><span><b>A complete WhatsApp Business profile:</b> name, logo, address, website and hours.</span></li>"),
    ("<li><span><b>Métodos de pago por escrito</b> en tu web o catálogo: “Solo aceptamos pagos en…”.</span></li>",
     "<li><span><b>Payment methods in writing</b> on your website or catalog: “We only accept payments via…”.</span></li>"),
    ("<li><span><b>Mismo nombre y misma foto</b> en todas las redes. Las copias cambian una letra o agregan “ofertas”, “oficial” u “outlet”.</span></li>",
     "<li><span><b>Same name and same photo</b> on every network. Copies change one letter or add “deals”, “official” or “outlet”.</span></li>"),
    ('<span class="when">Si aparece una copia</span>', '<span class="when">If a copy shows up</span>'),
    ("<h2>Repórtala y vuelve a avisar.</h2>", "<h2>Report it and warn again.</h2>"),
    ("<li><span><b>Guarda pruebas:</b> captura de la página, el link completo y el mensaje donde llegó, con la fecha.</span></li>",
     "<li><span><b>Keep evidence:</b> a screenshot of the page, the full link and the message it arrived in, with the date.</span></li>"),
    ("<li><span><b>Google:</b> busca “Google Safe Browsing reportar phishing” y pega el link, para que Chrome muestre la advertencia roja.</span></li>",
     "<li><span><b>Google:</b> search “Google Safe Browsing report phishing” and paste the link, so Chrome shows the red warning.</span></li>"),
    ("<li><span><b>Instagram y Facebook:</b> en el perfil o anuncio, menú de tres puntos, Reportar, “Se hace pasar por otra persona o empresa”.</span></li>",
     "<li><span><b>Instagram and Facebook:</b> on the profile or ad, three-dot menu, Report, “Pretending to be someone else or a business”.</span></li>"),
    ("<li><span><b>WhatsApp:</b> abre el chat, toca el nombre del contacto, Reportar.</span></li>", "<li><span><b>WhatsApp:</b> open the chat, tap the contact's name, Report.</span></li>"),
    ("<li><span><b>Avisa otra vez</b> a tus clientes con una captura de la copia tachada, para que la reconozcan.</span></li>",
     "<li><span><b>Warn your customers again</b> with a crossed-out screenshot of the copy, so they recognize it.</span></li>"),
    ("<b>Si alguien ya pagó:</b> que llame a su banco ese mismo día para disputar el cargo y haga la denuncia ante la unidad de delitos informáticos de su país.",
     "<b>If someone already paid:</b> they should call their bank that same day to dispute the charge and file a report with their country's cybercrime unit."),
    ('<span class="when">Para tus clientes</span>', '<span class="when">For your customers</span>'),
    ("<h2>Tres cosas que revisar antes de pagar.</h2>", "<h2>Three things to check before paying.</h2>"),
    ("<th>Revisa</th><th>Tienda real</th><th>Copia</th>", "<th>Check</th><th>Real store</th><th>Copy</th>"),
    ("<td>El link</td><td><code>tutienda.com</code></td><td class=\"no\"><code>tutienda-ofertas.shop</code></td>", "<td>The link</td><td><code>yourstore.com</code></td><td class=\"no\"><code>yourstore-deals.shop</code></td>"),
    ("<td>El precio</td><td>Descuento creíble</td><td class=\"no\">Demasiado bueno para ser verdad</td>", "<td>The price</td><td>A believable discount</td><td class=\"no\">Too good to be true</td>"),
    ("<td>El pago</td><td>Tarjeta en la web o en tienda</td><td class=\"no\">Transferencia personal o tarjeta de regalo</td>", "<td>The payment</td><td>Card on the website or in store</td><td class=\"no\">Personal transfer or gift card</td>"),
    ("<span>Mensaje para tus clientes</span>", "<span>Message for your customers</span>"),
    ("""Antes de pagar una oferta de Black Friday, revisa tres cosas:
1. El link: si no es exactamente <var>[tusitio.com]</var>, no somos nosotros.
2. El precio: si es demasiado bueno, es mentira.
3. El pago: transferencia a una cuenta personal o tarjeta de regalo, no pagues.
¿Dudas? Escríbenos aquí antes de pagar.""",
     """Before paying for a Black Friday deal, check three things:
1. The link: if it isn't exactly <var>[yoursite.com]</var>, it isn't us.
2. The price: if it's too good, it's a lie.
3. The payment: a transfer to a personal account or a gift card, don't pay.
Questions? Message us here before paying."""),
    ("<h2>¿Qué tan fácil es copiar tu tienda hoy?</h2>", "<h2>How easy is it to copy your store today?</h2>"),
    ("<p>En una conversación corta reviso tus canales, te digo dónde estás expuesto y qué automatizar para que tu equipo responda estas dudas sin perder horas.</p>",
     "<p>In a short conversation I review your channels, tell you where you're exposed, and what to automate so your team can answer these questions without losing hours.</p>"),
    (">Escribir “REVISIÓN” por Instagram</a><span>Te responde Juan, no un bot.</span>", ">Message “REVIEW” on Instagram</a><span>Juan replies, not a bot.</span>"),
    ('<a href="/en/gta6-pc/">Guía GTA 6 PC</a>', '<a href="/en/gta6-pc/">GTA 6 PC guide</a>'),
    ("label.textContent='Copiado';", "label.textContent='Copied';"), ("label.textContent='Copiar'}", "label.textContent='Copy'}"),
    ('data-t="t1">Copiar</button>', 'data-t="t1">Copy</button>'), ('data-t="t2">Copiar</button>', 'data-t="t2">Copy</button>'), ('data-t="t3">Copiar</button>', 'data-t="t3">Copy</button>'),
],
}


def head_links(es, en):
    return (f'<link rel="alternate" hreflang="es" href="{SITE}{es}">\n<link rel="alternate" hreflang="en" href="{SITE}{en}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITE}{es}">\n')


def add_switch(html, href, label, title):
    html = re.sub(r'\n<link rel="alternate" hreflang[^\n]*', "", html)
    html = re.sub(r'<a class="lang"[^>]*>[^<]*</a>\s*', "", html)
    html = html.replace('<a class="btn-o"', f'<a class="lang" href="{href}" hreflang="{label.lower()}" title="{title}">{label}</a>\n      <a class="btn-o"', 1)
    html = re.sub(r"\n  \.links a\.lang\{[^\n]*", "", html)
    if LANG_CSS not in html:
        html = html.replace("</style>", f"  {LANG_CSS}\n</style>", 1)
    return html


missing = []
for src, es_url, dst, en_url in PAGES:
    sp = ROOT / src
    es = sp.read_text(encoding="utf-8")
    es = add_switch(es, en_url, "EN", "Read in English")
    es = es.replace("</style>", "</style>", 1)
    es = re.sub(r'(<link rel="icon")', head_links(es_url, en_url).rstrip("\n").replace("\n", "\n") + "\n" + r"\1", es, count=1) if 'hreflang="x-default"' not in es else es
    sp.write_text(es, encoding="utf-8")

    en = es
    for a, b in COMMON:
        en = en.replace(a, b)
    for a, b in T[src]:
        if a not in en:
            missing.append((src, a[:80]))
        en = en.replace(a, b)
    en = en.replace(f'<a class="lang" href="{en_url}" hreflang="en" title="Read in English">EN</a>', f'<a class="lang" href="{es_url}" hreflang="es" title="Leer en español">ES</a>')
    en = en.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/en/">')
    dp = ROOT / dst
    dp.parent.mkdir(parents=True, exist_ok=True)
    dp.write_text(en, encoding="utf-8")

if missing:
    print("SIN TRADUCIR (el español cambió):")
    for s, a in missing: print(" ", s, "|", a)
    sys.exit(1)
print("ok:", ", ".join(d for _, _, d, _ in PAGES))
