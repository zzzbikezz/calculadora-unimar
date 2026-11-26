import csv
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from calculadora.excepciones import ReporteError
from servicios import historial, reportes
from utilidades.generadores import iterar_registros, ultimas_lineas_log

ENT = {"tension": 12.0, "resistencia_carga": 10.0, "material": "cobre", "longitud_ida": 5.0, "seccion_mm2": 2.5}
RES = {"rc_ohm": 0.0672, "rt_ohm": 10.0672, "corriente_a": 1.192, "caida_tension_v": 0.0801,
       "potencia_cable_w": 0.0955}


class PruebasServicios(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.ruta = self.dir / "data" / "historial.json"

    def test_crea_archivo_si_no_existe(self):
        self.assertEqual(historial.cargar_historial(self.ruta), [])
        self.assertTrue(self.ruta.exists())

    def test_guarda_y_persiste(self):
        historial.guardar_calculo(ENT, RES, self.ruta)
        historial.guardar_calculo(ENT, RES, self.ruta)
        datos = historial.cargar_historial(self.ruta)  # "reinicio": se vuelve a leer del disco
        self.assertEqual([r["id"] for r in datos], ["0001", "0002"])

    def test_json_corrupto(self):
        self.ruta.parent.mkdir(parents=True)
        self.ruta.write_text("{esto no es json", encoding="utf-8")
        self.assertEqual(historial.cargar_historial(self.ruta), [])
        self.assertEqual(json.loads(self.ruta.read_text(encoding="utf-8")), [])
        self.assertEqual(len(list(self.ruta.parent.glob("*.corrupto.*.json"))), 1)

    def test_filtros(self):
        a = historial.guardar_calculo(ENT, RES, self.ruta)
        otro = dict(ENT, material="aluminio")
        historial.guardar_calculo(otro, RES, self.ruta)
        regs = historial.cargar_historial(self.ruta)
        self.assertEqual(len(historial.filtrar_historial(regs, material="aluminio")), 1)
        hoy = date.today()
        self.assertEqual(len(list(iterar_registros(regs, desde=hoy, hasta=hoy))), 2)
        self.assertEqual(historial.filtrar_historial(regs, material="oro"), [])
        self.assertEqual(a["id"], "0001")

    def test_csv(self):
        reg = historial.guardar_calculo(ENT, RES, self.ruta)
        ruta_csv = reportes.exportar_csv([reg], self.dir / "rep")
        with open(ruta_csv, encoding="utf-8-sig") as f:
            filas = list(csv.reader(f))
        self.assertEqual(filas[0], reportes.ENCABEZADOS)
        self.assertEqual(len(filas), 2)
        with self.assertRaises(ReporteError):
            reportes.exportar_csv([], self.dir / "rep")

    def test_generador_logs(self):
        log = self.dir / "a.log"
        log.write_text("t | INFO | m | uno\nt | ERROR | m | dos\nt | INFO | m | tres\n", encoding="utf-8")
        self.assertEqual(len(ultimas_lineas_log(log, 10)), 3)
        self.assertEqual(len(ultimas_lineas_log(log, 10, ["ERROR"])), 1)
        self.assertTrue(ultimas_lineas_log(log, 2)[0].endswith("tres"))


if __name__ == "__main__":
    unittest.main()
