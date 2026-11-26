import unittest

from calculadora.excepciones import ErrorDeValidacion
from calculadora.validaciones import validar_entradas, validar_numero, validar_seccion


class PruebasValidaciones(unittest.TestCase):
    def test_coma_y_punto(self):
        self.assertEqual(validar_numero("2,5", "x"), 2.5)
        self.assertEqual(validar_numero("2.5", "x"), 2.5)

    def test_seccion_formatos_validos(self):
        for texto in ("2.5", "2,5", "2.5 mm2", "2,5 mm²", "2.5MM2"):
            self.assertEqual(validar_seccion(texto), 2.5, texto)

    def test_seccion_formatos_invalidos(self):
        for texto in ("2.5 cm2", "AWG 12", "dos mm2", "", "  ", "2,5,3", "2,5 mm3"):
            with self.assertRaises(ErrorDeValidacion, msg=texto):
                validar_seccion(texto)

    def test_valores_no_validos(self):
        for texto in ("", "abc", "0", "-5", "nan", "inf", "-inf", "9" * 400):
            with self.assertRaises(ErrorDeValidacion, msg=texto):
                validar_numero(texto, "campo")

    def test_entradas_completas(self):
        d = validar_entradas("12", "10", "cobre", "5", "2,5 mm²")
        self.assertEqual(d["seccion_mm2"], 2.5)

    def test_material_invalido(self):
        with self.assertRaises(ErrorDeValidacion):
            validar_entradas("12", "10", "madera", "5", "2.5")


if __name__ == "__main__":
    unittest.main()
