import os
import requests
from urllib.parse import urlparse
import yt_dlp

def telecharger_fichier_standard(url, dossier_destination):
    """Télécharge un fichier standard (Raw GitHub, CDN, Image, etc.)"""
    try:
        # Extraire le nom du fichier depuis l'URL
        nom_fichier = os.path.basename(urlparse(url).path)
        if not nom_fichier:
            nom_fichier = "fichier_telecharge"
            
        chemin_complet = os.path.join(dossier_destination, nom_fichier)
        
        print(f"[*] Téléchargement de : {nom_fichier}...")
        
        # Téléchargement avec un stream pour voir l'avancement si besoin
        reponse = requests.get(url, stream=True)
        reponse.raise_for_status() # Déclenche une erreur si le lien est mort (404, 500, etc.)
        
        with open(chemin_complet, 'wb') as f:
            for chunk in reponse.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print(f"[+] Succès ! Fichier enregistré dans : {chemin_complet}")
        
    except Exception as e:
        print(f"[-] Erreur lors du téléchargement : {e}")

def telecharger_youtube(url, dossier_destination):
    """Télécharge une vidéo YouTube en combinant la meilleure qualité vidéo et audio."""
    print("[*] Analyse du lien YouTube...")
    
    # Configuration pour yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(dossier_destination, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best', # Meilleure qualité dispo
        'quiet': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[+] Téléchargement YouTube terminé avec succès !")
    except Exception as e:
        print(f"[-] Erreur YouTube : {e}")

def main():
    print("--- OUTIL : DOWNLOADER UNIVERSEL ---")
    url = input("Entre l'URL à télécharger (YouTube, GitHub Raw, CDN...) : ").strip()
    
    if not url:
        print("[-] URL vide.")
        return

    # Création d'un dossier "downloads" à la racine de ton projet
    # (juste à côté de toolhub.py)
    dossier_racine = os.path.dirname(os.path.dirname(__file__))
    dossier_downloads = os.path.join(dossier_racine, "downloads")
    
    if not os.path.exists(dossier_downloads):
        os.makedirs(dossier_downloads)

    # Détection du type de lien
    if "youtube.com" in url or "youtu.be" in url:
        telecharger_youtube(url, dossier_downloads)
    else:
        telecharger_fichier_standard(url, dossier_downloads)

if __name__ == "__main__":
    main()
