import unittest

from calculadora.calculos import calcular_circuito, convertir_mm2_a_m2, formatear_resultados


class PruebasCalculos(unittest.TestCase):
    def test_1_referencia(self):
        r = calcular_circuito(12, 10, "cobre", 5, 2.5)
        self.assertAlmostEqual(r["rc_ohm"], 0.0672, places=4)
        self.assertAlmostEqual(r["rt_ohm"], 10.0672, places=4)
        self.assertAlmostEqual(r["corriente_a"], 1.1920, places=4)
        self.assertAlmostEqual(r["caida_tension_v"], 0.0801, places=4)
        self.assertAlmostEqual(r["potencia_cable_w"], 0.0955, places=4)

    def test_2_material_distinto(self):
        cobre = calcular_circuito(12, 10, "cobre", 5, 2.5)
        alu = calcular_circuito(12, 10, "aluminio", 5, 2.5)
        self.assertGreater(alu["rc_ohm"], cobre["rc_ohm"])
        self.assertAlmostEqual(alu["rc_ohm"], 0.106, places=4)

    def test_3_seccion(self):
        mayor = calcular_circuito(12, 10, "cobre", 5, 6)
        menor = calcular_circuito(12, 10, "cobre", 5, 1)
        self.assertLess(mayor["rc_ohm"], menor["rc_ohm"])

    def test_conversion_area(self):
        self.assertAlmostEqual(convertir_mm2_a_m2(2.5), 2.5e-6)

    def test_formato(self):
        r = calcular_circuito(12, 10, "cobre", 5, 2.5)
        self.assertEqual(formatear_resultados(r)[0][1], "0.0672")


if __name__ == "__main__":
    unittest.main()
