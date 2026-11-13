# ruff: noqa: E501 - generated data rows
"""
The countries of the world in the four languages of the site — ISO 3166-1 alpha-2 codes and their CLDR names
(V5.12 W2, lane B; DECISIONS §5.7: «The country lists come from CLDR (Unicode licence), in fr/it/en/ar, generated
once into apps/core/countries.py. No new dependency is added.»).

GENERATED ONCE from the CLDR 48.0 data that ICU 78.2 ships (Node's ``Intl.DisplayNames``, type
``region``), every two-letter region CLDR names, without the groupings and reservations that are not a country
(EU, EZ, UN, QO, ZZ, the exceptional reservations AC, CP, CQ, DG, EA, IC, TA and the withdrawn codes). Licence:
the Unicode License v3, ``apps/core/LICENSE-CLDR.txt``. Pure Python: forms, the rules' facts and the tests read it.

A person's nationality and country of residence are stored as the code (the rules engine reads ISO codes: rules.engine
``nationality`` / ``residence_country``); the name is the visitor's language at render time.
"""

from __future__ import annotations

import unicodedata

CLDR_VERSION = "48.0"
LANGUAGES = ("fr", "it", "en", "ar")

#: (code, fr, it, en, ar)
COUNTRIES: tuple[tuple[str, str, str, str, str], ...] = (
    ('AD', 'Andorre', 'Andorra', 'Andorra', 'أندورا'),
    ('AE', 'Émirats arabes unis', 'Emirati Arabi Uniti', 'United Arab Emirates', 'الإمارات العربية المتحدة'),
    ('AF', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'أفغانستان'),
    ('AG', 'Antigua-et-Barbuda', 'Antigua e Barbuda', 'Antigua & Barbuda', 'أنتيغوا وبربودا'),
    ('AI', 'Anguilla', 'Anguilla', 'Anguilla', 'أنغويلا'),
    ('AL', 'Albanie', 'Albania', 'Albania', 'ألبانيا'),
    ('AM', 'Arménie', 'Armenia', 'Armenia', 'أرمينيا'),
    ('AO', 'Angola', 'Angola', 'Angola', 'أنغولا'),
    ('AQ', 'Antarctique', 'Antartide', 'Antarctica', 'أنتاركتيكا'),
    ('AR', 'Argentine', 'Argentina', 'Argentina', 'الأرجنتين'),
    ('AS', 'Samoa américaines', 'Samoa Americane', 'American Samoa', 'ساموا الأمريكية'),
    ('AT', 'Autriche', 'Austria', 'Austria', 'النمسا'),
    ('AU', 'Australie', 'Australia', 'Australia', 'أستراليا'),
    ('AW', 'Aruba', 'Aruba', 'Aruba', 'أروبا'),
    ('AX', 'Îles Åland', 'Isole Åland', 'Åland Islands', 'جزر آلاند'),
    ('AZ', 'Azerbaïdjan', 'Azerbaigian', 'Azerbaijan', 'أذربيجان'),
    ('BA', 'Bosnie-Herzégovine', 'Bosnia ed Erzegovina', 'Bosnia & Herzegovina', 'البوسنة والهرسك'),
    ('BB', 'Barbade', 'Barbados', 'Barbados', 'بربادوس'),
    ('BD', 'Bangladesh', 'Bangladesh', 'Bangladesh', 'بنغلاديش'),
    ('BE', 'Belgique', 'Belgio', 'Belgium', 'بلجيكا'),
    ('BF', 'Burkina Faso', 'Burkina Faso', 'Burkina Faso', 'بوركينا فاسو'),
    ('BG', 'Bulgarie', 'Bulgaria', 'Bulgaria', 'بلغاريا'),
    ('BH', 'Bahreïn', 'Bahrein', 'Bahrain', 'البحرين'),
    ('BI', 'Burundi', 'Burundi', 'Burundi', 'بوروندي'),
    ('BJ', 'Bénin', 'Benin', 'Benin', 'بنين'),
    ('BL', 'Saint-Barthélemy', 'Saint-Barthélemy', 'St. Barthélemy', 'سان بارتليمي'),
    ('BM', 'Bermudes', 'Bermuda', 'Bermuda', 'برمودا'),
    ('BN', 'Brunei', 'Brunei', 'Brunei', 'بروناي'),
    ('BO', 'Bolivie', 'Bolivia', 'Bolivia', 'بوليفيا'),
    ('BQ', 'Pays-Bas caribéens', 'Caraibi Olandesi', 'Caribbean Netherlands', 'هولندا الكاريبية'),
    ('BR', 'Brésil', 'Brasile', 'Brazil', 'البرازيل'),
    ('BS', 'Bahamas', 'Bahamas', 'Bahamas', 'جزر البهاما'),
    ('BT', 'Bhoutan', 'Bhutan', 'Bhutan', 'بوتان'),
    ('BV', 'Île Bouvet', 'Isola Bouvet', 'Bouvet Island', 'جزيرة بوفيه'),
    ('BW', 'Botswana', 'Botswana', 'Botswana', 'بوتسوانا'),
    ('BY', 'Biélorussie', 'Bielorussia', 'Belarus', 'بيلاروس'),
    ('BZ', 'Belize', 'Belize', 'Belize', 'بليز'),
    ('CA', 'Canada', 'Canada', 'Canada', 'كندا'),
    ('CC', 'Îles Cocos', 'Isole Cocos (Keeling)', 'Cocos (Keeling) Islands', 'جزر كوكوس (كيلينغ)'),
    ('CD', 'Congo-Kinshasa', 'Congo - Kinshasa', 'Congo - Kinshasa', 'الكونغو - كينشاسا'),
    ('CF', 'République centrafricaine', 'Repubblica Centrafricana', 'Central African Republic', 'جمهورية أفريقيا الوسطى'),
    ('CG', 'Congo-Brazzaville', 'Congo-Brazzaville', 'Congo - Brazzaville', 'الكونغو - برازافيل'),
    ('CH', 'Suisse', 'Svizzera', 'Switzerland', 'سويسرا'),
    ('CI', 'Côte d’Ivoire', 'Costa d’Avorio', 'Côte d’Ivoire', 'ساحل العاج'),
    ('CK', 'Îles Cook', 'Isole Cook', 'Cook Islands', 'جزر كوك'),
    ('CL', 'Chili', 'Cile', 'Chile', 'تشيلي'),
    ('CM', 'Cameroun', 'Camerun', 'Cameroon', 'الكاميرون'),
    ('CN', 'Chine', 'Cina', 'China', 'الصين'),
    ('CO', 'Colombie', 'Colombia', 'Colombia', 'كولومبيا'),
    ('CR', 'Costa Rica', 'Costa Rica', 'Costa Rica', 'كوستاريكا'),
    ('CU', 'Cuba', 'Cuba', 'Cuba', 'كوبا'),
    ('CV', 'Cap-Vert', 'Capo Verde', 'Cape Verde', 'الرأس الأخضر'),
    ('CW', 'Curaçao', 'Curaçao', 'Curaçao', 'كوراساو'),
    ('CX', 'Île Christmas', 'Isola Christmas', 'Christmas Island', 'جزيرة كريسماس'),
    ('CY', 'Chypre', 'Cipro', 'Cyprus', 'قبرص'),
    ('CZ', 'Tchéquie', 'Cechia', 'Czechia', 'التشيك'),
    ('DE', 'Allemagne', 'Germania', 'Germany', 'ألمانيا'),
    ('DJ', 'Djibouti', 'Gibuti', 'Djibouti', 'جيبوتي'),
    ('DK', 'Danemark', 'Danimarca', 'Denmark', 'الدانمرك'),
    ('DM', 'Dominique', 'Dominica', 'Dominica', 'دومينيكا'),
    ('DO', 'République dominicaine', 'Repubblica Dominicana', 'Dominican Republic', 'جمهورية الدومينيكان'),
    ('DZ', 'Algérie', 'Algeria', 'Algeria', 'الجزائر'),
    ('EC', 'Équateur', 'Ecuador', 'Ecuador', 'الإكوادور'),
    ('EE', 'Estonie', 'Estonia', 'Estonia', 'إستونيا'),
    ('EG', 'Égypte', 'Egitto', 'Egypt', 'مصر'),
    ('EH', 'Sahara occidental', 'Sahara Occidentale', 'Western Sahara', 'الصحراء الغربية'),
    ('ER', 'Érythrée', 'Eritrea', 'Eritrea', 'إريتريا'),
    ('ES', 'Espagne', 'Spagna', 'Spain', 'إسبانيا'),
    ('ET', 'Éthiopie', 'Etiopia', 'Ethiopia', 'إثيوبيا'),
    ('FI', 'Finlande', 'Finlandia', 'Finland', 'فنلندا'),
    ('FJ', 'Fidji', 'Figi', 'Fiji', 'فيجي'),
    ('FK', 'Îles Malouines', 'Isole Falkland', 'Falkland Islands', 'جزر فوكلاند'),
    ('FM', 'Micronésie', 'Micronesia', 'Micronesia', 'ميكرونيزيا'),
    ('FO', 'Îles Féroé', 'Isole Fær Øer', 'Faroe Islands', 'جزر فارو'),
    ('FR', 'France', 'Francia', 'France', 'فرنسا'),
    ('GA', 'Gabon', 'Gabon', 'Gabon', 'الغابون'),
    ('GB', 'Royaume-Uni', 'Regno Unito', 'United Kingdom', 'المملكة المتحدة'),
    ('GD', 'Grenade', 'Grenada', 'Grenada', 'غرينادا'),
    ('GE', 'Géorgie', 'Georgia', 'Georgia', 'جورجيا'),
    ('GF', 'Guyane française', 'Guyana Francese', 'French Guiana', 'غويانا الفرنسية'),
    ('GG', 'Guernesey', 'Guernsey', 'Guernsey', 'غيرنزي'),
    ('GH', 'Ghana', 'Ghana', 'Ghana', 'غانا'),
    ('GI', 'Gibraltar', 'Gibilterra', 'Gibraltar', 'جبل طارق'),
    ('GL', 'Groenland', 'Groenlandia', 'Greenland', 'غرينلاند'),
    ('GM', 'Gambie', 'Gambia', 'Gambia', 'غامبيا'),
    ('GN', 'Guinée', 'Guinea', 'Guinea', 'غينيا'),
    ('GP', 'Guadeloupe', 'Guadalupa', 'Guadeloupe', 'غوادلوب'),
    ('GQ', 'Guinée équatoriale', 'Guinea Equatoriale', 'Equatorial Guinea', 'غينيا الاستوائية'),
    ('GR', 'Grèce', 'Grecia', 'Greece', 'اليونان'),
    ('GS', 'Géorgie du Sud-et-les Îles Sandwich du Sud', 'Georgia del Sud e Sandwich Australi', 'South Georgia & South Sandwich Islands', 'جورجيا الجنوبية وجزر ساندويتش الجنوبية'),
    ('GT', 'Guatemala', 'Guatemala', 'Guatemala', 'غواتيمالا'),
    ('GU', 'Guam', 'Guam', 'Guam', 'غوام'),
    ('GW', 'Guinée-Bissau', 'Guinea-Bissau', 'Guinea-Bissau', 'غينيا بيساو'),
    ('GY', 'Guyana', 'Guyana', 'Guyana', 'غيانا'),
    ('HK', 'R.A.S. chinoise de Hong Kong', 'RAS di Hong Kong', 'Hong Kong SAR China', 'هونغ كونغ الصينية (منطقة إدارية خاصة)'),
    ('HM', 'Îles Heard-et-MacDonald', 'Isole Heard e McDonald', 'Heard & McDonald Islands', 'جزيرة هيرد وجزر ماكدونالد'),
    ('HN', 'Honduras', 'Honduras', 'Honduras', 'هندوراس'),
    ('HR', 'Croatie', 'Croazia', 'Croatia', 'كرواتيا'),
    ('HT', 'Haïti', 'Haiti', 'Haiti', 'هايتي'),
    ('HU', 'Hongrie', 'Ungheria', 'Hungary', 'هنغاريا'),
    ('ID', 'Indonésie', 'Indonesia', 'Indonesia', 'إندونيسيا'),
    ('IE', 'Irlande', 'Irlanda', 'Ireland', 'أيرلندا'),
    ('IL', 'Israël', 'Israele', 'Israel', 'إسرائيل'),
    ('IM', 'Île de Man', 'Isola di Man', 'Isle of Man', 'جزيرة مان'),
    ('IN', 'Inde', 'India', 'India', 'الهند'),
    ('IO', 'Territoire britannique de l’océan Indien', 'Territorio Britannico dell’Oceano Indiano', 'British Indian Ocean Territory', 'الإقليم البريطاني في المحيط الهندي'),
    ('IQ', 'Irak', 'Iraq', 'Iraq', 'العراق'),
    ('IR', 'Iran', 'Iran', 'Iran', 'إيران'),
    ('IS', 'Islande', 'Islanda', 'Iceland', 'آيسلندا'),
    ('IT', 'Italie', 'Italia', 'Italy', 'إيطاليا'),
    ('JE', 'Jersey', 'Jersey', 'Jersey', 'جيرسي'),
    ('JM', 'Jamaïque', 'Giamaica', 'Jamaica', 'جامايكا'),
    ('JO', 'Jordanie', 'Giordania', 'Jordan', 'الأردن'),
    ('JP', 'Japon', 'Giappone', 'Japan', 'اليابان'),
    ('KE', 'Kenya', 'Kenya', 'Kenya', 'كينيا'),
    ('KG', 'Kirghizstan', 'Kirghizistan', 'Kyrgyzstan', 'قيرغيزستان'),
    ('KH', 'Cambodge', 'Cambogia', 'Cambodia', 'كمبوديا'),
    ('KI', 'Kiribati', 'Kiribati', 'Kiribati', 'كيريباتي'),
    ('KM', 'Comores', 'Comore', 'Comoros', 'جزر القمر'),
    ('KN', 'Saint-Christophe-et-Niévès', 'Saint Kitts e Nevis', 'St. Kitts & Nevis', 'سانت كيتس ونيفيس'),
    ('KP', 'Corée du Nord', 'Corea del Nord', 'North Korea', 'كوريا الشمالية'),
    ('KR', 'Corée du Sud', 'Corea del Sud', 'South Korea', 'كوريا الجنوبية'),
    ('KW', 'Koweït', 'Kuwait', 'Kuwait', 'الكويت'),
    ('KY', 'Îles Caïmans', 'Isole Cayman', 'Cayman Islands', 'جزر كايمان'),
    ('KZ', 'Kazakhstan', 'Kazakistan', 'Kazakhstan', 'كازاخستان'),
    ('LA', 'Laos', 'Laos', 'Laos', 'لاوس'),
    ('LB', 'Liban', 'Libano', 'Lebanon', 'لبنان'),
    ('LC', 'Sainte-Lucie', 'Saint Lucia', 'St. Lucia', 'سانت لوسيا'),
    ('LI', 'Liechtenstein', 'Liechtenstein', 'Liechtenstein', 'ليختنشتاين'),
    ('LK', 'Sri Lanka', 'Sri Lanka', 'Sri Lanka', 'سريلانكا'),
    ('LR', 'Liberia', 'Liberia', 'Liberia', 'ليبيريا'),
    ('LS', 'Lesotho', 'Lesotho', 'Lesotho', 'ليسوتو'),
    ('LT', 'Lituanie', 'Lituania', 'Lithuania', 'ليتوانيا'),
    ('LU', 'Luxembourg', 'Lussemburgo', 'Luxembourg', 'لوكسمبورغ'),
    ('LV', 'Lettonie', 'Lettonia', 'Latvia', 'لاتفيا'),
    ('LY', 'Libye', 'Libia', 'Libya', 'ليبيا'),
    ('MA', 'Maroc', 'Marocco', 'Morocco', 'المغرب'),
    ('MC', 'Monaco', 'Monaco', 'Monaco', 'موناكو'),
    ('MD', 'Moldavie', 'Moldavia', 'Moldova', 'مولدوفا'),
    ('ME', 'Monténégro', 'Montenegro', 'Montenegro', 'الجبل الأسود'),
    ('MF', 'Saint-Martin', 'Saint Martin', 'St. Martin', 'سان مارتن'),
    ('MG', 'Madagascar', 'Madagascar', 'Madagascar', 'مدغشقر'),
    ('MH', 'Îles Marshall', 'Isole Marshall', 'Marshall Islands', 'جزر مارشال'),
    ('MK', 'Macédoine du Nord', 'Macedonia del Nord', 'North Macedonia', 'مقدونيا الشمالية'),
    ('ML', 'Mali', 'Mali', 'Mali', 'مالي'),
    ('MM', 'Myanmar (Birmanie)', 'Myanmar (Birmania)', 'Myanmar (Burma)', 'ميانمار (بورما)'),
    ('MN', 'Mongolie', 'Mongolia', 'Mongolia', 'منغوليا'),
    ('MO', 'R.A.S. chinoise de Macao', 'RAS di Macao', 'Macao SAR China', 'منطقة ماكاو الإدارية الخاصة'),
    ('MP', 'Îles Mariannes du Nord', 'Isole Marianne Settentrionali', 'Northern Mariana Islands', 'جزر ماريانا الشمالية'),
    ('MQ', 'Martinique', 'Martinica', 'Martinique', 'جزر المارتينيك'),
    ('MR', 'Mauritanie', 'Mauritania', 'Mauritania', 'موريتانيا'),
    ('MS', 'Montserrat', 'Montserrat', 'Montserrat', 'مونتسرات'),
    ('MT', 'Malte', 'Malta', 'Malta', 'مالطا'),
    ('MU', 'Maurice', 'Mauritius', 'Mauritius', 'موريشيوس'),
    ('MV', 'Maldives', 'Maldive', 'Maldives', 'جزر المالديف'),
    ('MW', 'Malawi', 'Malawi', 'Malawi', 'ملاوي'),
    ('MX', 'Mexique', 'Messico', 'Mexico', 'المكسيك'),
    ('MY', 'Malaisie', 'Malaysia', 'Malaysia', 'ماليزيا'),
    ('MZ', 'Mozambique', 'Mozambico', 'Mozambique', 'موزمبيق'),
    ('NA', 'Namibie', 'Namibia', 'Namibia', 'ناميبيا'),
    ('NC', 'Nouvelle-Calédonie', 'Nuova Caledonia', 'New Caledonia', 'كاليدونيا الجديدة'),
    ('NE', 'Niger', 'Niger', 'Niger', 'النيجر'),
    ('NF', 'Île Norfolk', 'Isola Norfolk', 'Norfolk Island', 'جزيرة نورفولك'),
    ('NG', 'Nigeria', 'Nigeria', 'Nigeria', 'نيجيريا'),
    ('NI', 'Nicaragua', 'Nicaragua', 'Nicaragua', 'نيكاراغوا'),
    ('NL', 'Pays-Bas', 'Paesi Bassi', 'Netherlands', 'هولندا'),
    ('NO', 'Norvège', 'Norvegia', 'Norway', 'النرويج'),
    ('NP', 'Népal', 'Nepal', 'Nepal', 'نيبال'),
    ('NR', 'Nauru', 'Nauru', 'Nauru', 'ناورو'),
    ('NU', 'Niue', 'Niue', 'Niue', 'نيوي'),
    ('NZ', 'Nouvelle-Zélande', 'Nuova Zelanda', 'New Zealand', 'نيوزيلندا'),
    ('OM', 'Oman', 'Oman', 'Oman', 'عُمان'),
    ('PA', 'Panama', 'Panama', 'Panama', 'بنما'),
    ('PE', 'Pérou', 'Perù', 'Peru', 'بيرو'),
    ('PF', 'Polynésie française', 'Polinesia Francese', 'French Polynesia', 'بولينيزيا الفرنسية'),
    ('PG', 'Papouasie-Nouvelle-Guinée', 'Papua Nuova Guinea', 'Papua New Guinea', 'بابوا غينيا الجديدة'),
    ('PH', 'Philippines', 'Filippine', 'Philippines', 'الفلبين'),
    ('PK', 'Pakistan', 'Pakistan', 'Pakistan', 'باكستان'),
    ('PL', 'Pologne', 'Polonia', 'Poland', 'بولندا'),
    ('PM', 'Saint-Pierre-et-Miquelon', 'Saint-Pierre e Miquelon', 'St. Pierre & Miquelon', 'سان بيير ومكويلون'),
    ('PN', 'Îles Pitcairn', 'Isole Pitcairn', 'Pitcairn Islands', 'جزر بيتكيرن'),
    ('PR', 'Porto Rico', 'Portorico', 'Puerto Rico', 'بورتوريكو'),
    ('PS', 'Territoires palestiniens', 'Territori Palestinesi', 'Palestinian Territories', 'الأراضي الفلسطينية'),
    ('PT', 'Portugal', 'Portogallo', 'Portugal', 'البرتغال'),
    ('PW', 'Palaos', 'Palau', 'Palau', 'بالاو'),
    ('PY', 'Paraguay', 'Paraguay', 'Paraguay', 'باراغواي'),
    ('QA', 'Qatar', 'Qatar', 'Qatar', 'قطر'),
    ('RE', 'La Réunion', 'Riunione', 'Réunion', 'روينيون'),
    ('RO', 'Roumanie', 'Romania', 'Romania', 'رومانيا'),
    ('RS', 'Serbie', 'Serbia', 'Serbia', 'صربيا'),
    ('RU', 'Russie', 'Russia', 'Russia', 'روسيا'),
    ('RW', 'Rwanda', 'Ruanda', 'Rwanda', 'رواندا'),
    ('SA', 'Arabie saoudite', 'Arabia Saudita', 'Saudi Arabia', 'المملكة العربية السعودية'),
    ('SB', 'Îles Salomon', 'Isole Salomone', 'Solomon Islands', 'جزر سليمان'),
    ('SC', 'Seychelles', 'Seychelles', 'Seychelles', 'سيشل'),
    ('SD', 'Soudan', 'Sudan', 'Sudan', 'السودان'),
    ('SE', 'Suède', 'Svezia', 'Sweden', 'السويد'),
    ('SG', 'Singapour', 'Singapore', 'Singapore', 'سنغافورة'),
    ('SH', 'Sainte-Hélène', 'Sant’Elena', 'St. Helena', 'سانت هيلينا'),
    ('SI', 'Slovénie', 'Slovenia', 'Slovenia', 'سلوفينيا'),
    ('SJ', 'Svalbard et Jan Mayen', 'Svalbard e Jan Mayen', 'Svalbard & Jan Mayen', 'سفالبارد وجان ماين'),
    ('SK', 'Slovaquie', 'Slovacchia', 'Slovakia', 'سلوفاكيا'),
    ('SL', 'Sierra Leone', 'Sierra Leone', 'Sierra Leone', 'سيراليون'),
    ('SM', 'Saint-Marin', 'San Marino', 'San Marino', 'سان مارينو'),
    ('SN', 'Sénégal', 'Senegal', 'Senegal', 'السنغال'),
    ('SO', 'Somalie', 'Somalia', 'Somalia', 'الصومال'),
    ('SR', 'Suriname', 'Suriname', 'Suriname', 'سورينام'),
    ('SS', 'Soudan du Sud', 'Sud Sudan', 'South Sudan', 'جنوب السودان'),
    ('ST', 'Sao Tomé-et-Principe', 'São Tomé e Príncipe', 'São Tomé & Príncipe', 'ساو تومي وبرينسيبي'),
    ('SV', 'Salvador', 'El Salvador', 'El Salvador', 'السلفادور'),
    ('SX', 'Saint-Martin (partie néerlandaise)', 'Sint Maarten', 'Sint Maarten', 'سانت مارتن'),
    ('SY', 'Syrie', 'Siria', 'Syria', 'سوريا'),
    ('SZ', 'Eswatini', 'Eswatini', 'Eswatini', 'إسواتيني'),
    ('TC', 'Îles Turques-et-Caïques', 'Isole Turks e Caicos', 'Turks & Caicos Islands', 'جزر توركس وكايكوس'),
    ('TD', 'Tchad', 'Ciad', 'Chad', 'تشاد'),
    ('TF', 'Terres australes françaises', 'Terre Australi Francesi', 'French Southern Territories', 'الأقاليم الجنوبية الفرنسية'),
    ('TG', 'Togo', 'Togo', 'Togo', 'توغو'),
    ('TH', 'Thaïlande', 'Thailandia', 'Thailand', 'تايلاند'),
    ('TJ', 'Tadjikistan', 'Tagikistan', 'Tajikistan', 'طاجيكستان'),
    ('TK', 'Tokelau', 'Tokelau', 'Tokelau', 'توكيلاو'),
    ('TL', 'Timor oriental', 'Timor Est', 'Timor-Leste', 'تيمور - ليشتي'),
    ('TM', 'Turkménistan', 'Turkmenistan', 'Turkmenistan', 'تركمانستان'),
    ('TN', 'Tunisie', 'Tunisia', 'Tunisia', 'تونس'),
    ('TO', 'Tonga', 'Tonga', 'Tonga', 'تونغا'),
    ('TR', 'Turquie', 'Turchia', 'Türkiye', 'تركيا'),
    ('TT', 'Trinité-et-Tobago', 'Trinidad e Tobago', 'Trinidad & Tobago', 'ترينيداد وتوباغو'),
    ('TV', 'Tuvalu', 'Tuvalu', 'Tuvalu', 'توفالو'),
    ('TW', 'Taïwan', 'Taiwan', 'Taiwan', 'تايوان'),
    ('TZ', 'Tanzanie', 'Tanzania', 'Tanzania', 'تنزانيا'),
    ('UA', 'Ukraine', 'Ucraina', 'Ukraine', 'أوكرانيا'),
    ('UG', 'Ouganda', 'Uganda', 'Uganda', 'أوغندا'),
    ('UM', 'Îles mineures éloignées des États-Unis', 'Isole Minori Esterne degli Stati Uniti', 'U.S. Outlying Islands', 'جزر الولايات المتحدة النائية'),
    ('US', 'États-Unis', 'Stati Uniti', 'United States', 'الولايات المتحدة'),
    ('UY', 'Uruguay', 'Uruguay', 'Uruguay', 'أورغواي'),
    ('UZ', 'Ouzbékistan', 'Uzbekistan', 'Uzbekistan', 'أوزبكستان'),
    ('VA', 'État de la Cité du Vatican', 'Città del Vaticano', 'Vatican City', 'الفاتيكان'),
    ('VC', 'Saint-Vincent-et-les Grenadines', 'Saint Vincent e Grenadine', 'St. Vincent & Grenadines', 'سانت فنسنت وجزر غرينادين'),
    ('VE', 'Venezuela', 'Venezuela', 'Venezuela', 'فنزويلا'),
    ('VG', 'Îles Vierges britanniques', 'Isole Vergini Britanniche', 'British Virgin Islands', 'جزر فيرجن البريطانية'),
    ('VI', 'Îles Vierges des États-Unis', 'Isole Vergini Americane', 'U.S. Virgin Islands', 'جزر فيرجن الأمريكية'),
    ('VN', 'Viêt Nam', 'Vietnam', 'Vietnam', 'فيتنام'),
    ('VU', 'Vanuatu', 'Vanuatu', 'Vanuatu', 'فانواتو'),
    ('WF', 'Wallis-et-Futuna', 'Wallis e Futuna', 'Wallis & Futuna', 'جزر والس وفوتونا'),
    ('WS', 'Samoa', 'Samoa', 'Samoa', 'ساموا'),
    ('XK', 'Kosovo', 'Kosovo', 'Kosovo', 'كوسوفو'),
    ('YE', 'Yémen', 'Yemen', 'Yemen', 'اليمن'),
    ('YT', 'Mayotte', 'Mayotte', 'Mayotte', 'مايوت'),
    ('ZA', 'Afrique du Sud', 'Sudafrica', 'South Africa', 'جنوب أفريقيا'),
    ('ZM', 'Zambie', 'Zambia', 'Zambia', 'زامبيا'),
    ('ZW', 'Zimbabwe', 'Zimbabwe', 'Zimbabwe', 'زيمبابوي'),
)

_BY_CODE = {row[0]: row for row in COUNTRIES}
CODES = frozenset(_BY_CODE)


def fold(text: str) -> str:
    """Diacritics and case off: «Côte d’Ivoire» matches «cote d'ivoire» (the combobox's own rule, server side)."""
    text = unicodedata.normalize("NFKD", str(text or "")).replace("’", "'")
    return "".join(c for c in text if not unicodedata.combining(c)).casefold().strip()


def name(code: str, language: str = "fr") -> str:
    """The country's name in ``language`` (fr, it, en, ar; another falls back to English); "" for no such code."""
    row = _BY_CODE.get(str(code or "").upper())
    if row is None:
        return ""
    lang = str(language or "")[:2]
    return row[1 + LANGUAGES.index(lang)] if lang in LANGUAGES else row[3]


def choices(language: str = "fr") -> list[tuple[str, str]]:
    """(code, name) in ``language``, in that language's alphabetical order (diacritics folded)."""
    pairs = [(row[0], name(row[0], language)) for row in COUNTRIES]
    return sorted(pairs, key=lambda pair: fold(pair[1]))


def match(text: str) -> str:
    """The code a free text names — a code, or a name in any of the four languages — or "" (the earlier free fields)."""
    value = str(text or "").strip()
    if value.upper() in CODES:
        return value.upper()
    folded = fold(value)
    if not folded:
        return ""
    for row in COUNTRIES:
        if folded in {fold(n) for n in row[1:]}:
            return row[0]
    return ""
