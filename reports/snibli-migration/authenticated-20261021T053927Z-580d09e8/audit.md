# SNIBLI migration audit

2026-10-21T05:40:15.822648+00:00

Coverage: AUTHENTICATED_LOCAL_FILE_EXPORT

PASS applies only to the named check, never to full migration equivalence.

- **PASS** `authenticated`: "Existing CSRF/login/confirmation client; credentials not exported"
- **UNKNOWN** `configured_forms_vs_v3_9_2`: {"status": "UNKNOWN", "bindings": 57, "unique_keys": 55, "matches_release_v3_9_2": false, "warnings": ["BINDING_METADATA_NOT_IN_REGISTRY:dc.type.genre"], "scope": "Configured forms only; does not establish active collection membership"}
- **FAIL** `vocabulary_values_vs_v3_9_2`: {"status": "FAIL", "results": [{"vocabulary": "selfDenominationPairs", "status": "PASS", "detail": {"observed_values": ["ñonmda", "qa'yool", "úza'", "koti'", "teenek", "popti'-abxub'al", "ta_yoi_mam", "maayat'aan", "yoremnokki", "yaak_avu", "cmiique_litom", "púrhepecha", "tektiteco", "lhima'alh'ama'", "tohol-ab'al", "tutunakú", "mé'phaa", "bats'il_k'op", "jiaj noki", "otetzane"], "expected_values": ["ñonmda", "qa'yool", "úza'", "koti'", "teenek", "popti'-abxub'al", "ta_yoi_mam", "maayat'aan", "yoremnokki", "yaak_avu", "cmiique_litom", "púrhepecha", "tektiteco", "lhima'alh'ama'", "tohol-ab'al", "tutunakú", "mé'phaa", "bats'il_k'op", "jiaj noki", "otetzane"]}}, {"vocabulary": "linguisticFamilyPairs", "status": "PASS", "detail": {"observed_values": ["Indoeuropeo", "Maya", "Oto-mangue", "Mixe-zoque", "Yuto-nahua", "Cochimí-yumana", "Chontal de Oaxaca", "Huave", "Álgica", "Seri", "Tarasca", "Totonaco-tepehua", "Afroasiática", "caucásica", "Indoeuropeo", "Niger-congo", "Caucásica nororiental", "Aimárica", "Túrquica", "Criolla", "Sino-tibetana", "Austronesia", "Álgica", "Lengua construida", "Urálica", "Aislada", "Tupí", "Esquimo-aleutiana", "Japonica", "Kartveliana", "Austroasiática", "Dravídica", "Coreánica", "Sahariana", "Kra-dai", "Mongólica", "Na-dené", "Quechua", "Ubanguiana"], "expected_values": ["Indoeuropeo", "Maya", "Oto-mangue", "Mixe-zoque", "Yuto-nahua", "Cochimí-yumana", "Chontal de Oaxaca", "Huave", "Álgica", "Seri", "Tarasca", "Totonaco-tepehua", "Afroasiática", "caucásica", "Indoeuropeo", "Niger-congo", "Caucásica nororiental", "Aimárica", "Túrquica", "Criolla", "Sino-tibetana", "Austronesia", "Álgica", "Lengua construida", "Urálica", "Aislada", "Tupí", "Esquimo-aleutiana", "Japonica", "Kartveliana", "Austroasiática", "Dravídica", "Coreánica", "Sahariana", "Kra-dai", "Mongólica", "Na-dené", "Quechua", "Ubanguiana"]}}, {"vocabulary": "educationLevelPairs", "status": "PASS", "detail": {"observed_values": ["Preescolar", "Primaria", "Secundaria", "Preparatoria", "Universidad", "Postgrado"], "expected_values": ["Preescolar", "Primaria", "Secundaria", "Preparatoria", "Universidad", "Postgrado"]}}, {"vocabulary": "linguisticBranchPairs", "status": "PASS", "detail": {"observed_values": ["Romance", "Germánico", "Q'anjob'alano", "Amuzgo-mixtecano", "Aguacateco-ixil", "Zoqueano del golfo", "Cora-huichol", "Delta-California", "Mixtecano", "Zapotecano", "Otopame", "Chinantecano", "Popolocano", "Lengua aislada", "Cholano", "Taracahita", "Kaqchikel-tz'utuhil", "Algonquino-fox", "Yumano", "Pai-yumano del norte", "K'ichiano", "Yucateco-lacandón", "Teko-mam", "Cahita", "Mixeano", "Nahuatlano", "Tepimano", "Tepehua", "Totonaco", "Tlapaneco-subtiaba", "Tseltalano", "Zoquenano", "cushítica", "abjasio-abaza", "indoirania", "germánica", "kwa", "semítica", "itálica (romance)", "ávaro-andina", "aimara", "oghuz", "kipchak", "eslava", "criollo de base inglesa", "mandé", "tibeto-birmana", "celta", "naj", "malayo-polinesia", "algonquina", "ogur", "helénica", "auxiliar internacional", "fino-ugria", "vasca", "atlántica", "tupí-guaraní", "chádica", "oceánica", "criollo de base francesa", "ugria", "armenia", "bantú", "volta-níger", "esquimal", "japonesa", "georgiana", "mon-jemer", "dravídica meridional", "coreana", "sahariana occidental", "itálica", "tai", "báltica", "mongólica", "atabascana", "quechua", "ubanguiana", "albanesa", "karluk", "sínica"], "expected_values": ["Romance", "Germánico", "Q'anjob'alano", "Amuzgo-mixtecano", "Aguacateco-ixil", "Zoqueano del golfo", "Cora-huichol", "Delta-California", "Mixtecano", "Zapotecano", "Otopame", "Chinantecano", "Popolocano", "Lengua aislada", "Cholano", "Taracahita", "Kaqchikel-tz'utuhil", "Algonquino-fox", "Yumano", "Pai-yumano del norte", "K'ichiano", "Yucateco-lacandón", "Teko-mam", "Cahita", "Mixeano", "Nahuatlano", "Tepimano", "Tepehua", "Totonaco", "Tlapaneco-subtiaba", "Tseltalano", "Zoquenano", "cushítica", "abjasio-abaza", "indoirania", "germánica", "kwa", "semítica", "itálica (romance)", "ávaro-andina", "aimara", "oghuz", "kipchak", "eslava", "criollo de base inglesa", "mandé", "tibeto-birmana", "celta", "naj", "malayo-polinesia", "algonquina", "ogur", "helénica", "auxiliar internacional", "fino-ugria", "vasca", "atlántica", "tupí-guaraní", "chádica", "oceánica", "criollo de base francesa", "ugria", "armenia", "bantú", "volta-níger", "esquimal", "japonesa", "georgiana", "mon-jemer", "dravídica meridional", "coreana", "sahariana occidental", "itálica", "tai", "báltica", "mongólica", "atabascana", "quechua", "ubanguiana", "albanesa", "karluk", "sínica"]}}, {"vocabulary": "extentTypePairs", "status": "PASS", "detail": {"observed_values": ["Impreso", "Impreso hojas", "Digital", "Digital hojas", "Fotografía", "Libro", "Dirección electrónica"], "expected_values": ["Impreso", "Impreso hojas", "Digital", "Digital hojas", "Fotografía", "Libro", "Dirección electrónica"]}}, {"vocabulary": "languageUsagePairs", "status": "PASS", "detail": {"observed_values": ["Monolingüe", "Bilingüe", "Multilingüe"], "expected_values": ["Monolingüe", "Bilingüe", "Multilingüe"]}}, {"vocabulary": "common_types", "status": "FAIL", "detail": {"observed_values": ["Animation", "Article", "Book", "Book chapter", "Dataset", "Learning Object", "Image", "Image, 3-D", "Map", "Musical Score", "Plan or blueprint", "Preprint", "Presentation", "Recording, acoustical", "Recording, musical", "Recording, oral", "Software", "Technical Report", "Thesis", "Video", "Working Paper", "Other", "Pagina Web", "Códice", "Reseña", "Documento Colonial"], "expected_values": ["Animation", "Article", "Book", "Book chapter", "Dataset", "Learning Object", "Image", "Image, 3-D", "Map", "Musical Score", "Plan or blueprint", "Preprint", "Presentation", "Recording, acoustical", "Recording, musical", "Recording, oral", "Software", "Technical Report", "Thesis", "Video", "Working Paper", "Other", "Pagina Web"]}}, {"vocabulary": "accessRightsPairs", "status": "PASS", "detail": {"observed_values": ["Acceso abierto", "Acceso embargado", "Acceso restringido", "Acceso a registro bibliográfico"], "expected_values": ["Acceso abierto", "Acceso embargado", "Acceso restringido", "Acceso a registro bibliográfico"]}}, {"vocabulary": "iso6391Pairs", "status": "PASS", "detail": {"observed_values": ["spa", "eng", "knj", "amu", "agu", "ayo", "crn", "cuc", "cut", "ctp", "pei", "chj", "coz", "chd", "chf", "cac", "ctu", "var", "hus", "huv", "hch", "ixc", "ixl", "jac", "cak", "kic", "klb", "dih", "yku", "quc", "lac", "mam", "mat", "yua", "mfy", "maz", "maq", "mco", "mix", "nah", "plo", "ote", "ppi", "pbs", "ood", "pls", "poi", "ckt", "kjb", "kek", "pos", "sei", "tar", "tsz", "ttc", "tpt", "thn", "stp", "poq", "toj", "top", "trs", "otm", "tcf", "tzc", "tzo", "yaq", "zap", "zoc", "aa", "ab", "ae", "af", "ak", "am", "an", "ar", "as", "av", "ay", "az", "ba", "be", "bg", "bh", "bi", "bm", "bn", "bo", "br", "bs", "ca", "ce", "ch", "co", "cr", "cs", "cu", "cv", "cy", "da", "de", "dv", "dz", "ee", "el", "en", "eo", "es", "et", "eu", "fa", "ff", "fi", "fj", "fo", "fr", "fy", "ga", "gd", "gl", "gn", "gu", "gv", "ha", "he", "hi", "ho", "hr", "ht", "hu", "hy", "hz", "ia", "id", "ie", "ig", "ii", "ik", "io", "is", "it", "iu", "ja", "jv", "ka", "kg", "ki", "kj", "kk", "kl", "km", "kn", "ko", "kr", "ks", "ku", "kv", "kw", "ky", "la", "lb", "lg", "li", "ln", "lo", "lt", "lu", "lv", "mg", "mh", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my", "na", "nb", "nd", "ne", "ng", "nl", "nn", "no", "nr", "nv", "ny", "oc", "oj", "om", "or", "os", "pa", "pi", "pl", "ps", "pt", "qc", "rm", "rn", "ro", "ru", "rw", "sa", "sc", "sd", "se", "sg", "si", "sk", "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", "sv", "sw", "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts", "tt", "tw", "ty", "ug", "uk", "ur", "uz", "ve", "vi", "vo", "wa", "wo", "xh", "yi", "yo", "za", "zh", "zu"], "expected_values": ["spa", "eng", "knj", "amu", "agu", "ayo", "crn", "cuc", "cut", "ctp", "pei", "chj", "coz", "chd", "chf", "cac", "ctu", "var", "hus", "huv", "hch", "ixc", "ixl", "jac", "cak", "kic", "klb", "dih", "yku", "quc", "lac", "mam", "mat", "yua", "mfy", "maz", "maq", "mco", "mix", "nah", "plo", "ote", "ppi", "pbs", "ood", "pls", "poi", "ckt", "kjb", "kek", "pos", "sei", "tar", "tsz", "ttc", "tpt", "thn", "stp", "poq", "toj", "top", "trs", "otm", "tcf", "tzc", "tzo", "yaq", "zap", "zoc", "aa", "ab", "ae", "af", "ak", "am", "an", "ar", "as", "av", "ay", "az", "ba", "be", "bg", "bh", "bi", "bm", "bn", "bo", "br", "bs", "ca", "ce", "ch", "co", "cr", "cs", "cu", "cv", "cy", "da", "de", "dv", "dz", "ee", "el", "en", "eo", "es", "et", "eu", "fa", "ff", "fi", "fj", "fo", "fr", "fy", "ga", "gd", "gl", "gn", "gu", "gv", "ha", "he", "hi", "ho", "hr", "ht", "hu", "hy", "hz", "ia", "id", "ie", "ig", "ii", "ik", "io", "is", "it", "iu", "ja", "jv", "ka", "kg", "ki", "kj", "kk", "kl", "km", "kn", "ko", "kr", "ks", "ku", "kv", "kw", "ky", "la", "lb", "lg", "li", "ln", "lo", "lt", "lu", "lv", "mg", "mh", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my", "na", "nb", "nd", "ne", "ng", "nl", "nn", "no", "nr", "nv", "ny", "oc", "oj", "om", "or", "os", "pa", "pi", "pl", "ps", "pt", "qc", "rm", "rn", "ro", "ru", "rw", "sa", "sc", "sd", "se", "sg", "si", "sk", "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", "sv", "sw", "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts", "tt", "tw", "ty", "ug", "uk", "ur", "uz", "ve", "vi", "vo", "wa", "wo", "xh", "yi", "yo", "za", "zh", "zu"]}}, {"vocabulary": "linguiscgroupPairs", "status": "PASS", "detail": {"observed_values": ["Español", "Inglés", "Akateko", "Amuzgo", "Awakateko", "Ayapaneco", "Cora", "Cucapá", "Cuicateco", "Chatino", "Chichimeca Jonaz", "Chinanteco", "Chocholteco", "Chontal de Oaxaca", "Chontal de Tabasco", "Chuj", "Ch'ol", "Guarijío", "Huasteco", "Huave", "Huichol", "Ixcateco", "Ixil", "Jakalteko", "Kaqchikel", "Kickapoo", "Kiliwa", "Kumiai", "Ku'ahl", "K'iche'", "Lacandón", "Mam", "Matlatzinca", "Maya yucateco", "Mayo", "Mazahua", "Mazateco", "Mixe", "Mixteco", "Náhuatl", "Oluteco", "Otomí", "Paipai", "Pame", "Pápago (Tohono O'odham)", "Pima", "Popoloca", "Popoluca de la Sierra", "Qato'k", "Q'anjob'al", "Q'eqchi'", "Sayulteco", "Seri", "Tarahumara", "Tarasco (Purépecha)", "Teko", "Tepehua", "Tepehuano del norte", "Tepehuano del sur", "Texistepequeño", "Tojolabal", "Totonaco", "Triqui", "Tlahuica", "Tlapaneco", "Tseltal", "Tsotsil", "Yaqui", "Zapoteco", "Zoque", "P'urepecha", "Tarasco", "afar", "abjasio (o abjasiano)", "avéstico", "afrikáans", "akano", "amhárico", "aragonés", "árabe", "asamés", "avar (o ávaro)", "aimara", "azerí", "baskir", "bielorruso", "búlgaro", "bhoyapurí", "bislama", "bambara", "bengalí", "tibetano", "bretón", "bosnio", "catalán", "checheno", "chamorro", "corso", "cree", "checo", "eslavo eclesiástico antiguo", "chuvasio", "galés", "danés", "alemán", "maldivo (dhivehi)", "dzongkha", "ewé", "griego (moderno)", "inglés", "esperanto", "español (castellano)", "estonio", "euskera", "persa (farsi)", "fula", "finés", "fiyiano", "feroés", "francés", "frisón", "irlandés", "gaélico escocés", "gallego", "guaraní", "guyaratí", "manés", "hausa", "hebreo", "hindi", "hiri motu", "croata", "haitiano", "húngaro", "armenio", "herero", "interlingua", "indonesio", "occidental", "igbo", "yi de Sichuán", "iñupiaq", "ido", "islandés", "italiano", "inuktitut", "japonés", "javanés", "georgiano", "kongo (kikongo)", "kikuyu", "kuanyama", "kazajo", "groenlandés (kalaallisut)", "camboyano (jemer)", "canarés", "coreano", "kanuri", "cachemiro", "kurdo", "komi", "córnico", "kirguís", "latín", "luxemburgués", "luganda", "limburgués", "lingala", "lao", "lituano", "luba-katanga", "letón", "malgache", "marshalés", "maorí", "macedonio", "malayalam", "mongol", "maratí", "malayo", "maltés", "birmano", "nauruano", "noruego bokmål", "ndebele del norte", "nepalí", "ndonga", "neerlandés", "nynorsk", "noruego", "ndebele del sur", "navajo", "chichewa", "occitano", "ojibwa", "oromo", "oriya (odia)", "osético", "panyabí", "pali", "polaco", "pastú (pashto)", "portugués", "quechua", "romanche", "kirundi", "rumano", "ruso", "ruandés (kiñaruanda)", "sánscrito", "sardo", "sindhi", "sami septentrional", "sango", "cingalés", "eslovaco", "esloveno", "samoano", "shona", "somalí", "albanés", "serbio", "suazi (swati)", "sesotho", "sundanés", "sueco", "suajili", "tamil", "télugu", "tayiko", "tailandés", "tigriña", "turcomano", "tagalo", "setsuana", "tongano", "turco", "tsonga", "tártaro", "twi", "tahitiano", "uigur", "ucraniano", "urdu", "uzbeko", "venda", "vietnamita", "volapük", "valón", "wolof", "xhosa", "yídish", "yoruba", "chuan (zhuang)", "chino", "zulú"], "expected_values": ["Español", "Inglés", "Akateko", "Amuzgo", "Awakateko", "Ayapaneco", "Cora", "Cucapá", "Cuicateco", "Chatino", "Chichimeca Jonaz", "Chinanteco", "Chocholteco", "Chontal de Oaxaca", "Chontal de Tabasco", "Chuj", "Ch'ol", "Guarijío", "Huasteco", "Huave", "Huichol", "Ixcateco", "Ixil", "Jakalteko", "Kaqchikel", "Kickapoo", "Kiliwa", "Kumiai", "Ku'ahl", "K'iche'", "Lacandón", "Mam", "Matlatzinca", "Maya yucateco", "Mayo", "Mazahua", "Mazateco", "Mixe", "Mixteco", "Náhuatl", "Oluteco", "Otomí", "Paipai", "Pame", "Pápago (Tohono O'odham)", "Pima", "Popoloca", "Popoluca de la Sierra", "Qato'k", "Q'anjob'al", "Q'eqchi'", "Sayulteco", "Seri", "Tarahumara", "Tarasco (Purépecha)", "Teko", "Tepehua", "Tepehuano del norte", "Tepehuano del sur", "Texistepequeño", "Tojolabal", "Totonaco", "Triqui", "Tlahuica", "Tlapaneco", "Tseltal", "Tsotsil", "Yaqui", "Zapoteco", "Zoque", "P'urepecha", "Tarasco", "afar", "abjasio (o abjasiano)", "avéstico", "afrikáans", "akano", "amhárico", "aragonés", "árabe", "asamés", "avar (o ávaro)", "aimara", "azerí", "baskir", "bielorruso", "búlgaro", "bhoyapurí", "bislama", "bambara", "bengalí", "tibetano", "bretón", "bosnio", "catalán", "checheno", "chamorro", "corso", "cree", "checo", "eslavo eclesiástico antiguo", "chuvasio", "galés", "danés", "alemán", "maldivo (dhivehi)", "dzongkha", "ewé", "griego (moderno)", "inglés", "esperanto", "español (castellano)", "estonio", "euskera", "persa (farsi)", "fula", "finés", "fiyiano", "feroés", "francés", "frisón", "irlandés", "gaélico escocés", "gallego", "guaraní", "guyaratí", "manés", "hausa", "hebreo", "hindi", "hiri motu", "croata", "haitiano", "húngaro", "armenio", "herero", "interlingua", "indonesio", "occidental", "igbo", "yi de Sichuán", "iñupiaq", "ido", "islandés", "italiano", "inuktitut", "japonés", "javanés", "georgiano", "kongo (kikongo)", "kikuyu", "kuanyama", "kazajo", "groenlandés (kalaallisut)", "camboyano (jemer)", "canarés", "coreano", "kanuri", "cachemiro", "kurdo", "komi", "córnico", "kirguís", "latín", "luxemburgués", "luganda", "limburgués", "lingala", "lao", "lituano", "luba-katanga", "letón", "malgache", "marshalés", "maorí", "macedonio", "malayalam", "mongol", "maratí", "malayo", "maltés", "birmano", "nauruano", "noruego bokmål", "ndebele del norte", "nepalí", "ndonga", "neerlandés", "nynorsk", "noruego", "ndebele del sur", "navajo", "chichewa", "occitano", "ojibwa", "oromo", "oriya (odia)", "osético", "panyabí", "pali", "polaco", "pastú (pashto)", "portugués", "quechua", "romanche", "kirundi", "rumano", "ruso", "ruandés (kiñaruanda)", "sánscrito", "sardo", "sindhi", "sami septentrional", "sango", "cingalés", "eslovaco", "esloveno", "samoano", "shona", "somalí", "albanés", "serbio", "suazi (swati)", "sesotho", "sundanés", "sueco", "suajili", "tamil", "télugu", "tayiko", "tailandés", "tigriña", "turcomano", "tagalo", "setsuana", "tongano", "turco", "tsonga", "tártaro", "twi", "tahitiano", "uigur", "ucraniano", "urdu", "uzbeko", "venda", "vietnamita", "volapük", "valón", "wolof", "xhosa", "yídish", "yoruba", "chuan (zhuang)", "chino", "zulú"]}}, {"vocabulary": "openaire_types", "status": "PASS", "detail": {"observed_values": ["interactive resource", "website", "dataset", "interview", "image", "moving image", "video", "still image", "other", "software", "research software", "workflow", "cartographic material", "map", "sound", "musical composition", "text", "annotation", "bibliography", "book", "book part", "conference object", "conference proceedings", "conference paper", "conference poster", "conference paper not in proceedings", "conference poster not in proceedings", "lecture", "letter", "periodical", "journal", "contribution to journal", "journal article", "data paper", "review article", "research article", "corrigendum", "software paper", "editorial", "letter to the editor", "newspaper", "newspaper article", "magazine", "patent", "preprint", "report", "report part", "internal report", "memorandum", "other type of report", "policy report", "project deliverable", "data management plan", "report to funding agency", "research report", "technical report", "research proposal", "review", "book review", "technical documentation", "working paper", "thesis", "bachelor thesis", "doctoral thesis", "master thesis", "musical notation", "blog post", "website", "learning object", "clinical trial", "clinical study", "tesis licenciatura", "tesis doctorado", "tesis maestria"], "expected_values": ["interactive resource", "website", "dataset", "interview", "image", "moving image", "video", "still image", "other", "software", "research software", "workflow", "cartographic material", "map", "sound", "musical composition", "text", "annotation", "bibliography", "book", "book part", "conference object", "conference proceedings", "conference paper", "conference poster", "conference paper not in proceedings", "conference poster not in proceedings", "lecture", "letter", "periodical", "journal", "contribution to journal", "journal article", "data paper", "review article", "research article", "corrigendum", "software paper", "editorial", "letter to the editor", "newspaper", "newspaper article", "magazine", "patent", "preprint", "report", "report part", "internal report", "memorandum", "other type of report", "policy report", "project deliverable", "data management plan", "report to funding agency", "research report", "technical report", "research proposal", "review", "book review", "technical documentation", "working paper", "thesis", "bachelor thesis", "doctoral thesis", "master thesis", "musical notation", "blog post", "website", "learning object", "clinical trial", "clinical study", "tesis licenciatura", "tesis doctorado", "tesis maestria"]}}, {"vocabulary": "primaryClassificationPairs", "status": "PASS", "detail": {"observed_values": ["Didácticos", "Históricos", "Culturales", "Lingüísticos", "Derecho", "Salud"], "expected_values": ["Didácticos", "Históricos", "Culturales", "Lingüísticos", "Derecho", "Salud"]}}, {"vocabulary": "languageTargetPairs", "status": "PASS", "detail": {"observed_values": ["L1", "L2", "L1 y L2"], "expected_values": ["L1", "L2", "L1 y L2"]}}, {"vocabulary": "topicsPairs", "status": "PASS", "detail": {"observed_values": ["Lingüística", "Educación", "Alfabetización", "Lexicografía", "Lexicología", "Morfosintaxis", "Semántica", "Sociolingüística", "Historiografía lingüística", "Documentación lingüística", "Etnohistoria", "Educación indígena", "Fonología", "Fonética", "Morfología", "Sintaxis", "Pragmática", "Descripción gramatical", "Planificación lingüística", "Políticas lingüísticas", "Literatura indígena", "Narrativa", "Traducción", "Interpretación", "Contacto lingüístico", "Análisis del discurso", "Etnolingüística", "Familias lingüísticas", "Género lingüístico", "Psicolingüística", "Patrimonio lingüístico", "Diversidad lingüística", "Corpus lingüístico", "Campos semánticos", "Partículas discursivas", "Técnicas etnográficas", "Transcripción", "Género gramatical", "Filología indoamericana", "Etnografía"], "expected_values": ["Lingüística", "Educación", "Alfabetización", "Lexicografía", "Lexicología", "Morfosintaxis", "Semántica", "Sociolingüística", "Historiografía lingüística", "Documentación lingüística", "Etnohistoria", "Educación indígena", "Fonología", "Fonética", "Morfología", "Sintaxis", "Pragmática", "Descripción gramatical", "Planificación lingüística", "Políticas lingüísticas", "Literatura indígena", "Narrativa", "Traducción", "Interpretación", "Contacto lingüístico", "Análisis del discurso", "Etnolingüística", "Familias lingüísticas", "Género lingüístico", "Psicolingüística", "Patrimonio lingüístico", "Diversidad lingüística", "Corpus lingüístico", "Campos semánticos", "Partículas discursivas", "Técnicas etnográficas", "Transcripción", "Género gramatical", "Filología indoamericana", "Etnografía"]}}, {"vocabulary": "registeredLanguagePairs", "status": "PASS", "detail": {"observed_values": ["Español", "Inglés", "Akateko", "Amuzgo", "Awakateko", "Ayapaneco", "Cora", "Cucapá", "Cuicateco", "Chatino", "Chichimeca Jonaz", "Chinanteco", "Chocholteco", "Chontal de Oaxaca", "Chontal de Tabasco", "Chuj", "Ch'ol", "Guarijío", "Huasteco", "Huave", "Huichol", "Ixcateco", "Ixil", "Jakalteko", "Kaqchikel", "Kickapoo", "Kiliwa", "Kumiai", "Ku'ahl", "K'iche'", "Lacandón", "Mam", "Matlatzinca", "Maya yucateco", "Mayo", "Mazahua", "Mazateco", "Mixe", "Mixteco", "Náhuatl", "Oluteco", "Otomí", "Paipai", "Pame", "Pápago (Tohono O'odham)", "Pima", "Popoloca", "Popoluca de la Sierra", "Qato'k", "Q'anjob'al", "Q'eqchi'", "Sayulteco", "Seri", "Tarahumara", "Tarasco (Purépecha)", "Teko", "Tepehua", "Tepehuano del norte", "Tepehuano del sur", "Texistepequeño", "Tojolabal", "Totonaco", "Triqui", "Tlahuica", "Tlapaneco", "Tseltal", "Tsotsil", "Yaqui", "Zapoteco", "Zoque", "P'urepecha", "Tarasco", "afar", "abjasio (o abjasiano)", "avéstico", "afrikáans", "akano", "amhárico", "aragonés", "árabe", "asamés", "avar (o ávaro)", "aimara", "azerí", "baskir", "bielorruso", "búlgaro", "bhoyapurí", "bislama", "bambara", "bengalí", "tibetano", "bretón", "bosnio", "catalán", "checheno", "chamorro", "corso", "cree", "checo", "eslavo eclesiástico antiguo", "chuvasio", "galés", "danés", "alemán", "maldivo (o dhivehi)", "dzongkha", "ewé", "griego (moderno)", "inglés", "esperanto", "español (o castellano)", "estonio", "euskera", "persa (o farsi)", "fula", "finés (o finlandés)", "fiyiano (o fiyi)", "feroés", "francés", "frisón (o frisio)", "irlandés (o gaélico)", "gaélico escocés", "gallego", "guaraní", "guyaratí (o gujaratí)", "manés (gaélico manés o de Isla de Man)", "hausa", "hebreo", "hindi (o hindú)", "hiri motu", "croata", "haitiano", "húngaro", "armenio", "herero", "interlingua", "indonesio", "occidental", "igbo", "yi de Sichuán", "iñupiaq", "ido", "islandés", "italiano", "inuktitut (o inuit)", "japonés", "javanés", "georgiano", "kongo (o kikongo)", "kikuyu", "kuanyama", "kazajo (o kazajio)", "groenlandés (o kalaallisut)", "camboyano (o jemer)", "canarés", "coreano", "kanuri", "cachemiro (o cachemir)", "kurdo", "komi", "córnico", "kirguís", "latín", "luxemburgués", "luganda", "limburgués", "lingala", "lao", "lituano", "luba-katanga (o chiluba)", "letón", "malgache (o malagasy)", "marshalés", "maorí", "macedonio", "malayalam", "mongol", "maratí", "malayo", "maltés", "birmano", "nauruano", "noruego bokmål", "ndebele del norte", "nepalí", "ndonga", "neerlandés (u holandés)", "nynorsk", "noruego", "ndebele del sur", "navajo", "chichewa", "occitano", "ojibwa", "oromo", "oriya", "osético (u osetio, u oseta)", "panyabí (o penyabi)", "pali", "polaco", "pastú (o pastún, o pashto)", "portugués", "quechua", "romanche", "kirundi", "rumano", "ruso", "ruandés (o kiñaruanda)", "sánscrito", "sardo", "sindhi", "sami septentrional", "sango", "cingalés", "eslovaco", "esloveno", "samoano", "shona", "somalí", "albanés", "serbio", "suazi (o swati, o siSwati)", "sesotho", "sundanés (o sondanés)", "sueco", "suajili", "tamil", "télugu", "tayiko", "tailandés", "tigriña", "turcomano", "tagalo", "setsuana", "tongano", "turco", "tsonga", "tártaro", "twi", "tahitiano", "uigur", "ucraniano", "urdu", "uzbeko", "venda", "vietnamita", "volapük", "valón", "wolof", "xhosa", "yídish (o yidis, o yiddish)", "yoruba", "chuan (o chuang, o zhuang)", "chino", "zulú"], "expected_values": ["Español", "Inglés", "Akateko", "Amuzgo", "Awakateko", "Ayapaneco", "Cora", "Cucapá", "Cuicateco", "Chatino", "Chichimeca Jonaz", "Chinanteco", "Chocholteco", "Chontal de Oaxaca", "Chontal de Tabasco", "Chuj", "Ch'ol", "Guarijío", "Huasteco", "Huave", "Huichol", "Ixcateco", "Ixil", "Jakalteko", "Kaqchikel", "Kickapoo", "Kiliwa", "Kumiai", "Ku'ahl", "K'iche'", "Lacandón", "Mam", "Matlatzinca", "Maya yucateco", "Mayo", "Mazahua", "Mazateco", "Mixe", "Mixteco", "Náhuatl", "Oluteco", "Otomí", "Paipai", "Pame", "Pápago (Tohono O'odham)", "Pima", "Popoloca", "Popoluca de la Sierra", "Qato'k", "Q'anjob'al", "Q'eqchi'", "Sayulteco", "Seri", "Tarahumara", "Tarasco (Purépecha)", "Teko", "Tepehua", "Tepehuano del norte", "Tepehuano del sur", "Texistepequeño", "Tojolabal", "Totonaco", "Triqui", "Tlahuica", "Tlapaneco", "Tseltal", "Tsotsil", "Yaqui", "Zapoteco", "Zoque", "P'urepecha", "Tarasco", "afar", "abjasio (o abjasiano)", "avéstico", "afrikáans", "akano", "amhárico", "aragonés", "árabe", "asamés", "avar (o ávaro)", "aimara", "azerí", "baskir", "bielorruso", "búlgaro", "bhoyapurí", "bislama", "bambara", "bengalí", "tibetano", "bretón", "bosnio", "catalán", "checheno", "chamorro", "corso", "cree", "checo", "eslavo eclesiástico antiguo", "chuvasio", "galés", "danés", "alemán", "maldivo (o dhivehi)", "dzongkha", "ewé", "griego (moderno)", "inglés", "esperanto", "español (o castellano)", "estonio", "euskera", "persa (o farsi)", "fula", "finés (o finlandés)", "fiyiano (o fiyi)", "feroés", "francés", "frisón (o frisio)", "irlandés (o gaélico)", "gaélico escocés", "gallego", "guaraní", "guyaratí (o gujaratí)", "manés (gaélico manés o de Isla de Man)", "hausa", "hebreo", "hindi (o hindú)", "hiri motu", "croata", "haitiano", "húngaro", "armenio", "herero", "interlingua", "indonesio", "occidental", "igbo", "yi de Sichuán", "iñupiaq", "ido", "islandés", "italiano", "inuktitut (o inuit)", "japonés", "javanés", "georgiano", "kongo (o kikongo)", "kikuyu", "kuanyama", "kazajo (o kazajio)", "groenlandés (o kalaallisut)", "camboyano (o jemer)", "canarés", "coreano", "kanuri", "cachemiro (o cachemir)", "kurdo", "komi", "córnico", "kirguís", "latín", "luxemburgués", "luganda", "limburgués", "lingala", "lao", "lituano", "luba-katanga (o chiluba)", "letón", "malgache (o malagasy)", "marshalés", "maorí", "macedonio", "malayalam", "mongol", "maratí", "malayo", "maltés", "birmano", "nauruano", "noruego bokmål", "ndebele del norte", "nepalí", "ndonga", "neerlandés (u holandés)", "nynorsk", "noruego", "ndebele del sur", "navajo", "chichewa", "occitano", "ojibwa", "oromo", "oriya", "osético (u osetio, u oseta)", "panyabí (o penyabi)", "pali", "polaco", "pastú (o pastún, o pashto)", "portugués", "quechua", "romanche", "kirundi", "rumano", "ruso", "ruandés (o kiñaruanda)", "sánscrito", "sardo", "sindhi", "sami septentrional", "sango", "cingalés", "eslovaco", "esloveno", "samoano", "shona", "somalí", "albanés", "serbio", "suazi (o swati, o siSwati)", "sesotho", "sundanés (o sondanés)", "sueco", "suajili", "tamil", "télugu", "tayiko", "tailandés", "tigriña", "turcomano", "tagalo", "setsuana", "tongano", "turco", "tsonga", "tártaro", "twi", "tahitiano", "uigur", "ucraniano", "urdu", "uzbeko", "venda", "vietnamita", "volapük", "valón", "wolof", "xhosa", "yídish (o yidis, o yiddish)", "yoruba", "chuan (o chuang, o zhuang)", "chino", "zulú"]}}, {"vocabulary": "srsc", "status": "UNKNOWN", "detail": "No complete raw vocabulary evidence"}, {"vocabulary": "openaire_organization_types", "status": "PASS", "detail": {"observed_values": ["", "FundingOrganization"], "expected_values": ["", "FundingOrganization"]}}, {"vocabulary": "mediumPairs", "status": "PASS", "detail": {"observed_values": ["Impreso", "Digital", "Audiovisual", "Sonoro"], "expected_values": ["Impreso", "Digital", "Audiovisual", "Sonoro"]}}, {"vocabulary": "licensePairs", "status": "PASS", "detail": {"observed_values": ["Creative Commons", "Dominio público", "Atribución 4.0 Internacional. https://creativecommons.org/licenses/by/4.0/", "Atribución-CompartirIgual 4.0 Internacional. https://creativecommons.org/licenses/by-sa/4.0/", "Atribución-NoComercial 4.0 Internacional. https://creativecommons.org/licenses/by-nc/4.0/", "Atribución-NoComercial-CompartirIgual 4.0 Internacional. https://creativecommons.org/licenses/by-nc-sa/4.0/", "Atribución-SinDerivadas 4.0 Internacional. https://creativecommons.org/licenses/by-nd/4.0/", "Atribución-NoComercial-SinDerivadas 4.0 Internacional. https://creativecommons.org/licenses/by-nc-nd/4.0/", "CC0 1.0 Universal. https://creativecommons.org/publicdomain/zero/1.0/", "Reconocimiento-Uso no Comercial-Sin Obras Derivadas 2.5 (Perú) https://creativecommons.org/licenses/by-nc-nd/2.5/pe/", "Autorisation HAL v1 https://about.hal.science/hal-authorisation-v1/#autorisation-hal-v1", "Copyright/Todos los derechos reservados", "Copyleft"], "expected_values": ["Creative Commons", "Dominio público", "Atribución 4.0 Internacional. https://creativecommons.org/licenses/by/4.0/", "Atribución-CompartirIgual 4.0 Internacional. https://creativecommons.org/licenses/by-sa/4.0/", "Atribución-NoComercial 4.0 Internacional. https://creativecommons.org/licenses/by-nc/4.0/", "Atribución-NoComercial-CompartirIgual 4.0 Internacional. https://creativecommons.org/licenses/by-nc-sa/4.0/", "Atribución-SinDerivadas 4.0 Internacional. https://creativecommons.org/licenses/by-nd/4.0/", "Atribución-NoComercial-SinDerivadas 4.0 Internacional. https://creativecommons.org/licenses/by-nc-nd/4.0/", "CC0 1.0 Universal. https://creativecommons.org/publicdomain/zero/1.0/", "Reconocimiento-Uso no Comercial-Sin Obras Derivadas 2.5 (Perú) https://creativecommons.org/licenses/by-nc-nd/2.5/pe/", "Autorisation HAL v1 https://about.hal.science/hal-authorisation-v1/#autorisation-hal-v1", "Copyright/Todos los derechos reservados", "Copyleft"]}}, {"vocabulary": "common_iso_languages", "status": "PASS", "detail": {"observed_values": ["", "en_US", "en", "es", "de", "fr", "it", "ja", "zh", "pt", "tr", "other"], "expected_values": ["", "en_US", "en", "es", "de", "fr", "it", "ja", "zh", "pt", "tr", "other"]}}, {"vocabulary": "openaire_version_types", "status": "PASS", "detail": {"observed_values": ["http://purl.org/coar/version/c_b1a7d7d4d402bcce", "http://purl.org/coar/version/c_71e4c1898caa6e32", "http://purl.org/coar/version/c_ab4af688f83e57aa", "http://purl.org/coar/version/c_fa2ee174bc00049f", "http://purl.org/coar/version/c_970fb48d4fbd8a85", "http://purl.org/coar/version/c_e19f295774971610", "http://purl.org/coar/version/c_dc82b40f9837b551", "http://purl.org/coar/version/c_be7fb7dd8ff6fe43"], "expected_values": ["http://purl.org/coar/version/c_b1a7d7d4d402bcce", "http://purl.org/coar/version/c_71e4c1898caa6e32", "http://purl.org/coar/version/c_ab4af688f83e57aa", "http://purl.org/coar/version/c_fa2ee174bc00049f", "http://purl.org/coar/version/c_970fb48d4fbd8a85", "http://purl.org/coar/version/c_e19f295774971610", "http://purl.org/coar/version/c_dc82b40f9837b551", "http://purl.org/coar/version/c_be7fb7dd8ff6fe43"]}}], "scope": "Literal values against preserved release; no normalization or fuzzy match"}
- **UNKNOWN** `active_collection_membership`: ["INVALID_ACTIVE_DEFINITION_EVIDENCE", "NO_ACTIVE_SUBMISSION_FORMS", "UNOBSERVABLE_SURFACE:active_submission_definition", "UNOBSERVABLE_SURFACE:active_submission_sections", "UNRESOLVED_ACTIVE_DEFINITION"]
- **NOT_TESTED** `full_migration_equivalence`: "Requires approved baseline, identity review and semantic validation"

## Warnings

- Collection not selected; active membership is NOT_TESTED
- INVALID_ACTIVE_DEFINITION_EVIDENCE
- NO_ACTIVE_SUBMISSION_FORMS
- UNOBSERVABLE_SURFACE:active_submission_definition
- UNOBSERVABLE_SURFACE:active_submission_sections
- UNRESOLVED_ACTIVE_DEFINITION
- Administrative account privileges do not authorize any data mutation.
- Global configured forms do not prove active collection membership.

## Configuration, endpoints and errors

```json
{
  "configuration": {
    "api_base": "https://www.iifl.unam.mx/server/api",
    "requested_collection_uuid": null,
    "limits": {
      "timeout": 10,
      "max_seconds": 180,
      "max_requests": 200,
      "max_pages": 50,
      "page_size": 100
    },
    "credentials_persisted": false,
    "allowed_methods": [
      "GET",
      "POST /authn/login once"
    ]
  },
  "endpoints": [
    {
      "surface": "metadata_schemas",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadataschemas?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.140667+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "87568ada9cb74d321809fa4dc6a3b88879da6f7b6613c456efff330df47fa45f",
      "bytes": 5318,
      "raw_file": "raw/0004-87568ada9cb74d321809fa4dc6a3b88879da6f7b6613c456efff330df47fa45f.response"
    },
    {
      "surface": "metadata_fields",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.241887+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "e98e075f389f0f164defc5c5c8d8682228886f8eb477e7a46a1b3b3ef32c8e2f",
      "bytes": 82475,
      "raw_file": "raw/0005-e98e075f389f0f164defc5c5c8d8682228886f8eb477e7a46a1b3b3ef32c8e2f.response"
    },
    {
      "surface": "metadata_fields",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields?page=1&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.368108+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "212d65d4bb59b63aa11edd72cba8adecafe2b83dab041b6eb3877d63fa0914af",
      "bytes": 83631,
      "raw_file": "raw/0006-212d65d4bb59b63aa11edd72cba8adecafe2b83dab041b6eb3877d63fa0914af.response"
    },
    {
      "surface": "metadata_fields",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields?page=2&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.446263+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "7cce942271b5e0c6498454a79593025eeca8d7202915cd5f29a83bf82a2473cd",
      "bytes": 90966,
      "raw_file": "raw/0007-7cce942271b5e0c6498454a79593025eeca8d7202915cd5f29a83bf82a2473cd.response"
    },
    {
      "surface": "metadata_fields_by_schema:dc",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=dc",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.524059+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "92b875b616097611a7976fe380dcd8a6425bf332b2c471327f631efdd2f3bdb5",
      "bytes": 82248,
      "raw_file": "raw/0008-92b875b616097611a7976fe380dcd8a6425bf332b2c471327f631efdd2f3bdb5.response"
    },
    {
      "surface": "metadata_fields_by_schema:dc",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=1&size=100&schema=dc",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.578974+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "4c97f066633f416a5bde20429ef00f7a1dc1dd66c6d47ea8e0633598bfce800a",
      "bytes": 6379,
      "raw_file": "raw/0009-4c97f066633f416a5bde20429ef00f7a1dc1dd66c6d47ea8e0633598bfce800a.response"
    },
    {
      "surface": "metadata_fields_by_schema:eperson",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=eperson",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.641422+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "c07b99fe348bfdcb3e0623bd4cb47eb317bc17e0aeffdbce559284f94d0bdf59",
      "bytes": 4911,
      "raw_file": "raw/0010-c07b99fe348bfdcb3e0623bd4cb47eb317bc17e0aeffdbce559284f94d0bdf59.response"
    },
    {
      "surface": "metadata_fields_by_schema:dspace",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=dspace",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.710073+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "fcc1336cdb22a6bae2d59c0f85fc26633cc6e6127e37db5ca5a7d8fa70a61513",
      "bytes": 11196,
      "raw_file": "raw/0011-fcc1336cdb22a6bae2d59c0f85fc26633cc6e6127e37db5ca5a7d8fa70a61513.response"
    },
    {
      "surface": "metadata_fields_by_schema:dcterms",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=dcterms",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.781632+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "ab23ace7a333f04e6a754def4845a43aec5386ef808e0c655db0e6779e03009c",
      "bytes": 45804,
      "raw_file": "raw/0012-ab23ace7a333f04e6a754def4845a43aec5386ef808e0c655db0e6779e03009c.response"
    },
    {
      "surface": "metadata_fields_by_schema:local",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=local",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.855216+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "c7ed8b9adce4cdaef457006e73360cc15c5ee0096286428a2bda7da72e4d0774",
      "bytes": 261,
      "raw_file": "raw/0013-c7ed8b9adce4cdaef457006e73360cc15c5ee0096286428a2bda7da72e4d0774.response"
    },
    {
      "surface": "metadata_fields_by_schema:relation",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=relation",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:16.934991+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "1fffc11f9167bb018681ad9d1021543c3873620c56b87bd3c33413738aa5e16e",
      "bytes": 51550,
      "raw_file": "raw/0014-1fffc11f9167bb018681ad9d1021543c3873620c56b87bd3c33413738aa5e16e.response"
    },
    {
      "surface": "metadata_fields_by_schema:person",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=person",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.015831+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "7064bbb16eccd2cee96dffd1df2ca425b2b9136638f25d525594f8a408fd9dba",
      "bytes": 14992,
      "raw_file": "raw/0015-7064bbb16eccd2cee96dffd1df2ca425b2b9136638f25d525594f8a408fd9dba.response"
    },
    {
      "surface": "metadata_fields_by_schema:project",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=project",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.173298+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "b2cfc5d7626be355a9b1c118f5cdf77e6dfdc7598bdc4d2966bed5cab3ceefe7",
      "bytes": 5799,
      "raw_file": "raw/0016-b2cfc5d7626be355a9b1c118f5cdf77e6dfdc7598bdc4d2966bed5cab3ceefe7.response"
    },
    {
      "surface": "metadata_fields_by_schema:organization",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=organization",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.251812+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "4ba2a2c6e0001dc3138737384298b7f0e8d637784da3e000c38da67c9c7488a8",
      "bytes": 7713,
      "raw_file": "raw/0017-4ba2a2c6e0001dc3138737384298b7f0e8d637784da3e000c38da67c9c7488a8.response"
    },
    {
      "surface": "metadata_fields_by_schema:periodical",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=periodical",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.323670+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "12abcaa38c2d522ca340fac0f2f138c707b614aeb69d33095b9726326845bf04",
      "bytes": 266,
      "raw_file": "raw/0018-12abcaa38c2d522ca340fac0f2f138c707b614aeb69d33095b9726326845bf04.response"
    },
    {
      "surface": "metadata_fields_by_schema:creativework",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=creativework",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.410037+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "ac4d3290cda4c9e816dc59e860a57bfb3e20f10e9d57d03dbf2e7db622c378a3",
      "bytes": 3648,
      "raw_file": "raw/0019-ac4d3290cda4c9e816dc59e860a57bfb3e20f10e9d57d03dbf2e7db622c378a3.response"
    },
    {
      "surface": "metadata_fields_by_schema:creativeworkseries",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=creativeworkseries",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.512127+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "159672d321ede3fa3aacb58e7dba915599e592045a45bdd1e403aca0c449cbd4",
      "bytes": 1336,
      "raw_file": "raw/0020-159672d321ede3fa3aacb58e7dba915599e592045a45bdd1e403aca0c449cbd4.response"
    },
    {
      "surface": "metadata_fields_by_schema:publicationissue",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=publicationissue",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.625181+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "80ecf96b4756af725c9e9b44284c7a73a6ca9de9e5c73ff0a9460bc12b65f83d",
      "bytes": 1168,
      "raw_file": "raw/0021-80ecf96b4756af725c9e9b44284c7a73a6ca9de9e5c73ff0a9460bc12b65f83d.response"
    },
    {
      "surface": "metadata_fields_by_schema:publicationvolume",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=publicationvolume",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.733675+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "f24c2f81cc57063a9d653d3b6a7ac08cd2ff41dcdc45e61da54f81e2dee283c4",
      "bytes": 1192,
      "raw_file": "raw/0022-f24c2f81cc57063a9d653d3b6a7ac08cd2ff41dcdc45e61da54f81e2dee283c4.response"
    },
    {
      "surface": "metadata_fields_by_schema:oaire",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=oaire",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.841506+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "aa215b8621c78295dba8b1a3a0a3cb7ce89e8be9119a9e33769a7e941467f01a",
      "bytes": 11938,
      "raw_file": "raw/0023-aa215b8621c78295dba8b1a3a0a3cb7ce89e8be9119a9e33769a7e941467f01a.response"
    },
    {
      "surface": "metadata_fields_by_schema:datacite",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=datacite",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:17.937815+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "6e6d0b1c3f9326325543018654086af71ad87ffb71f46fa2def469474a176b0b",
      "bytes": 1986,
      "raw_file": "raw/0024-6e6d0b1c3f9326325543018654086af71ad87ffb71f46fa2def469474a176b0b.response"
    },
    {
      "surface": "metadata_fields_by_schema:iiif",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=iiif",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:18.035461+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "827e288744289aad1a496d8576ff6cf18b1d31fd6a40b6cc2449bfadaa08fc68",
      "bytes": 7166,
      "raw_file": "raw/0025-827e288744289aad1a496d8576ff6cf18b1d31fd6a40b6cc2449bfadaa08fc68.response"
    },
    {
      "surface": "metadata_fields_by_schema:workflow",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/metadatafields/search/bySchema?page=0&size=100&schema=workflow",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:18.116698+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "b2302ef98d8156c481682553594e8a2201a72f5786f2862cd8fbc97325927472",
      "bytes": 1935,
      "raw_file": "raw/0026-b2302ef98d8156c481682553594e8a2201a72f5786f2862cd8fbc97325927472.response"
    },
    {
      "surface": "submission_definitions",
      "endpoint": "https://www.iifl.unam.mx/server/api/config/submissiondefinitions?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:18.255142+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "8d3416378b83cd3125e940e00d6a2c19b12c6f462d6aa8c746b47753b3c35df3",
      "bytes": 7560,
      "raw_file": "raw/0027-8d3416378b83cd3125e940e00d6a2c19b12c6f462d6aa8c746b47753b3c35df3.response"
    },
    {
      "surface": "submission_sections",
      "endpoint": "https://www.iifl.unam.mx/server/api/config/submissionsections?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:18.337872+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "f07bcf39228234836d6b3a1c67778c2ce53d344caaebb0511f70144bf7256ac9",
      "bytes": 19274,
      "raw_file": "raw/0028-f07bcf39228234836d6b3a1c67778c2ce53d344caaebb0511f70144bf7256ac9.response"
    },
    {
      "surface": "submission_forms",
      "endpoint": "https://www.iifl.unam.mx/server/api/config/submissionforms?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:18.442209+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "6f0b6dcad77ff623abaa5e1e5c927040936e08de469b8884712cc1802091b6c5",
      "bytes": 82531,
      "raw_file": "raw/0029-6f0b6dcad77ff623abaa5e1e5c927040936e08de469b8884712cc1802091b6c5.response"
    },
    {
      "surface": "collections",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/collections?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:18.932890+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "d0ff862f854d7229cc492f972636f9f6e154d5a6ad62d3e3ebfc783536240f34",
      "bytes": 305635,
      "raw_file": "raw/0030-d0ff862f854d7229cc492f972636f9f6e154d5a6ad62d3e3ebfc783536240f34.response"
    },
    {
      "surface": "collections",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/collections?page=1&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:19.644373+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "3282ca11642790e8736b951e45eea249f58d72482a640d5d81b1465aaad32bf3",
      "bytes": 306179,
      "raw_file": "raw/0031-3282ca11642790e8736b951e45eea249f58d72482a640d5d81b1465aaad32bf3.response"
    },
    {
      "surface": "collections",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/collections?page=2&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:20.078822+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "0c0450c4d7458d045d91603369b774510bb02d249971fc6678a8b90766f1abc5",
      "bytes": 306341,
      "raw_file": "raw/0032-0c0450c4d7458d045d91603369b774510bb02d249971fc6678a8b90766f1abc5.response"
    },
    {
      "surface": "collections",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/collections?page=3&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:20.621996+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "2dde1011a5efdadc4b109b2d21739a218215163f229a39f29696004634056007",
      "bytes": 306359,
      "raw_file": "raw/0033-2dde1011a5efdadc4b109b2d21739a218215163f229a39f29696004634056007.response"
    },
    {
      "surface": "collections",
      "endpoint": "https://www.iifl.unam.mx/server/api/core/collections?page=4&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:21.118391+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "9a83b5fcc9bb9648c67b9db9cebe0990437de0a9821a6292425c6561038270b2",
      "bytes": 168242,
      "raw_file": "raw/0034-9a83b5fcc9bb9648c67b9db9cebe0990437de0a9821a6292425c6561038270b2.response"
    },
    {
      "surface": "vocabularies",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:21.470865+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "1bd1fbf11125c87c1916db07d6416cdfd1ca1211bcf75b0b674f18eecc3a18f8",
      "bytes": 11143,
      "raw_file": "raw/0035-1bd1fbf11125c87c1916db07d6416cdfd1ca1211bcf75b0b674f18eecc3a18f8.response"
    },
    {
      "surface": "vocabulary_entries:selfDenominationPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/selfDenominationPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:21.705016+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "954b3095ad765ea5521509320d2bb3c47c1ad2a1e6f2ef6f4c1132291a76067a",
      "bytes": 3003,
      "raw_file": "raw/0036-954b3095ad765ea5521509320d2bb3c47c1ad2a1e6f2ef6f4c1132291a76067a.response"
    },
    {
      "surface": "vocabulary_entries:linguisticFamilyPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/linguisticFamilyPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:21.990280+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "796b6a05fe43b43590904e367e6539477d62bbecb7fc05eb19a037929ce9ffcc",
      "bytes": 5629,
      "raw_file": "raw/0037-796b6a05fe43b43590904e367e6539477d62bbecb7fc05eb19a037929ce9ffcc.response"
    },
    {
      "surface": "vocabulary_entries:educationLevelPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/educationLevelPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:22.219184+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "8daddcc3c333a189c4860763e8a8f3d463b7dc5cab926c0b00b0ce939ed3a934",
      "bytes": 1198,
      "raw_file": "raw/0038-8daddcc3c333a189c4860763e8a8f3d463b7dc5cab926c0b00b0ce939ed3a934.response"
    },
    {
      "surface": "vocabulary_entries:linguisticBranchPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/linguisticBranchPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:22.467236+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "7023311495551829562b3a06848891f9fa168632596e4cfde5576db710cea5d7",
      "bytes": 11529,
      "raw_file": "raw/0039-7023311495551829562b3a06848891f9fa168632596e4cfde5576db710cea5d7.response"
    },
    {
      "surface": "vocabulary_entries:extentTypePairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/extentTypePairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:22.708956+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "2df12528d9bbc264f861594c929e0c327f4d84da3629b483ea30874c7ae454da",
      "bytes": 1298,
      "raw_file": "raw/0040-2df12528d9bbc264f861594c929e0c327f4d84da3629b483ea30874c7ae454da.response"
    },
    {
      "surface": "vocabulary_entries:languageUsagePairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/languageUsagePairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:22.936588+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "dbff7360ac18acf1a134f295e56f178eeef15ca373bc9274b46aca4f0dc91639",
      "bytes": 717,
      "raw_file": "raw/0041-dbff7360ac18acf1a134f295e56f178eeef15ca373bc9274b46aca4f0dc91639.response"
    },
    {
      "surface": "vocabulary_entries:common_types",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/common_types/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:23.171263+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "f1aae4ea4de544edb18510a1ce2e2195484466d4c396bd5379d925746488a88c",
      "bytes": 3858,
      "raw_file": "raw/0042-f1aae4ea4de544edb18510a1ce2e2195484466d4c396bd5379d925746488a88c.response"
    },
    {
      "surface": "vocabulary_entries:accessRightsPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/accessRightsPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:23.403577+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "4eb5932131a3004e7df076e84751a6a1464c33d186b637ea0413091e963bdae5",
      "bytes": 928,
      "raw_file": "raw/0043-4eb5932131a3004e7df076e84751a6a1464c33d186b637ea0413091e963bdae5.response"
    },
    {
      "surface": "vocabulary_entries:iso6391Pairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/iso6391Pairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:23.649857+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "84cec11ed57b692809f3737284ef3f2cb9631eac9ed9407e248ecebdb6c7172e",
      "bytes": 12711,
      "raw_file": "raw/0044-84cec11ed57b692809f3737284ef3f2cb9631eac9ed9407e248ecebdb6c7172e.response"
    },
    {
      "surface": "vocabulary_entries:iso6391Pairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/iso6391Pairs/entries?page=1&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:23.791995+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "0227ee167f63f55061e104ff5abc8103cc0fd2f5215d6683b8ffb0073b10339f",
      "bytes": 12846,
      "raw_file": "raw/0045-0227ee167f63f55061e104ff5abc8103cc0fd2f5215d6683b8ffb0073b10339f.response"
    },
    {
      "surface": "vocabulary_entries:iso6391Pairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/iso6391Pairs/entries?page=2&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:24.214071+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "927b012ef01d4c1cafa48ce017ecbe076661167861d08124f585b7a33cb58f59",
      "bytes": 6934,
      "raw_file": "raw/0046-927b012ef01d4c1cafa48ce017ecbe076661167861d08124f585b7a33cb58f59.response"
    },
    {
      "surface": "vocabulary_entries:linguiscgroupPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/linguiscgroupPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:24.464315+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "b870628bb8ff77d0f4dbe7c39534333913766f17a65f8ffbefebbd5ffcae8de6",
      "bytes": 13871,
      "raw_file": "raw/0047-b870628bb8ff77d0f4dbe7c39534333913766f17a65f8ffbefebbd5ffcae8de6.response"
    },
    {
      "surface": "vocabulary_entries:linguiscgroupPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/linguiscgroupPairs/entries?page=1&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:24.598169+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "c93c2d300d57ca540c3335226e17a9c824d797283608ae0c7c755d12714a426a",
      "bytes": 14210,
      "raw_file": "raw/0048-c93c2d300d57ca540c3335226e17a9c824d797283608ae0c7c755d12714a426a.response"
    },
    {
      "surface": "vocabulary_entries:linguiscgroupPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/linguiscgroupPairs/entries?page=2&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:24.734975+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "25e9db1188d600892065c6d31e3ac8f9e655c69da7bae5bc8f58cec523bee214",
      "bytes": 7938,
      "raw_file": "raw/0049-25e9db1188d600892065c6d31e3ac8f9e655c69da7bae5bc8f58cec523bee214.response"
    },
    {
      "surface": "vocabulary_entries:openaire_types",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/openaire_types/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:24.982966+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "9e215364fdfa5b2aa624f072e8066bc4faa974ce82dafde4d243e885bde4a6f3",
      "bytes": 11002,
      "raw_file": "raw/0050-9e215364fdfa5b2aa624f072e8066bc4faa974ce82dafde4d243e885bde4a6f3.response"
    },
    {
      "surface": "vocabulary_entries:primaryClassificationPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/primaryClassificationPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:25.341634+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "4e945b06aa2efd24c5ae54f5855faab0af99dde822eb83946fde2aa72b86153a",
      "bytes": 1394,
      "raw_file": "raw/0051-4e945b06aa2efd24c5ae54f5855faab0af99dde822eb83946fde2aa72b86153a.response"
    },
    {
      "surface": "vocabulary_entries:languageTargetPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/languageTargetPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:25.602290+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "4dca0d6738f8e2caab6e769d32ed55be4690a1214a0aac9aabf775bacf8537ba",
      "bytes": 710,
      "raw_file": "raw/0052-4dca0d6738f8e2caab6e769d32ed55be4690a1214a0aac9aabf775bacf8537ba.response"
    },
    {
      "surface": "vocabulary_entries:genrePairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/genrePairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:25.935509+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "ffa6e5a60e232038a955e472b51311c040c5cd20ef19c1be5dc0736d1d1c6032",
      "bytes": 725,
      "raw_file": "raw/0053-ffa6e5a60e232038a955e472b51311c040c5cd20ef19c1be5dc0736d1d1c6032.response"
    },
    {
      "surface": "vocabulary_entries:topicsPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/topicsPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:26.203148+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "e8addfdb17b3658ff5e2dcf9a941869caf4415b1cc9c3dee842dfd2d9a68fddb",
      "bytes": 6329,
      "raw_file": "raw/0054-e8addfdb17b3658ff5e2dcf9a941869caf4415b1cc9c3dee842dfd2d9a68fddb.response"
    },
    {
      "surface": "vocabulary_entries:registeredLanguagePairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/registeredLanguagePairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:26.529829+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "ce2bda62fb47e65ec70ece30e8eb5cf6df7bc10c60db1d94c16b2bd6c0e87b43",
      "bytes": 13886,
      "raw_file": "raw/0055-ce2bda62fb47e65ec70ece30e8eb5cf6df7bc10c60db1d94c16b2bd6c0e87b43.response"
    },
    {
      "surface": "vocabulary_entries:registeredLanguagePairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/registeredLanguagePairs/entries?page=1&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:26.753568+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "be5c2582e53f4f89477ae9bcc8c9e8111d3560a68752e1db87adb17c9aa41db3",
      "bytes": 14673,
      "raw_file": "raw/0056-be5c2582e53f4f89477ae9bcc8c9e8111d3560a68752e1db87adb17c9aa41db3.response"
    },
    {
      "surface": "vocabulary_entries:registeredLanguagePairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/registeredLanguagePairs/entries?page=2&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:26.894213+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "b0d82edbc6bc27116351da37034d6916ad25872cbe2618f6aa2091f2de8f2175",
      "bytes": 8103,
      "raw_file": "raw/0057-b0d82edbc6bc27116351da37034d6916ad25872cbe2618f6aa2091f2de8f2175.response"
    },
    {
      "surface": "vocabulary_entries:srsc",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/srsc/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:27.173989+00:00",
      "http_status": 422,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "5f2ca241590ebac0c7900f21bece11f663463468be22191cac158c04efa24b33",
      "bytes": 191,
      "raw_file": "raw/0058-5f2ca241590ebac0c7900f21bece11f663463468be22191cac158c04efa24b33.response"
    },
    {
      "surface": "vocabulary_top:srsc",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularyEntryDetails/search/top?page=0&size=100&vocabulary=srsc",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:27.655831+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "f9f54adde7524fa4787c781bb1f2a05ee80789b62931c3c87d7e703abc9e76d2",
      "bytes": 9455,
      "raw_file": "raw/0059-f9f54adde7524fa4787c781bb1f2a05ee80789b62931c3c87d7e703abc9e76d2.response"
    },
    {
      "surface": "vocabulary_entries:openaire_organization_types",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/openaire_organization_types/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:27.937707+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "65fe87d89a8eef2401fdf38335b69464d33674cbc66b5b60fd912c0de829c5ee",
      "bytes": 593,
      "raw_file": "raw/0060-65fe87d89a8eef2401fdf38335b69464d33674cbc66b5b60fd912c0de829c5ee.response"
    },
    {
      "surface": "vocabulary_entries:mediumPairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/mediumPairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:28.210520+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "74f7c88fdc490a4f182fcdf24d4d1a43146a2a337ba4ecf22d41044756e9fe94",
      "bytes": 824,
      "raw_file": "raw/0061-74f7c88fdc490a4f182fcdf24d4d1a43146a2a337ba4ecf22d41044756e9fe94.response"
    },
    {
      "surface": "vocabulary_entries:licensePairs",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/licensePairs/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:28.496675+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "d982a197bf3ecfa274a540a0a7e717df0d126a29e4a5bd7eaedbde1a2599080a",
      "bytes": 3516,
      "raw_file": "raw/0062-d982a197bf3ecfa274a540a0a7e717df0d126a29e4a5bd7eaedbde1a2599080a.response"
    },
    {
      "surface": "vocabulary_entries:common_iso_languages",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/common_iso_languages/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:28.793604+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "591505c78e3c781789cf08df9834881d9d618987a546d46c42a53d71785fdde0",
      "bytes": 1826,
      "raw_file": "raw/0063-591505c78e3c781789cf08df9834881d9d618987a546d46c42a53d71785fdde0.response"
    },
    {
      "surface": "vocabulary_entries:openaire_version_types",
      "endpoint": "https://www.iifl.unam.mx/server/api/submission/vocabularies/openaire_version_types/entries?page=0&size=100",
      "method": "GET",
      "captured_at": "2026-10-21T05:40:29.070937+00:00",
      "http_status": 200,
      "content_type": "application/hal+json;charset=UTF-8",
      "sha256": "03788d8645c6b17fac5946383dae4f787db5bf1138ed3552e13df8aefbdb9d83",
      "bytes": 1786,
      "raw_file": "raw/0064-03788d8645c6b17fac5946383dae4f787db5bf1138ed3552e13df8aefbdb9d83.response"
    }
  ],
  "errors": [
    {
      "surface": "vocabulary_entries:srsc",
      "code": "invalid_response",
      "http_status": 422
    }
  ]
}
```
