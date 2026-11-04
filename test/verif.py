"""Outils pour vérifier tes exercices.

Tu n'as pas besoin de lire ni de modifier ce fichier : les fichiers verif_X_Y.py s'en servent.
"""
import contextlib
import io
import os
import traceback

# Pour les chapitres pygame : pas de vraie fenêtre ni de son pendant les vérifications,
# et pas de message d'accueil de pygame.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

_bilan = {"ok": 0, "total": 0}


def _ok(description):
    _bilan["ok"] += 1
    print(f"  OK     {description}")


def _echec(description, *details):
    print(f"  ÉCHEC  {description}")
    for detail in details:
        print(f"         {detail}")


def verifier(description, obtenu, attendu):
    """Vérifie que obtenu == attendu."""
    _bilan["total"] += 1
    if obtenu == attendu:
        _ok(description)
    else:
        _echec(description, f"attendu : {attendu!r}", f"obtenu  : {obtenu!r}")


def verifier_vrai(description, condition, detail=""):
    """Vérifie qu'une condition est vraie."""
    _bilan["total"] += 1
    if condition:
        _ok(description)
    else:
        _echec(description, detail)


def verifier_erreur(description, type_erreur, fonction, *args):
    """Vérifie que fonction(*args) lève une erreur de type type_erreur.

    Renvoie l'erreur levée (pour pouvoir vérifier son message), ou None.
    """
    _bilan["total"] += 1
    try:
        fonction(*args)
    except type_erreur as erreur:
        _ok(description)
        return erreur
    except Exception as erreur:
        _echec(description, f"attendu : une {type_erreur.__name__}",
               f"obtenu  : {type(erreur).__name__}: {erreur}")
        return None
    _echec(description, f"attendu : une {type_erreur.__name__}", "obtenu  : aucune erreur")
    return None


def sans_affichage(fonction, *args):
    """Exécute fonction(*args) et renvoie (résultat, texte affiché par des print)."""
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        resultat = fonction(*args)
    return resultat, tampon.getvalue()


def groupe(titre):
    """Décorateur : exécute tout de suite la fonction décorée, en attrapant les plantages.

    Si ton code plante pendant un groupe, le groupe s'arrête mais les suivants continuent.
    """
    def decorateur(fonction):
        print(f"\n{titre}")
        try:
            fonction()
        except Exception as erreur:
            _bilan["total"] += 1
            lieu = traceback.extract_tb(erreur.__traceback__)[-1]
            fichier = os.path.relpath(lieu.filename)
            _echec("le code a planté pendant ce groupe",
                   f"{type(erreur).__name__}: {erreur}",
                   f"à la ligne {lieu.lineno} de {fichier} : {lieu.line}")
        return fonction
    return decorateur


def bilan():
    ok, total = _bilan["ok"], _bilan["total"]
    print(f"\nBilan : {ok}/{total} vérifications réussies")
    if ok == total:
        print("Tout est bon, tu peux passer à la suite.")
    else:
        print("Corrige les ÉCHEC dans l'ordre, du premier au dernier, puis relance.")
