from unittest import TestCase
from xplane_airports.AptDat import Airport, AptDat, MetadataKey, AptDatLine, RunwayType


class TestAptDatLine(TestCase):
    def test_file_headers(self):
        for file_header in ('I\r\n', ' A\n', '1000 Generated by WorldEditor\r\n'):
            self.assertTrue(AptDatLine(file_header).is_file_header())
            self.assertTrue(AptDatLine(file_header).is_ignorable())
            self.assertFalse(AptDatLine(file_header).is_airport_header())
            self.assertFalse(AptDatLine(file_header).is_runway())

    def test_airport_headers(self):
        line = AptDatLine('1    695 1 0 EDX6 Schwalmstadt Ziegenhain\r\n')
        self.assertTrue(line.is_airport_header())
        self.assertFalse(line.is_ignorable())
        self.assertFalse(line.is_file_header())
        self.assertFalse(line.is_runway())

    def test_runway_line(self):
        line = AptDatLine('100 30.00 3 0 0.00 0 0 0 14  50.90432000  009.23853100    0    0 1 0 0 0 32  50.89749800  009.24514000    0    0 1 0 0 0')
        self.assertTrue(line.is_runway())
        self.assertFalse(line.is_airport_header())
        self.assertFalse(line.is_ignorable())
        self.assertFalse(line.is_file_header())
        self.assertEqual(line.runway_type, RunwayType.LAND_RUNWAY)

    def test_tokens(self):
        line = AptDatLine('100 30.00 3 0 0.00 0 0 0 14  50.90432000  009.23853100    0    0 1 0 0 0 32  50.89749800  009.24514000    0    0 1 0 0 0')
        self.assertTrue(line.is_runway())
        self.assertFalse(line.is_airport_header())
        self.assertFalse(line.is_ignorable())
        self.assertFalse(line.is_file_header())


class TestAptDat(TestCase):
    def setUp(self):
        self.apt_dat_single_string = """I
                        1000 Generated by WorldEditor

                        1    695 1 0 EDX6 Schwalmstadt Ziegenhain
                        100 30.00 3 0 0.00 0 0 0 14  50.90432000  009.23853100    0    0 1 0 0 0 32  50.89749800  009.24514000    0    0 1 0 0 0
                        100 30.00 3 0 0.00 0 0 0 03  50.90159600  009.23946100    0    0 1 0 0 0 21  50.90923600  009.24563000    0    0 1 0 0 0
                        110 1 0.00 0.0000 Asphalt paths
                        111  50.90234299  009.24281174
                        99
                        """

        self.apt_dat_single_string1 = """I
                            1000 Generated by WorldEditor

                            1     20 1 0 KBOS Boston Logan Intl
                            100 46.02 1 1 0.00 1 3 1 15R  42.37428432 -071.01792575  268   61 3 8 1 0 33L  42.35466419 -070.99162135    0   53 3 8 1 0
                            100 46.02 1 1 0.00 1 3 1 04L  42.35800046 -071.01437574    0    0 3 0 0 2 22R  42.37830380 -071.00455234  248   61 3 0 0 0
                            100 46.02 1 1 0.00 1 3 1 04R  42.35107249 -071.01183012  352    0 3 2 1 0 22L  42.37691354 -070.99932612  365   61 3 9 0 0
                            100 46.02 1 1 0.00 1 3 1 09  42.35576765 -071.01292865    0    0 3 0 0 0 27  42.36023032 -070.98773848    0   49 3 0 0 1
                            100 29.87 1 1 0.00 0 2 0 15L  42.37359269 -071.00916205    0   30 2 0 0 0 33R  42.36861510 -071.00249217    0   30 2 0 0 0
                            100 29.87 1 0 0.00 0 3 1 14  42.35661149 -071.02331027    0    0 2 0 0 0 32  42.34861319 -071.00828089    0  244 3 0 1 1
                            110 2 0.00 257.3300 Concrete Pad Hangar
                            111  42.36509655 -071.00267196
                            99
                           """

        self.apt_dat_multi_string = """A
                                1000 Generated by WorldEditor

                                1   2084 0 0 YTWB Toowoomba
                                100 29.87 1 0 0.25 0 2 0 11 -27.54021531  151.91198836    0    0 2 0 1 0 29 -27.54021533  151.92212245    0    0 2 0 1 0
                                100 49.99 15 0 0.25 0 0 0 07 -27.54417182  151.91052007    0    0 0 0 0 0 25 -27.54206566  151.91805380    0    0 0 0 0 0
                                1302 icao_code YTWB
                                110 2 1.00 190.0000 New Taxiway 13
                                111 -27.54381636  151.91715300
                                111 -27.54388400  151.91714277
                                111 -27.54390957  151.91731210
                                1200 Taxi network
                                1201 47.54 -122.308 both 5416 A_start
                                1000 Calm and south flows
                                1001 YTWB 000 359 5

                                1     39 0 0 SDCR Fazenda Caicara
                                100 17.98 5 0 0.00 0 0 0 09 -24.06946550 -046.82978069    0    0 0 0 0 0 27 -24.06748020 -046.82470758    0    0 0 0 0 0
                                110 4 0.00 0.0000 Dirtway
                                112 -24.06984901 -046.83011229 -24.06987583 -046.83011229
                                112 -24.07008327 -046.83006415 -24.07010219 -046.83004461
                                112 -24.07014133 -046.82997383 -24.07016201 -046.82995406
                                112 -24.07086622 -046.82960021 -24.07088131 -046.82959287

                                1    978 1 0 SCVO Maria Ester
                                100 20.12 3 0 0.00 0 0 0 06 -38.23172467 -072.48881639    0    0 1 0 0 0 24 -38.23021033 -072.48162169    0    0 1 0 0 0
                                110 3 0.25 75.0000 Base grass
                                111 -38.23230963 -072.49005050
                                111 -38.23036611 -072.48081362
                                111 -38.22980450 -072.48098277


                                1   1235 0 0 YTNK Tennant Creek
                                100 29.87 1 0 0.25 0 1 0 07 -19.63589237  134.16954220    0    0 2 0 0 0 25 -19.63113463  134.18751318    0    0 2 0 0 0
                                100 17.98 1 1 0.25 0 1 0 11 -19.63383181  134.17579223    0    0 1 0 0 0 29 -19.63848096  134.18455258    0    0 1 0 0 0
                                100 11.89 1 0 0.25 0 0 0 2 -19.63780860  134.18404058    0    0 1 0 0 0 20 -19.63169996  134.18683776    0    0 1 0 0 0
                                110 1 1.00 74.3000 New Taxiway 2
                                111 -19.63151194  134.18661256
                                111 -19.63157860  134.18668333
                                99
                                """

        self.multi_parser = AptDat.from_file_text(self.apt_dat_multi_string, 'foo.dat')
        self.single_parser = AptDat.from_file_text(self.apt_dat_single_string, 'bar.dat')[0]
        self.single_parser1 = AptDat.from_file_text(self.apt_dat_single_string1, '')[0]
        self.single_parser_from_multi = self.multi_parser["sCvO"]

    #######################################
    # Tests for the multi-apt.dat parser
    #######################################
    def test_names(self):
        for expected, actual in zip(self.multi_parser.names, ["Toowoomba", "Fazenda Caicara", "Maria Ester", "Tennant Creek"]):
            self.assertEqual(expected, actual, "Airport names do not match")

    def test_ids(self):
        self.assertListEqual(list(self.multi_parser.ids), ["YTWB", "SDCR", "SCVO", "YTNK"], "ICAO codes do not match")

    def test_have_atc(self):
        self.assertListEqual(list(apt.has_atc for apt in self.multi_parser), [False, False, True, False], "ATC statuses do not match")

    def test_elevation(self):
        self.assertAlmostEqual(list(apt.elevation_ft_amsl for apt in self.multi_parser), [2084, 39, 978, 1235], "Elevations do not match")

    def test_latitude(self):
        lats = list(apt.latitude for apt in self.multi_parser)
        self.assertAlmostEqual(lats[0], -27.54021532, msg="Latitudes do not match")
        self.assertAlmostEqual(lats[1], -24.06847285, msg="Latitudes do not match")
        self.assertAlmostEqual(lats[2], -38.23096750, msg="Latitudes do not match")
        self.assertAlmostEqual(lats[3], -19.63351350, msg="Latitudes do not match")

    def test_longitude(self):
        longs = list(apt.longitude for apt in self.multi_parser)
        self.assertAlmostEqual(longs[0], 151.917055405, msg="Longitudes do not match")
        self.assertAlmostEqual(longs[1], -46.827244135, msg="Longitudes do not match")
        self.assertAlmostEqual(longs[2], -72.485219040, msg="Longitudes do not match")
        self.assertAlmostEqual(longs[3],  134.17852769, msg="Longitudes do not match")

    def _compare_actual_full_texts_to_expected(self, actual_texts, expected_texts):
        self.assertEqual(len(actual_texts), len(expected_texts), "Missing airport data")

        for actual_text, expected_text in zip(actual_texts, expected_texts):
            for actual_line, expected_line in zip(actual_text.split("\n"), expected_text.split("\n")):
                actual_line = actual_line.strip()
                expected_line = expected_line.strip()

                DEBUG = True
                if DEBUG and actual_line != expected_line:
                    print("Mismatch between lines (actual, followed by expected):")
                    print(actual_line)
                    print("-------------")
                    print(expected_line)
                self.assertEqual(actual_line, expected_line, "Lines in full text don't match")

    def test_get_full_text(self):
        canonical = []
        canonical.append("""1   2084 0 0 YTWB Toowoomba
                            100 29.87 1 0 0.25 0 2 0 11 -27.54021531  151.91198836    0    0 2 0 1 0 29 -27.54021533  151.92212245    0    0 2 0 1 0
                            100 49.99 15 0 0.25 0 0 0 07 -27.54417182  151.91052007    0    0 0 0 0 0 25 -27.54206566  151.91805380    0    0 0 0 0 0
                            1302 icao_code YTWB
                            110 2 1.00 190.0000 New Taxiway 13
                            111 -27.54381636  151.91715300
                            111 -27.54388400  151.91714277
                            111 -27.54390957  151.91731210
                            1200 Taxi network
                            1201 47.54 -122.308 both 5416 A_start
                            1000 Calm and south flows
                            1001 YTWB 000 359 5
                            """)
        canonical.append("""1     39 0 0 SDCR Fazenda Caicara
                            100 17.98 5 0 0.00 0 0 0 09 -24.06946550 -046.82978069    0    0 0 0 0 0 27 -24.06748020 -046.82470758    0    0 0 0 0 0
                            110 4 0.00 0.0000 Dirtway
                            112 -24.06984901 -046.83011229 -24.06987583 -046.83011229
                            112 -24.07008327 -046.83006415 -24.07010219 -046.83004461
                            112 -24.07014133 -046.82997383 -24.07016201 -046.82995406
                            112 -24.07086622 -046.82960021 -24.07088131 -046.82959287""")
        canonical.append("""1    978 1 0 SCVO Maria Ester
                            100 20.12 3 0 0.00 0 0 0 06 -38.23172467 -072.48881639    0    0 1 0 0 0 24 -38.23021033 -072.48162169    0    0 1 0 0 0
                            110 3 0.25 75.0000 Base grass
                            111 -38.23230963 -072.49005050
                            111 -38.23036611 -072.48081362
                            111 -38.22980450 -072.48098277""")
        canonical.append("""1   1235 0 0 YTNK Tennant Creek
                            100 29.87 1 0 0.25 0 1 0 07 -19.63589237  134.16954220    0    0 2 0 0 0 25 -19.63113463  134.18751318    0    0 2 0 0 0
                            100 17.98 1 1 0.25 0 1 0 11 -19.63383181  134.17579223    0    0 1 0 0 0 29 -19.63848096  134.18455258    0    0 1 0 0 0
                            100 11.89 1 0 0.25 0 0 0 2 -19.63780860  134.18404058    0    0 1 0 0 0 20 -19.63169996  134.18683776    0    0 1 0 0 0
                            110 1 1.00 74.3000 New Taxiway 2
                            111 -19.63151194  134.18661256
                            111 -19.63157860  134.18668333""")
        self._compare_actual_full_texts_to_expected(list(str(apt) for apt in self.multi_parser), canonical)

    def test_sort(self):
        canonical = []
        canonical.append("""1     39 0 0 SDCR Fazenda Caicara
                            100 17.98 5 0 0.00 0 0 0 09 -24.06946550 -046.82978069    0    0 0 0 0 0 27 -24.06748020 -046.82470758    0    0 0 0 0 0
                            110 4 0.00 0.0000 Dirtway
                            112 -24.06984901 -046.83011229 -24.06987583 -046.83011229
                            112 -24.07008327 -046.83006415 -24.07010219 -046.83004461
                            112 -24.07014133 -046.82997383 -24.07016201 -046.82995406
                            112 -24.07086622 -046.82960021 -24.07088131 -046.82959287""")
        canonical.append("""1    978 1 0 SCVO Maria Ester
                            100 20.12 3 0 0.00 0 0 0 06 -38.23172467 -072.48881639    0    0 1 0 0 0 24 -38.23021033 -072.48162169    0    0 1 0 0 0
                            110 3 0.25 75.0000 Base grass
                            111 -38.23230963 -072.49005050
                            111 -38.23036611 -072.48081362
                            111 -38.22980450 -072.48098277""")
        canonical.append("""1   1235 0 0 YTNK Tennant Creek
                            100 29.87 1 0 0.25 0 1 0 07 -19.63589237  134.16954220    0    0 2 0 0 0 25 -19.63113463  134.18751318    0    0 2 0 0 0
                            100 17.98 1 1 0.25 0 1 0 11 -19.63383181  134.17579223    0    0 1 0 0 0 29 -19.63848096  134.18455258    0    0 1 0 0 0
                            100 11.89 1 0 0.25 0 0 0 2 -19.63780860  134.18404058    0    0 1 0 0 0 20 -19.63169996  134.18683776    0    0 1 0 0 0
                            110 1 1.00 74.3000 New Taxiway 2
                            111 -19.63151194  134.18661256
                            111 -19.63157860  134.18668333""")
        canonical.append("""1   2084 0 0 YTWB Toowoomba
                            100 29.87 1 0 0.25 0 2 0 11 -27.54021531  151.91198836    0    0 2 0 1 0 29 -27.54021533  151.92212245    0    0 2 0 1 0
                            100 49.99 15 0 0.25 0 0 0 07 -27.54417182  151.91052007    0    0 0 0 0 0 25 -27.54206566  151.91805380    0    0 0 0 0 0
                            1302 icao_code YTWB
                            110 2 1.00 190.0000 New Taxiway 13
                            111 -27.54381636  151.91715300
                            111 -27.54388400  151.91714277
                            111 -27.54390957  151.91731210
                            1200 Taxi network
                            1201 47.54 -122.308 both 5416 A_start
                            1000 Calm and south flows
                            1001 YTWB 000 359 5
                            """)
        self.multi_parser.sort()
        self._compare_actual_full_texts_to_expected(list(str(apt) for apt in self.multi_parser), canonical)

    def test_metadata_parsing(self):
        ytwb_text = """A
                    1000 Generated by WorldEditor

                    1   2084 0 0 YTWB Toowoomba
                    1302 datum_lat 123
                    1302 gui_label 3D
                    1302 icao_code YTWB
                    1302 iata_code FHGWGADS
                    1302 fake_key fjwpf
                    100 29.87 1 0 0.25 0 2 0 11 -27.54021531  151.91198836    0    0 2 0 1 0 29 -27.54021533  151.92212245    0    0 2 0 1 0
                    100 49.99 15 0 0.25 0 0 0 07 -27.54417182  151.91052007    0    0 0 0 0 0 25 -27.54206566  151.91805380    0    0 0 0 0 0
                    110 2 1.00 190.0000 New Taxiway 13
                    """

        ytwb = AptDat.from_file_text(ytwb_text, 'ytwb.dat')[0]
        self.assertEqual(ytwb.metadata[MetadataKey.ICAO_CODE], 'YTWB')
        self.assertEqual(ytwb.metadata[MetadataKey.IATA_CODE], 'FHGWGADS')
        self.assertEqual(ytwb.metadata[MetadataKey.LABEL_3D_OR_2D], '3D')

    def test_empty_metadata_entires(self):
        ytwb_broken_text = """A
                            1000 Generated by WorldEditor
        
                            1   2084 0 0 YTWB Toowoomba
                            1302 datum_lat 
                            1302 gui_label 
                            1302 icao_code 
                            1302 iata_code FHGWGADS
                            1302 fake_key fjwpf
                            100 29.87 1 0 0.25 0 2 0 11 -27.54021531  151.91198836    0    0 2 0 1 0 29 -27.54021533  151.92212245    0    0 2 0 1 0
                            100 49.99 15 0 0.25 0 0 0 07 -27.54417182  151.91052007    0    0 0 0 0 0 25 -27.54206566  151.91805380    0    0 0 0 0 0
                            110 2 1.00 190.0000 New Taxiway 13
                            """
        ytwb = Airport.from_str(ytwb_broken_text, 'ytwb.dat')
        self.assertFalse(MetadataKey.ICAO_CODE in ytwb.metadata)
        self.assertFalse(MetadataKey.DATUM_LAT in ytwb.metadata)
        self.assertFalse(MetadataKey.ICAO_CODE in ytwb.metadata)
        self.assertEqual(ytwb.metadata[MetadataKey.IATA_CODE], 'FHGWGADS')

        strval = str(ytwb)
        self.assertFalse('datum_lat' in strval)
        self.assertFalse('gui_label' in strval)
        self.assertFalse('icao_code' in strval)
        self.assertTrue('iata_code' in strval)

    def test_addition_operator(self):
        combined = AptDat.from_file_text(self.apt_dat_multi_string, 'combined.dat')
        self.assertEqual(str(combined), str(self.multi_parser))

        # Test += op
        combined += self.single_parser
        for apt_code in list(self.multi_parser.ids) + [self.single_parser.id]:
            self.assertTrue(apt_code in combined.ids)
        for apt_name in list(self.multi_parser.names) + [self.single_parser.name]:
            self.assertTrue(apt_name in combined.names)
        for text in [str(self.multi_parser), str(self.single_parser)]:
            self.assertTrue(text in str(combined))

        # Test + op
        new_combined = self.multi_parser + self.single_parser
        self.assertEqual(str(new_combined), str(combined))

    def test_contains(self):
        self.assertTrue('YTWB' in self.multi_parser)
        self.assertTrue('SDCR' in self.multi_parser)
        self.assertTrue('SCVO' in self.multi_parser)
        self.assertTrue('YTNK' in self.multi_parser)
        for apt in self.multi_parser:
            self.assertTrue(apt in self.multi_parser)
        self.assertFalse('KSEA' in self.multi_parser)

    def test_clone(self):
        cloned = self.multi_parser.clone()
        for i in range(len(cloned)):
            self.assertEqual(cloned[i], self.multi_parser[i])

    def test_delete(self):
        cloned = self.multi_parser.clone()
        self.assertTrue('YTWB' in cloned)
        del cloned['YTWB']
        self.assertFalse('YTWB' in cloned)

        apt0 = cloned[0]
        self.assertTrue(apt0 in cloned)
        del cloned[0]
        self.assertFalse(apt0 in cloned)

        aptLast = cloned[-1]
        self.assertTrue(aptLast in cloned)
        del cloned[aptLast]
        self.assertFalse(aptLast in cloned)

    def test_reversed(self):
        reversed_ids = [apt.id for apt in reversed(self.multi_parser)]
        for i, apt_id in enumerate(apt.id for apt in self.multi_parser):
            self.assertEqual(apt_id, reversed_ids[len(reversed_ids) - 1 - i])

    #######################################
    # Tests for the single apt.dat parser
    #######################################
    def test_get_apt_name(self):
        error_msg = "Airport names do not match"
        self.assertEqual(self.single_parser.name, "Schwalmstadt Ziegenhain", error_msg)
        self.assertEqual(self.single_parser1.name, "Boston Logan Intl", error_msg)
        self.assertEqual(self.single_parser_from_multi.name, "Maria Ester", error_msg)

    def test_get_apt_ICAO_code(self):
        error_msg = "ICAO codes do not match"
        self.assertEqual(self.single_parser.id, "EDX6", error_msg)
        self.assertEqual(self.single_parser1.id, "KBOS", error_msg)
        self.assertEqual(self.single_parser_from_multi.id, "SCVO", error_msg)

    def test_has_atc(self):
        error_msg = "ATC status does not match"
        self.assertTrue(self.single_parser.has_atc, error_msg)
        self.assertTrue(self.single_parser1.has_atc, error_msg)
        self.assertTrue(self.single_parser_from_multi.has_atc, error_msg)

    def test_get_elevation_feet_amsl(self):
        error_msg = "Elevation does not match"
        self.assertAlmostEqual(self.single_parser.elevation_ft_amsl, 695.0, msg=error_msg)
        self.assertAlmostEqual(self.single_parser1.elevation_ft_amsl, 20.0, msg=error_msg)
        self.assertAlmostEqual(self.single_parser_from_multi.elevation_ft_amsl, 978, msg=error_msg)

    def test_properties(self):
        for apt in self.multi_parser:
            self.assertEqual(apt.has_taxi_route, apt.id == 'YTWB', 'Only YTWB in the list should have this feature')
            self.assertEqual(apt.has_traffic_flow, apt.id == 'YTWB', 'Only YTWB in the list should have this feature')
