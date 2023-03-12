import unittest
from ..src.bfibundle import BfiSource,BfiTaxonomy,BfiLiterature


class BundleTest(unittest.TestCase):
    def test_all_partners(self) -> None:
        bacteria_list = BfiSource.bacterial_partners()
        fungal_list = BfiSource.fungal_partners()
        self.assertTrue(len(bacteria_list)==len(fungal_list))
        
    def test_bfi_bacterial_partners(self) -> None:
        bacterial_partner = BfiSource.bfi_bacterial_partner('Agrococcus')
        self.assertTrue(
            (all(rec for rec in bacterial_partner))
        )
        
    def test_bfi_fungal_partners(self) -> None:
        fungal_partner = BfiSource.bfi_fungal_partner('Fusarium')
        self.assertTrue(
            (all(rec for rec in fungal_partner))
        )
        
    def test_bfi_partners(self) -> None:
        partners = BfiSource.bfi_partners('Agroccocus', 'Fusarium')
        self.assertTrue(
            (all(rec for rec in partners))
        )
        
    def by_id(self) -> None:
        id_rec = BfiSource.by_id('bfisrc-f95973f4a8094f60a601eaeab807535f')