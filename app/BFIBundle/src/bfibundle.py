import requests
from crossref.restful import Works
from typing import List,Dict
from utils import data_dump

#set global variable
api_url = "https://sfa-bfi.edgebioinformatics.org/api"
   
class BfiSource:
    
    interactions_api_url = api_url + '/interactions'
    
    @staticmethod
    def bacterial_partners() -> List[str]:
        """Get list of all bacterial partners in a BFI pair on their lowest taxonomic classification
        
        Returns:
            List of all bacterial partners
        """
        
        bacterial_partners_url = BfiSource.interactions_api_url + '/bacterial_associates'
        try:
            response = requests.get(bacterial_partners_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
    
    @staticmethod
    def fungal_partners() -> List[str]:
        """Get list of all fungal partners in a BFI pair on their lowest taxonomic classification
        
        Returns:
            List of all fungal partners
        """
        
        fungal_partners_url = BfiSource.interactions_api_url + '/fungal_hosts'
        try: 
            response = requests.get(fungal_partners_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
    
    @staticmethod
    def bfi_fungal_partner(fungal_partner: str) -> List[Dict[str, str]]:
        """Search by fungal partner to reeturn all records associated with the fungal partner

        Args:
            fungal_partner (str): fungal partner taxa

        Returns:
            List[Dict[str, str]]: list of records
        """
        
        params = {"Fungal_host_taxa": fungal_partner}
        bfi_fungal_partner_url = BfiSource.interactions_api_url + '/bfi/fungi'
        try:
            response = requests.get(bfi_fungal_partner_url, params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
        
    @staticmethod
    def bfi_bacterial_partner(bacterial_partner : str) -> List[Dict[str, str]]:
        """Search by bacterial partner to return all records associated with the bacterial partner
        
        Args:
            bacterial_partner (str): bacterial partner taxa

        Returns:
            List[Dict[str, str]]: list of records
        """
        
        params = {"Bacterial_associate_taxa": bacterial_partner}
        bfi_fungal_partner_url = BfiSource.interactions_api_url + '/bfi/bacteria'
        try:
            response = requests.get(bfi_fungal_partner_url, params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
            
    @staticmethod
    def bfi_partners(bacterial_partner : str,fungal_partner : str) -> List[Dict[str, str]]:
        '''Search by bacterial partner to return all records associated with the bacterial partner
        
        Args:
            fungal_partner (str): bacterial partner taxa
            bacterial_partner (str): bacterial partner taxa
        Returns:
            List[Dict[str, str]]: record with search
        
        '''
        
        params = {"Bacterial_associate_taxa": bacterial_partner, "Fungal_host_taxa": fungal_partner}
        bfi_partners_url = BfiSource.interactions_api_url + '/bfi/partners'
        try:
            response = requests.get(bfi_partners_url, params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
            
    @staticmethod
    def by_id(id : str) -> List[Dict[str, str]]:
        """Search for BFI partnership by id

        Args:
            id (str):  unique bfi id

        Returns:
            List[Dict[str, str]]: List of record matching corresponding id
        """
        
        params = {"id" : id}
        bfi_partners_url = BfiSource.interactions_api_url + '/bfi/id'
        try:
            response = requests.get(bfi_partners_url, params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
         
    @staticmethod   
    def dump_bfi(tsv: bool) -> None:
        """Data dump of all described bfi in bfi collection to tsv
        
        Args:
            tsv (bool): default = True, if set to False will writ out json 
        """
        data_dump(api_url,tsv=True)
            
    
class BfiLiterature:
    
    semantic_scholar_api = "http://api.semanticscholar.org/graph/v1/paper"
    
    @staticmethod
    def keyword_search(keywords : List[str], offset: int=10, limit: int=10):
        """Search for litrature using a set of keywords, ex: Bacterial+Fungal+Interactions

        Args:
            keywords (List[str]): list of keywords to search by
            offset (int): search offset 
            limit (int): search limit
        """
        
        params = '+'.join(keywords)
        semantic_search_url = BfiLiterature.semantic_scholar_api + '/search?query=' 
        semantic_search_url_formatted = semantic_search_url + params
        try:
            response = requests.get(semantic_search_url_formatted, params={"offset":offset,"limit":limit})
            print(response.url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
    
    @staticmethod   
    def paperId_search(id: str):
        """Search for paper using SD

        Args:
            id (str): sd id from semantic scholar

        Returns:
            dict: dict of found lit source from SD id
        """
        paper_id_url = f'{BfiLiterature.semantic_scholar_api}/{id}'
        
        params = {"fields":"url,year,authors"}
        try:
            response = requests.get(paper_id_url,params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            print(err)
    
    @staticmethod   
    def doi_search(doi: str):
        """Search by doi to retrieve

        Args:
            doi (str): doi string, this is Link key from BFI Source
        """
        works = Works()
        
        return works.doi(doi)
    
    
class BfiTaxonomy:
    
    _api = api_url + '/interactions/taxa'
    bacterial_taxonomy_url = _api + '/bacteria'
    bacterial_mapping_url = bacterial_taxonomy_url + '/mapLineage?='
    fungal_taxonomy_url = _api + '/fungi'
    fungal_mapping_url = fungal_taxonomy_url + '/mapLineage?='
    taxonomy = ['phylum','class','order','family','genus']
        
    @staticmethod
    def bacteria(taxa_level: str, taxa: str):
        """Lookup up bacteria by specifying taxa level and bacteria name ex: (genus, Achromobacter)

        Args:
            taxa_level (str): acceptable levels [phylum, class, order, family, genus]
            taxa (str): bacteria name corresponding to taxa level

        Returns:
            List[dict(s)]: All taxonomic records with corresponding search, will return empty list if taxa not in database
        """
        
        
        if taxa_level not in BfiTaxonomy.taxonomy:
            print(f'taxonomy level not accepted, taxa levels: {BfiTaxonomy.taxonomy}')
        taxa_level = taxa_level.capitalize()
        return requests.get(BfiTaxonomy.bacterial_taxonomy_url, params={taxa_level: taxa}).json()
    
    @staticmethod
    def map_bacteria(id: str) -> List[Dict[str, str]]:
        """Find bacterial record using bfirsc id

        Args:
            id (str): bfisrc id (ex: bfisrc-8d85x6d6fd5c6sadff6asdfe)

        Returns:
            List[Dict[str, str]]: corresponding bacterial taxonomy record 
        """
        
        query = BfiTaxonomy.bacterial_mapping_url + f'{id}'
        return requests.get(query).json()
    
    @staticmethod
    def fungi(taxa_level,taxa) -> List[Dict[str, str]]:
        """Lookup up fungi by specifying taxa level and fungi name ex: (genus, Achromobacter)

        Args:
            taxa_level (str): acceptable levels [phylum, class, order, family, genus]
            taxa (str): fungal name corresponding to taxa level

        Returns:
            List[dict(s)]: All taxonomic records with corresponding search, will return empty list if taxa not in database
        """
        
        if taxa_level not in BfiTaxonomy.taxonomy:
            print(f'taxonomy level not accepted, taxa levels: {BfiTaxonomy.taxonomy}')
        taxa_level = taxa_level.capitalize()
        return requests.get(BfiTaxonomy.fungal_taxonomy_url, params={taxa_level: taxa}).json()
    
    @staticmethod
    def map_fungi(id: str) -> List[Dict[str, str]]:
        """Find fungal taxonomy record using bfirsc id

        Args:
            id (str): bfisrc id (ex: bfisrc-8d85x6d6fd5c6sadff6asdfe)

        Returns:
            List[Dict[str, str]]: corresponding fungal taxonomy record 
        """
        
        query = BfiTaxonomy.bacterial_mapping_url + f'{id}'
        return requests.get(query).json()
    
    @staticmethod
    def map_taxa(id: str):
        """Find both fungal and bacterial taxonomy of bfi pair using bfi id

        Args:
            id (str): id (str): bfisrc id (ex: bfisrc-8d85x6d6fd5c6sadff6asdfe)
        """
        partner_taxonomy_dict = {} 
        partner_taxonomy_dict['fungal_taxonomy'] = BfiTaxonomy.map_fungi(id)
        partner_taxonomy_dict['bacterial_taxonomy'] = BfiTaxonomy.map_bacteria(id)
        
        return(partner_taxonomy_dict)        