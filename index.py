import psycopg

DSN = "dbname=postgres2 user=tata password=secret host=postgres2 port=5432"


def init_db():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("ALTER TABLE IF EXISTS playlist_chanson DROP CONSTRAINT IF EXISTS fk_id_playlist;")
            cur.execute("ALTER TABLE IF EXISTS playlist_chanson DROP CONSTRAINT IF EXISTS fk_id_chanson;")
            cur.execute("ALTER TABLE IF EXISTS playlists DROP CONSTRAINT IF EXISTS fk_id_utilisateur;")

            cur.execute("DROP TABLE IF EXISTS playlist_chanson;")
            cur.execute("DROP TABLE IF EXISTS playlists;")
            cur.execute("DROP TABLE IF EXISTS chansons;")
            cur.execute("DROP TABLE IF EXISTS utilisateurs;")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS utilisateurs (
                    id_utilisateur INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nom_utilisateur VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(50) UNIQUE NOT NULL,
                    date_inscription DATE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS chansons (
                    id_chanson INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    titre VARCHAR(255) NOT NULL,
                    artiste VARCHAR(255) NOT NULL,
                    album VARCHAR(255) NOT NULL,
                    duree VARCHAR(255) NOT NULL,
                    genre VARCHAR(255) NOT NULL,
                    annee_sortie INT NOT NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id_playlist INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nom_playlist VARCHAR(255) NOT NULL,
                    id_utilisateur INT,
                    date_creation DATE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS playlist_chanson (
                    id_playlist INT NOT NULL,
                    id_chanson INT NOT NULL
                );
            """)

            cur.execute("""
                ALTER TABLE playlists
                ADD CONSTRAINT fk_id_utilisateur
                FOREIGN KEY (id_utilisateur) REFERENCES utilisateurs(id_utilisateur) ON DELETE CASCADE;
            """)

            cur.execute("""
                ALTER TABLE playlist_chanson
                ADD CONSTRAINT fk_id_playlist
                FOREIGN KEY (id_playlist) REFERENCES playlists(id_playlist) ON DELETE CASCADE;
            """)

            cur.execute("""
                ALTER TABLE playlist_chanson
                ADD CONSTRAINT fk_id_chanson
                FOREIGN KEY (id_chanson) REFERENCES chansons(id_chanson) ON DELETE CASCADE;
            """)

    print("Base initialisée !")

def creer_playlist(user=1):
    nom = input("choisissez un nom pour votre playlist : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nom_playlist FROM playlists WHERE nom_playlist = %s", (nom,))
            is_new_playlist = cur.fetchone()

            if is_new_playlist:
                print("Une playlist du me^me nom est déjà utilisée !")
                return

            cur.execute("""
                INSERT INTO playlists (nom_playlist, id_utilisateur)
                VALUES (%s, %s)
            """, (nom, user))

    print("🆗    playlist ajoutée !")

def creer_utilisateur():
    nom = input("choisissez un nom d'utilisateur : ")
    email = input("choisissez un email : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email FROM utilisateurs WHERE email = %s", (nom,))
            is_new_playlist = cur.fetchone()

            if is_new_playlist:
                print("Cet email a déjà été utilisée, veuillez en choisir un autre !")
                return

            cur.execute("""
                INSERT INTO utilisateurs (nom_utilisateur, email)
                VALUES (%s, %s)
            """, (nom, email))

    print(" 🆗   Utilisateur ajoutée !")

def creer_chanson():
    titre = input("choisissez un titre : ")
    artiste = input("choisissez un artiste : ")
    album = input("choisissez un album : ")
    duree = input("choisissez une durée : ")
    genre = input("choisissez un genre : ")
    annee_sortie = input("choisissez une année de sortie  : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chansons (titre, artiste, album, duree, genre, annee_sortie)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (titre, artiste, album, duree, genre, annee_sortie))


    print(" 🆗   chanson ajoutée !")

def ajouter_chanson_playlist():
    voir_chanson()
    chanson = input("indiquer la chanson à ajouter via son numéro...: ")
    voir_playlist()
    playlist = input("indiquer le nom de la playlist associé à la chanson, via son numéro...: ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO playlist_chanson (id_chanson, id_playlist)
                VALUES (%s, %s)
            """, (chanson, playlist))


    print(" 🆗   la chanson a bien été ajouté à votre playlist !")

def voir_utilisateur():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_utilisateur, nom_utilisateur FROM utilisateurs")
            utilisateurs = cur.fetchall()
            for utilisateur in utilisateurs:
                print(f"id utilisateur: {utilisateur[0]}, nom utilisateur: {utilisateur[1]}")
    
    print("===============")

def voir_playlist():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_playlist, nom_playlist FROM playlists")
            playlists = cur.fetchall()
            for playlist in playlists:
                print(f"id playlist: {playlist[0]}, nom playlist: {playlist[1]}")


    print("=======================")

def voir_chanson():
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM chansons WHERE titre = %s OR artiste = %s OR genre = %s", ())
            chansons = cur.fetchall()
            for chanson in chansons:
                print(f"id : {chanson[0]}, \n titre: {chanson[1]}, \n artiste: {chanson[2]}, \n album: {chanson[3]}, \n duree: {chanson[4]}, \n genre: {chanson[5]}, \n annee_sortie:{chanson[6]}")
            print("***********")


    print("========== FIN DE LA RECHERCHER =============")

def voir_chanson_playlist(playlist, user=1):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.titre, p.nom_playlist, u.email
                FROM playlist_chanson AS pc
                INNER JOIN chansons AS c ON pc.id_chanson = c.id_chanson
                INNER JOIN playlists AS p ON pc.id_playlist = p.id_playlist
                INNER JOIN utilisateurs AS u ON p.id_utilisateur = u.id_utilisateur
                WHERE p.id_utilisateur = %s AND p.id_playlist = %s
            """, (user, playlist))
            chansons = cur.fetchall()
            for chanson in chansons:
                print(chanson)

def modifier_utilisateur(id_user):
    nom = input("choisissez un nouveau nom d'utilisateur : ")
    email = input("choisissez un nouvel email : ")

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT email FROM utilisateurs WHERE email = %s", (nom,))
            is_new_playlist = cur.fetchone()

            if is_new_playlist:
                print("Cet email a déjà été utilisée, veuillez en choisir un autre. modification annulée !")
                return

            cur.execute("""
                UPDATE utilisateurs SET nom_utilisateur = %s, email = %s
                WHERE id_utilisateur = %s;
            """, (nom, email, id_user))

    print(" 🆗   Utilisateur modifié avec succés !")

def supprimer_utilisateur(id_user):

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM utilisateurs WHERE id_utilisateur = %s;
            """, (id_user,))

    print(" 🆗   Utilisateur supprimé avec succés !")

def rechercher_utilisateur(user_input):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_utilisateur, nom_utilisateur FROM utilisateurs WHERE nom_utilisateur = %s", (user_input,))
            utilisateurs = cur.fetchall()
            if utilisateurs:
                for utilisateur in utilisateurs:
                    print(f"id utilisateur: {utilisateur[0]}, nom utilisateur: {utilisateur[1]}")
            else:
                print("aucun utilisateur trouvé")
    
    print("===============")

def rechercher_chanson(user_input):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM chansons WHERE titre = %s OR artiste = %s OR genre = %s", (user_input, user_input, user_input))
            chansons = cur.fetchall()
            if chansons:
                for chanson in chansons:
                    print(f"id : {chanson[0]}, \n titre: {chanson[1]}, \n artiste: {chanson[2]}, \n album: {chanson[3]}, \n duree: {chanson[4]}, \n genre: {chanson[5]}, \n annee_sortie:{chanson[6]}")
                print("***********")
            else:
                print(" il n'y a pas de chanson associé à :", user_input)


    print("========== FIN DE LA RECHERCHER =============")

def rechercher_playlist(user_input):
    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_playlist, nom_playlist FROM playlists WHERE nom_playlist = %s", (user_input,))
            playlists = cur.fetchall()
            for playlist in playlists:
                print(f"id playlist: {playlist[0]}, nom playlist: {playlist[1]}")

    print("=======================")

def afficher_menu():
    print("\n===== MENU PLAYLIST =====")
    print("1 - Créer un utilisateur")
    print("2 - Créer une playlist")
    print("3 - Créer une chanson")
    print("4 - ajouter une chanson à une playlist")

    print("5 - voir les utilisateurs ")
    print("6 - voir les playlist ")
    print("7 -  voir les chansons")
    print("8 -  voir les chansons associées à la playlist")
    print("9 -  Modifier un utilisateur")
    print("10 -  Supprimer un utilisateur")
    print("11 -  Rechercher...")
    print("12 - Modifier une playlist")
    print("0 - Quitter")
    print()

def afficher_recherche_menu():
    print("\n===== MENU PLAYLIST =====")
    print("1 - un utilisateur")
    print("2 - une chanson")
    print("3 - une playlist")
    print("0 - Quitter")
    print()

def afficher_suppression_menu():
    print("\n===== MENU PLAYLIST =====")
    print("1 - un utilisateur")
    print("2 - une chanson")
    print("3 - une playlist")
    print("0 - Quitter")
    print()

def ihm():
    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        match choix:
            case "1":
                creer_utilisateur()
            case "2":
                creer_playlist()
            case "3":
                creer_chanson()
            case "4":
                ajouter_chanson_playlist()
            case "5":
                voir_utilisateur()
            case "6":
                voir_playlist()
            case "7":
                voir_chanson()
            case "8":
                voir_playlist()
                playlist = input("choisissez l'id playlist: ")
                user = input('choisissez l\'id de l\'utilisateur')
                voir_chanson_playlist(playlist, user=1)
            case "9":
                voir_utilisateur()
                user = input("choisissez le numéro de l'utilisateur a modifier ")
                modifier_utilisateur(user)
            case "10":
                voir_utilisateur()
                user = input("choisissez le numéro de l'utilisateur a supprimer ")
                supprimer_utilisateur(user)
            case "11":
                while True:
                    afficher_recherche_menu()
                    choix_recherche = input("que voulez-vous rechercher ? : ")
                    match choix_recherche:
                        case "1":
                            user_input = input("écrivez le  nom d'utilisateur a rechercher: ")
                            rechercher_utilisateur(user_input)
                        case "2":
                            user_input = input("écrivez le titre, l'artiste ou le genre: ")
                            rechercher_chanson(user_input)
                        case "3":
                            pass
                            user_input = input("écrivez le nom de la playlist: ")
                            rechercher_playlist(user_input)
                        case "0":
                            break
                        case _:
                            print("Choix invalide.")
            case "12":
                voir_playlist()
                user = input("choisissez le numéro de l'utilisateur a supprimer ")
                # TODO modifier plyalist
                supprimer_utilisateur(user)

            case "0":
                print("Au revoir !")
                break
            case _:
                print("Choix invalide.")

if __name__ == "__main__":
    init_db()
    ihm()
