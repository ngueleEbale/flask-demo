from web3 import Web3
import json
from flask import Flask
import config as config

# Se connecter à Ganache
web3 = Web3(Web3.HTTPProvider(config.ganache_url))  

# Adresse du contrat intelligent
contract_address = config.adresse_contrat

# Charger l'ABI à partir du fichier JSON
with open(config.abi_path, 'r') as f:
    contract_abi = json.load(f)

# Instanciation du contrat
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Fonction pour enregistrer une naissance
def enregistrer_naissance(nom, prenom, nom_pere, travail_pere, nom_mere, travail_mere, date_naissance, sexe, lieu_naissance, nipu):
    nonce = web3.eth.getTransactionCount(config.adresse_compte)
    txn_dict = contract.functions.enregistrerNaissance(nom, prenom, nom_pere, travail_pere, nom_mere, travail_mere, date_naissance, sexe, lieu_naissance, nipu).buildTransaction({
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })
    private_key = config.clé_privee
    signed_txn = web3.eth.account.signTransaction(txn_dict, private_key=private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)
    print("Transaction hash:", txn_receipt.transactionHash.hex())
    return txn_receipt

# Fonction pour consulter les détails d'une naissance en particulier
def consulter_details(id_naissance):
    return contract.functions.consulterDetails(id_naissance).call()

# Fonction pour récupérer toutes les naissances enregistrées
def recup_toutes_les_naissances():
    return contract.functions.recupToutesLesNaissances().call()

# Exemple d'utilisation
if __name__ == "__main__":
    # Enregistrer une nouvelle naissance
    tx_receipt = enregistrer_naissance("Jean", "Pierre", "Dupont", "Ingénieur", "Dupont", "Médecin", 1654932000, "M", "Paris", "20220218-01M")
    print("Transaction réussie:", tx_receipt)

    # Consulter les détails d'une naissance par ID
    id_naissance = 0  # Remplacer par l'ID de la naissance que vous souhaitez consulter
    details_naissance = consulter_details(id_naissance)
    print("Détails de la naissance:", details_naissance)

    # Récupérer toutes les naissances enregistrées
    toutes_les_naissances = recup_toutes_les_naissances()
    print("Toutes les naissances enregistrées:", toutes_les_naissances)
