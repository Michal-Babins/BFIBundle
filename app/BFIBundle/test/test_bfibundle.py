import unittest
from bfibundle import ( BfiSource,BfiTaxonomy,BfiLiterature )


class SourceTest(unittest.TestCase):
    def test_all_partners(self) -> None:
        bacteria_list = BfiSource.bacterial_partners()
        fungal_list = BfiSource.fungal_partners()
        self.assertTrue(all(item for item in bacteria_list))
        self.assertTrue(all(item for item in fungal_list))
        
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
        
    def test_by_id(self) -> None:
        id_rec = BfiSource.by_id('bfisrc-f95973f4a8094f60a601eaeab807535f')
        self.assertTrue(
            (all(rec for rec in id_rec))
        )
        
class TaxonomyTest(unittest.TestCase):
    def test_search_bacteria(self):
        bac_rec =  BfiTaxonomy.bacteria('genus','Agroccous')
        self.assertTrue(
            (all(rec for rec in bac_rec))
        )
       
    def test_search_fungi(self):
       fun_rec =  BfiTaxonomy.fungi('genus','Fusarium')
       self.assertTrue(
            (all(rec for rec in fun_rec))
        )
       
       
    def test_map_bac(self):
        bac_tax_rec = BfiTaxonomy.map_bacteria('bfisrc-f95973f4a8094f60a601eaeab807535f')
        self.assertTrue(
            (all(rec for rec in bac_tax_rec))
        )
        
    def test_map_bac(self):
        fun_tax_rec = BfiTaxonomy.map_fungi('bfisrc-f95973f4a8094f60a601eaeab807535f')
        self.assertTrue(
            (all(rec for rec in fun_tax_rec))
        )
        
    def test_map_tax(self):
        tax_rec = BfiTaxonomy.map_taxa('bfisrc-f95973f4a8094f60a601eaeab807535f')
        self.assertTrue(
            (all(rec for rec in tax_rec))
        )
       
       
class LiteratureTest(unittest.TestCase):
    def test_search_bfi(self):
        res = BfiLiterature.keyword_search(['Bacterial','Fungal','Interactions'])
        self.assertIn('data',res)
    
    def test_search_paper_by_id(self):
        res = BfiLiterature.paperId_search('16ad00ecfa24b3f740a02b0b453002a4c33942c6')
        self.assertTrue(res)
        
    def test_search_doi(self):
        res = BfiLiterature.doi_search('https://doi.org/10.1111/1574-6968.12287')
        self.assertTrue(res)