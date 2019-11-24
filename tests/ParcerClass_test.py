import unittest
from parser.Parser import Parser

class ParcerClassTest(unittest.TestCase):

    def setUp(self):

        self.tagToValidate = "validator"

    def test_init(self):
        urlPrefs = {'validator': ['main', {'itemtype': 'http://schema.org/Product'}],
                      'nameTag': [],
                      'priceTag': [],
                      'measurmentTag': [],
                      'shortDescTag': [],
                      'longDescTag': []}
        parser = Parser(**urlPrefs)
        self.assertEqual(['main', {'itemtype': 'http://schema.org/Product'}], parser._tags['validator'])

        urlPrefs = {'validator': ['main', {'itemtype': 'http://schema.org/Product'}],
                      'nameTag': [],
                      'priceTag': [],
                      'shortDescTag': [],
                      'longDescTag': []}
        with self.assertRaises(ValueError):
            parser = Parser(**urlPrefs)


        urlPrefs = {'validator': ['main', {'itemtype': 'http://schema.org/Product'}],
                      'nameTag': [],
                      'priceTag': [],
                      'measurmentTag': '',
                      'shortDescTag': [],
                      'longDescTag': []}
        with self.assertRaises(ValueError):
            parser = Parser(**urlPrefs)

    def test_urlopen(self):
        urlPrefs = {'validator': [],
                      'nameTag': [],
                      'priceTag': [],
                      'measurmentTag': [],
                      'shortDescTag': [],
                      'longDescTag': []}
        parser = Parser(**urlPrefs)

        urlToOpen = 'https://santehnika-online.ru/product/akrilovaya_vanna_riho_miami_180_1656309/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)

        urlToOpen = 'https://www.sdvor.com/moscow/'
        with self.assertRaises(UserWarning):
            result = parser.urlopen(urlToOpen)

        urlToOpen = 'https://www.ekonomstroy.ru/catalog/betonokontakt/gruntovka_starateli_beton_kontakt_20kg/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)

        urlToOpen = 'https://www.sdvor.com/moscow/product/mastika-prikleivajuschaja-tehnonikol-no27-22-kg-37678/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)

        urlToOpen = 'https://www.stroyshopper.ru/product/keramogranit_gracia_ceramica_aragon_dark_450kh450kh8/'
        result = parser.urlopen(urlToOpen)
        self.assertIsInstance(result, str)

    def test_urlvalidate(self):

        urlPrefs = {'validator': ['main', {'itemtype': 'http://schema.org/Product'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://santehnika-online.ru/product/akrilovaya_vanna_riho_miami_180_1656309/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertFalse(status)
        status = result = None

        urlToOpen = 'https://santehnika-online.ru/product/akrilovaya_1vanna_riho_miami_180_1656309/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertFalse(status)
        status = result = None

        urlToOpen = 'https://santehnika-online.ru/vanny/akrilovye/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertFalse(status)

        urlPrefs = {'validator': ['span', {'class': 'span_price'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://www.ekonomstroy.ru/catalog/betonokontakt/gruntovka_starateli_beton_kontakt_20kg/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertTrue(status)
        status = result = None

        urlToOpen = 'https://www.ekonomstroy.ru/catalog/betonokontakt/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertFalse(status)

        urlPrefs = {'validator': ['h1', {'class': 'container_title'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://www.sdvor.com/moscow/product/mastika-prikleivajuschaja-tehnonikol-no27-22-kg-37678/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertTrue(status)
        status = result = None

        urlToOpen = 'https://www.sdvor.com/moscow/category/obmazochnaja-gidroizoljatsija-5100/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertFalse(status)

        urlPrefs = {'validator': ['p', {'class': 'item_price'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        urlToOpen = 'https://www.stroyshopper.ru/product/keramogranit_gracia_ceramica_aragon_dark_450kh450kh8/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertTrue(status)
        status = result = None

        urlToOpen = 'https://www.stroyshopper.ru/category/gracia_ceramica_keramogranit/'
        status, result = parser.urlTagValidate(self.tagToValidate, urlToOpen)
        self.assertFalse(status)

        with self.assertRaises(ValueError):
            status, result = parser.urlTagValidate('cutomTag', urlToOpen)

        with self.assertRaises(ValueError):
            status, result = parser.urlTagValidate('nameTag', urlToOpen)

    def test_smallValidationTagTester(self):

        # stroyshopper
        urlPrefs = {'validator': ['p', {'class': 'item_price'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        targetUrls = [
            'https://www.stroyshopper.ru/product/keramogranit_gracia_ceramica_aragon_dark_450kh450kh8/',
            'https://www.stroyshopper.ru/product/kolesootbojnik_arec_ko500/',
            'https://www.stroyshopper.ru/product/polukombinezon_muzhskoj_t_seryjchernyj/',
            'https://www.stroyshopper.ru/product/bra_odeon_light_2838_1w/',
            'https://www.stroyshopper.ru/product/komod_fink-44_mst-kuf-44-16_or/',
            'https://www.stroyshopper.ru/product/oboi_limonta_tessuti_veneziani_27752/',
            'https://www.stroyshopper.ru/product/stul_lt_c17451_walnutfabric/',
            'https://www.stroyshopper.ru/product/krestiki-dlja-kafelja-25-mm/',
            'https://www.stroyshopper.ru/product/rukav_rezinovyj_gost_18698-79_v_20-0_63_m/',
            'https://www.stroyshopper.ru/product/drenazhnaja_asbestovaja_truba_d350_l-5_00/',
            'https://www.stroyshopper.ru/product/germetik_kauchukovyj_tytan_professional_dla_krovli_chernyj_310_ml/',
            'https://www.stroyshopper.ru/product/dubel_raspornyj_tchappai_sinij_5kh30_1_tys_sht/'
        ]
        commonUrls = [
            'https://www.stroyshopper.ru/category/vanny/ifo/',
            'https://www.stroyshopper.ru/category/rozetki_i_vyklyuchateli/rozetki_i_vykluchateli_cveta_goluboj/',
            'https://www.stroyshopper.ru/brand/la-beaute/',
            'https://www.stroyshopper.ru/brand/p-s-international/',
            'https://www.stroyshopper.ru/brand/skyland/',
            'https://www.stroyshopper.ru/brand/talkberg/',
            'https://www.stroyshopper.ru/about/',
            'https://www.stroyshopper.ru/']

        result = parser.testUniqTag(self.tagToValidate, targetUrls, commonUrls)

        self.assertEqual(len(targetUrls), result['result']['TP'])
        self.assertEqual(len(commonUrls), result['result']['TN'])
        self.assertEqual(0, result['result']['FP'])
        self.assertEqual(0, result['result']['FN'])

        self.assertEqual(len(targetUrls), len(result['target']['foundTag']))
        self.assertEqual(len(commonUrls), len(result['common']['emptyTag']))
        self.assertEqual(0, len(result['target']['emptyTag']))
        self.assertEqual(0, len(result['common']['foundTag']))
        self.assertEqual(0, len(result['target']['errors']))
        self.assertEqual(0, len(result['common']['errors']))

    @unittest.skip("passed")
    def test_bigValidationTagTester(self):

        # stroyshopper
        urlPrefs = {'validator': ['p', {'class': 'item_price'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        targetUrls = [
            'https://www.stroyshopper.ru/product/keramogranit_gracia_ceramica_aragon_dark_450kh450kh8/',
            'https://www.stroyshopper.ru/product/kolesootbojnik_arec_ko500/',
            'https://www.stroyshopper.ru/product/polukombinezon_muzhskoj_t_seryjchernyj/',
            'https://www.stroyshopper.ru/product/bra_odeon_light_2838_1w/',
            'https://www.stroyshopper.ru/product/komod_fink-44_mst-kuf-44-16_or/',
            'https://www.stroyshopper.ru/product/oboi_limonta_tessuti_veneziani_27752/',
            'https://www.stroyshopper.ru/product/stul_lt_c17451_walnutfabric/',
            'https://www.stroyshopper.ru/product/krestiki-dlja-kafelja-25-mm/',
            'https://www.stroyshopper.ru/product/rukav_rezinovyj_gost_18698-79_v_20-0_63_m/',
            'https://www.stroyshopper.ru/product/drenazhnaja_asbestovaja_truba_d350_l-5_00/',
            'https://www.stroyshopper.ru/product/germetik_kauchukovyj_tytan_professional_dla_krovli_chernyj_310_ml/',
            'https://www.stroyshopper.ru/product/dubel_raspornyj_tchappai_sinij_5kh30_1_tys_sht/'
        ]
        commonUrls = [
            'https://www.stroyshopper.ru/category/vanny/ifo/',
            'https://www.stroyshopper.ru/category/rozetki_i_vyklyuchateli/rozetki_i_vykluchateli_cveta_goluboj/',
            'https://www.stroyshopper.ru/brand/la-beaute/',
            'https://www.stroyshopper.ru/brand/p-s-international/',
            'https://www.stroyshopper.ru/brand/skyland/',
            'https://www.stroyshopper.ru/brand/talkberg/',
            'https://www.stroyshopper.ru/about/',
            'https://www.stroyshopper.ru/']

        result = parser.testUniqTag(self.tagToValidate, targetUrls, commonUrls)

        self.assertEqual(len(targetUrls), result['result']['TP'])
        self.assertEqual(len(commonUrls), result['result']['TN'])
        self.assertEqual(0, result['result']['FP'])
        self.assertEqual(0, result['result']['FN'])

        self.assertEqual(len(targetUrls), len(result['target']['foundTag']))
        self.assertEqual(len(commonUrls), len(result['common']['emptyTag']))
        self.assertEqual(0, len(result['target']['emptyTag']))
        self.assertEqual(0, len(result['common']['foundTag']))
        self.assertEqual(0, len(result['target']['errors']))
        self.assertEqual(0, len(result['common']['errors']))

        # sdvor
        urlPrefs = {'validator': ['h1', {'class': 'container_title'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        targetUrls = [
            'https://www.sdvor.com/moscow/product/mastika-prikleivajuschaja-tehnonikol-no27-22-kg-37678/',
            'https://www.sdvor.com/moscow/product/bide-napolnoe-jacob-delafon-odeon-up-e4738-00-335899/',
            'https://www.sdvor.com/moscow/product/plintus-kronopol-p85-3747-pandora-oak-2500h85h16mm-112527/',
            'https://www.sdvor.com/moscow/product/bide-napolnoe-jacob-delafon-ove-e1705-00-335900/',
            'https://www.sdvor.com/moscow/product/plintus-ideal-komfort-216-dub-safari-161816/',
            'https://www.sdvor.com/moscow/product/plintus-ideal-komfort-218-dub-evropejskij-161818/',
            'https://www.sdvor.com/moscow/product/laminat-aurum-gusto-malibu-platan-65224/',
            'https://www.sdvor.com/moscow/product/profil-stykoperekryvajuschij-ps-03900083-buk-9282/',
            'https://www.sdvor.com/moscow/product/plintus-arbiton-loctike-102-mr0801-belyj-2420h80h15-mm-105257/',
            'https://www.sdvor.com/moscow/product/laminat-tarkett-pilot-farman-217566/',
            'https://www.sdvor.com/moscow/product/vedro-plastmassovoe-mernoe-12-l-27650/',
            'https://www.sdvor.com/moscow/product/homut-truby-universalnyj-docke-premium-plombir-33107/',
            'https://www.sdvor.com/moscow/product/blok-gazobetonnyj-75x250x600-mm-b35-d500-bonolit-440103/',
            'https://www.sdvor.com/moscow/product/trava-iskusstvennaja-megan-38-38mm-2m-356169/',
            'https://www.sdvor.com/moscow/product/laminat-platinium-linea-dub-lion-129880/'
        ]
        commonUrls = [
            'https://www.sdvor.com/moscow/category/baki-dlja-sistem-vodosnabzhenija-8920/',
            'https://www.sdvor.com/moscow/brigade/',
            'https://www.sdvor.com/moscow/category/setka-metallicheskaja-5606/',
            'https://www.sdvor.com/moscow/category/kirpich-7555/',
            'https://www.sdvor.com/moscow/category/batarejki-i-akkumuljatory-8142/',
            'https://www.sdvor.com/moscow/category/kontrolnye-i-izmeritelnye-pribory-7336/',
            'https://www.sdvor.com/moscow/c/promo/',
            'https://www.sdvor.com/moscow/category/klejkie-lenty-skotch-5616/',
            'https://www.sdvor.com/moscow/orders/cart/',
            'https://www.sdvor.com/law/',
            'https://www.sdvor.com/moscow/category/vodostochnye-sistemy-9049/',
            'https://www.sdvor.com/moscow/category/dveri-i-komplektujuschie-8057/',
            'https://www.sdvor.com/moscow/offer1/',
            'https://www.sdvor.com/moscow/contacts/',
            'https://www.sdvor.com/moscow/category/pakety-i-korobki-5016/'
            ]

        result = parser.testUniqTag(self.tagToValidate, targetUrls, commonUrls)

        self.assertEqual(len(targetUrls), result['result']['TP'])
        self.assertEqual(len(commonUrls), result['result']['TN'])
        self.assertEqual(0, result['result']['FP'])
        self.assertEqual(0, result['result']['FN'])

        self.assertEqual(len(targetUrls), len(result['target']['foundTag']))
        self.assertEqual(len(commonUrls), len(result['common']['emptyTag']))
        self.assertEqual(0, len(result['target']['emptyTag']))
        self.assertEqual(0, len(result['common']['foundTag']))
        self.assertEqual(0, len(result['target']['errors']))
        self.assertEqual(0, len(result['common']['errors']))


        # ekonomstroy
        urlPrefs = {'validator': ['span', {'class': 'span_price'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        targetUrls = [
            'https://www.ekonomstroy.ru/catalog/kley_plitochnyy/kley_plitochnyy_veber_vetonit_granit_fiks_25kg/',
            'https://www.ekonomstroy.ru/catalog/komplektuyushchie_k_bytovym_filtram/kasseta_barer_6_zhestkost/',
            'https://www.ekonomstroy.ru/catalog/aerozolnye/kraska_aeroz_kudo_universalnaya_zheltyy_520ml/',
            'https://www.ekonomstroy.ru/catalog/akrilovye_vanny/vanna_akrilovaya_bas_verona_1500_700_450_pryamougolnaya_sliv_pereliv_metal_karkas_s_regulir_nozh_/',
            'https://www.ekonomstroy.ru/catalog/chayniki/chaynik_nerzh_3_0l_art_tm_deco_hy_3807_12_so_svistkom/',
            'https://www.ekonomstroy.ru/catalog/koronki_po_steklu_keramogranitu/sverlo_balerinka_p_kafelyu_s_zashchitnoy_reetkoy_matrix/',
            'https://www.ekonomstroy.ru/catalog/rozetki_elektricheskie/rozetka_1_mestnaya_s_zazemleniem_otkrytoy_ustanovki_16a_250v_antratsit_blanca_schneider_electric/',
            'https://www.ekonomstroy.ru/catalog/lestnitsy_stremyanki/stremyanka_3stupeni_eurogold_rezinovye_nakladki/',
            'https://www.ekonomstroy.ru/catalog/lyuki_dvertsy_revizionnye_santekhnicheskie/lyuk_santekhnicheskiy_lm_250kh250_/',
            'https://www.ekonomstroy.ru/catalog/kovriki/kovrik_yacheistyy_gryazesbornyy_80_120_1_2sm_vortex_2/',
            'https://www.ekonomstroy.ru/catalog/kryshka_kolodeznaya/kryshka_kolodeznaya_zh_b_pp_10_1_s_plastmassovym_lyukom/',
            'https://www.ekonomstroy.ru/catalog/provod_ustanovochnyy_bytovoy/provod_shvvp_2kh0_5/'
        ]
        commonUrls = [
            'https://www.ekonomstroy.ru/brands/makita/?PAGEN_1=3',
            'https://www.ekonomstroy.ru/brands/makita/?PAGEN_1=2',
            'https://www.ekonomstroy.ru/catalog/molotki_klepalnye_i_steplery/?sort_type=PRICE_DOWN',
            'https://www.ekonomstroy.ru/catalog/ballony_gazovye/?sort_type=NAME_DOWN',
            'https://www.ekonomstroy.ru/catalog/urovni_vodyanye/filter/clear/apply/',
            'https://www.ekonomstroy.ru/catalog/plitka_shakhty/',
            'https://www.ekonomstroy.ru/catalog/armatura/',
            'https://www.ekonomstroy.ru/catalog/lampochki_galogennye/',
            'https://www.ekonomstroy.ru/catalog/sistemy_vodoochistki_dzhileks/',
            'https://www.ekonomstroy.ru/catalog/pilomaterial_stroganyy/',
            'https://www.ekonomstroy.ru/catalog/utepliteli/',
            'https://www.ekonomstroy.ru/catalog/zamki_kodovye/',
            'https://www.ekonomstroy.ru/catalog/zazhimy_krokodily/'
            ]

        result = parser.testUniqTag(self.tagToValidate, targetUrls, commonUrls)

        self.assertEqual(len(targetUrls), result['result']['TP'])
        self.assertEqual(len(commonUrls), result['result']['TN'])
        self.assertEqual(0, result['result']['FP'])
        self.assertEqual(0, result['result']['FN'])

        self.assertEqual(len(targetUrls), len(result['target']['foundTag']))
        self.assertEqual(len(commonUrls), len(result['common']['emptyTag']))
        self.assertEqual(0, len(result['target']['emptyTag']))
        self.assertEqual(0, len(result['common']['foundTag']))
        self.assertEqual(0, len(result['target']['errors']))
        self.assertEqual(0, len(result['common']['errors']))


        # zergud
        urlPrefs = {'validator': ['div', {'class': 'product'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        targetUrls = [
            'http://zergud.ru/catalog/keramogranit_plitka_oblitsovochnaya/tekhnicheskiy_keramogranit/keramogranit_atem_gres_ekonom_e0010_300x300x12/',
            'http://zergud.ru/catalog/kley/kley_dlya_plitki_i_keramogranita/brend/zergud/klej-dlya-pliki-zergud-25-kg/',
            'http://zergud.ru/catalog/keramogranit_plitka_oblitsovochnaya/plitka/palitra/offer_palitra-plitka-nastennaya-belaya-prozrachnaya-c-whm051r-25x35/',
            'http://zergud.ru/catalog/kley/kley_dlya_plitki_i_keramogranita/brend/zergud/klej-dlya-keramogranita-leto-0322-zergud-25-kg/',
            'http://zergud.ru/catalog/keramogranit_plitka_oblitsovochnaya/tekhnicheskiy_keramogranit/keramogranit_italon_basic_nikel_300x300x8_mm/',
            'http://zergud.ru/catalog/keramogranit_plitka_oblitsovochnaya/tekhnicheskiy_keramogranit/keramogranit_italon_basic_nikel_300kh300kh12_mm_usilennyy/',
            'http://zergud.ru/catalog/pilomaterialy/fanera/fanera_fk_1525kh1525kh24_mm_sort_ii_ii_vv_vv_sh2_shlifovannaya/',
            'http://zergud.ru/catalog/krovlya_sayding_vodostochnye_sistemy/vodostochnye_sistemy/zhelob_vodostochnyy_ruplast_korichnevyy_3m/',
            'http://zergud.ru/catalog/gipsokarton_i_komplektuyushchie/profilya_dlya_gkl/profil_otsinkovannyy_pp_60kh27kh3000_mm/',
            'http://zergud.ru/catalog/keramogranit_plitka_oblitsovochnaya/fasadnyy_keramogranit/estima_your_color/offer_Fasadnyy_keramogranit_Estima_Your_Color_YC_87_60kh120_nepolir/',
            'http://zergud.ru/catalog/electroinstrumenty/gaykoverty/nabor-makita-gaykovert-akkumulyatornyy-td110dwae-ruletka-pgc-80520/',
            'http://zergud.ru/catalog/keramogranit_plitka_oblitsovochnaya/stupeni/semir-grafit-grupa-paradyz-3932/offer_semir-grafit-plitka-fasadnaja-strukturnaja-24-5kh6-58kh0-7437488/'
        ]
        commonUrls = [
            'http://zergud.ru/catalog/kley/silikony/',
            'http://zergud.ru/catalog/napolnye_pokrytiya/linoleum/',
            'http://zergud.ru/catalog/sanfayans_smesiteli/komplektuyushchie_dlya_vann/',
            'http://zergud.ru/catalog/podvesnoy_potolok/zvezdnoe_nebo/',
            'http://zergud.ru/catalog/electroinstrumenty/svarochnyy_apparat/',
            'http://zergud.ru/catalog/electroinstrumenty/shtroborezy/',
            'http://zergud.ru/catalog/krovlya_sayding_vodostochnye_sistemy/vodostochnye_sistemy/',
            'http://zergud.ru/catalog/electroinstrumenty/shlifovalny_inctument/',
            'http://zergud.ru/catalog/lakokrasochnye_materialy/antiseptiki/',
            'http://zergud.ru/catalog/utepliteli_i_teploizolyatsiya/tekhnicheskaya_teploizolyatsiya/',
            'http://zergud.ru/catalog/utepliteli_i_teploizolyatsiya/uteplitel/',
            'http://zergud.ru/news/keramicheskiy_andegraund/',
            'http://zergud.ru/partner/',
            'http://zergud.ru/catalog/setki_serpyanki_lenty_khoztovary/',
            'http://zergud.ru/catalog/podvesnoy_potolok/podvesnye_sistemy/',
            'http://zergud.ru/catalog/stroitelnaya-tekhnika-i-oborudovanie/',
            'http://zergud.ru/catalog/inzhenernaya_santekhnika/gazosnabzhenie/',
            'http://zergud.ru/catalog/electroinstrumenty/gaykoverty/'
        ]

        result = parser.testUniqTag(self.tagToValidate, targetUrls, commonUrls)

        # print(result)

        self.assertEqual(len(targetUrls), result['result']['TP'])
        self.assertEqual(len(commonUrls), result['result']['TN'])
        self.assertEqual(0, result['result']['FP'])
        self.assertEqual(0, result['result']['FN'])

        self.assertEqual(len(targetUrls), len(result['target']['foundTag']))
        self.assertEqual(len(commonUrls), len(result['common']['emptyTag']))
        self.assertEqual(0, len(result['target']['emptyTag']))
        self.assertEqual(0, len(result['common']['foundTag']))
        self.assertEqual(0, len(result['target']['errors']))
        self.assertEqual(0, len(result['common']['errors']))


        # electro-mpo
        urlPrefs = {'validator': ['div', {'class': 'Microdata_product'}],
                     'nameTag': [],
                     'priceTag': [],
                     'measurmentTag': [],
                     'shortDescTag': [],
                     'longDescTag': []}
        parser = Parser(**urlPrefs)
        status = result = None

        targetUrls = [
            'https://www.electro-mpo.ru/catalog/svetilniki_svetodiodnye_svetilniki_i_lenty_prozhek/s05_svetodiodnye_prozhektory/s0579-prozhektor-b0043566-lpr-021-0-65k-100-220v-1/',
            'https://www.electro-mpo.ru/catalog/lestnitsy_stremyanki_vyshki_tury/v62_stremyanki_bytovye_professionalnye/v6222-stremyanka-al160-bytovaya-alyuminievaya-6-st/',
            'https://www.electro-mpo.ru/catalog/avtomaty_uzo_difavtomaty/a27_avtomaticheskie_vyklyuchateli_sh200l_s200m_abb/a2703-avtomaticheskiy-vyklyuchatel-sh201l-s16a-1p-/',
            'https://www.electro-mpo.ru/catalog/provod_i_kabel/p07_vvg_vvg_p_kabel_silovoy_mednyy_gost_rossiya/p0764-kabel-vvg-3kh1-5ok-n-re-0-66-gost-uluchshenn/',
            'https://www.electro-mpo.ru/catalog/svetilniki_svetodiodnye_svetilniki_i_lenty_prozhek/s05_svetodiodnye_prozhektory/s0579-prozhektor-b0043566-lpr-021-0-65k-100-220v-1/',
            'https://www.electro-mpo.ru/catalog/lestnitsy_stremyanki_vyshki_tury/v62_stremyanki_bytovye_professionalnye/v6222-stremyanka-al160-bytovaya-alyuminievaya-6-st/',
            'https://www.electro-mpo.ru/catalog/avtomaty_uzo_difavtomaty/a27_avtomaticheskie_vyklyuchateli_sh200l_s200m_abb/a2703-avtomaticheskiy-vyklyuchatel-sh201l-s16a-1p-/',
            'https://www.electro-mpo.ru/catalog/domofony_izveshchateli_ibp_akb_zaryadnye_ustroystv/n6418-panel-vyzova-qm-305n-dlya-tsvetnogo-videodom/',
            'https://www.electro-mpo.ru/catalog/sredstva_individualnoy_zashchity_i_okhrana_truda_o/i1912_poyas_a_predokhranitelnyy_s_dvumya_stropami_/',
            'https://www.electro-mpo.ru/catalog/teplyy_pol_sistemy_antiobledeneniya_nagrevatelnyy_/p9201-nagrevatelnyy-mat-dsvf-150-140f0328-odnozhil/',
        ]
        commonUrls = [
            'https://www.electro-mpo.ru/catalog/elektricheskie_payalniki_gazovye_gorelki_i_payalny/',
            'https://www.electro-mpo.ru/catalog/elektroshchity_vru_avr_shchap_yau_shchur_shchu/',
            'https://www.electro-mpo.ru/catalog/molniezashchita_zazemlenie_ogranichiteli_perenaprya/',
            'https://www.electro-mpo.ru/catalog/vilki_razemy_udliniteli_setevye_filtry/',
            'https://www.electro-mpo.ru/about/news/bolshoe-postuplenie-svetotekhniki-ot-general/',
            'https://www.electro-mpo.ru/info/enchiridion/',
            'https://www.electro-mpo.ru/info/',
            'https://www.electro-mpo.ru/catalog/kabelnye_lotki_napolnye_lyuchki_i_rozetochnye_blok/',
            'https://www.electro-mpo.ru/sborka/',
            'https://www.electro-mpo.ru/catalog/rozetki_vyklyuchateli_svetoregulyatory_zvonki/',
            'https://www.electro-mpo.ru/about/news/',
            'https://www.electro-mpo.ru/catalog/svetilniki_svetodiodnye_svetilniki_i_lenty_prozhek/',
            'https://www.electro-mpo.ru/catalog/otvertki_klyuchi_nabory_instrumentov_yashchiki_i_s/',
            'https://www.electro-mpo.ru/catalog/ruchnoy_instrument_zamki_navesnye/',
            'https://www.electro-mpo.ru/contacts/',
            'https://www.electro-mpo.ru/catalog/press_kleshchi_gubtsevyy_instrument_instrument_dlya/',
            'https://www.electro-mpo.ru/catalog/rasprodazha_ostatkov_provod_i_kabel/',
            'https://www.electro-mpo.ru/about/',
        ]

        result = parser.testUniqTag(self.tagToValidate, targetUrls, commonUrls)
        print(result)
        self.assertEqual(len(targetUrls), result['result']['TP'])
        self.assertEqual(len(commonUrls), result['result']['TN'])
        self.assertEqual(0, result['result']['FP'])
        self.assertEqual(0, result['result']['FN'])

        self.assertEqual(len(targetUrls), len(result['target']['foundTag']))
        self.assertEqual(len(commonUrls), len(result['common']['emptyTag']))
        self.assertEqual(0, len(result['target']['emptyTag']))
        self.assertEqual(0, len(result['common']['foundTag']))
        self.assertEqual(0, len(result['target']['errors']))
        self.assertEqual(0, len(result['common']['errors']))

    def test_urlparse(self):

        urlPrefs = {'validator': ['div', {'class': 'Microdata_product'}],
                     'nameTag': ['h1', {}],
                     'priceTag': ['i', {'itemprop': 'price'}],
                     'measurmentTag': ['', ''],
                     'shortDescTag': ['div', {'class': 'description_tab_block'}],
                     'longDescTag': ['', '']}
        parser = Parser(**urlPrefs)
        results = None

        targetUrls = [
            'https://www.electro-mpo.ru/catalog/svetilniki_svetodiodnye_svetilniki_i_lenty_prozhek/s05_svetodiodnye_prozhektory/s0579-prozhektor-b0043566-lpr-021-0-65k-100-220v-1/',
            'https://www.electro-mpo.ru/catalog/lestnitsy_stremyanki_vyshki_tury/v62_stremyanki_bytovye_professionalnye/v6222-stremyanka-al160-bytovaya-alyuminievaya-6-st/',
            ]

        results = [{'name': 'С0579. Прожектор Б0043566 LPR-021-0-65K-100 220В 100Вт 8000Лм 6500К светодиодный IP65 (ЭРА)',
                   'price': '1146.72',
                   'measurment': '',
                   'info': '<table id="card_pattern" width="300" border="0"> <tbody> </tbody><caption> <center> <span style="font-size: 20px; color: #032f89"> <b>Прожектор Б0043566 LPR-021-0-65K-100 220В 100 Вт 8000Лм 6500К светодиодный IP65 («ЭРА», Китай)</b> </span> </center> </caption><tbody><tr><td id="cell_pattern" colspan="1" rowspan="1" valign="top">&nbsp;</td><td id="cell_pattern" colspan="1" rowspan="1" valign="top">&nbsp;</td><td id="cell_pattern" colspan="1" rowspan="1" valign="top">&nbsp;</td><td id="cell_pattern" colspan="1" rowspan="1" valign="top">&nbsp;</td><td id="cell_pattern" colspan="1" rowspan="1" valign="top">&nbsp;</td><td id="cell_pattern" colspan="1" rowspan="1" valign="top">&nbsp;</td></tr><tr><td id="cell_pattern" colspan="3" rowspan="1" valign="top"><table width="510"> <tbody> <tr class="px13"> <td>  Предназначен для освещения фасадов зданий, архитектурных сооружений, рекламных щитов, открытых территорий.<br> Материал корпуса: анодированный алюминий.<br> Материал рассеивателя: закалённое стекло.<br> Номинальное напряжение: 200-240 В, 50 Гц.<br> Номинальная мощность: 100 Вт (соответствует галогенной лампе 1000 Вт).<br>  Источник света: светодиоды (LED).<br> Цветовая температура: 6500 К (дневной свет).<br> Угол рассеивания: 120°.<br> Световой поток: 8000 лм. <br> Светоодача: 80 лм/Вт.<br> Степень защиты: IP65.<br> Коэффициент пульсации: менее 20%.<br> Индекс цветопередачи: 75.<br> Масса: 0,88 кг.<br> Срок службы: 30 000 часов.<br> Температура эксплуатации: от -40 °C до +45°C. <br> Габаритные размеры: 251х183х36 мм.<br> Сертификат: EAC.<br> Изготовитель: «ЭРА», Китай.<br> <b>Номер по прайс-листу: С0579.</b> </td></tr> </tbody> </table></td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td id="cell_pattern" colspan="3" rowspan="1" valign="top">&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></tbody></table>',
                   'moreInfo': '',
                   'url': 'https://www.electro-mpo.ru/catalog/svetilniki_svetodiodnye_svetilniki_i_lenty_prozhek/s05_svetodiodnye_prozhektory/s0579-prozhektor-b0043566-lpr-021-0-65k-100-220v-1/'},
                   {'name': 'В6222. Стремянка AL160 бытовая алюминиевая 6 ступеней (Gierre)',
                    'price': '5079.73',
                    'measurment': '',
                    'info': '<table id="card_pattern" width="300" border="0"> <tbody> </tbody><caption> <center> <span style="font-size: 20px; color: #032f89"> <b>Стремянка AL160 бытовая алюминиевая 6 ступеней («Gierre»)</b> </span> </center> </caption><tbody><tr><td id="cell_pattern" colspan="2" rowspan="7" valign="top">&nbsp;</td><td id="cell_pattern" colspan="2" rowspan="6" valign="top"><table width="500"> <tbody> <tr class="px13"> <td> Предназначена для бытового использования. <br> Рифлёная поверхность ступеней и платформ. <br> Платформы и ступени выдерживают нагрузку до 150 кг. <br> Изготовитель: «Gierre». </td> </tr> </tbody> </table></td></tr><tr></tr><tr></tr><tr></tr><tr></tr><tr></tr><tr><td id="cell_pattern" colspan="1" rowspan="1" valign="top">&nbsp;</td><td id="cell_pattern" colspan="1" rowspan="1" valign="top"><table width="400" height="185" cellspacing="0" border="1"> <tbody>  <tr class="px13" valign="center" align="center"> <td width="80">Марка</td> <td>Кол-во ступеней</td> <td>Высота платформы H от пола, м</td> <td>Масса, кг</td> <td><b>№ по п/л</b></td> </tr> <tr class="px13" valign="center" align="center">   <td>AL160</td>   <td>6</td>   <td>1,23</td>   <td>5,2</td>   <td><b>В6222</b></td> </tr> </tbody> </table></td></tr></tbody></table>',
                    'moreInfo': '',
                    'url': 'https://www.electro-mpo.ru/catalog/lestnitsy_stremyanki_vyshki_tury/v62_stremyanki_bytovye_professionalnye/v6222-stremyanka-al160-bytovaya-alyuminievaya-6-st/'},
                    ]

        for i, url in enumerate(targetUrls):
            parced = parser.parseUrl(url)
            self.assertEqual(results[i]['name'], parced['name'])
            self.assertEqual(results[i]['price'], parced['price'])
            self.assertEqual(results[i]['url'], parced['url'])

        # ekonomstroy
        urlPrefs = {'validator': ['span', {'class': 'span_price'}],
                     'nameTag': ['h1', {'class': 'bx-title dbg_title'}],
                     'priceTag': ['span', {'class': 'span_price'}],
                     'measurmentTag': ['', ''],
                     'shortDescTag': ['div', {'class': 'descr'}],
                     'longDescTag': ['', '']}
        parser = Parser(**urlPrefs)
        results = None

        targetUrls = [
            'https://www.ekonomstroy.ru/catalog/kley_plitochnyy/kley_plitochnyy_veber_vetonit_granit_fiks_25kg/',
            'https://www.ekonomstroy.ru/catalog/chayniki/chaynik_nerzh_3_0l_art_tm_deco_hy_3807_12_so_svistkom/'
            ]

        results = [{'name': 'Клей плиточный Weber Vetonit Granit Fix 25 кг 1009950',
                   'price': '450 руб. /\n шт',
                   'measurment': '',
                   'info': '',
                   'moreInfo': '',
                   'url': 'https://www.ekonomstroy.ru/catalog/kley_plitochnyy/kley_plitochnyy_veber_vetonit_granit_fiks_25kg/'},
                   {'name': 'Чайник нержавейка 3,0 л арт. ТМ DECO.HY-3807 (12) со свистком',
                    'price': '1 330 руб. /\n шт',
                    'measurment': '',
                    'info': '',
                    'moreInfo': '',
                    'url': 'https://www.ekonomstroy.ru/catalog/chayniki/chaynik_nerzh_3_0l_art_tm_deco_hy_3807_12_so_svistkom/'},
        ]

        for i, url in enumerate(targetUrls):
            parced = parser.parseUrl(url)
            self.assertEqual(results[i]['name'], parced['name'])
            self.assertEqual(results[i]['price'], parced['price'])
            self.assertEqual(results[i]['url'], parced['url'])


if __name__ == '__main__':
    unittest.main()
