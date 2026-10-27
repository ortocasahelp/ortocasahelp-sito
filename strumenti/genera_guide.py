"""Genera le pagine-guida statiche di OrtoCasa Help e la sitemap.

Uso:  python3 strumenti/genera_guide.py
Modifica i testi in GUIDE qui sotto e rilancia: rigenera guide/<slug>/index.html e sitemap.xml.
"""
import datetime
import email.utils
import html
import json
import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://ortocasahelp.netlify.app"
AGGIORNATA = "2026-10-26"

GUIDE = [
    {
        "slug": "motozappa",
        "titolo": "Come scegliere la motozappa per l'orto di casa",
        "titolo_breve": "Motozappa",
        "descrizione": "Elettrica, a batteria o a scoppio? Come scegliere la motozappa giusta per il tuo orto, cosa guardare nella scheda e gli errori da evitare.",
        "attacco": "Dipende da tre cose: quanta terra lavori, com'è il terreno e quanta fatica vuoi fare tu. Il resto viene dopo.",
        "foto": "photo-1679128719010-aaa99859ad97",
        "alt": "Motozappa ferma su una strada di campagna",
        "q": "motozappa",
        "agrieuro": "https://www.agrieuro.com/motozappe-c-22.html",
        "azione": "Vedi le motozappe",
        "in_breve": [
            "Orto piccolo con terra già lavorata: elettrica o a batteria.",
            "Orto medio e terreno normale: a scoppio, leggera o media.",
            "Terreno duro, prato da rompere o superfici grandi: pesante, con marce e retromarcia.",
        ],
        "sezioni": [
            ("Quale tipo ti serve", "voci", [
                ("Elettrica a filo", "Leggera e senza manutenzione del motore. Il cavo però limita: va bene per aiuole e orti vicino a casa."),
                ("A batteria", "Come l'elettrica, ma senza cavo. Controlla che l'autonomia basti per tutto l'orto, o prendi una seconda batteria."),
                ("A scoppio leggera", "Si sposta facilmente e si carica in auto. Ideale per rifinire e per terreni già lavorati."),
                ("A scoppio media o pesante", "Più peso e più potenza, con marce e retromarcia. Serve su terreni compatti e superfici grandi, ma è più faticosa da girare."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Larghezza di lavoro: più è larga, meno passate fai, ma tra le file strette diventa scomoda.",
                "Profondità di lavoro: per l'orto di casa non serve andare molto a fondo.",
                "Retromarcia: sulle pesanti è quasi indispensabile per uscire dagli angoli.",
                "Manico regolabile e ripiegabile: per la tua altezza e per il trasporto.",
                "Assistenza e ricambi: meglio una marca che ha un centro vicino a casa.",
            ]),
            ("Errori da evitare", "punti", [
                "Lavorare la terra bagnata: fai zolle, la compatti e te la porti dietro tutto l'anno.",
                "Prendere la più potente per sicurezza: in un orto piccolo è solo più pesante da manovrare.",
                "Passare troppe volte: sbricioli troppo la terra, e alla prima pioggia fa la crosta.",
            ]),
        ],
    },
    {
        "slug": "robot-tagliaerba",
        "titolo": "Come scegliere il robot tagliaerba",
        "titolo_breve": "Robot tagliaerba",
        "descrizione": "Con filo o senza filo, superficie, pendenza e passaggi stretti: come scegliere il robot tagliaerba giusto per il tuo prato.",
        "attacco": "Il robot giusto si sceglie guardando il prato, non la scheda: superficie, pendenza, ostacoli e passaggi stretti.",
        "foto": "photo-1741326757602-186060c5d5b5",
        "alt": "Robot tagliaerba al lavoro su un prato",
        "q": "robot tagliaerba",
        "agrieuro": "https://www.agrieuro.com/robot-tagliaerba-c-59.html",
        "azione": "Vedi i robot",
        "in_breve": [
            "Superficie massima dichiarata più grande del tuo prato, non uguale.",
            "Pendenza massima adatta al tuo terreno, se il prato non è in piano.",
            "Con filo perimetrale costa meno, senza filo si installa più in fretta.",
        ],
        "sezioni": [
            ("Con filo o senza filo", "voci", [
                ("Con filo perimetrale", "Un filo lungo il bordo del prato gli dice dove fermarsi. È affidabile ed economico, ma l'installazione richiede un pomeriggio."),
                ("Senza filo", "Si orienta con il segnale satellitare o con le telecamere, e le zone si disegnano dall'app. Sotto alberi fitti o vicino a muri alti può perdere precisione."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Superficie massima e ore di lavoro al giorno.",
                "Pendenza massima, in percentuale.",
                "Gestione di più zone e dei passaggi stretti tra una zona e l'altra.",
                "Altezza di taglio regolabile.",
                "Antifurto con PIN e allarme, e controllo dall'app.",
                "Rumore, se hai i vicini vicini.",
            ]),
            ("Errori da evitare", "punti", [
                "Prenderlo al limite della superficie: lavora tutto il giorno e si consuma prima.",
                "Farlo lavorare di notte: è il momento in cui girano ricci e piccoli animali.",
                "Non preparare il prato: buche, sassi e radici affioranti vanno sistemati prima.",
            ]),
        ],
        "nota": "Il robot taglia poco e spesso. L'erba tagliata resta sul prato, si decompone e torna al terreno: niente sacchi da svuotare.",
    },
    {
        "slug": "irrigazione-a-goccia",
        "titolo": "Irrigazione a goccia per l'orto: cosa serve e come montarla",
        "titolo_breve": "Irrigazione a goccia",
        "descrizione": "I pezzi che servono per l'irrigazione a goccia dell'orto, in che ordine montarli e gli errori che fanno intasare l'impianto.",
        "attacco": "Acqua alla radice, foglie asciutte, meno spreco. Si monta in un pomeriggio e dura anni.",
        "foto": "photo-1748432171507-c1d62fe2e859",
        "alt": "Aiuola con impianto di irrigazione a goccia",
        "q": "kit irrigazione a goccia",
        "agrieuro": "https://www.agrieuro.com/irrigazione-g-14.html",
        "azione": "Vedi l'irrigazione",
        "in_breve": [
            "Ala gocciolante lungo le file, gocciolatori singoli per vasi e piante isolate.",
            "Sempre filtro e riduttore di pressione subito dopo il rubinetto.",
            "Un programmatore, e l'orto si bagna anche quando non ci sei.",
        ],
        "sezioni": [
            ("I pezzi, nell'ordine dell'acqua", "sequenza", [
                ("Programmatore", "Al rubinetto: decide quando e per quanto bagnare."),
                ("Filtro", "Ferma sabbia e impurità che altrimenti intasano i gocciolatori."),
                ("Riduttore di pressione", "L'acqua di casa ha troppa pressione per i tubi della goccia."),
                ("Tubo di linea", "Porta l'acqua fino all'orto."),
                ("Ala gocciolante o gocciolatori", "L'ala lungo le file di ortaggi, i gocciolatori singoli per vasi e piante isolate."),
                ("Tappi di fine linea", "Chiudono ogni fila. Si aprono per sciacquare l'impianto."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Distanza tra i gocciolatori: più fitta per gli ortaggi in fila, più larga per le piante distanziate.",
                "Gocciolatori autocompensanti, se l'orto non è in piano o le file sono lunghe.",
                "Diametri e raccordi compatibili tra loro: meglio un kit o un'unica marca.",
            ]),
            ("Errori da evitare", "punti", [
                "Montare l'impianto senza filtro: i gocciolatori si intasano in poche settimane.",
                "Bagnare poco tutti i giorni: meglio meno volte e più a lungo, così le radici scendono in profondità.",
                "Lasciarlo pieno d'acqua d'inverno: svuotalo prima del gelo.",
            ]),
        ],
        "nota": "Copri l'ala gocciolante con la pacciamatura: l'acqua evapora meno e le erbacce crescono meno.",
    },
    {
        "slug": "decespugliatore",
        "titolo": "Come scegliere il decespugliatore per orto e giardino",
        "titolo_breve": "Decespugliatore",
        "descrizione": "A batteria, elettrico o a scoppio, con filo o con lama: come scegliere il decespugliatore giusto per bordi, fossi ed erba alta, e gli errori da evitare.",
        "attacco": "Prima della potenza, guarda cosa devi tagliare: i bordi del prato, l'erba alta del fosso o i rovi in fondo all'orto.",
        "foto": "photo-1768268004427-6fb88cbd1605",
        "alt": "Uomo che taglia l'erba con un decespugliatore",
        "q": "decespugliatore",
        "agrieuro": "https://www.agrieuro.com/decespugliatori-c-3.html",
        "azione": "Vedi i decespugliatori",
        "in_breve": [
            "Bordi e giardino piccolo: a batteria o elettrico, con testina a filo.",
            "Erba alta, fossi e superfici grandi: a scoppio, con impugnatura a manubrio.",
            "Rovi e steli legnosi: serve la lama, il filo non basta.",
        ],
        "sezioni": [
            ("Quale tipo ti serve", "voci", [
                ("Elettrico a filo", "Leggero, silenzioso, parte subito. Il cavo però limita: va bene per i bordi vicino a casa."),
                ("A batteria", "Niente cavo e niente miscela. Controlla che l'autonomia basti per tutto il giro, o prendi una seconda batteria. Se hai già attrezzi a batteria, resta sulla stessa marca."),
                ("A scoppio", "Il più adatto per erba alta, fossi e superfici grandi. Pesa di più, fa rumore e vuole manutenzione: filtro, candela, carburante fresco."),
                ("A zaino", "Il motore sta sulla schiena e le braccia si stancano meno. Utile se tagli per ore, su argini e scarpate."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Impugnatura: a manubrio per i lavori lunghi e l'erba alta, ad anello per i bordi e i punti stretti.",
                "Cosa c'è in dotazione: testina a filo per l'erba, lama per rovi e steli legnosi.",
                "Asta divisibile: si carica meglio in auto, e su alcuni modelli si montano altri accessori.",
                "Peso e imbracatura: provalo in mano, con la cinghia regolata alla tua altezza.",
                "A scoppio, due o quattro tempi: il quattro tempi non vuole la miscela, ma di solito pesa di più.",
                "Assistenza e ricambi vicino a casa: filo, testine e lame si consumano.",
            ]),
            ("Errori da evitare", "punti", [
                "Lavorare senza protezioni: visiera o occhiali, cuffie, guanti, pantaloni lunghi e scarpe chiuse. Il filo lancia sassi lontano.",
                "Tagliare con persone o animali vicino: allontana tutti prima di partire.",
                "Rasare il colletto di alberi e cespugli: il filo ferisce la corteccia e apre la porta alle malattie. Lì finisci a mano.",
                "Lasciare la miscela nel serbatoio per l'inverno: a fine stagione svuotalo o fai girare il motore finché si ferma.",
            ]),
        ],
        "nota": "L'erba tagliata non buttarla: falla appassire un giorno e stendila in strato sottile tra le file dell'orto. È pacciamatura gratis.",
    },
    {
        "slug": "biotrituratore",
        "titolo": "Come scegliere il biotrituratore per orto e giardino",
        "titolo_breve": "Biotrituratore",
        "descrizione": "A lame o a rullo, elettrico o a scoppio: come scegliere il biotrituratore per potature e foglie, cosa guardare nella scheda e gli errori da evitare.",
        "attacco": "Prima della potenza, guarda cosa devi triturare: i rametti verdi della siepe, le potature legnose del frutteto o le foglie e gli scarti dell'orto.",
        "foto": "photo-1726379781464-98ba39da2c0f",
        "alt": "Foglia rossa su un mucchio di legno triturato",
        "q": "biotrituratore",
        "agrieuro": "https://www.agrieuro.com/biotrituratori-c-42.html",
        "azione": "Vedi i biotrituratori",
        "in_breve": [
            "Rametti sottili, foglie e scarti verdi: elettrico a lame.",
            "Potature legnose di siepe e frutteto: elettrico a rullo, più lento ma più silenzioso.",
            "Tante potature, rami più grossi o lontano dalla presa: a scoppio.",
        ],
        "sezioni": [
            ("Quale tipo ti serve", "voci", [
                ("Elettrico a lame", "Le lame girano veloci e sminuzzano fine. Va bene per rametti, foglie e scarti verdi. Fa parecchio rumore e con i rami fibrosi tende a intasarsi."),
                ("Elettrico a rullo", "Un rullo dentato schiaccia e spezza il legno piano piano, e si tira dentro i rami da solo. È più silenzioso e regge meglio le potature legnose. Il trito esce più grosso."),
                ("A scoppio", "Niente cavo e più forza: serve per potature abbondanti e lavori lontano da casa. Pesa di più, fa rumore e vuole la manutenzione del motore."),
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Diametro massimo dei rami: sceglilo sui rami che poti di solito, non sul ramo grosso che capita una volta l'anno.",
                "Bocca di carico: larga per le frasche. Alcuni modelli hanno una seconda apertura per foglie e scarti morbidi.",
                "Contenitore di raccolta: chiuso e capiente, così il trito non lo raccogli da terra.",
                "Ruote e peso: lo sposterai spesso tra la catasta delle potature e l'orto.",
                "Inversione del rullo, sui modelli a rullo: sblocca il ramo quando si inceppa.",
                "Assistenza e ricambi vicino a casa: lame e rulli si consumano.",
            ]),
            ("Errori da evitare", "punti", [
                "Spingere i rami con le mani dentro la bocca: usa il pressino in dotazione. E sempre occhiali, guanti e cuffie.",
                "Lasciare seccare le potature per mesi: il legno secco è duro e consuma le lame. Tritura poco dopo la potatura.",
                "Far entrare sassi, terra o il filo di ferro delle legature: rovinano lame e rullo.",
                "Triturare piante malate e spargerle nell'orto: quelle vanno nel verde, non nella pacciamatura.",
                "Usare una prolunga lunga e sottile: il motore perde forza e si scalda. Serve un cavo adatto alla potenza.",
            ]),
        ],
        "nota": "Il trito di potature è ottima pacciamatura per vialetti, siepi e piante perenni. Nell'orto non interrarlo fresco, perché toglie azoto agli ortaggi: mettilo nel compost o lascialo in superficie.",
    },
    {
        "slug": "serra-da-giardino",
        "titolo": "Come scegliere la serra da giardino per l'orto di casa",
        "titolo_breve": "Serra da giardino",
        "descrizione": "Mini serra, tunnel o serra in policarbonato: come scegliere la serra da giardino per l'orto, dove metterla, cosa guardare e gli errori da evitare.",
        "attacco": "La serra serve a partire prima in primavera e a chiudere più tardi in autunno. Prima delle misure, decidi cosa ci vuoi fare: far nascere le piantine, anticipare gli ortaggi o coltivare anche d'inverno.",
        "foto": "photo-1516253593875-bd7ba052fbc5",
        "alt": "Annaffiatoio verde dentro una serra",
        "q": "serra da giardino",
        "azione": "Vedi le serre",
        "in_breve": [
            "Semine e piantine di primavera: mini serra a scaffale o serra addossata al muro.",
            "Ortaggi in terra da anticipare: tunnel con telo, semplice da montare sopra le aiuole.",
            "Uso tutto l'anno in un posto fisso: struttura in alluminio e pannelli in policarbonato.",
        ],
        "sezioni": [
            ("Quale tipo ti serve", "voci", [
                ("Mini serra a scaffale", "Qualche ripiano coperto da una fodera in plastica, da mettere contro un muro al sole. Va bene per semenzai e piantine. È leggera: col vento si ribalta, quindi va fissata."),
                ("Serra addossata al muro", "Si appoggia alla parete di casa, che di notte restituisce un po' del calore preso di giorno. È comoda perché sta vicino alla porta e al rubinetto."),
                ("Tunnel con telo", "Archi in metallo coperti da un telo in plastica, piantati direttamente sopra le aiuole. Copre tanta terra con poca spesa, ma il telo invecchia al sole e dopo qualche stagione va cambiato."),
                ("Serra in policarbonato", "Telaio in alluminio e pannelli rigidi. Isola meglio del telo, regge meglio vento e grandine e dura di più. Vuole una base in piano e ancorata bene."),
            ]),
            ("Dove metterla", "punti", [
                "In pieno sole, con il lato lungo verso sud se puoi: d'inverno la luce è poca e non va sprecata.",
                "Lontana dagli alberi: d'estate fanno ombra e in autunno riempiono il tetto di foglie.",
                "Riparata dal vento forte, ma non chiusa in un angolo dove l'aria non gira.",
                "Vicino al rubinetto: in serra si annaffia anche d'inverno, e la pioggia non arriva.",
                "Su terreno in piano che non tiene l'acqua: con nebbie e piogge d'autunno, il ristagno porta muffe.",
            ]),
            ("Cosa guardare nella scheda", "punti", [
                "Finestre sul tetto o sui lati e porta larga: da primavera, con il sole, dentro si cuoce se non arieggi.",
                "Tipo di copertura: il policarbonato alveolare isola più di quello compatto, e il telo deve essere trattato contro i raggi UV.",
                "Altezza alle pareti e al colmo: devi lavorarci in piedi, e pomodori e cetrioli crescono in alto.",
                "Base e ancoraggi: picchetti, tasselli o un telaio da fissare a terra. Una serra leggera senza ancoraggi vola via col primo temporale.",
                "Resistenza a neve e vento dichiarata, se la lasci montata tutto l'inverno.",
                "Ricambi: un pannello rotto o un telo strappato si sostituiscono, senza cambiare la serra.",
            ]),
            ("Errori da evitare", "punti", [
                "Tenerla chiusa nelle giornate di sole, anche d'inverno: la temperatura sale in fretta e le piantine si scottano. Apri al mattino e richiudi a metà pomeriggio.",
                "Pensare che dentro non geli: senza riscaldamento, nelle notti più fredde si va comunque sotto zero. Per le piante delicate tieni pronto un telo di tessuto non tessuto.",
                "Annaffiare la sera bagnando le foglie: con l'umidità della notte arrivano le muffe. Meglio al mattino, alla base delle piante.",
                "Mettere ogni anno gli stessi ortaggi nella stessa terra: in serra le malattie del terreno si accumulano. Ruota le colture e aggiungi compost.",
                "Lasciare la neve sul tetto: spazzala via, soprattutto dai teli e dai pannelli sottili.",
            ]),
        ],
        "nota": "D'estate, in pianura, la serra chiusa diventa un forno: apri tutto o stendi sopra una rete ombreggiante. Non è obbligatorio usarla in luglio e agosto: lasciala aperta, coltiva fuori e riprendila a settembre per insalate e radicchi.",
    },
    {
        "slug": "microgreens",
        "titolo": "Microgreens in casa: come coltivarli passo per passo",
        "titolo_breve": "Microgreens",
        "descrizione": "Microortaggi in casa in 7-14 giorni: quali semi usare, terriccio o fibra di cocco, vaschette, luce e annaffiatura. Passo per passo, con gli errori da evitare.",
        "attacco": "Bastano una vaschetta, un po' di substrato e una finestra luminosa: in una o due settimane tagli il primo raccolto.",
        "foto": "photo-1648128774225-b7cf04eb94c6",
        "alt": "Vaschette di microgreens verdi appena cresciuti",
        "q": "semi microgreens",
        "agrieuro": "",
        "dove_titolo": "Dove comprare semi, substrato e vaschette",
        "azione": "Vedi semi e kit",
        "in_breve": [
            "Per iniziare: ravanello, senape, rucola e crescione, i più facili e veloci.",
            "Usa semi non trattati, venduti per germogli o microgreens.",
            "Si raccolgono tra 7 e 14 giorni, quando le prime foglioline sono aperte.",
        ],
        "sezioni": [
            ("Quali semi scegliere", "voci", [
                ("Ravanello", "Germina in 1-2 giorni ed è pronto in 7-10. Sapore piccante, steli spesso rosati."),
                ("Senape, rucola e crescione", "Veloci e saporiti, ottimi per iniziare. Il seme è piccolo: non va coperto."),
                ("Broccolo e cavolo rosso", "Sapore delicato, pronti in circa 10-12 giorni."),
                ("Pisello e girasole", "Semi grossi: vanno messi a bagno 8-12 ore prima della semina. Danno germogli croccanti in 10-14 giorni."),
                ("Basilico e coriandolo", "Più lenti, due o tre settimane, ma molto profumati: da provare quando hai preso la mano."),
            ]),
            ("Cosa serve", "voci", [
                ("Semi", "Non conciati, cioè senza trattamenti: sulla confezione c'è scritto per germogli o per microgreens. I semi da orto normali spesso sono trattati e non vanno mangiati da germogli."),
                ("Substrato", "Terriccio fine da semina, fibra di cocco oppure tappetini di canapa o juta. Si usa una volta sola, poi va nel compost."),
                ("Vaschette", "Due vaschette una dentro l'altra: sopra quella con i fori, sotto quella piena che raccoglie l'acqua e serve ad annaffiare dal basso."),
                ("Acqua e luce", "Uno spruzzino per i primi giorni. Poi una finestra luminosa, oppure d'inverno una lampada LED per piante accesa 12-16 ore al giorno."),
            ]),
            ("Passo per passo", "sequenza", [
                ("Prepara il substrato", "Stendi 2-3 cm di terriccio, oppure un tappetino, livella e bagna bene."),
                ("Semina fitto", "Distribuisci i semi in modo uniforme, quasi a toccarsi. Premili appena; non coprirli, o al massimo con un velo di terriccio."),
                ("Buio e peso per 2-4 giorni", "Copri con un'altra vaschetta e un piccolo peso sopra: i semi germinano insieme e radicano bene."),
                ("Luce", "Quando i germogli sollevano il coperchio, scopri e metti alla luce."),
                ("Acqua dal basso", "Versa l'acqua nella vaschetta sotto, non sulle foglie. Il substrato deve restare umido, mai fradicio."),
                ("Raccolta", "Taglia con forbici pulite appena sopra il substrato quando le prime foglie sono aperte. Sciacqua e consuma subito, o tieni in frigo 3-5 giorni."),
            ]),
            ("Errori da evitare", "punti", [
                "Seminare troppo rado: i germogli crescono storti e sprechi spazio.",
                "Bagnare dall'alto tutti i giorni: foglie bagnate e poca aria fanno marcire.",
                "Scambiare i peli delle radici per muffa: la peluria bianca e uniforme sulle radici è normale; la muffa è grigia, a ragnatela, e ha cattivo odore.",
                "Poca luce: i germogli si allungano, diventano pallidi e si piegano.",
                "Riusare lo stesso substrato: si butta nel compost e si riparte da capo.",
            ]),
        ],
        "nota": "Un ciclo dura una o due settimane: seminando una vaschetta ogni 5-7 giorni hai microgreens freschi tutto l'anno, anche d'inverno.",
    },
    {
        "slug": "aromatiche-in-casa",
        "titolo": "Aromatiche in casa d'inverno: quali coltivare e come",
        "titolo_breve": "Aromatiche in casa",
        "descrizione": "Prezzemolo, erba cipollina, menta, timo, rosmarino e basilico in casa d'inverno: quali scegliere, dove metterle, quanta luce e acqua servono, gli errori da evitare.",
        "attacco": "Con una finestra luminosa, i vasi giusti e poca acqua hai erbe fresche anche a gennaio. Il segreto è la luce.",
        "foto": "photo-1723475170878-8b5f75ce249c",
        "alt": "Pianta di basilico su un tavolo di legno",
        "q": "kit erbe aromatiche",
        "agrieuro": "",
        "dove_titolo": "Dove comprare semi, piante e lampade",
        "azione": "Vedi semi e kit",
        "in_breve": [
            "Le più facili in casa d'inverno: prezzemolo, erba cipollina, menta e timo.",
            "Rosmarino e salvia vogliono la finestra più luminosa e una stanza fresca.",
            "Il basilico d'inverno cresce solo con il caldo e una lampada LED.",
        ],
        "sezioni": [
            ("Quali aromatiche scegliere", "voci", [
                ("Prezzemolo", "Si accontenta della luce di una finestra. Taglia gli steli esterni e lascia crescere il centro."),
                ("Erba cipollina", "Facilissima: si taglia a 3-4 cm dalla base e ricaccia."),
                ("Menta", "Cresce in fretta e invade: tienila in un vaso tutto suo."),
                ("Timo e origano", "Vogliono sole e poca acqua: annaffia solo quando la terra è asciutta in superficie."),
                ("Rosmarino e salvia", "In casa soffrono l'aria calda e secca dei termosifoni: mettili alla finestra più luminosa in una stanza fresca. Dove l'inverno è mite, stanno meglio fuori, al riparo."),
                ("Basilico", "È una pianta estiva: d'inverno in casa vuole almeno 15-18 °C e una lampada LED. Dura qualche mese, poi si riparte dalla semina."),
            ]),
            ("Dove metterle", "punti", [
                "Davanti alla finestra più luminosa, meglio esposta a sud o a ovest.",
                "Lontano da termosifoni e stufe: l'aria calda e secca le rovina in pochi giorni.",
                "Se la luce non basta, una lampada LED per piante a 20-30 cm, accesa 12-14 ore al giorno.",
                "Gira i vasi ogni settimana, così crescono dritte.",
            ]),
            ("Vasi, terriccio e acqua", "punti", [
                "Vasi con il foro di drenaggio e il sottovaso: l'acqua ferma fa marcire le radici.",
                "Terriccio universale di buona qualità; per rosmarino, timo e salvia aggiungi un terzo di sabbia o perlite.",
                "D'inverno si annaffia poco: tocca la terra con un dito e bagna solo se è asciutta.",
                "Niente concime fino a primavera: con poca luce la pianta non lo usa.",
            ]),
            ("Errori da evitare", "punti", [
                "Lasciare la piantina del supermercato nel suo vasetto: dentro ci sono tante piante fitte in poca terra. Dividila in 2-3 vasi più grandi.",
                "Annaffiare tutti i giorni per sicurezza.",
                "Tagliare più di un terzo della pianta alla volta.",
            ]),
        ],
        "nota": "Vuoi qualcosa di pronto in pochi giorni? Sullo stesso davanzale puoi coltivare i microgreens di rucola, senape o basilico: si tagliano in una-due settimane.",
    },
]

LOGO = ('<svg viewBox="66 78 380 364" fill="none" aria-hidden="true"><path d="M256 96 L414 222 Q428 233 428 251 L428 392 Q428 424 396 424 L116 424 Q84 424 84 392 L84 251 Q84 233 98 222 Z" fill="#F07F1A" stroke="#F07F1A" stroke-width="24" stroke-linejoin="round"/><rect x="243" y="280" width="26" height="148" rx="13" fill="#2D1846"/><path d="M256 318 C232 262 188 236 142 240 C144 290 192 326 256 318 Z" fill="#C9E86A"/><path d="M256 292 C282 230 330 202 376 208 C372 262 322 298 256 292 Z" fill="#C9E86A"/></svg>')


ORGANIZZAZIONE = {"@type": "Organization", "name": "OrtoCasa Help", "url": f"{SITO}/"}


def briciole_dati(passi):
    """BreadcrumbList schema.org da una lista di (nome, url)."""
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": nome, "item": u} for i, (nome, u) in enumerate(passi, start=1)]}


def piede_link(base):
    """Link di servizio nel piè di pagina; base è il percorso relativo alla radice del sito."""
    return (f'<a href="{base}guide/">Tutte le guide</a> · <a href="{base}chi-siamo/">Chi siamo</a> · '
            f'<a href="{base}privacy/">Privacy e cookie</a>')


def e(t):
    return html.escape(t, quote=True)


def foto(fid, w):
    return f"https://images.unsplash.com/{fid}?auto=format&fit=crop&w={w}&q=70"


def blocco_negozi(g, classe=""):
    return (f'<div class="dove {classe}" data-q="{e(g["q"])}" data-agrieuro="{e(g.get("agrieuro", ""))}" '
            f'data-titolo="{e(g["titolo_breve"])}"></div>')


def sezione(titolo, tipo, voci):
    out = [f'<section class="parte"><h2>{e(titolo)}</h2>']
    if tipo == "voci":
        out.append('<dl class="voci">' + "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in voci) + "</dl>")
    elif tipo == "sequenza":
        out.append('<ol class="sequenza">' + "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in voci) + "</ol>")
    else:
        out.append('<ul class="punti">' + "".join(f"<li>{e(v)}</li>" for v in voci) + "</ul>")
    out.append("</section>")
    return "".join(out)


def pagina(g, altre):
    url = f"{SITO}/guide/{g['slug']}/"
    dati = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": g["titolo"], "description": g["descrizione"],
         "image": foto(g["foto"], 1200), "dateModified": AGGIORNATA, "inLanguage": "it-IT", "mainEntityOfPage": url,
         "author": ORGANIZZAZIONE, "publisher": ORGANIZZAZIONE},
        briciole_dati([("Home", f"{SITO}/"), ("Guide", f"{SITO}/guide/"), (g["titolo_breve"], url)]),
    ]}
    corpo = "".join(sezione(*s) for s in g["sezioni"])
    nota = f'<p class="nota">{e(g["nota"])}</p>' if g.get("nota") else ""
    link_altre = "".join(f'<li><a href="../{a["slug"]}/">{e(a["titolo_breve"])}</a></li>' for a in altre)
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{e(g["titolo"])} | OrtoCasa Help</title>
<meta name="description" content="{e(g["descrizione"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(g["titolo"])}">
<meta property="og:description" content="{e(g["descrizione"])}">
<meta property="og:image" content="{foto(g["foto"], 1200)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="it_IT">
<meta name="theme-color" content="#2D1846">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="48x48" href="/icone/favicon-48.png">
<link rel="apple-touch-icon" href="/icone/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="OrtoCasa">
<script src="/app.js" defer></script>
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="stylesheet" href="../../fonts.css">
<link rel="stylesheet" href="../guida.css">
<link rel="alternate" type="application/rss+xml" title="Guide di OrtoCasa Help" href="{SITO}/feed.xml">
<script type="application/ld+json">{json.dumps(dati, ensure_ascii=False)}</script>
</head>
<body>
<header class="testata"><div class="contenitore">
  <a href="../../" class="logo" aria-label="OrtoCasa Help, torna alla home">{LOGO}<span class="marchio"><span class="o">O</span>rtoCasa Help</span></a>
</div></header>
<main>
  <article>
    <div class="apertura"><div class="contenitore">
      <p class="briciole"><a href="../../">Home</a> / <a href="../">Guide</a></p>
      <h1>{e(g["titolo"])}</h1>
      <p class="attacco">{e(g["attacco"])}</p>
      <img class="foto" src="{foto(g["foto"], 900)}" srcset="{foto(g["foto"], 600)} 600w, {foto(g["foto"], 900)} 900w, {foto(g["foto"], 1400)} 1400w" sizes="(min-width: 800px) 720px, 100vw" alt="{e(g["alt"])}" fetchpriority="high">
    </div></div>
    <div class="contenitore testo">
      <section class="in-breve"><h2>In breve</h2><ul>{"".join(f"<li>{e(v)}</li>" for v in g["in_breve"])}</ul></section>
      {corpo}
      {nota}
      <section class="parte" id="dove"><h2>{e(g.get("dove_titolo", "Dove comprarla"))}</h2><p class="sotto">Si apre la pagina del negozio, con i suoi prezzi, spedizioni e garanzie.</p>{blocco_negozi(g)}</section>
      <section class="parte altre"><h2>Altre guide</h2><ul>{link_altre}</ul></section>
      <p class="firma">Guida di OrtoCasa Help, a cura di un perito agrario. Aggiornata il {AGGIORNATA[8:10]}/{AGGIORNATA[5:7]}/{AGGIORNATA[:4]}.</p>
    </div>
  </article>
</main>
<div class="barra-acquisto"><a class="primario" id="barra-agrieuro" href="#dove">Vedi su AgriEuro</a><a class="secondario" href="#dove">Altri negozi</a></div>
<footer><div class="contenitore">
  <p>OrtoCasa Help partecipa a programmi di affiliazione: se acquisti dopo aver cliccato un nostro link, il negozio ci riconosce una commissione, senza costi aggiuntivi per te. In qualità di Affiliato Amazon, OrtoCasa Help riceve un guadagno dagli acquisti idonei.</p>
  <p>Foto da <a href="https://unsplash.com/?utm_source=ortocasahelp&amp;utm_medium=referral" rel="noopener" target="_blank">Unsplash</a>. © 2026 OrtoCasa Help · {piede_link("../../")}</p>
</div></footer>
<script src="../../negozi.js"></script>
<script src="../guida.js"></script>
</body>
</html>
"""


def pagina_indice(guide):
    url = f"{SITO}/guide/"
    titolo = "Guide per l'orto e il giardino"
    descrizione = ("Le guide di OrtoCasa Help, scritte da un perito agrario: come scegliere motozappa, robot tagliaerba, "
                   "irrigazione a goccia, decespugliatore, biotrituratore e gli altri attrezzi per l'orto di casa.")
    dati = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": titolo, "description": descrizione, "url": url, "inLanguage": "it-IT",
         "publisher": ORGANIZZAZIONE,
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i, "url": f"{SITO}/guide/{g['slug']}/", "name": g["titolo"]}
             for i, g in enumerate(guide, start=1)]}},
        briciole_dati([("Home", f"{SITO}/"), ("Guide", url)]),
    ]}
    schede = "".join(
        f'<li><a href="{g["slug"]}/"><img src="{foto(g["foto"], 600)}" alt="{e(g["alt"])}" loading="lazy" width="600" height="375">'
        f'<span class="nome">{e(g["titolo"])}</span><span class="riassunto">{e(g["descrizione"])}</span></a></li>'
        for g in guide)
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{e(titolo)} | OrtoCasa Help</title>
<meta name="description" content="{e(descrizione)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(titolo)}">
<meta property="og:description" content="{e(descrizione)}">
<meta property="og:image" content="{foto(guide[0]["foto"], 1200)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="it_IT">
<meta name="theme-color" content="#2D1846">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" sizes="48x48" href="/icone/favicon-48.png">
<link rel="apple-touch-icon" href="/icone/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="OrtoCasa">
<script src="/app.js" defer></script>
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="stylesheet" href="../fonts.css">
<link rel="stylesheet" href="guida.css">
<link rel="alternate" type="application/rss+xml" title="Guide di OrtoCasa Help" href="{SITO}/feed.xml">
<script type="application/ld+json">{json.dumps(dati, ensure_ascii=False)}</script>
</head>
<body class="senza-barra">
<header class="testata"><div class="contenitore">
  <a href="../" class="logo" aria-label="OrtoCasa Help, torna alla home">{LOGO}<span class="marchio"><span class="o">O</span>rtoCasa Help</span></a>
</div></header>
<main>
  <div class="apertura"><div class="contenitore">
    <p class="briciole"><a href="../">Home</a> / Guide</p>
    <h1>{e(titolo)}</h1>
    <p class="attacco">Come scegliere l'attrezzo giusto per il tuo orto, spiegato da un perito agrario. Niente classifiche pagate.</p>
  </div></div>
  <div class="contenitore testo">
    <ul class="elenco-guide">{schede}</ul>
    <p class="firma">Aggiornate il {AGGIORNATA[8:10]}/{AGGIORNATA[5:7]}/{AGGIORNATA[:4]}. <a href="../chi-siamo/">Chi scrive le guide</a></p>
  </div>
</main>
<footer><div class="contenitore">
  <p>OrtoCasa Help partecipa a programmi di affiliazione: se acquisti dopo aver cliccato un nostro link, il negozio ci riconosce una commissione, senza costi aggiuntivi per te. In qualità di Affiliato Amazon, OrtoCasa Help riceve un guadagno dagli acquisti idonei.</p>
  <p>Foto da <a href="https://unsplash.com/?utm_source=ortocasahelp&amp;utm_medium=referral" rel="noopener" target="_blank">Unsplash</a>. © 2026 OrtoCasa Help · {piede_link("../")}</p>
</div></footer>
</body>
</html>
"""


def feed_rss(guide):
    """Feed RSS delle guide: Pinterest lo legge e crea un pin per ogni guida (auto-pubblicazione)."""
    data = email.utils.format_datetime(datetime.datetime.fromisoformat(AGGIORNATA + "T08:00:00+02:00"))
    voci = []
    for g in guide:
        url = f"{SITO}/guide/{g['slug']}/"
        img = foto(g["foto"], 1000) + "&fm=jpg"
        voci.append(
            f"<item><title>{e(g['titolo'])}</title><link>{url}</link><guid isPermaLink=\"true\">{url}</guid>"
            f"<pubDate>{data}</pubDate><description>{e(g['descrizione'])}</description>"
            f'<enclosure url="{e(img)}" type="image/jpeg" length="0"/>'
            f'<media:content url="{e(img)}" medium="image" type="image/jpeg"/></item>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
            f"<title>OrtoCasa Help: guide per l'orto e il giardino</title><link>{SITO}/guide/</link>"
            f'<atom:link href="{SITO}/feed.xml" rel="self" type="application/rss+xml"/>'
            "<description>Guide di un perito agrario per scegliere gli attrezzi dell'orto di casa.</description>"
            f"<language>it-it</language><lastBuildDate>{data}</lastBuildDate>"
            + "".join(voci) + "</channel></rss>\n")


def main():
    for g in GUIDE:
        altre = [a for a in GUIDE if a["slug"] != g["slug"]]
        dest = RADICE / "guide" / g["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(pagina(g, altre), encoding="utf-8")
        print("scritta", dest.relative_to(RADICE))
    (RADICE / "guide" / "index.html").write_text(pagina_indice(GUIDE), encoding="utf-8")
    print("scritta guide/index.html")
    (RADICE / "feed.xml").write_text(feed_rss(GUIDE), encoding="utf-8")
    print("scritta feed.xml")
    urls = ([f"{SITO}/", f"{SITO}/guide/"] + [f"{SITO}/guide/{g['slug']}/" for g in GUIDE]
            + [f"{SITO}/chi-siamo/", f"{SITO}/privacy/"])
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f"  <url><loc>{u}</loc><lastmod>{AGGIORNATA}</lastmod></url>" for u in urls]
    sitemap.append("</urlset>")
    (RADICE / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (RADICE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITO}/sitemap.xml\n", encoding="utf-8")
    print("scritte sitemap.xml e robots.txt")


if __name__ == "__main__":
    main()
