# Curated site data for Do Events.
# Long-form stories & highlights come from each film's YouTube description (youtube.json).

SITE = {
    "name": "Do Events",
    "name_ar": "دو للمناسبات",
    "tagline": "Your event is reality.",
    "tagline_ar": "مناسبتك حقيقة",
    "address": "23 July Street, Way No. 13408, Salalah, Oman",
    "address_ar": "شارع 23 يوليو، طريق 13408، صلالة",
    "phone": "+968 9551 3848",
    "phone_href": "tel:+96895513848",
    "whatsapp": "+968 9562 4666",
    "whatsapp_href": "https://wa.me/96895624666",
    "instagram": "https://www.instagram.com/do.events_oman/",
    "instagram_handle": "@do.events_oman",
    "youtube": "https://www.youtube.com/@DoEvents",
    "chocolate": "@do_chocolate",
    "map_link": "https://share.google/28hxAO8yYmiMNq1IO",
    "map_embed": "https://maps.google.com/maps?q=237Q%2BHC%20Salalah%2C%20Oman&z=16&output=embed",
    "showreel": "showreel",
    "showreel_yt": "A_9xjlTUJOw",
}

CATS = {
    "wedding": "Weddings",
    "engagement": "Engagements",
    "corporate": "Corporate & Festivals",
}

# slug, youtube id, category, display title, client line, venue, short excerpt
CASES = [
    dict(slug="theater-festival", yt="ov8ZNYHqf3Q", cat="corporate",
         title="Dhofar International Theater Festival", short="DITFest 2026",
         client="Dhofar International Theater Festival · 2nd Edition", venue="Salalah, Dhofar", year="2026",
         excerpt="Illuminated maroon arches, a red carpet and a gala dinner for one of the region's leading cultural events."),
    dict(slug="theater-red-carpet", yt="n0eROqDd9nU", cat="corporate",
         title="DITFest Red Carpet Night", short="Red Carpet",
         client="Dhofar International Theater Festival", venue="Salalah, Dhofar", year="2026",
         excerpt="VIP arrivals, press walls and an open-air dinner leading to the main-stage ceremony."),
    dict(slug="mymoon-launch", yt="SCAKBtfRPn8", cat="corporate",
         title="Mymoon Perfume Launch", short="Mymoon",
         client="Mymoon Perfumes", venue="Oman", year="",
         excerpt="A luxury fragrance launch blending elegance with authentic Omani identity."),
    dict(slug="triple-wedding", yt="5I26wbjP98E", cat="wedding",
         title="Emerald & Rust Triple Wedding", short="Triple Wedding",
         client="Abdullah & Esraa · Asim & Rahaf · Mohammed & Ghala", venue="Salalah", year="",
         excerpt="One night, three love stories — set inside a vintage palace garden."),
    dict(slug="royal-blue", yt="JYo2PGopQqw", cat="wedding",
         title="Royal Blue Wedding", short="Royal Blue",
         client="Saqr & Nada", venue="Salalah", year="",
         excerpt="A starry royal-blue ballroom with a giant LED stage and a mirror-black runway."),
    dict(slug="beach-engagement", yt="bBPpiRfQi5g", cat="engagement",
         title="Beach Engagement", short="Sahil & Hana",
         client="Sahil & Hana", venue="Salalah Beach", year="",
         excerpt="A clear-top marquee on the Salalah shoreline, dressed in navy and champagne."),
    dict(slug="red-rose", yt="2sep255v2Xk", cat="wedding",
         title="Red Rose & Turquoise Wedding", short="Red Rose",
         client="Almarhoon Wedding · Abdullah & Dalia", venue="Salalah", year="2026",
         excerpt="A giant rose sculpture, turquoise velvet and a glossy black runway."),
    dict(slug="white-millennium", yt="ZGHwkhYWJM8", cat="wedding",
         title="White Luxury Wedding", short="All White",
         client="AlRawas Wedding", venue="Millennium Resort Salalah", year="",
         excerpt="The Millennium Resort ballroom transformed into a cascading all-white dream."),
    dict(slug="albarami-lounge", yt="9xPSXcoOFL4", cat="wedding",
         title="Luxury Lounge Wedding", short="Al Barami",
         client="Al Barami Wedding", venue="Salalah", year="",
         excerpt="Sculpted light, a cascading crystal chandelier and an illuminated black floor."),
    dict(slug="gold-purple", yt="ewvGzIO_NNQ", cat="wedding",
         title="Gold & Purple Wedding", short="Al Gafri",
         client="Al Gafri Wedding", venue="Salalah", year="",
         excerpt="A regal setting where the shine of gold meets the softness of purple."),
    dict(slug="green-wedding", yt="Bmqu5iCaTnY", cat="wedding",
         title="Green Theme Wedding", short="AlShanfari",
         client="AlShanfari Wedding", venue="Salalah", year="",
         excerpt="A ceiling of lush vines, golden light frames and flying birds."),
    dict(slug="garden-wedding", yt="YwdYmS8Hxp4", cat="wedding",
         title="Enchanted Garden Wedding", short="Garden",
         client="Almarhoon & Alshanfari Wedding", venue="Salalah", year="",
         excerpt="Crystal birds in flight, lily-of-the-valley lamps and a garden full of softness."),
    dict(slug="altayar-kosha", yt="l9bjSkndycY", cat="wedding",
         title="Luxury Kosha Wedding", short="AlTayar",
         client="AlTayar Wedding", venue="Salalah", year="",
         excerpt="Blush blossoms suspended above a curved white kosha and sculpted frames."),
    dict(slug="alyaffi-alrawas", yt="xam7vGjXABk", cat="wedding",
         title="Premium Wedding Décor", short="Alyaffi & AlRawas",
         client="Alyaffi & AlRawas Wedding", venue="Salalah", year="",
         excerpt="Flowing white canopies, golden butterflies and a complete premium hall."),
    dict(slug="fatmah-binzain", yt="0mdOFZG83js", cat="wedding",
         title="Crystal Luxury Wedding", short="Bin Zain",
         client="Ali & Fatmah Bin Zain", venue="Salalah", year="2022",
         excerpt="Towering crystal columns and blossoms over a marble-blue backdrop."),
    dict(slug="waves-wedding", yt="DWjS_RoMTfk", cat="wedding",
         title="Waves Theme Wedding", short="Waves",
         client="AlRawas Wedding", venue="Salalah", year="2021",
         excerpt="Tables that flow in curved rings like gentle ocean waves."),
    dict(slug="mirror-wedding", yt="VP9lmf3peW4", cat="wedding",
         title="Mirror Theme Wedding", short="Mirror",
         client="AlRawas Wedding", venue="Salalah", year="",
         excerpt="A mirror-themed hall that reflects elegance from every angle."),
    dict(slug="table-hospitality", yt="f0hboc6ERsM", cat="wedding",
         title="Table & Hospitality Styling", short="Al Rawas Feras",
         client="Al Rawas Feras Wedding", venue="Millennium Resort Salalah", year="",
         excerpt="Every table made part of the celebration — candlelight, crystal and lilac florals."),
    dict(slug="stage-runway", yt="FUYcq-IonV0", cat="wedding",
         title="Stage & Runway Wedding", short="Runway",
         client="Private Wedding", venue="Salalah", year="",
         excerpt="A glossy white runway leading to a sculptural kosha — modern luxury with softness."),
    dict(slug="red-blush", yt="14jtpcJeNn8", cat="wedding",
         title="Red & Blush Wedding", short="Red & Blush",
         client="Private Wedding", venue="Salalah", year="",
         excerpt="Warm reds and blush pinks around a sculpted white kosha chair."),
    dict(slug="blush-pink", yt="tFcK3MbUtUk", cat="wedding",
         title="Blush Pink Wedding", short="Bin Sabaar",
         client="Bin Sabaar Wedding", venue="Salalah", year="",
         excerpt="Peach blossoms on crystal strands and champagne ribbons in a dreamy blush hall."),
]

# Slugs with a local film (all except Mirror, which plays from YouTube)
NO_LOCAL_FILM = {"mirror-wedding"}

FEATURED = ["theater-festival", "triple-wedding", "mymoon-launch", "royal-blue", "beach-engagement"]

# From the company profile
NOTABLE = [
    ("Working Women's Day", "Under the patronage of H.H. Sayyid Marwan bin Turki Al Said, Governor of Dhofar"),
    ("International Green Energy Conference 2023", "Under the patronage of H.H. Sayyid Marwan bin Turki Al Said, Governor of Dhofar"),
    ("Arab Center for Prosthetics — 3rd Anniversary", "Under the patronage of H.E. Mohammed bin Saif Al Busaidi, Wali of Salalah"),
    ("Innovation Vision", "Organised with the Ministry of Commerce, Industry & Investment Promotion"),
    ("Ministry of Education — 2024", "Teachers' Day, Holy Qur'an Honouring Ceremony and Outstanding Students' Honouring"),
    ("Future Vision Conference", "Dhofar University, under the patronage of H.E. Dr. Ahmed Al Ghassani, Chairman of Dhofar Municipality"),
    ("OQ", "Three corporate events delivered for OQ"),
    ("Dhofar International Theater Festival 2026", "Full venue design, red carpet and production for the 2nd edition"),
]

MARQUEE_CLIENTS = [
    "Dhofar International Theater Festival", "Ministry of Education", "OQ", "Dhofar University",
    "Millennium Resort Salalah", "Mymoon Perfumes", "Green Energy Conference 2023", "Dhofar Championship",
]

# ---------------------------------------------------------------- Arabic
SITE_AR = {
    "address": "شارع 23 يوليو، طريق رقم 13408، صلالة، سلطنة عُمان",
}

CATS_AR = {
    "wedding": "حفلات الزفاف",
    "engagement": "حفلات الخطوبة",
    "corporate": "الفعاليات والمهرجانات",
}

# slug: (title, client, venue, excerpt, short)
CASES_AR = {
    "theater-festival": ("مهرجان ظفار الدولي للمسرح", "مهرجان ظفار الدولي للمسرح · النسخة الثانية", "صلالة، ظفار",
                         "أقواس عنابية مضيئة وسجادة حمراء وعشاء احتفالي لواحد من أبرز الفعاليات الثقافية في المنطقة.", "المهرجان 2026"),
    "theater-red-carpet": ("ليلة السجادة الحمراء", "مهرجان ظفار الدولي للمسرح", "صلالة، ظفار",
                           "وصول كبار الضيوف وجدران إعلامية وعشاء في الهواء الطلق وصولاً إلى حفل المسرح الرئيسي.", "السجادة الحمراء"),
    "mymoon-launch": ("حفل تدشين عطر ماي مون", "عطور ماي مون", "سلطنة عُمان",
                      "إطلاق فاخر لعلامة عطرية يمزج بين الأناقة والهوية العُمانية الأصيلة.", "ماي مون"),
    "triple-wedding": ("الزفاف الثلاثي بالأخضر الزمردي", "عبدالله وإسراء · عاصم ورهف · محمد وغلا", "صلالة",
                       "ليلة واحدة وثلاث قصص فرح — في أجواء حديقة قصر كلاسيكية.", "الزفاف الثلاثي"),
    "royal-blue": ("زفاف الأزرق الملكي", "صقر وندى", "صلالة",
                   "قاعة بالأزرق الملكي تتلألأ كليلة مرصّعة بالنجوم، بشاشة عرض ضخمة وممر أسود كالمرآة.", "الأزرق الملكي"),
    "beach-engagement": ("خطوبة على الشاطئ", "ساهل وهناء", "شاطئ صلالة",
                         "خيمة شفافة على شاطئ صلالة بستائر كحلية وشامبين منسدلة.", "ساهل وهناء"),
    "red-rose": ("زفاف الورد الأحمر والفيروزي", "أفراح المرهون · عبدالله وداليا", "صلالة",
                 "وردة حمراء عملاقة وستائر مخملية فيروزية وممر أسود لامع.", "الورد الأحمر"),
    "white-millennium": ("الزفاف الأبيض الفاخر", "أفراح الرواس", "منتجع ميلينيوم صلالة",
                         "قاعة منتجع ميلينيوم تتحوّل إلى حلم أبيض متكامل بثريات كريستالية متدفقة.", "الأبيض"),
    "albarami-lounge": ("زفاف الجلسات الفاخرة", "أفراح البرعمي", "صلالة",
                        "إضاءة منحوتة وثريا كريستالية متدفقة وأرضية سوداء مضيئة.", "البرعمي"),
    "gold-purple": ("زفاف الذهبي والبنفسجي", "زفاف الغافري", "صلالة",
                    "أجواء ملكية يلتقي فيها بريق الذهب بنعومة البنفسجي.", "الغافري"),
    "green-wedding": ("الزفاف بالثيم الأخضر", "زفاف الشنفري", "صلالة",
                      "سقف من الأغصان الخضراء الكثيفة وإطارات ذهبية مضيئة وطيور محلّقة.", "الشنفري"),
    "garden-wedding": ("زفاف الحديقة الساحرة", "زفاف المرهون والشنفري", "صلالة",
                       "طيور كريستالية محلّقة وفوانيس زنبق الوادي وحديقة مليئة بالنعومة.", "الحديقة"),
    "altayar-kosha": ("زفاف الكوشة الفاخرة", "زفاف الطيار", "صلالة",
                      "زهور وردية معلّقة فوق كوشة بيضاء منحنية وإطارات منحوتة.", "الطيار"),
    "alyaffi-alrawas": ("ديكور الزفاف الفاخر", "زفاف اليافعي والرواس", "صلالة",
                        "مظلات بيضاء منسابة وفراشات ذهبية وقاعة متكاملة بلمسات فاخرة.", "اليافعي والرواس"),
    "fatmah-binzain": ("زفاف الكريستال الفاخر", "علي وفاطمة بن زين", "صلالة",
                       "أعمدة كريستالية شاهقة وزهور فوق خلفية بلون الرخام الأزرق.", "بن زين"),
    "waves-wedding": ("زفاف ثيم الأمواج", "زفاف الرواس", "صلالة",
                      "طاولات تنساب في حلقات منحنية كأمواج البحر الهادئة.", "الأمواج"),
    "mirror-wedding": ("زفاف ثيم المرايا", "زفاف الرواس", "صلالة",
                       "قاعة بثيم المرايا تعكس الأناقة من كل زاوية.", "المرايا"),
    "table-hospitality": ("تنسيق الطاولات والضيافة", "زفاف الرواس فراس", "منتجع ميلينيوم صلالة",
                          "كل طاولة جزء من جمال الحفل — شموع وكريستال وزهور ليلكية.", "الرواس فراس"),
    "stage-runway": ("زفاف الكوشة والممر", "حفل زفاف خاص", "صلالة",
                     "ممر أبيض لامع يقود إلى كوشة منحوتة — فخامة عصرية بلمسة ناعمة.", "الممر"),
    "red-blush": ("زفاف الأحمر والوردي", "حفل زفاف خاص", "صلالة",
                  "درجات الأحمر الدافئ والوردي حول كوشة بمقعد أبيض منحوت.", "الأحمر والوردي"),
    "blush-pink": ("زفاف الوردي الهادئ", "أفراح بن صبعار", "صلالة",
                   "زهور الخوخ على خيوط كريستالية وأشرطة شامبين في قاعة وردية حالمة.", "بن صبعار"),
}

NOTABLE_AR = [
    ("فعالية يوم المرأة العاملة", "تحت رعاية صاحب السمو السيد مروان بن تركي آل سعيد، محافظ ظفار"),
    ("المؤتمر الدولي للطاقة الخضراء 2023", "تحت رعاية صاحب السمو السيد مروان بن تركي آل سعيد، محافظ ظفار"),
    ("الذكرى الثالثة لتأسيس المركز العربي للأطراف الصناعية", "تحت رعاية سعادة محمد بن سيف البوسعيدي، والي صلالة"),
    ("رؤية الابتكار", "بالتنظيم مع وزارة التجارة والصناعة وترويج الاستثمار"),
    ("وزارة التربية والتعليم — 2024", "يوم المعلم، وحفل تكريم القرآن الكريم، وحفل تكريم الطلبة المجيدين"),
    ("مؤتمر رؤية المستقبل", "جامعة ظفار، تحت رعاية سعادة الدكتور أحمد الغساني، رئيس بلدية ظفار"),
    ("OQ", "ثلاث فعاليات نُظّمت لشركة OQ"),
    ("مهرجان ظفار الدولي للمسرح 2026", "تصميم المكان والسجادة الحمراء والإنتاج الكامل للنسخة الثانية"),
]

MARQUEE_CLIENTS_AR = [
    "مهرجان ظفار الدولي للمسرح", "وزارة التربية والتعليم", "OQ", "جامعة ظفار",
    "منتجع ميلينيوم صلالة", "عطور ماي مون", "مؤتمر الطاقة الخضراء 2023", "بطولة ظفار",
]

# Client / partner logos for the hero strip. Drop the logo file into assets/img/clients/
# with the name below (SVG preferred, transparent PNG fine). Brands without a file are left out of the strip.
CLIENT_LOGOS = [
    dict(key="ditfest",          logo="ditfest",          en="Dhofar International Theater Festival", ar="مهرجان ظفار الدولي للمسرح"),
    dict(key="moe",              logo="moe-oman",         en="Ministry of Education",                 ar="وزارة التربية والتعليم"),
    dict(key="oq",               logo="oq",               en="OQ",                                    ar="OQ"),
    dict(key="du",               logo="dhofar-university", en="Dhofar University",                    ar="جامعة ظفار"),
    dict(key="millennium",       logo="millennium-salalah", en="Millennium Resort Salalah",            ar="منتجع ميلينيوم صلالة"),
    dict(key="mymoon",           logo="mymoon",           en="Mymoon Perfumes",                       ar="عطور ماي مون"),
    dict(key="green-energy",     logo="green-energy-2023", en="Green Energy Conference 2023",         ar="مؤتمر الطاقة الخضراء 2023"),
    dict(key="dhofar-champ",     logo="dhofar-championship", en="Dhofar Championship",                 ar="بطولة ظفار"),
]
